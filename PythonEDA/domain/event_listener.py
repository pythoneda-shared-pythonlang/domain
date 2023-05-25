from domain.event import Event
from domain.unsupported_event import UnsupportedEvent

import inspect
from typing import List,Type

class EventListener:

    _listeners = {}

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        """
        raise NotImplementedError(
            "supported_events() must be implemented by subclasses"
        )

    @classmethod
    def listeners(cls):
        return EventListener._listeners

    @classmethod
    def listeners_for(cls, eventClass: Type[Event]) -> List[Type]:
        result = EventListener._listeners.get(eventClass, [])
        EventListener._listeners[eventClass] = result
        return result

    @classmethod
    def find_listeners(cls):
        for subclass in EventListener.__subclasses__():
            for eventClass in subclass.supported_events():
                methodName = cls.buildMethodName(eventClass)
                method = getattr(subclass, methodName)
                if inspect.ismethod(method) and inspect.isclass(method.__self__):
                    EventListener.listen(subclass, eventClass)

    @classmethod
    def listen(cls, listener: Type, eventClass: Type[Event]):
        eventListeners = EventListener.listeners_for(eventClass)
        if listener not in eventListeners:
            eventListeners.append(listener)

    @classmethod
    async def accept(cls, event: Event):
        result = []
        listeners = EventListener.listeners_for(event.__class__)
        if len(listeners) == 0:
            raise UnsupportedEvent(event)
        for listener in listeners:
            methodName = cls.buildMethodName(event.__class__)
            method = getattr(listener, methodName)
            result.append(await method(event))
        return result


    @classmethod
    def buildMethodName(cls, eventClass: Type) -> str:
        return f'listen{eventClass.__name__}'

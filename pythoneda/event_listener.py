"""
pythoneda/event_listener.py

This script defines the EventListener class.

Copyright (C) 2023-today rydnr's PythonEDA

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.event import Event
from pythoneda.unsupported_event import UnsupportedEvent

import abc
import inspect
from typing import List,Type

class EventListener(abc.ABC):
    """
    This class can listen / receive events.

    Class name: EventListener

    Responsibilities:
        - Offers itself to be notified of new Events.
        - Provides a list of types of Events it supports.
        - Maintains a registry of listeners.

    Collaborators:
        - Event: The message emitted.
        - EventEmitter: Those which emit events.
    """

    _listeners = {}

    @classmethod
    @abc.abstractmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        :return: Such list.
        :rtype: List
        """
        raise NotImplementedError(
            "supported_events() must be implemented by subclasses"
        )

    @classmethod
    def listeners(cls):
        """
        Retrieves the registered listeners.
        :return: Such mapping.
        :rtype: Dict
        """
        return EventListener._listeners

    @classmethod
    def listeners_for(cls, eventClass: Type[Event]) -> List[Type]:
        """
        Retrieves the listeners associated to a certain Event class.
        :param eventClass: The type of event.
        :type eventClass: Type[Event]
        :return: The matching listeners.
        :rtype: List[Type]
        """
        result = EventListener._listeners.get(eventClass, [])
        EventListener._listeners[eventClass] = result
        return result

    @classmethod
    def find_listeners(cls):
        """
        Finds all available listeners.
        :return: Such list.
        :rtype: List
        """
        for subclass in EventListener.__subclasses__():
            for eventClass in subclass.supported_events():
                methodName = cls.build_method_name(eventClass)
                method = getattr(subclass, methodName)
                if inspect.ismethod(method) and inspect.isclass(method.__self__):
                    EventListener.listen(subclass, eventClass)

    @classmethod
    def listen(cls, listener: Type, eventClass: Type[Event]):
        """
        Annotates given listener to receive notifications of a certain type of events.
        :param listener: The listener instance.
        :type listener: Type[EventListener]
        :param eventClass: The type of Event.
        :type eventClass: Type[Event]
        """
        eventListeners = EventListener.listeners_for(eventClass)
        if listener not in eventListeners:
            eventListeners.append(listener)

    @classmethod
    async def accept(cls, event: Event):
        """
        Notification of a supported event.
        :param event: The event.
        :type event: Event
        :return: Potentially, a list of triggered events in response.
        :rtype: List
        """
        result = []
        listeners = EventListener.listeners_for(event.__class__)
        if len(listeners) == 0:
            raise UnsupportedEvent(event)
        for listener in listeners:
            methodName = cls.build_method_name(event.__class__)
            method = getattr(listener, methodName)
            result.append(await method(event))
        return result


    @classmethod
    def build_method_name(cls, eventClass: Type) -> str:
        """
        Builds a method name for given event class, by prepending the Event class name with "listen".
        :param eventClass: The event class.
        :type eventClass: Type[Event]
        :return: The method name.
        :rtype: str
        """
        return f'listen{eventClass.__name__}'

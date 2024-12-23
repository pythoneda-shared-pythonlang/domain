# vim: set fileencoding=utf-8
"""
pythoneda/shared/event_listener.py

This script defines the EventListener class and the @listen decorator.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythonlang/domain

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
from . import BaseObject, Event
import abc
import functools
import inspect
from typing import Any, Callable, Dict, List, Type


_event_listeners = {}
_event_listeners_by_event_class = {}
_event_listener_methods = {}
_pending_event_listeners = {}


def _build_cls_key(cls):
    """
    Builds a key for given class.
    :param cls: The class.
    :type cls: type
    :return: A key.
    :rtype: str
    """
    return f"{cls.__module__}.{cls.__name__}"


def _is_function(fn) -> bool:
    """
    Checks whether given parameter is a function.
    :param fn: The potential function.
    :type fn: Any
    :return: True if it's a function, False otherwise.
    :rtype: bool
    """
    function_to_check = _unwrap_function(fn)
    result = callable(function_to_check)
    return result


def _unwrap_function(fn) -> Callable:
    """
    Unwraps given function.
    :param fn: The function.
    :type fn: Callable
    :return: The unwrapped function.
    :rtype: Callable
    """
    result = fn
    while hasattr(result, "__func__"):
        result = getattr(result, "__func__")
    return result


def _build_func_key(fn):
    """
    Builds a key for given function.
    :param fn: The function.
    :type fn: Callable
    :return: A key.
    :rtype: str
    """
    func = _unwrap_function(fn)
    return func


def _classes_by_key(key):
    """
    Retrieves the classes annotated under given key.
    :param key: The key.
    :type key: str
    :return: The list of classes.
    :rtype: List
    """
    return [m[1] for m in inspect.getmembers(key, inspect.isclass)]


def _add_to_pending(func: Callable, eventClass: Type[Any], store: Dict):
    """
    Adds given function (specifically a derived value) in a list.
    :param func: The function to add.
    :type func: Callable
    :param eventClass: The class of the event.
    :type eventClass: pythoneda.Event
    :param store: The dictionary to store the function.
    :type store: Dict
    """
    store[_build_func_key(func)] = eventClass


def _add_wrapper(func: Callable, eventClass: Type[Any]):
    """
    Annotates given wrapper.
    :param func: The wrapper.
    :type func: callable
    :param eventClass: The class of the event.
    :type eventClass: pythoneda.Event
    """
    unwrapped = _unwrap_function(func)
    _add_to_pending(unwrapped, eventClass, _pending_event_listeners)


def listen(eventClass: Type[Any]):
    """
    Decorator to annotate an event listener.
    :param eventClass: The class of the event.
    :type eventClass: pythoneda.Event
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        _add_wrapper(wrapper, eventClass)
        return wrapper

    return decorator


def _is_listen_method(fn: Callable) -> bool:
    """
    Checks whether a function is annotated with the @listen decorator.
    :param fn: The function to check.
    :type fn: Callable
    :return: True if it's a @listen class method; False otherwise.
    :rtype: bool
    """
    from .event_listener import _pending_event_listeners

    func = _unwrap_function(fn)
    return (
        isinstance(fn, classmethod)
        and _is_function(func)
        and _build_func_key(func) in _pending_event_listeners
    )


#    return _is_function(func) and _build_func_key(func) in _pending_event_listeners


def _process_pending_event_listeners(cls: Type[Any]):
    """
    Processes all pending event listeners of given class.
    :param cls: The class holding the event listeners.
    :type cls: Type[Any]
    """
    from .event_listener import (
        _pending_event_listeners,
        _event_listeners,
        _event_listener_methods,
    )

    for name, listener in vars(cls).items():
        if _is_listen_method(listener):
            # First, @classmethod. Then, @listen.
            # That's why we are passing `listener.__func__, which is our @listen function`
            _process_pending_event_listener(
                cls,
                listener,
                _pending_event_listeners,
                _event_listeners,
                _event_listeners_by_event_class,
                _event_listener_methods,
            )
    for current_parent in cls.mro():
        for name, listener in vars(current_parent).items():
            if _is_listen_method(listener):
                # First, @classmethod. Then, @listen.
                # That's why we are passing `listener.__func__, which is our @listen function`
                _process_pending_event_listener(
                    cls,
                    listener,
                    _pending_event_listeners,
                    _event_listeners,
                    _event_listeners_by_event_class,
                    _event_listener_methods,
                )


def _process_pending_event_listener(
    cls: Type[Any],
    listener: Callable,
    pending: List,
    listeners: Dict,
    listenersByEventClass: Dict,
    methods: Dict,
):
    """
    Processes a pending event listener.
    :param cls: The class holding the event listener.
    :type cls: Type[Any]
    :param listener: The listener.
    :type listener: Callable
    :param pending: The pending listeners.
    :type pending: List
    :param listeners: The final listeners.
    :type listeners: Dict
    :param listenersByEventClass: The mapping between event classes and listeners.
    :type listenersByEventClass: Dict
    :param methods: The listener methods.
    :type methods: Dict
    """
    func = _unwrap_function(listener)
    cls_key = _build_cls_key(cls)
    if _is_function(func) and _build_func_key(func) in pending:
        aux_listeners = listeners.get(cls_key, None)
        if aux_listeners is None:
            aux_listeners = []
        aux_listeners.append(pending[_build_func_key(func)])
        listeners[cls_key] = aux_listeners
        aux_listeners_by_event_class = listenersByEventClass.get(
            pending[_build_func_key(func)], None
        )
        if aux_listeners_by_event_class is None:
            aux_listeners_by_event_class = []
        if cls not in aux_listeners_by_event_class:
            aux_listeners_by_event_class.append(cls)
        listenersByEventClass[pending[_build_func_key(func)]] = (
            aux_listeners_by_event_class
        )
        aux_methods = methods.get(cls_key, None)
        if aux_methods is None:
            aux_methods = {}
        aux_methods[pending[_build_func_key(func)]] = func
        methods[cls_key] = aux_methods


def _propagate_event_listeners_upwards(cls):
    """
    Propagates event listeners from given class' parents.
    :param cls: The class holding the listeners.
    :type cls: type
    """
    from .event_listener import _event_listeners

    cls_key = _build_cls_key(cls)
    if cls_key not in _event_listeners.keys():
        _event_listeners[cls_key] = []
    for current_parent in cls.mro():
        parent_cls_key = _build_cls_key(current_parent)
        if parent_cls_key in _event_listeners.keys():
            for event_listener in _event_listeners[parent_cls_key]:
                if event_listener not in _event_listeners[cls_key]:
                    _event_listeners[cls_key].append(event_listener)


class EventListener(BaseObject, abc.ABC):
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

    @classmethod
    def listeners(cls):
        """
        Retrieves the registered listeners.
        :return: Such mapping.
        :rtype: Dict
        """
        from .event_listener import _event_listeners

        return _event_listeners

    @classmethod
    def listeners_by_event_class(cls):
        """
        Retrieves the registered listeners by event class.
        :return: Such mapping.
        :rtype: Dict
        """
        from .event_listener import _event_listeners_by_event_class

        return _event_listeners_by_event_class

    @classmethod
    def listener_methods(cls):
        """
        Retrieves the registered listener methods.
        :return: Such mapping.
        :rtype: Dict
        """
        from .event_listener import _event_listener_methods

        return _event_listener_methods

    @classmethod
    def listeners_for(cls, eventClass: Type[Event]) -> List[Type]:
        """
        Retrieves the listeners associated to a certain Event class.
        :param eventClass: The type of event.
        :type eventClass: Type[Event]
        :return: The matching listeners.
        :rtype: List[Type]
        """
        aux = EventListener.listeners_by_event_class().get(eventClass, [])
        EventListener.listeners_by_event_class()[eventClass] = aux

        result = [
            clz
            for clz in sorted(aux, key=cls._get_priority)
            if not inspect.isabstract(clz)
        ]

        return result

    @classmethod
    def delegate_priority(cls, primaryPort) -> int:
        """
        Delegates the priority information to given primary port.
        :param primaryPort: The primary port.
        :type primaryPort: type[pythoneda.PrimaryPort]
        :return: Such priority.
        :rtype: int
        """
        result = -1
        if cls.has_default_priority_method(primaryPort):
            result = primaryPort.default_priority()

        if cls.has_priority_method(primaryPort):
            instance = cls.get_primary_port_instance(primaryPort)
            if instance:
                result = instance.priority()

        return result

    @classmethod
    def listen_method_for(cls, eventClass: Type[Any]) -> Callable:
        """
        Retrieves the @listen() method for given event, in this class.
        :param eventClass: The event class.
        :type eventClass: Type[Any]
        :return: The @listen-decorated method.
        :rtype: Callable
        """
        cls_key = _build_cls_key(cls)
        methods = EventListener.listener_methods().get(cls_key, {})
        return methods.get(eventClass, None)

    @classmethod
    def _get_priority(cls, eventListener: Type[Any]) -> int:
        """
        Retrieves the priority of given listener, or 100 if it doesn't define it.
        :param eventListener: The event listener.
        :type eventListener: Type[Any]
        :return: The priority of the listener. The lower, the more preferred.
        :rtype: int
        """
        result = None
        try:
            result = eventListener.default_priority()
        except AttributeError:
            pass

        if result is None:
            result = 100

        return result

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
        method = cls.listen_method_for(event.__class__)
        if method is None:
            EventListener.logger().error(
                f"Cannot find @listen({cls.full_class_name(event.__class__)}) method on {cls.full_class_name(cls)}"
            )
        else:
            aux = await method(cls, event)
            if aux is not None:
                if isinstance(aux, list):
                    result = aux
                else:
                    result.append(aux)
        return result

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Initializes this class.
        :param kwargs: Any additional keyword arguments.
        :type kwargs: Dict
        """
        super().__init_subclass__(**kwargs)
        _process_pending_event_listeners(cls)
        #        for current_parent in cls.mro():
        #            _process_pending_event_listeners(current_parent)
        _propagate_event_listeners_upwards(cls)
        from .event_listener import (
            _pending_event_listeners,
        )

        del _pending_event_listeners


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

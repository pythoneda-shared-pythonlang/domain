"""
PythonEDA/event_emitter.py

This script defines the EventEmitter class.

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
from PythonEDA.event import Event

class EventEmitter:
    """
    Is able to emit Events.

    Class name: EventEmitter

    Responsibilities:
        - Emit events.
        - Maintain a registry of receivers or listeners.

    Collaborators:
        - Event: The events being emitted.
        - EventListener: Those interested in receiving events.
    """
    _receivers = []

    @classmethod
    def receivers(cls):
        """
        Retrieves the event listeners.
        :return: Such listeners.
        :rtype: List
        """
        return EventEmitter._receivers

    @classmethod
    def register_receiver(cls, receiver):
        """
        Registers a new listener.
        :param receiver: The event receiver to register.
        :type receiver: EventListener
        """
        if receiver not in EventEmitter._receivers:
            EventEmitter._receivers.append(receiver)

    @classmethod
    def unregister_receiver(cls, receiver):
        """
        Unlists a receiver.
        :param receiver: The event listener to unlist.
        :type receiver: EventListener
        """
        if receiver in EventEmitter._receivers:
            EventEmitter._receivers.remove(receiver)

    @classmethod
    async def emit(cls, event: Event):
        """
        Emits given event.
        :param event: The event to emit.
        :type event: Event
        """
        for receiver in EventEmitter._receivers:
            await receiver.accept(event)

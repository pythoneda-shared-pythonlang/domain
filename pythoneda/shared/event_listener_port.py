# vim: set fileencoding=utf-8
"""
pythoneda/shared/event_listener_port.py

This script defines the EventListenerPort class.

Copyright (C) 2023-today rydnr's pythoneda-shared/domain

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
from . import BaseObject, Event, EventListener, PrimaryPort
import abc
from typing import Type


class EventListenerPort(BaseObject, PrimaryPort, abc.ABC):
    """
    Port able to receive Events.

    Class name: EventListenerPort

    Responsibilities:
        - Listen for new events.

    Collaborators:
        - Event: The events being received.
    """

    @classmethod
    def listen(cls, listener: Type, eventClass: Type[Event]):
        """
        Annotates given listener to receive notifications of a certain type of events.
        :param listener: The listener instance.
        :type listener: Type[EventListener]
        :param eventClass: The type of Event.
        :type eventClass: Type[Event]
        """
        EventListenerPort.logger().info(f"{listener} listening to {eventClass} events")
        return EventListener.listen(listener, eventClass)

    @classmethod
    async def accept(cls, event: Event):
        """
        Notification of a supported event.
        :param event: The event.
        :type event: Event
        :return: Potentially, a list of triggered events in response.
        :rtype: List
        """
        EventListenerPort.logger().info(f"Accepting event {event}")
        return await EventListener.accept(event)
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

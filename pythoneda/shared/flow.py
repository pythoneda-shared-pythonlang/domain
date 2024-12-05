# vim: set fileencoding=utf-8
"""
pythoneda/shared/flow.py

This script defines the Flow class.

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
from . import Entity, Event
import abc
from typing import List


class Flow(Entity, abc.ABC):
    """
    Represents a Flow: a sequence of events.

    Class name: Flow

    Responsibilities:
        - Defines a sequence of events.

    Collaborators:
        - Event
    """

    def __init__(self, firstEvent: Event = None):
        """
        Creates a new Flow instance.
        :param firstEvent: The first event of the flow.
        :type firstEvent: pythoneda.shared.Event
        """
        super().__init__()
        self._first_event = None
        self._events = []
        self.add_event(firstEvent)

    @property
    def first_event(self) -> Event:
        """
        Retrieves the first event.
        :return: Such event.
        :rtype: pythoneda.Event
        """
        return self._first_event

    @property
    def events(self) -> List[Event]:
        """
        Retrieves the list of events of the flow.
        :return: Such list.
        :rtype: List[pythoneda.shared.Event]
        """
        return self._events

    def add_event(self, event: Event):
        """
        Adds a new event to the flow.
        :param event: The event.
        :type event: pythoneda.shared.Event
        """
        if event is not None:
            if self._first_event is None:
                self._first_event = event
            self._events.append(event)

    async def resume(self, event: Event):
        """
        Resumes the flow with a new event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        """
        if len(event.previous_event_ids) > 0:
            event_previous_events = event.previous_event_ids
            if type(event_previous_events) is str:
                previous_event_id = event_previous_events
            else:
                previous_event_id = event_previous_events[-1]

            my_previous_event_id = self._events[-1].id
            if previous_event_id == my_previous_event_id:
                await self.continue_flow(event, self._events[-1])

    def find_latest_event(self, eventClass: type) -> Event:
        """
        Finds the latest event of the given class.
        :param eventClass: The class of the event.
        :type eventClass: type
        :return: Such event.
        :rtype: pythoneda.shared.Event
        """
        for event in reversed(self._events):
            if isinstance(event, eventClass):
                return event
        return None

    @abc.abstractmethod
    async def continue_flow(self, event: Event, previousEvent: Event):
        """
        Continues the flow with a new event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :param previousEvent: The previous event.
        :type previousEvent: pythoneda.shared.Event
        """
        pass


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

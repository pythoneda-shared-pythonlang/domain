# vim: set fileencoding=utf-8
"""
pythoneda/shared/flow.py

This script defines the Flow class.

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
from . import Entity, Event
from typing import List


class Flow(Entity):
    """
    Represents a Flow: a sequence of events.

    Class name: Flow

    Responsibilities:
        - Defines a sequence of events.

    Collaborators:
        - Event
    """

    def __init__(self, firstEvent: Event):
        """
        Creates a new Flow instance.
        :param firstEvent: The first event of the flow.
        :type firstEvent: pythoneda.Event
        """
        super().__init__()
        self._events = []
        self._add_event(firstEvent)
        self._first_event = firstEvent

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
        :rtype: List[pythoneda.Event]
        """
        return self._events

    def _add_event(self, event: Event):
        """
        Adds a new event to the flow.
        :param event: The event.
        :type event: pythoneda.Event
        """
        self._events.append(event)
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

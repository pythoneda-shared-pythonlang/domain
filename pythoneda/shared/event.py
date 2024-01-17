# vim: set fileencoding=utf-8
"""
pythoneda/shared/event.py

This file defines the Event class.

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
from . import internal_attribute, ValueObject
from typing import List


class Event(ValueObject):
    """
    The base event class.

    Class name: Event

    Responsibilities:
        - Represents a change in the system state.
        - It's the only way to communicate among PythonEDA domains.

    Collaborators:
        - EventEmitter: Emits Events.
        - EventListener: Listens to Events.
    """

    def __init__(
        self,
        previousEventIds: List[str] = None,
        reconstructedId: str = None,
        reconstructedPreviousEventIds: List[str] = None,
    ):
        """
        Creates a new Event instance.
        :param previousEventIds: The id of previous events, if any.
        :type previousEventIds: List[str]
        :param reconstructedId: An optional id (in case it's a reconstruction of an external event).
        :type reconstructedId: str
        :param reconstructedPreviousEventIds: The id of the events this one is response to,
        in case it's a reconstruction of an external event.
        :type reconstructedPreviousEventIds: str
        """
        super().__init__()
        if reconstructedId:
            self._id = reconstructedId
        if previousEventIds:
            self._previous_event_ids = previousEventIds
        elif reconstructedPreviousEventIds:
            self._previous_event_ids = reconstructedPreviousEventIds

    @property
    @internal_attribute
    def previous_event_ids(self) -> List[str]:
        """
        Retrieves the id of the events this one is response to, if any.
        :return: Such ids.
        :rtype: List[str]
        """
        if hasattr(self, "_previous_event_ids"):
            return self._previous_event_ids
        else:
            return []
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

# vim: set fileencoding=utf-8
"""
pythoneda/shared/event_reference.py

This script defines the EventReference class.

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
from .value_object import primary_key_attribute, ValueObject
from typing import Dict


class EventReference(ValueObject):
    """
    Represents a reference to an event.

    Class name: EventReference

    Responsibilities:
        - Unambigously identify an event.

    Collaborators:
        - ValueObject: Provides attribute decorators, and __str__(), repr__(), __eq__() and __hash__().
    """

    def __init__(self, eventId: str, eventClass: str):
        """
        Creates a new EventReference instance.
        :param eventId: The event id.
        :type eventId: str
        :param eventClass: The event class.
        :type eventClass: str
        """
        self._event_id = eventId
        self._event_class = eventClass
        super().__init__(omitInternal=True)

    @property
    @primary_key_attribute
    def event_id(self) -> str:
        """
        Returns the event id.
        :return: The event id.
        :rtype: str
        """
        return self._event_id

    @property
    @primary_key_attribute
    def event_class(self) -> str:
        """
        Retrieves the event class.
        :return: Such class.
        :rtype: str
        """
        return self._event_class

    def to_dict(self) -> Dict:
        """
        Converts the object to a dictionary.
        :return: The dictionary.
        :rtype: Dict
        """
        return {"event_id": self.event_id, "event_class": self.event_class}


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

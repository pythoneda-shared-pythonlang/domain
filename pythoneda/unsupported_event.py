"""
pythoneda/unsupported_event.py

This script defines the UnsupportedEvent class.

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
import gettext
from pythoneda import DomainException

_ = gettext.gettext

class UnsupportedEvent(DomainException):
    """
    An unsupported event was emitted.

    Class name: UnsupportedEvent

    Responsibilities:
        - Contain context information about the event that was received and was not supported.

    Collaborators:
        - PrimaryPort: Ports that accept events and detect unsupported ones.
    """
    def __init__(self, event: str):
        """
        Creates a new instance.
        :param event: The unsupported event.
        :type event: str
        """
        super().__init__(f_('Unsupported event: {event}'))

"""
pythoneda/event.py

This file defines the Event class.

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
from pythoneda.value_object import ValueObject


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
    def __init__(self):
        """
        Creates a new event instance.
        """
        super().__init__()

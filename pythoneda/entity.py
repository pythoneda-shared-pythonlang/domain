"""
pythoneda/entity.py

This script defines the Entity class.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythoneda/domain

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
from pythoneda import ValueObject

class Entity(ValueObject):
    """
    Represents an Entity: something meaningful, unique, with set of attributes, and, in good designs, behavior.

    Class name: Entity

    Responsibilities:
        - Defines uniqueness constraints.
        - A cohesive group of related attribute values.
        - Specifies attributes, including primary key's and those used for filtering, using ValueObject's decorators.

    Collaborators:
        - ValueObject: Provides attribute decorators, and __str__(), repr__(), __eq__() and __hash__().
        - Repo: To rebuild them from persistence layers.
    """
    def __init__(self):
        """
        Creates a new Entity instance.
        """
        super().__init__()

"""
PythonEDA/domain_exception.py

This file defines the DomainException class.

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
from PythonEDA.value_object import ValueObject

class DomainException(Exception, ValueObject):
    """
    The parent class of all domain exceptions.

    Class name: Exception

    Responsibilities:
        - Represents an error in a domain.
        - Subclasses should provide as much context as possible.

    Collaborators:
        - Exception: Python's built-in exception class.
        - ValueObject: Overrides Python's default methods.
    """

    def __init__(self):
        """
        Creates a new DomainException instance.
        """
        super().__init__()

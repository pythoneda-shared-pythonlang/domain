"""
pythoneda/formatting.py

This file defines the Formatting class.

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
from .base_object import BaseObject

class Formatting(BaseObject):
    """
    Marks formatting wrappers.

    Class name: Formatting

    Responsibilities:
        - Wraps another instance's attributes.
        - Exposes only other instance's data, not behavior.

    Collaborators:
        - PythonEDA/ValueObject: It uses this class to determine the behavior of its "__eq__()", "__str__()", "__repr__()" and "__hash__()".

    """
    def __init__(self, fmt):
        """
        Creates a new instance.
        :param fmt: The wrapped instance.
        :type fmt: Object
        """
        self._fmt = fmt

    @property
    def _formatted(self):
        """
        Retrieves the wrapped instance.
        :return: Such instance.
        :rtype: Object
        """
        return self._fmt

    def __getattr__(self, attr):
        """
        Delegates any method call to the wrapped instance.
        :param attr: The attribute.
        :type attr: Object
        """
        return getattr(self._fmt, attr)

    def __str__(self):
        """
        Delegates the string representation to the wrapped instance.
        :return: The string representation of the wrapped instance.
        :rtype: str
        """
        return self._fmt.__str__()

    def __repr__(self):
        """
        Delegates the string representation to the wrapped instance.
        :return: The string representation of the wrapped instance.
        :rtype: str
        """
        return self._fmt.__repr__()

    def __eq__(self, other):
        """
        Delegates the equal checking to the wrapped instance.
        :param other: The instance to compare to.
        :type other: Formatting
        :return: True if the wrapped instance and given argument match; False otherwise.
        :rtype: bool
        """
        return self._fmt.__eq__(other)

    def __hash__(self):
        """
        Delegates the calculation of the hash code to the wrapped instance.
        :return: The hash value.
        :rtype: int
        """
        return self._fmt.__hash__()

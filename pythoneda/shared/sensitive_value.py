# vim: set fileencoding=utf-8
"""
pythoneda/shared/sensitive_value.py

This file defines the SensitiveValue class.

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
from .base_object import BaseObject


class SensitiveValue(BaseObject):
    """
    Prevents sensitive values to be exposed.

    Class name: SensitiveValue

    Responsibilities:
        - Wraps a sensitive value.
        - Overrides "__eq__()", "__str__()", "__repr__()" and "__hash__()" to avoid leaking the sensitive value,
        while preserving identity invariants.

    Collaborators:
        - Any primitive type or class to protect.
    """

    def __init__(self, value):
        """
        Creates a new instance.
        :param value: The value to protect.
        :type value: str
        """
        self._value = value

    def get(self):
        """
        Retrieves the actual value. USE WITH CARE.
        :return: The actual value.
        :rtype: str
        """
        return self._value

    def __getattr__(self, attr):
        """
        Delegates any method call to the wrapped instance.
        :param attr: The attribute.
        :type attr: str
        :return: The value of the wrapped instance's attribute.
        :rtype: int, str, object
        """
        return getattr(self._value, attr)

    def __str__(self):
        """
        Obfuscates the sensitive value.
        :return: An obfuscated value.
        :rtype: str
        """
        return "[hidden]"

    def __repr__(self):
        """
        Obfuscates the sensitive value.
        :return: An obfuscated value.
        :rtype: str
        """
        return "[hidden]"

    def __eq__(self, other):
        """
        Checks if the sensitive value is equal to given instance.
        :param other: The instance to compare to.
        :type other: int, str, object
        :return: True in such case.
        :rtype: bool
        """
        return self._value.__eq__(other)

    def __hash__(self):
        """
        Retrieves the hash of the sensitive value.
        :return: The hash of the sensitive value.
        :rtype: int
        """
        return self._value.__hash__()

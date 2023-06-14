"""
pythoneda/domain_exception.py

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
from pythoneda.value_object import ValueObject

import gettext
import os
from pathlib import Path

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

    locale_dir = ".i18n"

    def __init__(self, txt: str, *args):
        """
        Creates a new DomainException instance.
        :param txt: The exception message.
        :type txt: str
        """
        super().__init__(args)
        self._message = txt

    @property
    def message(self) -> str:
        """
        Retrieves the exception message.
        :return: The message.
        :rtype: str
        """
        return self._message

    def localized_message(self, locale: str) -> str:
        """
        Retrieves a localized version of the message.
        :param locale: The locale to use.
        :type locale: str
        :return: The message according to the locale.
        :rtype: str
        """
        localedir = os.path.join(Path(__file__).resolve().parent.parent, self.__class__.locale_dir, "locale")

        print(f'using locale folder {localedir}')
        t = gettext.translation("pythoneda", localedir=self.__class__.locale_dir, languages=[locale], fallback=True)
        _ = t.gettext

        return _(self.message)

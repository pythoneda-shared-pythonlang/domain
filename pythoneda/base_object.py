"""
pythoneda/base_object.py

This script defines the BaseObject class.

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
from .logging_port import LoggingPort
from .logging_port_fallback import LoggingPortFallback
from .ports import Ports
from typing import Type

class BaseObject():
    """
    Ancestor of all PythonEDA classes.

    Class name: BaseObject

    Responsibilities:
        - Define common behavior for all PythonEDA classes.

    Collaborators:
        - None
    """
    _logging_port = None

    @classmethod
    def full_class_name(cls, target:Type=None) -> str:
        """
        Retrieves the full class name of given class.
        :param target: The class. If omitted, this very class.
        :type target: Class
        :return: The key.
        :rtype: str
        """
        actual_target = target
        if actual_target is None:
            actual_target = cls
        return f'{actual_target.__module__}.{actual_target.__name__}'

    @classmethod
    def logger(cls, category:str=None):
        """
        Retrieves the logger instance.
        :param category: The logging category.
        :type category: str
        :return: Such instance.
        :rtype: Any
        """
        if cls._logging_port is None:
            cls._logging_port = Ports.instance().resolve(LoggingPort)
        if cls._logging_port is None:
            cls._logging_port = LoggingPort.LoggingFallback()

        if category is None:
            cat = cls.full_class_name(cls)
        else:
            cat = category

        return cls._logging_port.logger(cat)

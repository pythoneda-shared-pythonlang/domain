# vim: set fileencoding=utf-8
"""
pythoneda/shared/logging_port.py

This script defines the LoggingPort class.

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
from .port import Port
from abc import abstractmethod


class LoggingPort(Port):
    """
    Port for logging mechanisms.

    Class name: LoggingPort

    Responsibilities:
        - Provide logging mechanisms.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Initializes a new LoggingPort instance.
        """
        super().__init__()

    @abstractmethod
    def logger(self, category: str = None):
        """
        Retrieves the logger instance.
        :param category: The logging category.
        :type category: str
        :return: Such instance.
        :rtype: logging.Logger
        """
        return NotImplementedError(
            "logger(category) should be implemented by subclasses"
        )

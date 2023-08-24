"""
pythoneda/base_object.py

This script defines the BaseObject class.

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
from .logging_port import LoggingPort
from .ports import Ports

class BaseObject():
    """
    Ancestor of all PythonEDA classes.

    Class name: BaseObject

    Responsibilities:
        - Define common behavior for all PythonEDA classes.

    Collaborators:
        - None
    """
    _logger = None

    @classmethod
    def logger(cls):
        """
        Retrieves the logger instance.
        :return: Such instance.
        :rtype: logging.Logger
        """
        if cls._logger is None:
            cls._logger = Ports.instance().resolve(LoggingPort)
        return cls._logger

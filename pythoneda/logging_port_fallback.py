"""
pythoneda/logging_port_fallback.py

This script defines the LoggingPortFallback class.

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
class LoggingFallback:
    """
    Fallback logging.

    Class name: LoggingFallback

    Responsibilities:
    - Provide basic logging mechanisms.

    Collaborators:
    - None
    """

    _category = ""

    def __init__(self, category: str):
        """
        Initializes a new LoggingPortFallback instance.
        :param category: The logging category.
        :type category: str
        """
        super().__init__()
        _category = category

    @property
    def category(self) -> str:
        """
        Retrieves the logging category.
        :return: Such category.
        :rtype: str
        """
        return self._category

    def _log(self, level: str, message: str):
        """
        Logs a message.
        :param level: The logging level.
        :type level: str
        :param message: The error message.
        :type message: str
        """
        print(f"[{self.category}]-{level} {message}")

    def critical(self, message: str):
        """
        Logs a critical error.
        :param message: The error message.
        :type message: str
        """
        self._log("critical", message)

    def error(self, message: str):
        """
        Logs an error.
        :param message: The error message.
        :type message: str
        """
        self._log("error", message)

    def warning(self, message: str):
        """
        Logs a warning.
        :param message: The warning message.
        :type message: str
        """
        self._log("warning", message)

    def info(self, message: str):
        """
        Logs an informational message.
        :param message: The message.
        :type message: str
        """
        self._log("info", message)

    def debug(self, message: str):
        """
        Logs a debug message.
        :param message: The debug message.
        :type message: str
        """
        self._log("debug", message)

    def trace(self, message: str):
        """
        Logs a trace message.
        :param message: The message.
        :type message: str
        """
        self._log("trace", message)

class LoggingPortFallback():
    """
    Fallback logging.

    Class name: LoggingPortFallback

    Responsibilities:
    - Provide basic logging mechanisms.

    Collaborators:
    - None
    """
    def __init__(self):
        """
        Initializes a new LoggingPortFallback instance.
        """
        super().__init__()


    def logger(self, category: str):
        """
        Retrieves the logger instance.
        :param category: The logging category.
        :type category: str
        :return: Such instance.
        :rtype: logging.Logger
        """
        return LoggingFallback(category)

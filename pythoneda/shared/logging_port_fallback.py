# vim: set fileencoding=utf-8
"""
pythoneda/shared/logging_port_fallback.py

This script defines the LoggingPortFallback class.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythonlang/domain

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

    def __init__(self, thresholdLevel: str, category: str):
        """
        Initializes a new LoggingFallback instance.
        :param thresholdLevel: The threshold level.
        :type thresholdLevel: str
        :param category: The logging category.
        :type category: str
        """
        super().__init__()
        self._category = category
        self._threshold_level = thresholdLevel

    @property
    def category(self) -> str:
        """
        Retrieves the logging category.
        :return: Such category.
        :rtype: str
        """
        return self._category

    @property
    def threshold_level(self) -> str:
        """
        Retrieves the threshold level.
        :return: Such level.
        :rtype: str
        """
        return self._threshold_level

    def level_to_int(self, level: str) -> int:
        """
        Converts a logging level to an integer.
        :param level: The logging level.
        :type level: str
        :return: The integer representation.
        :rtype: int
        """
        lvl = level.lower()
        if lvl == "critical":
            return 50
        if lvl == "error":
            return 40
        if lvl == "warning":
            return 30
        if lvl == "info":
            return 20
        if lvl == "debug":
            return 10
        if lvl == "trace":
            return 5
        return 0

    def _log(self, level: str, message: str):
        """
        Logs a message.
        :param level: The logging level.
        :type level: str
        :param message: The error message.
        :type message: str
        """
        from .invariants import Invariants
        from .pythoneda_application import PythonedaApplication

        category = self.truncate_category(self.category, 25)
        invariant_app = Invariants.instance().apply(PythonedaApplication.invariant_type)
        level_value = self.level_to_int(level)
        threshold_value = self.level_to_int(self.threshold_level)
        if level_value <= threshold_value:
            from datetime import datetime

            time_format = "%Y-%m-%d %H:%M:%S"
            current_time = datetime.now().strftime(time_format)
            if invariant_app is None:
                print(f"[?!] {current_time} - {category} - {level.upper()} - {message}")
            else:
                print(
                    f"[{invariant_app.value}] {current_time} - {category} - {level.upper()} - {message}"
                )

    def truncate_category(self, category: str, maxLength: int):
        """
        Truncates a dot-separated category to fit within the maximum length.
        Keeps the last token and trims tokens from the left if necessary.
        :param category: The log category.
        :type category: str
        :param maxLength: The maximum allowed length for the category.
        :type maxLength: int
        :return: The truncated categeory.
        :rtype: str
        """
        tokens = category.split(".")

        # Start with the last token
        truncated = tokens[-1]

        # Add preceding tokens until the maxLength is reached
        for token in reversed(tokens[:-1]):
            candidate = f"{token}.{truncated}"
            if len(candidate) > maxLength:
                break
            truncated = candidate

        # If the category is truncated, prefix with '...'
        if len(truncated) < len(category):
            truncated = f"...{truncated}"

        return truncated

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


class LoggingPortFallback:
    """
    Fallback logging.

    Class name: LoggingPortFallback

    Responsibilities:
    - Provide basic logging mechanisms.

    Collaborators:
    - None
    """

    def __init__(self, thresholdLevel: str):
        """
        Initializes a new LoggingPortFallback instance.
        :param thresholdLevel: The threshold level.
        :type thresholdLevel: str
        """
        super().__init__()
        self._threshold_level = thresholdLevel

    @property
    def threshold_level(self) -> str:
        """
        Retrieves the threshold level.
        :return: Such level.
        :rtype: str
        """
        return self._threshold_level

    def logger(self, category: str):
        """
        Retrieves the logger instance.
        :param category: The logging category.
        :type category: str
        :return: Such instance.
        :rtype: logging.Logger
        """
        return LoggingFallback(self.threshold_level, category)


def format_log_message(category, message, max_category_length=30):
    """
    Formats a log message with a truncated category if necessary.

    Args:
        category (str): The log category.
        message (str): The log message.
        max_category_length (int): Maximum length for the category.

    Returns:
        str: The formatted log message.
    """
    truncated_category = truncate_category(category, max_category_length)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{current_time}] [{truncated_category}] {message}"


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

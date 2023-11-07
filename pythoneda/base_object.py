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
import re
from typing import Type


class BaseObject:
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
    def snake_to_camel(cls, input: str) -> str:
        """
        Converts a string in snake case to camel case.
        :param input: The snake-case input to convert.
        :type input: str
        :return: The camel-case version of the input.
        :rtype: str
        """
        components = input.split("_")
        return "".join(x.title() for x in components)

    @classmethod
    def camel_to_snake(cls, input: str) -> str:
        """
        Converts a string in camel case, to snake case.
        :param input: The camel-case input to convert.
        :type input: str
        :return: The snake-case version of the input.
        :rtype: str
        """
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", input)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", input).lower()

    @classmethod
    def kebab_to_camel(self, txt: str) -> str:
        """
        Transforms given kebab-case value to camel case.
        :param txt: The value.
        :type txt: str
        :return: The value formatted in camel case.
        :rtype: str
        """
        words = txt.split("-")
        result = "".join(word.capitalize() for word in words)
        return result[0].lower() + result[1:]

    @classmethod
    def camel_to_kebab(cls, txt: str) -> str:
        """
        Transforms given camel-case value to kebab case.
        :param txt: The value.
        :type txt: str
        :return: The value formatted in kebab case.
        :rtype: str
        """
        # Use regular expression to find capital letters and prepend them with a hyphen
        result = re.sub("([a-z0-9])([A-Z])", r"\1-\2", txt)
        # Convert the string to lowercase
        return result.lower()

    @classmethod
    def simplify_class_name(cls, input: str) -> str:
        """
        Simplifies given class name to remove the module if it's just a snake-case version of the actual class name.
        :param input: The class name to simplify.
        :type input: str
        :return: The simplified class name, or the input if it doesn't need to be simplified.
        :rtype: str
        """
        if "." not in input:
            return input  # If there's no dot, it's not a fully qualified class name

        module_name, class_name = input.rsplit(".", 1)

        # Extract the last part of the module path (if it exists)
        last_module_name = (
            module_name.split(".")[-1] if "." in module_name else module_name
        )

        # Convert the last part of the module path to CamelCase
        camel_case_last_module = cls.snake_to_camel(last_module_name)

        # Check if the class name is the CamelCase version of the last part of the module name
        if class_name == camel_case_last_module:
            # Remove the last part of the module name and append the class name
            return ".".join(module_name.split(".")[:-1] + [class_name])

        return input

    @classmethod
    def full_class_name(cls, target: Type = None) -> str:
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
        return f"{actual_target.__module__}.{actual_target.__name__}"

    @classmethod
    def logger(cls, category: str = None):
        """
        Retrieves the logger instance.
        :param category: The logging category.
        :type category: str
        :return: Such instance.
        :rtype: Any
        """
        if cls._logging_port is None:
            ports = Ports.instance()
            if ports is not None:
                cls._logging_port = ports.resolve(LoggingPort)
        if cls._logging_port is None:
            cls._logging_port = LoggingPortFallback()

        if category is None:
            cat = cls.simplify_class_name(cls.full_class_name(cls))
        else:
            cat = category

        return cls._logging_port.logger(cat)

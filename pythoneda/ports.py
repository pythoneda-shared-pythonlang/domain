"""
pythoneda/ports.py

This script defines the Ports class.

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
import importlib
from pythoneda import BaseObject, Port
from typing import Dict

class Ports(BaseObject):
    """
    Registry of available ports.

    Class name: Ports

    Responsibilities:
        - Maintain a registry of available ports.
        - Act as a singleton

    Collaborators:
        - Port: The resolved interfaces.
        - Adapter implementations in the infrastructure layer.
        - Application that provides the adapters when running the bounded context.
    """
    _singleton = None

    def __init__(self, mappings: Dict[Port, Port]):
        """
        Creates a new instance.
        :param mappings: The adapter mappings.
        :type mappings: Dict
        """
        self._mappings = mappings

    @classmethod
    def initialize(cls, mappings: Dict[Port, Port]):
        """
        Initializes the singleton.
        :param mappings: The adapter mappings.
        :type mappings: Dict
        """
        cls._singleton = Ports(mappings)

    @classmethod
    def instance(cls):
        """
        Retrieves the singleton instance.
        :return: Such instance.
        :rtype: Ports
        """
        return cls._singleton

    def resolve(self, port: Port) -> Port:
        """
        Resolves given port.
        :param port: The Port to resolve.
        :type port: Port
        :return: The adapter.
        :rtype: Port
        """
        return self._mappings.get(port, None)

    def resolve_by_module_name(self, moduleName: str, portName: str):
        """
        Resolves given port given a module name.
        :param moduleName: The name of the module.
        :type moduleName: str
        :param portName: The name of the Port to resolve.
        :type portName: str
        :return: The adapter.
        :rtype: Port
        """
        module = importlib.import_module(moduleName)
        port = getattr(module, portName)
        return self.resolve(port)

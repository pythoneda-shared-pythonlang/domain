"""
pythoneda/ports.py

This script defines the Ports class.

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
import importlib
from typing import Dict, List, Type


class Ports:
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

    def __init__(self, mappings: Dict[Type[Port], List[Port]]):
        """
        Creates a new instance.
        :param mappings: The adapter mappings.
        :type mappings: Dict
        """
        self._mappings = mappings

    @classmethod
    def initialize(cls, mappings: Dict[Type[Port], List[Port]]):
        """
        Initializes the singleton.
        :param mappings: The adapter mappings.
        :type mappings: Dict[Port, List[Port]]
        """
        cls._singleton = Ports(mappings)

    @classmethod
    def instance(cls):
        """
        Retrieves the singleton instance.
        :return: Such instance.
        :rtype: Ports
        """
        result = cls._singleton
        if result is None:
            import logging

            logging.getLogger("pythoneda.Ports").warning(
                "Ports not initialized. Adapters won't be available"
            )
            result = cls({})
        return result

    def resolve(self, port: Type[Port]) -> Port:
        """
        Resolves given port.
        :param port: The Port to resolve.
        :type port: pythoneda.Port
        :return: The adapter.
        :rtype: pythoneda.Port
        """
        result = None
        adapters = self.resolve_all(port)
        if len(adapters) > 0:
            result = self._instantiate_adapter(adapters[0])
        return result

    @staticmethod
    def _instantiate_adapter(adapterClass: Port) -> Port:
        """
        Instantiates given adapter.
        :param adapterClass: The adapter class.
        :type adapterClass: pythoneda.Port
        :return: The adapter instance.
        :rtype: pythoneda.Port
        """
        return adapterClass.instantiate()

    @classmethod
    def sort_by_priority(cls, otherClass: Port) -> int:
        """
        Delegates the priority information to given primary port.
        :param otherClass: The primary port.
        :type otherClass: pythoneda.Port
        :return: Such priority.
        :rtype: int
        """
        result = -1
        if otherClass.has_class_method("default_priority"):
            result = otherClass.default_priority()

        if otherClass.has_method("priority"):
            instance = otherClass.instantiate()
            if instance:
                result = instance.priority()

        return result

    def resolve_all(self, port: Type[Port]) -> List[Port]:
        """
        Resolves given port.
        :param port: The Port to resolve.
        :type port: Type[pythoneda.Port]
        :return: The adapter.
        :rtype: List[pythoneda.Port]
        """
        candidates = self._mappings.get(port, [])
        return sorted(candidates, key=self.__class__.sort_by_priority)

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

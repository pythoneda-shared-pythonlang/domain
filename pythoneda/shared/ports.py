# vim: set fileencoding=utf-8
"""
pythoneda/shared/ports.py

This script defines the Ports class.

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
from . import has_class_method, has_method
from .invariants import Invariants
from .port import Port
from .pythoneda_application import PythonedaApplication
import importlib
import inspect
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
        :param app: The application instance.
        :type app: pythoneda.shared.application.PythonEDA
        """
        self._mappings = mappings

    @classmethod
    def initialize(
        cls,
        mappings: Dict[Type[Port], List[Port]] = None,
    ):
        """
        Initializes the singleton.
        :param mappings: The adapter mappings.
        :type mappings: Dict[Port, List[Port]]
        """
        cls._singleton = Ports(mappings)

    @classmethod
    def instance(cls, warning: bool = True):
        """
        Retrieves the singleton instance.
        :param warning: Whether to show a warning if Ports is not initialized.
        :type warning: bool
        :return: Such instance.
        :rtype: Ports
        """
        result = cls._singleton
        if result is None and warning:
            import logging

            logging.getLogger("pythoneda.Ports").warning(
                "Ports not initialized. Adapters won't be available"
            )
            import traceback

            traceback.print_stack()

        return result

    def resolve(self, port: Type[Port]) -> List[Port]:
        """
        Resolves given port.
        :param port: The Port to resolve.
        :type port: Type[pythoneda.Port]
        :return: The adapters.
        :rtype: List[pythoneda.Port]
        """
        result = []
        adapter_classes_or_instances = self.resolve_all(port)
        for adapter_class_or_instance in adapter_classes_or_instances:
            if inspect.isclass(adapter_class_or_instance):
                adapter_class = adapter_class_or_instance
                result.append(self._instantiate_adapter(adapter_class))
            else:
                result.append(adapter_class_or_instance)

        return result

    def resolve_first(self, port: Type[Port]) -> Port:
        """
        Resolves given port to the first adapter found.
        :param port: The Port to resolve.
        :type port: Type[pythoneda.Port]
        :return: The adapter.
        :rtype: pythoneda.Port
        """
        result = None
        adapters = self.resolve(port)
        if len(adapters) > 0:
            result = adapters[0]

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
        if has_class_method(otherClass, "default_priority"):
            result = otherClass.default_priority()

        if has_method(otherClass, "priority"):
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

        candidates = self.filter_by_invariants(self._mappings.get(port, []))
        return sorted(candidates, key=self.__class__.sort_by_priority)

    def filter_by_invariants(self, adapters: List[Port]) -> List[Port]:
        """
        Filters given adapters by invariants.
        :param adapters: The adapters to filter.
        :type adapters: List[Port]
        :return: The filtered adapters.
        :rtype: List[Port]
        """
        result = []
        invariants = Invariants.instance()

        for adapter in adapters:
            if invariants.match(adapter, invariants.apply_all(self)):
                result.append(adapter)

        return result

    def resolve_by_module_name(self, moduleName: str, portName: str):
        """
        Resolves given port given a module name.
        :param moduleName: The name of the module.
        :type moduleName: str
        :param portName: The name of the Port to resolve.
        :type portName: str
        :param app: The application instance.
        :type app: pythoneda.shared.application.PythonEDA
        :return: The adapter.
        :rtype: Port
        """
        module = importlib.import_module(moduleName)
        port = getattr(module, portName)
        return self.resolve(port)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

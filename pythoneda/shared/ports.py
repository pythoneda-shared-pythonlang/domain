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
from .invariant import inject_invariants, Invariant
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

    def __init__(
        self, mappings: Dict[Type[Port], List[Port]], app: PythonedaApplication
    ):
        """
        Creates a new instance.
        :param mappings: The adapter mappings.
        :type mappings: Dict
        :param app: The application instance.
        :type app: pythoneda.shared.application.PythonEDA
        """
        self._mappings = mappings
        self._app = app

    @property
    def app(self):
        """
        Retrieves the application instance.
        :return: Such instance.
        :rtype: pythoneda.shared.PythonedaApplication
        """
        return self._app

    @classmethod
    @inject_invariants
    def initialize(
        cls,
        mappings: Dict[Type[Port], List[Port]],
        app: Invariant[PythonedaApplication] = None,
    ):
        """
        Initializes the singleton.
        :param mappings: The adapter mappings.
        :type mappings: Dict[Port, List[Port]]
        :param app: The application instance.
        :type app: pythoneda.shared.PythonedaApplication
        """
        cls._singleton = Ports(mappings, app)

    @classmethod
    @inject_invariants
    def instance(cls, app: Invariant[PythonedaApplication] = None):
        """
        Retrieves the singleton instance.
        :param app: The application instance.
        :type app: pythoneda.shared.application.PythonEDA
        :return: Such instance.
        :rtype: Ports
        """
        result = cls._singleton
        if result is None:
            import logging

            logging.getLogger("pythoneda.Ports").warning(
                "Ports not initialized. Adapters won't be available"
            )
            if app is not None:
                result = cls({}, app)

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
                result.append(self._instantiate_adapter(adapter_class, self.app))
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
    def _instantiate_adapter(adapterClass: Port, app) -> Port:
        """
        Instantiates given adapter.
        :param adapterClass: The adapter class.
        :type adapterClass: pythoneda.Port
        :param app: The application instance.
        :type app: pythoneda.shared.application.PythonEDA
        :return: The adapter instance.
        :rtype: pythoneda.Port
        """
        return adapterClass.instantiate(app)

    @classmethod
    def sort_by_priority(cls, otherClass: Port, app) -> int:
        """
        Delegates the priority information to given primary port.
        :param otherClass: The primary port.
        :type otherClass: pythoneda.Port
        :param app: The application instance.
        :type app: pythoneda.shared.application.PythonEDA
        :return: Such priority.
        :rtype: int
        """
        result = -1
        if has_class_method(otherClass, "default_priority"):
            result = otherClass.default_priority()

        if has_method(otherClass, "priority"):
            instance = otherClass.instantiate(app)
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

        def sort_by_priority_with_app(otherClass):
            return self.__class__.sort_by_priority(otherClass, self.app)

        candidates = self._mappings.get(port, [])
        return sorted(candidates, key=sort_by_priority_with_app)

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

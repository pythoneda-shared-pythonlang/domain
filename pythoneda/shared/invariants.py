# vim: set fileencoding=utf-8
"""
pythoneda/shared/invariants.py

This script defines the Invariants class.

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
from .base_object import BaseObject
from .invariant import Invariant
import functools
import inspect
import json
import threading
from typing import (
    Any,
    Dict,
    Generic,
    get_args,
    get_origin,
    List,
    Optional,
    Type,
    TypeVar,
)


class Invariants(BaseObject):
    """
    Represents a way to interact with the "invariant world".

    Responsibilities:
        - Provide a way to interact with any invariant.
    """

    _singleton = None

    def __init__(self):
        """
        Creates a new Invariants instance.
        """
        super().__init__()
        self._threadlocal_data = threading.local()
        self._threadlocal_data.values = {}

    @classmethod
    def instance(cls):
        """
        Retrieves an instance of the Invariants class.
        :return: Such instance.
        :rtype: pythoneda.shared.Invariants
        """
        if cls._singleton is None:
            cls._singleton = cls._initialize()

        return cls._singleton

    @classmethod
    def _initialize(cls):
        """
        Creates a new instance of this class.
        :return: The new instance.
        :rtype: pythoneda.shared.Invariants
        """
        return cls()

    def bind(self, invariant: Invariant, target: Any = None):
        """
        Binds an invariant to given target, or to all targets if none is specified.
        :param invariant: The invariant.
        :type invariant: pythoneda.shared.Invariant.
        :param target: The target instance.
        :type target: Any
        """
        if not hasattr(self._threadlocal_data, "values"):
            self._threadlocal_data.values = {}
        bound_invariants = self._threadlocal_data.values.get(target, {})
        bound_invariants[invariant.declared_type] = invariant
        self._threadlocal_data.values[target] = bound_invariants

    def bind_all(self, invariants: Dict[str, Invariant], target: Any = None):
        """
        Binds all given invariants to given target, or to all targets if none is specified.
        :param invariants: The invariants to bind.
        :type invariants: Dict[str, pythoneda.shared.Invariant]
        :param target: The target instance.
        :type target: Any
        """
        if not hasattr(self._threadlocal_data, "values"):
            self._threadlocal_data.values = {}
        self._threadlocal_data.values[target] = invariants

    def apply(self, invariantType: str, target: Any = None) -> Invariant:
        """
        Applies given invariant to a target instance.
        :param invariantType: The type of the invariant.
        :type invariantType: str
        :param target: The target instance.
        :type target: Any
        :return: The invariant for given target, or None.
        :rtype: pythoneda.shared.Invariant
        """
        # cls._threadlocal_data.values = {target: {invariantType: invariant}}
        # The 'target' key might be None if the invariant applies to any target
        result = None
        if hasattr(self._threadlocal_data, "values"):
            bound_invariants = self._threadlocal_data.values.get(target, None)
            if bound_invariants is None:
                bound_invariants = self._threadlocal_data.values.get(None, None)
            if bound_invariants is not None:
                result = bound_invariants.get(invariantType, None)

        return result

    def apply_all(self, target: Any = None) -> Dict[str, Invariant]:
        """
        Applies all invariants to a target instance.
        :param target: The target instance.
        :type target: Any
        :return: The invariants for given target.
        :rtype: Dict[str, pythoneda.shared.Invariant]
        """
        result = {}
        if hasattr(self._threadlocal_data, "values"):
            result = self._threadlocal_data.values.get(target, None)
            if result is None:
                result = self._threadlocal_data.values.get(None, {})

        return result

    def bind_all_from_json(self, jsonText: str):
        """
        Reconstructs invariants from given json text.
        :param jsonText: The json text.
        :type jsonText: str
        """
        # TODO: Implement this method
        import json

        self.bind_all_from_dict(json.loads(jsonText))

    def bind_all_from_dict(self, dict: Dict):
        """
        Reconstructs invariants from given json text.
        :param jsonText: The json text.
        :type jsonText: str
        """
        # TODO: Implement this method
        import json

        self._threadlocal_data.values = dict

    def to_json(self, target: Any = None) -> str:
        """
        Serializes invariants associated to given target, or all of them if None specified.
        :param target: The specific instance.
        :type target: Any
        :return: The serialized invariants for that target.
        :rtype: str
        """
        # TODO: Implement this method
        import json

        result = ""
        if hasattr(self._threadlocal_data, "values"):
            dict_to_serialize = self._threadlocal_data.values.get(target, None)
            if dict_to_serialize is None:
                dict_to_serialize = self._threadlocal_data.values.get(None, {})

            for k, v in dict_to_serialize.items():
                if isinstance(v, Invariant):
                    dict_to_serialize[k] = str(v.value)

            result = json.dumps(dict_to_serialize)

        return result

    def match(self, target: Any, invariants: Dict[str, Invariant]) -> bool:
        """
        Checks if given target matches all invariants.
        :param target: The target instance.
        :type target: Any
        :param invariants: The invariants.
        :type invariants: Dict[str, pythoneda.shared.Invariant]
        :return: True if the target matches all invariants; False otherwise.
        :rtype: bool
        """
        result = False
        if hasattr(self._threadlocal_data, "values"):
            bound_invariants = self._threadlocal_data.values.get(target, None)
            if bound_invariants is None:
                result = True
            else:
                result = True
                for invariantType, invariant in invariants.items():
                    target_invariant = bound_invariants.get(invariantType, None)
                    if target_invariant is None or not target_invariant.match(target):
                        result = False
                        break

        return result

    def __str__(self):
        """
        Retrieves a text representation of this instance.
        :return: Such representation.
        :rtype: str
        """
        return self.to_json(None)

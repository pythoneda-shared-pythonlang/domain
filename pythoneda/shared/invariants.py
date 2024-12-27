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
import functools
import inspect
import threading
from typing import Dict, Generic, get_args, get_origin, Optional, Type, TypeVar


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
    def initialize(cls):
        """
        Creates a new instance of this class.
        :return: The new instance.
        :rtype: pythoneda.shared.Invariants
        """
        instance = cls()

        if not hasattr(instance._threadlocal_data, "values"):
            # If the 'values' dictionary doesn't exist yet, create it
            instance._threadlocal_data.values = {}

        return instance

    def bind_invariant(self, invariant: Invariant, target: Any = None):
        """
        Binds an invariant to given target, or to all targets if none is specified.
        :param invariant: The type of the invariant.
        :type invariant: Type[pythoneda.shared.Invariant]
        :param target: The target instance.
        :type target: Any
        """
        bound_invariants = cls._threadlocal_data.values.get(target, {})
        bound_invariants[Invariant.__class__] = invariant
        cls._threadlocal_data.values[target] = bound_invariants

    def apply(self, invariantType: Type[Invariant], target: Any = None) -> Invariant:
        """
        Applies given invariant to a target instance.
        :param invariantType: The type of the invariant.
        :type invariantType: Type[pythoneda.shared.Invariant]
        :param target: The target instance.
        :type target: Any
        :return: The invariant for given target, or None.
        :rtype: pythoneda.shared.Invariant
        """
        result = None
        bound_invariants = cls._threadlocal_data.values.get(target, None)
        if bound_invariants is None:
            bound_invariants = cls._threadlocal_data.values.get(None, None)
        if bound_invariants is not None:
            result = bound_invariants.get(invariantType, None)

        return result

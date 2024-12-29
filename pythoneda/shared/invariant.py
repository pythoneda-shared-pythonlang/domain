# vim: set fileencoding=utf-8
"""
pythoneda/shared/invariant.py

This script contains the Invariant class and some decorators.

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
import functools
import inspect
import threading
from typing import Dict, Generic, get_args, get_origin, Optional, TypeVar


def inject_invariants(fn):
    """
    A decorator that:
    1) Reads the function signature.
    2) For parameters annotated with Invariant[SomeClass],
       if the caller didn't provide a value or provided None,
       we auto-create `Invariant(SomeClass)`.
    """
    sig = inspect.signature(fn)
    parameters = sig.parameters

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # 1) Bind the caller arguments
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # 2) For each parameter:
        for param_name, param in parameters.items():
            if param.default is None and param_name in bound_args.arguments:
                # Is the annotation something like Invariant[Application]?
                annotation = param.annotation
                # Check if it's a generic of Invariant
                if get_origin(annotation) == Invariant:
                    # E.g., get_args(annotation) -> (Application,)
                    (domain_type,) = get_args(annotation)

                    # If the caller passed None (or didn't pass anything):
                    if bound_args.arguments[param_name] is None:
                        # Create an Invariant value from that domain_type
                        bound_args.arguments[param_name] = Invariant.invariants().get(
                            param_name, {}
                        )

        # 3) Call the original function with updated bound_args
        return fn(*bound_args.args, **bound_args.kwargs)

    # Keep the same signature so help() and IDEs show correct info
    wrapper.__signature__ = sig
    return wrapper


def inject_all_invariants(fn):
    """
    A decorator that:
    1) Reads the function signature.
    2) For any parameter annotated with Dict[K, Invariant[V]],
       if the caller didn't provide a value or provided None,
       we auto-create a dict of invariants as a default.
    """
    sig = inspect.signature(fn)
    parameters = sig.parameters

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # For each parameter, check if it's annotated as a Dict[...] of Invariants
        for param_name, param in parameters.items():
            annotation = param.annotation
            if param_name in bound_args.arguments:
                dict_value = bound_args.arguments[param_name]

                # We only handle it if the annotation is a Dict[...] and the current value is None
                if dict_value is None and get_origin(annotation) == dict:
                    # e.g. Dict[str, Invariant[SomeClass]]
                    key_type, val_type = get_args(annotation)

                    # val_type should be something like Invariant[DomainType] in your design
                    if get_origin(val_type) == Invariant:
                        # We'll do something simple:
                        # Let's parse the domain type inside Invariant[...] if you want to be more dynamic
                        (domain_type,) = get_args(val_type)

                        bound_args.arguments[param_name] = Invariant.invariants()

        return fn(*bound_args.args, **bound_args.kwargs)

    # Keep the same signature so IDEs/docs see the original
    wrapper.__signature__ = sig
    return wrapper


T = TypeVar("T")


class Invariant(Generic[T]):
    """
    Represents a kind of invariant value that can be
    thread-locally bound for a given domain type.

    Responsibilities:
        - Provide a .value() that retrieves the thread-local value
          associated with its domain type (if any).
    """

    def __init__(self, value: T, declaredType: str):
        """
        Creates a new Invariant value.
        :param value: The invariant value.
        :type value: T
        :param declaredType: The type of this invariant.
        :type declaredType: str
        """
        self._value = value
        self._declared_type = declaredType

    @property
    def value(self) -> T:
        """
        Return the thread-local value associated with self._type,
        or None if nothing is bound for this type.
        """
        # Safely retrieve the dictionary of values if it exists,
        # or an empty dict if not
        return self._value

    @property
    def declared_type(self) -> str:
        """
        Retrieves the type of this invariant.
        :return: The type.
        :rtype: str
        """
        return self._declared_type

    def match(self, other: "Invariant") -> bool:
        """
        Check if the other invariant has the same value as this one.
        """
        return self._value == other._value

    def __str__(self) -> str:
        """
        Provides a string representation of this instance.
        :return: The text representing this instance.
        :rtype: str
        """
        return str(self._value)

    def __repr__(self) -> str:
        """
        Provides a string representation of this instance.
        :return: The text representing this instance.
        :rtype: str
        """
        return self.__str__()

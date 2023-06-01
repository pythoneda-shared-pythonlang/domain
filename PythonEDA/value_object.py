"""
value_object.py

This script contains the ValueObject class and some decorators.

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
from PythonEDA.formatting import Formatting
from PythonEDA.sensitive_value import SensitiveValue

import functools
from datetime import datetime
import importlib
import inspect
import re
from typing import Callable, Dict, List

_primary_key_attributes = {}
_filter_attributes = {}
_attributes = {}


def _build_func_key(func):
    """
    Builds a key for given function.
    :param func: The function.
    :type func: callable
    :return: A key.
    :rtype: str
    """
    return func.__module__

def _build_cls_key(cls):
    """
    Builds a key for given class.
    :param cls: The class.
    :type cls: type
    :return: A key.
    :rtype: str
    """
    return cls.__module__

def _classes_by_key(key):
    """
    Retrieves the classes annotated under given key.
    :param key: The key.
    :type key: str
    :return: The list of classes.
    :rtype: List
    """
    return [m[1] for m in inspect.getmembers(key, inspect.isclass)]

def _add_to_dictionary(func: Callable, value, dictionary: Dict):
    """
    Adds given function (specifically a derived value) in a dictionary.
    :param func: The function.
    :type func: callable
    :param value: The value to annotate.
    :type value: str, int, callable
    :param dictionary: The dictionary to store the function.
    :type dictionary: Dict
    """
    key = _build_func_key(func)
    if not key in dictionary.keys():
        dictionary[key] = []
    if not value in dictionary[key]:
        dictionary[key].append(value)

def _add_attribute(func):
    """
    Annotates given attribute getter.
    :param func: The getter.
    :type func: callable
    """
    _add_to_dictionary(func, func.__name__, _attributes)

def attribute(func):
    """
    Attribute decorator to annotate the property getter.
    :param func: The getter.
    :type func: callable
    """
    _add_attribute(func)
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper

def sensitive(func):
    """
    Decorator for sensitive attributes.
    :param func: The getter function to wrap.
    :type func: callable
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return SensitiveValue(func(self, *args, **kwargs))

    return wrapper


def primary_key_attribute(func):
    """
    Decorator for primary key attributes.
    :param func: The getter function to wrap.
    :type func: callable
    """
    _add_to_dictionary(func, func.__name__, _primary_key_attributes)
    _add_attribute(func)
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper


def filter_attribute(func):
    """
    Decorator for filter attributes.
    :param func: The getter function to wrap.
    :type func: callable
    """
    _add_dictionary(func, func.__name__, _filter_attributes)
    _add_attribute(func)
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper


class ValueObject:
    """
    A value object.

    Class name: ValueObject

    Responsibilities:
        - Represents a cohesive set of attributes.
        - Subclasses can add validations.

    Collaborators:
        - None
    """
    @classmethod
    def primary_key(cls) -> List:
        """
        Retrieves the list of attributes of the primary key (marked with @primary_key_attribute).
        :return: The primary key attributes.
        :rtype: List
        """
        result = []
        key = _build_cls_key(cls)
        if key in _primary_key_attributes:
            result = _primary_key_attributes[key]
        return result

    @classmethod
    def filter_attributes(cls) -> List:
        """
        Retrieves the list of attributes used to filter (marked with @filter_attribute).
        :return: The filter attributes.
        :rtype: List
        """
        result = []
        key = _build_cls_key(cls)
        if key in _filter_attributes:
            result = _filter_attributes[key]
        return result

    @classmethod
    def attributes(cls) -> List:
        """
        Retrieves all the attributes (marked with @attribute).
        :return: The class attributes.
        :rtype: List
        """
        result = []
        key = _build_cls_key(cls)
        if key in _attributes:
            result = _attributes[key]
        return ["id"] + result + ["_created", "_updated"]

    """
    Represents a value object.
    """

    def __init__(self):
        """
        Creates a new ValueObject instance.
        """
        self._id = id(self)
        self._created = datetime.now()
        self._updated = None

    @property
    def id(self):
        """
        Retrieves the autogenerated id value.
        :return: The id.
        :rtype: str
        """
        if hasattr(self, "_id"):
            return self._id
        else:
            return None

    @property
    def created(self):
        """
        Retrieves when the instance was created.
        :return: The created timestamp.
        :rtype: str
        """
        if hasattr(self, "_created"):
            return self._created
        else:
            return None

    @property
    def updated(self):
        """
        Retrieves the last time the value object was updated.
        :return: The updated timestamp.
        :rtype: str
        """
        if hasattr(self, "_updated"):
            return self._updated
        else:
            return None

    @classmethod
    def _propagate_attributes(cls):
        """
        Annotates this class' attributes among the descendants.
        """
        cls_key = _build_cls_key(cls)
        if cls_key in _attributes.keys():
            for subclass in cls.__subclasses__():
                subclass_key = _build_cls_key(subclass)
                if subclass_key not in _attributes.keys():
                    _attributes[subclass_key] = _attributes[cls_key].copy()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Initializes this class.
        :param kwargs: Any additional keyword arguments.
        :type kwargs: Dict
        """
        super().__init_subclass__(**kwargs)
        cls._propagate_attributes()

    def __str__(self):
        """
        Provides a string representation of this instance.
        :return: The text representing this instance.
        :rtype: str
        """
        aux = []
        key = _build_cls_key(self.__class__)
        if key in _attributes.keys():
            for attr in _attributes[key]:
                if hasattr(self, attr):
                    value = getattr(self, attr)
                    if callable(value):
                        aux.append(f'"{attr}": "' + str(value.fget(self)) + '"')
                    else:
                        aux.append(f'"{attr}": "' + str(value) + '"')
            internal = []
            if hasattr(self, "id") and self.id:
                internal.append(f'"id": "{self.id}"')
            internal.append(f'"class": "{self.__class__.__name__}"')
            if hasattr(self, "created") and self.created:
                internal.append(f'"created": "{self.created}"')
            if hasattr(self, "updated") and self.updated:
                internal.append(f'"updated": "{self.updated}"')
            aux.append('"_internal": { ' + ', '.join(internal) + ' }')

        if len(aux) > 0:
            result = '{ ' + ', '.join(aux) + ' }'
        else:
            result = super().__str__()

        return result

    def __repr__(self):
        """
        Provides a brief representation of this instance.
        :return: The brief text representing this instance.
        :rtype: str
        """
        result = []
        key = _build_cls_key(self.__class__)
        if key in _primary_key_attributes.keys():
            for attr in _primary_key_attributes[key]:
                result.append(f"'{attr}': '" + str(getattr(self, f"_{attr}")) + "'")

        if len(result) > 0:
            return "{ " + ", ".join(result) + " }"
        else:
            return super().__repr__()

    def __setattr__(self, varName, varValue):
        """
        Changes the value of an attribute of this instance.
        :param varName: The name of the attribute.
        :type varName: str
        :param varValue: The value of the attribute.
        :type varValue: int, bool, str, type
        """
        key = _build_cls_key(self.__class__)
        if key in _attributes.keys():
            if varName in [x for x in _attributes[key]]:
                self._updated = datetime.now()
        super(ValueObject, self).__setattr__(varName, varValue)

    def __eq__(self, other):
        """
        Checks if the identity of this entity matches given one.
        :param other: The other instance.
        :type other: ValueObject, type
        :return: True if both instances represent the same ValueObject; False otherwise.
        :rtype: bool
        """
        result = False
        if other is not None:
            if isinstance(other, Formatting):
                result = self.__eq__(other._formatted)
            elif isinstance(other, self.__class__):
                result = True
                for key in self.__class__.primary_key():
                    if getattr(self, key, None) != getattr(other, key, None):
                        result = False
                        break

        return result

    def __hash__(self):
        """
        Computes the hash of this instance.
        :return: Such value.
        :rtype: int
        """
        attrs = []
        for key in self.__class__.primary_key():
            attrs.append(getattr(self, key, None))
        if len(attrs) == 0:
            result = hash((self.id, self.__class__))
        else:
            result = hash(tuple(attrs))
        return result

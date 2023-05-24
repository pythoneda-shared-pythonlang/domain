from domain.formatting import Formatting

import functools
from datetime import datetime
import importlib
import inspect
import re
from typing import List

_primary_key_attributes = {}
_filter_attributes = {}
_attributes = {}


def _build_func_key(func):
    return func.__module__

def _build_cls_key(cls):
    return cls.__module__

def _classes_by_key(key):
    return [m[1] for m in inspect.getmembers(key, inspect.isclass)]

def _add_attribute_to_dictionary(func, dictionary):
    key = _build_func_key(func)
    if not key in dictionary.keys():
        dictionary[key] = []
    value = func.__name__
    if not value in dictionary[key]:
        dictionary[key].append(value)

def _add_attribute(func):
    _add_attribute_to_dictionary(func, _attributes)


def attribute(func):
    _add_attribute(func)
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper


def primary_key_attribute(func):
    _add_attribute_to_dictionary(func, _primary_key_attributes)
    _add_attribute(func)
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper


def filter_attribute(func):
    _add_attribute_to_dictionary(func, _filter_attributes)
    _add_attribute(func)
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return wrapper


class ValueObject:
    @classmethod
    def primary_key(cls) -> List:
        result = []
        key = _build_cls_key(cls)
        if key in _primary_key_attributes:
            result = _primary_key_attributes[key]
        return result

    @classmethod
    def filter_attributes(cls) -> List:
        result = []
        key = _build_cls_key(cls)
        if key in _filter_attributes:
            result = _filter_attributes[key]
        return result

    @classmethod
    def attributes(cls) -> List:
        result = []
        key = _build_cls_key(cls)
        if key in _attributes:
            result = _attributes[key]
        return ["id"] + result + ["_created", "_updated"]

    """
    Represents a value object.
    """

    def __init__(self):
        """Creates a new ValueObject instance"""
        self._id = id(self)
        self._created = datetime.now()
        self._updated = None

    @property
    def id(self):
        return self._id

    @property
    def created(self):
        return self._created

    @property
    def updated(self):
        return self._updated

    @classmethod
    def _propagate_attributes(cls):
        cls_key = _build_cls_key(cls)
        if cls_key in _attributes.keys():
            for subclass in cls.__subclasses__():
                subclass_key = _build_cls_key(subclass)
                if subclass_key not in _attributes.keys():
                    _attributes[subclass_key] = _attributes[cls_key].copy()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._propagate_attributes()

    def __str__(self):
        aux = []
        key = _build_cls_key(self.__class__)
        if key in _attributes.keys():
            for attr in _attributes[key]:
                aux.append(f"'{attr}': '" + str(getattr(self, f"_{attr}")) + "'")
            internal = []
            internal.append(f"'id': '{self._id}'")
            internal.append(f"'class': '{self.__class__.__name__}'")
            if self._created:
                internal.append(f"'_created': '{self._created}'")
            if self._updated:
                internal.append(f"'_updated': '{self._updated}'")
            aux.append("'_internal': { " + ", ".join(internal) + " }")

        if len(aux) > 0:
            result = "{ " + ", ".join(aux) + " }"
        else:
            result = super().__str__()

        return result

    def __repr__(self):
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
        key = _build_cls_key(self.__class__)
        if key in _attributes.keys():
            if varName in [x for x in _attributes[key]]:
                self._updated = datetime.now()
        super(ValueObject, self).__setattr__(varName, varValue)

    def __eq__(self, other):
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
        attrs = []
        for key in self.__class__.primary_key():
            attrs.append(getattr(self, key, None))
        if len(attrs) == 0:
            result = hash((self.id, self.__class__))
        else:
            result = hash(tuple(attrs))
        return result

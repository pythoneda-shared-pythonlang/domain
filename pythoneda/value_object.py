"""
pythoneda/value_object.py

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
import collections.abc
from datetime import datetime
import functools
import importlib
import inspect
import json
from pythoneda.formatting import Formatting
from pythoneda.sensitive_value import SensitiveValue
import re
from typing import Any, Callable, Dict, List
import uuid

_primary_key_properties = {}
_pending_primary_key_properties = []

_filter_properties = {}
_pending_filter_properties = []

_internal_properties = {}
_pending_internal_properties = []

_properties = {}
_pending_properties = []

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

    return f'{cls.__module__}.{cls.__name__}'

def _classes_by_key(key):
    """
    Retrieves the classes annotated under given key.
    :param key: The key.
    :type key: str
    :return: The list of classes.
    :rtype: List
    """
    return [m[1] for m in inspect.getmembers(key, inspect.isclass)]

def _add_to_pending(func:Callable, lst:List, name:str=""):
    """
    Adds given function (specifically a derived value) in a list.
    :param value: The value to annotate.
    :type value: Callable
    :param lst: The dictionary to store the function.
    :type lst: List
    """
    lst.append(func.__code__)

def _add_wrapper(func):
    """
    Annotates given property wrapper.
    :param func: The wrapper.
    :type func: callable
    """
    from pythoneda.value_object import _pending_properties
    _add_to_pending(func, _pending_properties, "properties")

def attribute(func):
    """
    Attribute decorator to annotate the property getter.
    :param func: The getter.
    :type func: callable
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    _add_wrapper(wrapper)

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
    _add_wrapper(wrapper)

    return wrapper

def primary_key_attribute(func):
    """
    Decorator for primary key attributes.
    :param func: The getter function to wrap.
    :type func: callable
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    from pythoneda.value_object import _pending_primary_key_properties
    _add_to_pending(wrapper, _pending_primary_key_properties, "primary_key_properties")
    _add_wrapper(wrapper)

    return wrapper

def filter_attribute(func):
    """
    Decorator for filter attributes.
    :param func: The getter function to wrap.
    :type func: callable
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    from pythoneda.value_object import _pending_filter_properties
    _add_to_pending(wrapper, _pending_filter_properties, "filter_properties")
    _add_wrapper(wrapper)

    return wrapper

def internal_attribute(func):
    """
    Decorator for internal attributes.
    :param func: The getter function to wrap.
    :type func: callable
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    from pythoneda.value_object import _pending_internal_properties
    _add_to_pending(wrapper, _pending_internal_properties, "internal_properties")
    return wrapper

def _process_pending_properties(cls:type, delete:bool=False):
    """
    Processes all pending properties of given class.
    :param cls: The class holding the properties.
    :type cls: type
    :param delete: Whether to clean up pending properties at the end or not.
    :type delete: bool
    """
    from pythoneda.value_object import _properties, _pending_properties, _primary_key_properties, _pending_primary_key_properties, _filter_properties, _pending_filter_properties, _internal_properties, _pending_internal_properties
    source = {}
    source["_properties"] = _pending_properties
    source["_primary_key_properties"] = _pending_primary_key_properties
    source["_filter_properties"] = _pending_filter_properties
    source["_internal_properties"] = _pending_internal_properties
    dest = {}
    dest["_properties"] = _properties
    dest["_primary_key_properties"] = _primary_key_properties
    dest["_filter_properties"] = _filter_properties
    dest["_internal_properties"] = _internal_properties
    for name, prop in cls.__dict__.items():
        if isinstance(prop, property):
            for key in [ "_primary_key_properties", "_filter_properties", "_properties", "_internal_properties" ]:
                _process_pending_property(cls, prop, source[key], dest[key], key)
    if False:
        del _pending_properties
        del _pending_filter_properties
        del _pending_primary_key_properties
        del _pending_internal_properties

def _process_pending_property(cls:type, prop:property, pending:List, properties:Dict, name:str=""):
    """
    Processes a pending property.
    :param cls: The class holding the property.
    :type cls: type
    :param prop: The property.
    :type prop: property
    :param pending: The pending properties.
    :type pending: List
    :param properties: The final properties.
    :type properties: Dict
    """
    cls_key = _build_cls_key(cls)
    if prop.fget.__code__ in pending:
        aux = properties.get(cls_key, None)
        if not aux:
            aux = []
        if not prop in aux:
            aux.append(prop)
        properties[cls_key] = aux

def _propagate_properties(cls):
    """
    Propagates properties from given class' parents.
    :param cls: The class holding the properties.
    :type cls: type
    """
    from pythoneda.value_object import _properties, _primary_key_properties, _filter_properties, _internal_properties
    cls_key = _build_cls_key(cls)
    for current_parent in cls.mro():
        parent_cls_key = _build_cls_key(current_parent)
        for props in [ _properties, _primary_key_properties, _filter_properties ]:
            if parent_cls_key in props.keys():
                if cls_key not in props.keys():
                    props[cls_key] = []
                for prop in props[parent_cls_key]:
                    if not prop in props[cls_key]:
                        props[cls_key].append(prop)
        if parent_cls_key in _internal_properties.keys():
            if cls_key not in _internal_properties.keys():
                _internal_properties[cls_key] = []
            for prop in _internal_properties[parent_cls_key]:
                if not prop in _internal_properties[cls_key]:
                    _internal_properties[cls_key].append(prop)

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
        from pythoneda.value_object import _primary_key_properties
        if key in _primary_key_properties.keys():
            result = list(map(lambda p: p.fget.__name__, _primary_key_properties[key]))
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
        if key in _filter_properties:
            result = _filter_properties[key]
        return result

    @classmethod
    def attributes(cls) -> List:
        """
        Retrieves all the attributes (marked with @attribute).
        :return: The class attributes.
        :rtype: List
        """
        from pythoneda.value_object import _properties, _internal_properties
        result = []
        key = _build_cls_key(cls)
        if key in _properties:
            result = _properties[key]
        if key in _internal_properties:
            result = result + _internal_properties[key]
        return result

    def __init__(self):
        """
        Creates a new ValueObject instance.
        """
        self._id = str(uuid.uuid4())
        self._created = datetime.now()
        self._updated = None

    @property
    @internal_attribute
    def id(self) -> str:
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
    @internal_attribute
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
    @internal_attribute
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
    def __init_subclass__(cls, **kwargs):
        """
        Initializes this class.
        :param kwargs: Any additional keyword arguments.
        :type kwargs: Dict
        """
        super().__init_subclass__(**kwargs)
        for current_parent in cls.mro():
            _process_pending_properties(current_parent, False)
        _process_pending_properties(cls, True)
        _propagate_properties(cls)
        cls_key = _build_cls_key(cls)
        from pythoneda.value_object import _internal_properties

    def _is_json_compatible(self, obj:Any) -> bool:
        """
        Checks if given value is already compatible with json format.
        :param obj: The value.
        :type obj: typing.Any
        :return: True in such case.
        :rtype: bool
        """
        return callable(getattr(obj, 'to_json', None))

    def _property_to_json(self, prop:property, includeNulls:bool=True) -> str:
        """
        Builds a json-compatible representation of given property.
        :param prop: The property.
        :type prop: Any
        :param includeNulls: Whether to include nulls or not.
        :type includeNulls: bool
        :return: A json representation of given property.
        :rtype: str
        """
        result = None
        result = f'"{prop.fget.__name__}": {self._value_to_json(prop.fget(self), includeNulls)}'
        return result

    def _value_to_json(self, value:Any, includeNulls:bool=True) -> str:
        """
        Builds a json-compatible representation of given value.
        :param value: The value.
        :type value: Any
        :param includeNulls: Whether to include nulls or not.
        :type includeNulls: bool
        :return: A json representation of given value.
        :rtype: str
        """
        result = None
        if callable(value):
            value = value.fget(self)
        if value:
            if type(value) is list or type(value) is dict:
                items = list(map(self._value_to_json, value))
                if len(items) > 0:
                    if type(value) is list:
                        result = '[ ' + ', '.join(items) + ' ]'
                    if type(value) is dict:
                        result = '{ ' + ', '.join(items) + ' }'
            elif self._is_json_compatible(value):
                result = value.to_json()
            else:
                result = json.dumps(str(value))
        elif includeNulls:
            result = "null"
        return result

    def _property_to_json_excluding_nulls(self, prop:property) -> str:
        """
        Builds a json-compatible representation of given property, excluding nulls.
        :param prop: The property.
        :type prop: property
        :return: A json representation of given attribute.
        :rtype: str
        """
        return self._property_to_json(attribute, includeNulls=False)

    def _properties_to_json(self, properties:List[property], includeNulls:bool=True) -> List[str]:
        """
        Builds a json-compatible representation of given attributes.
        :param properties: The properties.
        :type properties: List[property]
        :param includeNulls: Whether to include nulls or not.
        :type includeNulls: bool
        :return: A list with the json representation of each attribute.
        :rtype: List[str]
        """
        if includeNulls:
            result = list(filter(lambda x: x is not None, map(self._property_to_json, properties)))
        else:
            result = list(filter(lambda x: x is not None, map(self._property_to_json_excluding_nulls, properties)))

        return result

    def to_json(self) -> Dict:
        """
        Provides a JSON representation of this instance.
        :return: The JSON representing this instance.
        :rtype: str
        """
        return json.loads(self.__str__())

    def __str__(self) -> str:
        """
        Provides a string representation of this instance.
        :return: The text representing this instance.
        :rtype: str
        """
        aux = []
        key = _build_cls_key(self.__class__)
        if key in _properties.keys():
            aux = self._properties_to_json(_properties[key])
        internal = []
        if key in _internal_properties.keys():
            internal = self._properties_to_json(_internal_properties[key])
            internal.append(f'"class": "{self.__class__.__module__}.{self.__class__.__name__}"')
            aux.append('"_internal": { ' + ', '.join(internal) + ' }')

        if len(aux) > 0:
            result = '{ ' + ', '.join(aux) + ' }'
        else:
            result = super().__str__()

        return result

    def __repr__(self) -> str:
        """
        Provides a brief representation of this instance.
        :return: The brief text representing this instance.
        :rtype: str
        """
        result = []
        aux = []
        key = _build_cls_key(self.__class__)
        if key in _primary_key_properties.keys():
            aux = self._properties_to_json(_primary_key_properties[key], includeNulls=False)

        if len(aux) > 0:
            result = '{ ' + ', '.join(aux) + ' }'
        else:
            result = super().__repr__()

        return result

    def __setattr__(self, varName, varValue):
        """
        Changes the value of an attribute of this instance.
        :param varName: The name of the attribute.
        :type varName: str
        :param varValue: The value of the attribute.
        :type varValue: int, bool, str, type
        """
        key = _build_cls_key(self.__class__)
        if key in _properties.keys():
            if varName in [x for x in _properties[key]]:
                self._updated = datetime.now()
        super(ValueObject, self).__setattr__(varName, varValue)

    def __eq__(self, other) -> bool:
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

    def __hash__(self) -> int:
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

# vim: set fileencoding=utf-8
"""
pythoneda/shared/value_object.py

This script contains the ValueObject class and some decorators.

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
from . import BaseObject, Formatting, SensitiveValue
import functools
import importlib
import inspect
import json
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Union


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

    return f"{cls.__module__}.{cls.__name__}"


def _classes_by_key(key):
    """
    Retrieves the classes annotated under given key.
    :param key: The key.
    :type key: str
    :return: The list of classes.
    :rtype: List
    """
    return [m[1] for m in inspect.getmembers(key, inspect.isclass)]


def _add_to_pending(func: Callable, lst: List, name: str = ""):
    """
    Adds given function (specifically a derived value) in a list.
    :param func: The value to annotate.
    :type func: Callable
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
    from pythoneda.shared.value_object import _pending_properties

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

    from pythoneda.shared.value_object import _pending_primary_key_properties

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

    from pythoneda.shared.value_object import _pending_internal_properties

    _add_to_pending(wrapper, _pending_internal_properties, "internal_properties")
    return wrapper


def _process_pending_properties(cls: type, delete: bool = False):
    """
    Processes all pending properties of given class.
    :param cls: The class holding the properties.
    :type cls: type
    :param delete: Whether to clean up pending properties at the end or not.
    :type delete: bool
    """
    from pythoneda.shared.value_object import (
        _properties,
        _pending_properties,
        _primary_key_properties,
        _pending_primary_key_properties,
        _filter_properties,
        _pending_filter_properties,
        _internal_properties,
        _pending_internal_properties,
    )

    source = {
        "_properties": _pending_properties,
        "_primary_key_properties": _pending_primary_key_properties,
        "_filter_properties": _pending_filter_properties,
        "_internal_properties": _pending_internal_properties,
    }
    dest = {
        "_properties": _properties,
        "_primary_key_properties": _primary_key_properties,
        "_filter_properties": _filter_properties,
        "_internal_properties": _internal_properties,
    }
    for name, prop in cls.__dict__.items():
        if isinstance(prop, property):
            for key in [
                "_primary_key_properties",
                "_filter_properties",
                "_properties",
                "_internal_properties",
            ]:
                _process_pending_property(cls, prop, source[key], dest[key], key)
    if delete:
        del _pending_properties
        del _pending_filter_properties
        del _pending_primary_key_properties
        del _pending_internal_properties


def _process_pending_property(
    cls: type, prop: property, pending: List, properties: Dict, name: str = ""
):
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
        if prop not in aux:
            aux.append(prop)
        properties[cls_key] = aux


def _propagate_properties(cls):
    """
    Propagates properties from given class' parents.
    :param cls: The class holding the properties.
    :type cls: type
    """
    from pythoneda.shared.value_object import (
        _properties,
        _primary_key_properties,
        _filter_properties,
        _internal_properties,
    )

    cls_key = _build_cls_key(cls)
    for current_parent in cls.mro():
        parent_cls_key = _build_cls_key(current_parent)
        for props in [_properties, _primary_key_properties, _filter_properties]:
            if parent_cls_key in props.keys():
                if cls_key not in props.keys():
                    props[cls_key] = []
                for prop in props[parent_cls_key]:
                    if prop not in props[cls_key]:
                        props[cls_key].append(prop)
        if parent_cls_key in _internal_properties.keys():
            if cls_key not in _internal_properties.keys():
                _internal_properties[cls_key] = []
            for prop in _internal_properties[parent_cls_key]:
                if prop not in _internal_properties[cls_key]:
                    _internal_properties[cls_key].append(prop)


class ValueObject(BaseObject):
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
    def empty(cls):
        """
        Builds an empty instance. Required for unmarshalling.
        :return: An empty instance.
        :rtype: pythoneda.ValueObject
        """
        return cls()

    @classmethod
    def primary_key(cls) -> List:
        """
        Retrieves the list of attributes of the primary key (marked with @primary_key_attribute).
        :return: The primary key attributes.
        :rtype: List
        """
        result = []
        key = _build_cls_key(cls)
        from pythoneda.shared.value_object import _primary_key_properties

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
        from pythoneda.shared.value_object import _properties, _internal_properties

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
    def id(self) -> Union[str, None]:
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

    @staticmethod
    def _is_json_compatible(obj: Any) -> bool:
        """
        Checks if given value is already compatible with json format.
        :param obj: The value.
        :type obj: typing.Any
        :return: True in such case.
        :rtype: bool
        """
        return callable(getattr(obj, "to_json", None))

    def _property_to_json(self, prop: property, includeNulls: bool = False) -> str:
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
        if hasattr(prop, "fget"):
            value = self._value_to_json(prop.fget(self), includeNulls)
            if value:
                result = f'"{prop.fget.__name__}": {value}'
        return result

    def _property_to_tuple(self, prop: property, includeNulls: bool = False) -> tuple:
        """
        Builds a tuple of name, value of given property.
        :param prop: The property.
        :type prop: Any
        :param includeNulls: Whether to include nulls or not.
        :type includeNulls: bool
        :return: A tuple representation of given property.
        :rtype: tuple[str, str]
        """
        name = None
        value = None
        if hasattr(prop, "fget"):
            name = prop.fget.__name__
            value = self._value_to_json(prop.fget(self), includeNulls)
        return name, value

    @classmethod
    def _property_name(cls, prop: property) -> str:
        """
        Retrieves the name of the property.
        :param prop: The property.
        :type prop: Any
        :return: The property name.
        :rtype: str
        """
        result = None
        if hasattr(prop, "fget"):
            result = prop.fget.__name__
        return result

    def _method_takes_no_arguments(self, f: Callable) -> bool:
        """
        Checks if given method takes no arguments.
        :param f: The method to check.
        :type f: Callable
        :return: True if the method can be called without any argument.
        :rtype: bool
        """
        sig = inspect.signature(f)
        params = sig.parameters.values()
        return all(param.name == "self" for param in params)

    def _function_takes_no_arguments(self, f: Callable) -> bool:
        """
        Checks if given function takes no arguments.
        :param f: The function to check.
        :type f: Callable
        :return: True if the function can be called without any argument.
        :rtype: bool
        """
        sig = inspect.signature(f)
        params = sig.parameters.values()
        return len(params) == 0

    def _value_to_json(self, value: Any, includeNulls: bool = False) -> str:
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
            if inspect.isfunction(value) and self._function_takes_no_arguments(value):
                value = value()
            elif inspect.ismethod(value) and self._method_takes_no_arguments(value):
                value = value()
            elif isinstance(value, property):
                value = self._property_to_json(value, includeNulls)
        if value:
            if type(value) is list or type(value) is dict:
                items = list(map(lambda x: self._value_to_json(x, includeNulls), value))
                result = json.dumps(items)
            elif self._is_json_compatible(value):
                result = f"j{value.to_json()}"
            elif type(value) is str:
                result = f'"{value}"'
            elif type(value) is datetime:
                result = f'"{str(value)}"'
            else:
                result = json.dumps(str(value))
        elif includeNulls:
            result = "NULL"
        return result

    def _property_to_json_excluding_nulls(self, prop: property) -> str:
        """
        Builds a json-compatible representation of given property, excluding nulls.
        :param prop: The property.
        :type prop: property
        :return: A json representation of given attribute.
        :rtype: str
        """
        return self._property_to_json(prop, includeNulls=False)

    def _property_to_json_including_nulls(self, prop: property) -> str:
        """
        Builds a json-compatible representation of given property, including nulls.
        :param prop: The property.
        :type prop: property
        :return: A json representation of given attribute.
        :rtype: str
        """
        return self._property_to_json(prop, includeNulls=True)

    def _properties_to_json(
        self, properties: List[property], includeNulls: bool = False
    ) -> List[str]:
        """
        Builds a json-compatible representation of given attributes.
        :param properties: The properties.
        :type properties: List[property]
        :param includeNulls: Whether to include nulls or not.
        :type includeNulls: bool
        :return: A list with the json representation of each attribute.
        :rtype: List[str]
        """
        return list(
            filter(
                lambda x: x is not None,
                map(lambda x: self._property_to_json(x, includeNulls), properties),
            )
        )

    def _get_attribute_to_json(self, varName) -> str:
        """
        Retrieves the value of an attribute of this instance, as Json.
        :param varName: The name of the attribute.
        :type varName: str
        :return: The attribute value in json format.
        :rtype: str
        """
        return self.__getattribute__(varName)

    def to_dict(self) -> Dict:
        """
        Provides a dictionary representation of this instance.
        :return: The dictionary representing this instance.
        :rtype: str
        """
        result = {}
        internal_properties = {}
        key = _build_cls_key(self.__class__)
        if key in _internal_properties.keys():
            for prop in _internal_properties[key]:
                name, value = self._property_to_tuple(prop)
                if value:
                    internal_properties[name] = value
        internal = {
            "properties": internal_properties,
            "class": f"{self.__class__.__module__}.{self.__class__.__name__}",
        }
        result["_internal"] = internal
        if key in _properties.keys():
            for prop in _properties[key]:
                name, _ = self._property_to_tuple(prop)
                value = self._get_attribute_to_json(name)
                if value is not None:
                    result[name] = value
        return result

    @classmethod
    def default_json_serializer(cls, obj) -> Dict:
        """
        Uses obj.to_dict() in the JSON serialization process.
        :param obj: The object to serialize to JSON.
        :type obj: Any
        :return: A dictionary.
        :rtype: Dict
        """
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        else:
            raise TypeError(
                f"{obj.__class__.__name__} does not define to_dict() to serialize to JSON"
            )

    def to_json(self) -> str:
        """
        Provides a JSON representation of this instance.
        :return: The JSON representing this instance.
        :rtype: str
        """
        return json.dumps(
            self.to_dict(), default=self.__class__.default_json_serializer
        )

    @classmethod
    def from_json(cls, text: str):
        """
        Builds an instance based on given text.
        :param text: The serialized instance.
        :type text: str
        :return: A reconstructed instance.
        :rtype: pythoneda.ValueObject
        """
        result = None
        try:
            result = cls.from_dict(json.loads(text))
        except json.JSONDecodeError as e:
            ValueObject.logger().error(f"decoding error: {e}")
        except Exception as e:
            ValueObject.logger().error(f"Unexpected error: {e}")
            import traceback

            traceback.print_exc()
        return result

    @classmethod
    def from_dict(cls, contents: Dict):
        """
        Builds an instance based on given dictionary.
        :param contents: The instance properties.
        :type contents: Dict
        :return: A reconstructed instance.
        :rtype: pythoneda.ValueObject
        """
        module_name, class_name = contents["_internal"]["class"].rsplit(".", 1)
        module = importlib.import_module(module_name)
        actual_class = getattr(module, class_name)
        return actual_class.new_from_json(contents)

    @classmethod
    def new_from_json(cls, dictFromJson: Dict):
        """
        Builds an instance based on given dictionary.
        :param dictFromJson: The dictionary.
        :type dictFromJson: Dict
        :return: A reconstructed instance.
        :rtype: pythoneda.ValueObject
        """
        result = cls.empty()
        key = _build_cls_key(cls)
        for name, value in dictFromJson.items():
            for prop in _properties[key]:
                prop_name = cls._property_name(prop)
                if name == prop_name:
                    result._set_attribute_from_json(name, value)

        return result

    def _set_attribute_from_json(self, varName, varValue):
        """
        Changes the value of an attribute of this instance.
        :param varName: The name of the attribute.
        :type varName: str
        :param varValue: The value of the attribute.
        :type varValue: int, bool, str, type
        """
        try:
            self.__setattr__(varName, varValue)
        except AttributeError:
            self.__setattr__(f"_{varName}", varValue)

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
        if key in _internal_properties.keys():
            internal = self._properties_to_json(_internal_properties[key])
            internal.append(
                f'"class": "{self.__class__.__module__}.{self.__class__.__name__}"'
            )
            aux.append('"_internal": { ' + ", ".join(internal) + " }")

        if len(aux) > 0:
            result = "{ " + ", ".join(aux) + " }"
        else:
            result = super().__str__()

        return result

    def __repr__(self) -> str:
        """
        Provides a brief representation of this instance.
        :return: The brief text representing this instance.
        :rtype: str
        """
        aux = []
        key = _build_cls_key(self.__class__)
        if key in _primary_key_properties.keys():
            aux = self._properties_to_json(
                _primary_key_properties[key], includeNulls=False
            )

        if len(aux) > 0:
            result = "{ " + ", ".join(aux) + " }"
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
        super().__setattr__(varName, varValue)

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


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

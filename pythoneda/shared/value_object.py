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
from .base_object import BaseObject
from datetime import datetime
from .formatting import Formatting
import functools
import importlib
import inspect
from .invariant import Invariant
from .invariants import Invariants
import json
from .sensitive_value import SensitiveValue
from ._utils import has_method
import uuid
from typing import Any, Callable, Dict, List, Optional, Type, Union


_primary_key_properties = {}
_pending_primary_key_properties = []

_filter_properties = {}
_pending_filter_properties = []

_sensitive_properties = {}
_pending_sensitive_properties = []

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


def _find_cls_key(cls, props: Dict):
    """
    Finds a key for given class in a collection.
    :param cls: The class.
    :type cls: type
    :param props: The collection to inspect.
    :type props: Dict
    :return: A key.
    :rtype: str
    """
    global _properties
    result = _build_cls_key(cls)

    if not result in props:
        result = None
        for ancestor in cls.__mro__[1:]:
            key = _build_cls_key(ancestor)
            if key in props:
                result = key
                break

    return result


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
    from .value_object import _pending_properties

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

    from .value_object import _pending_sensitive_properties

    _add_to_pending(wrapper, _pending_sensitive_properties, "sensitive_properties")
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

    from .value_object import _pending_primary_key_properties

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

    from pythoneda.shared.value_object import _pending_filter_properties

    _add_to_pending(wrapper, _pending_filter_properties, "filter_properties")
    _add_wrapper(wrapper)

    return wrapper


def sensitive_attribute(func):
    """
    Decorator for sensitive attributes.
    :param func: The getter function to wrap.
    :type func: callable
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    from pythoneda.shared.value_object import _pending_sensitive_properties

    _add_to_pending(wrapper, _pending_sensitive_properties, "sensitive_properties")
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

    from .value_object import _pending_internal_properties

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
    from .value_object import (
        _properties,
        _pending_properties,
        _primary_key_properties,
        _pending_primary_key_properties,
        _filter_properties,
        _pending_filter_properties,
        _sensitive_properties,
        _pending_sensitive_properties,
        _internal_properties,
        _pending_internal_properties,
    )

    source = {
        "_properties": _pending_properties,
        "_primary_key_properties": _pending_primary_key_properties,
        "_filter_properties": _pending_filter_properties,
        "_sensitive_properties": _pending_sensitive_properties,
        "_internal_properties": _pending_internal_properties,
    }
    dest = {
        "_properties": _properties,
        "_primary_key_properties": _primary_key_properties,
        "_filter_properties": _filter_properties,
        "_sensitive_properties": _sensitive_properties,
        "_internal_properties": _internal_properties,
    }
    for name, prop in cls.__dict__.items():
        if isinstance(prop, property):
            for key in [
                "_primary_key_properties",
                "_filter_properties",
                "_sensitive_properties",
                "_properties",
                "_internal_properties",
            ]:
                _process_pending_property(cls, prop, source[key], dest[key], key)
    if delete:
        del _pending_properties
        del _pending_filter_properties
        del _pending_sensitive_properties
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
    from .value_object import (
        _properties,
        _primary_key_properties,
        _filter_properties,
        _sensitive_properties,
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


def make_hashable(obj):
    if isinstance(obj, (list, tuple)):
        return tuple(make_hashable(e) for e in obj)
    elif isinstance(obj, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, set):
        return frozenset(make_hashable(e) for e in obj)
    else:
        return obj


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

    def __init__(
        self, omitNulls: Optional[bool] = True, omitInternal: Optional[bool] = False
    ):
        """
        Creates a new ValueObject instance.
        :param omitNulls: Whether to omit null values or not.
        :type omitNulls: bool
        :param omitInternal: Whether to omit null values or not.
        :type omitInternal: bool
        """
        self._id = str(uuid.uuid4())
        self._created = datetime.now()
        self._updated = None
        self._deleted = None
        self._omit_internal_attributes = omitInternal
        self._omit_nulls = omitNulls
        super().__init__()

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
        from .value_object import _primary_key_properties

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
            result = list(map(lambda p: p.fget.__name__, _filter_properties[key]))
        return result

    @classmethod
    def sensitive_attributes(cls) -> List:
        """
        Retrieves the list of sensitive attributes (marked with @sensitive).
        :return: The sensitive attributes.
        :rtype: List
        """
        result = []
        key = _build_cls_key(cls)
        if key in _sensitive_properties:
            result = list(map(lambda p: p.fget.__name__, _sensitive_properties[key]))
        return result

    @classmethod
    def attributes(cls) -> List:
        """
        Retrieves all the attributes (marked with @attribute).
        :return: The class attributes.
        :rtype: List
        """
        from .value_object import _properties, _internal_properties

        result = []
        key = _build_cls_key(cls)
        if key in _properties:
            result = list(map(lambda p: p.fget.__name__, _properties[key]))
        if key in _internal_properties:
            result = result + list(
                map(lambda p: p.fget.__name__, _internal_properties[key])
            )
        return result

    @property
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

    @property
    @internal_attribute
    def deleted(self):
        """
        Retrieves when the value object was deleted, in such case.
        :return: The deleted timestamp.
        :rtype: str
        """
        if hasattr(self, "_deleted"):
            return self._deleted
        else:
            return None

    @property
    @internal_attribute
    def invariants(self) -> Dict[Type[Invariant], Invariant]:
        """
        Retrieves the invariants.
        :return: The runtime invariants.
        :rtype: Dict[Type[pythoneda.shared.Invariant], pythoneda.shared.Invariant]
        """
        return Invariants.instance().apply_all(self)

    @property
    def omit_nulls(self) -> bool:
        """
        Checks if null values should be omitted when serializing this instance.
        :return: True if they should be omitted, False otherwise.
        :rtype: bool
        """
        return self._omit_nulls

    @property
    def omit_internal_attributes(self) -> bool:
        """
        Checks if internal attributes should be omitted when serializing this instance.
        :return: True if they should be omitted, False otherwise.
        :rtype: bool
        """
        return self._omit_internal_attributes

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

    def _normalize_value(self, value: Any) -> Any:
        """
        Converts a value (which might be a nested ValueObject, dict, list, datetime, etc.)
        into a JSON-friendly Python type: dict, list, str, int, float, bool, or None.
        :param value: The value to normalize.
        :type value: Any
        :return: The normalized value.
        :rtype: Any
        """
        # 1. If it's already None, bool, int, float, or string, just return it.
        if value is None or isinstance(value, (bool, int, float, str)):
            return value

        # 2. Handle datetime
        if isinstance(value, datetime):
            # Return an ISO-formatted string
            return value.isoformat()

        # 3. If it's another ValueObject, recursively convert it via to_dict()
        if isinstance(value, ValueObject):
            return value.to_dict()

        # 4. If it's a list (or tuple), recursively convert each element
        if isinstance(value, (list, tuple)):
            return [self._normalize_value(v) for v in value]

        # 5. If it's a dict, recursively convert each key-value pair
        if isinstance(value, dict):
            return {k: self._normalize_value(v) for k, v in value.items()}

        # 6. If it has a .to_dict() method, call that, then normalize
        if hasattr(value, "to_dict") and callable(value.to_dict):
            # to_dict might still contain nested objects, so normalize again
            return self._normalize_value(value.to_dict())

        # 7. Fallback: just convert to string
        return str(value)

    def to_dict(
        self, omitNulls: Optional[bool] = None, omitInternal: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Returns this instance as a Python dict of {property_name: property_value}.
        This method only takes into account @property marked as @attribute, @primary_key_attribute, @internal_attribute, or @sensitive too.
        :return: The dictionary representing this instance.
        :rtype: Dict[str, Any]
        """
        result = {}
        internal = {}

        omit_nulls = omitNulls
        if omitNulls is None:
            omit_nulls = self.omit_nulls

        omit_internal = omitInternal
        if omitInternal is None:
            omit_internal = self.omit_internal_attributes

        if self.id is not None or not omit_nulls:
            result["id"] = self.id

        # Identify the "key" for this class
        cls_key = _build_cls_key(self.__class__)

        if cls_key in _properties:
            for prop in _properties[cls_key]:
                name = prop.fget.__name__
                raw_value = prop.fget(self)  # The actual Python object
                if not omit_nulls or raw_value is not None:
                    result[name] = self._normalize_value(raw_value)
        if not omit_internal:
            # 2b) Convert "internal" attributes
            if cls_key in _internal_properties:
                for prop in _internal_properties[cls_key]:
                    name = prop.fget.__name__
                    raw_value = prop.fget(self)
                    if not omit_nulls or raw_value is not None:
                        internal[name] = self._normalize_value(raw_value)

                # 2c) Include class info, or anything else internal
                internal["class"] = (
                    f"{self.__class__.__module__}.{self.__class__.__name__}"
                )
                result["_internal"] = internal

        return result

    def to_dict_simplified(self, omitNulls: Optional[bool] = None) -> Dict:
        """
        Provides a simplified dictionary representation of this instance.
        :param omitNulls: Whether to omit null values or not.
        :type omitNulls: bool
        :return: The dictionary representing this instance.
        :rtype: str
        """
        return self.to_dict(omitNulls=omitNulls, omitInternal=True)

    def to_json(self) -> str:
        """
        Provides a JSON representation of this instance.
        :return: The JSON representing this instance.
        :rtype: str
        """
        return json.dumps(self.to_dict(), default=self._normalize_value)

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
        if "_internal" in contents:
            module_name, class_name = contents["_internal"]["class"].rsplit(".", 1)
            module = importlib.import_module(module_name)
            actual_class = getattr(module, class_name)
            result = actual_class.new_from_json(contents)
        else:
            result = cls.new_from_json(contents)

        return result

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
        id = dictFromJson.get("id", None)
        if id is not None:
            result._id = id

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
        Returns a JSON-compatible string representation of this ValueObject.
        """
        return json.dumps(
            self.to_dict(), ensure_ascii=False, default=self._normalize_value
        )

    def __repr__(self) -> str:
        """
        Provides a brief representation of this instance.
        :return: The brief text representing this instance.
        :rtype: str
        """
        return json.dumps(self.to_dict_simplified(), ensure_ascii=False)

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
            attrs.append(make_hashable(getattr(self, key, None)))
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

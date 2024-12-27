# vim: set fileencoding=utf-8
"""
pythoneda/shared/__init__.py

This file ensures pythoneda.shared is a namespace.

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
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from ._utils import (
    full_class_name,
    snake_to_camel,
    camel_to_snake,
    kebab_to_camel,
    camel_to_kebab,
    kebab_to_snake,
    snake_to_kebab,
    simplify_class_name,
    has_method,
    has_class_method,
    sort_by_priority,
    method_has_no_parameters,
    method_has_one_parameter,
    has_default_constructor,
    has_one_param_constructor,
)
from .pythoneda_application import PythonedaApplication
from .port import Port
from .ports import Ports
from .logging_port import LoggingPort
from .logging_port_fallback import LoggingPortFallback
from .base_object import BaseObject
from .invariant import inject_all_invariants, inject_invariants, Invariant
from .invariants import Invariants
from .formatting import Formatting
from .sensitive_value import SensitiveValue
from .value_object import (
    attribute,
    filter_attribute,
    internal_attribute,
    primary_key_attribute,
    sensitive,
    ValueObject,
)
from .domain_exception import DomainException
from .unsupported_event import UnsupportedEvent
from .entity import Entity
from .entity_in_progress import EntityInProgress
from .event import Event
from .event_emitter import EventEmitter
from .event_listener import listen, EventListener
from .primary_port import PrimaryPort
from .event_listener_port import EventListenerPort
from .repo import Repo
from .flow import Flow

# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

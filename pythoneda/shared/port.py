# vim: set fileencoding=utf-8
"""
pythoneda/shared/port.py

This script defines the Port class.

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
import abc
from typing import Dict, Tuple


class Port(abc.ABC):
    """
    Represents a primary or secondary port.

    Class name: Port

    Responsibilities:
        - They are interfaces that get implemented by adapters in the infrastructure layer.
        - Port implementations interact with the outside.

    Collaborators:
        - Adapter implementations in the infrastructure layer.
        - Application that resolve Ports with adapters when running the bounded context.
        - Ports maintain a registry of Port instances.
    """

    _enabled = True

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()

    @classmethod
    def enable(cls, *args: Tuple, **kwargs: Dict):
        """
        Enables this port.
        :param args: Additional positional arguments.
        :type args: Tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: Dict
        """
        cls._enabled = True

    @classmethod
    @property
    def enabled(cls) -> bool:
        """
        Checks whether this port is enabled or not.
        :return: Such condition.
        :rtype: bool
        """
        return cls._enabled

    @classmethod
    @abc.abstractmethod
    def instantiate(cls):
        """
        Creates an instance.
        :return: The new instance.
        :rtype: pythoneda.shared.Port
        """
        pass


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

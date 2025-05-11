# vim: set fileencoding=utf-8
"""
pythoneda/shared/pythoneda_application.py

This script defines the PythonedaApplication class.

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
from .base_object import BaseObject
from .invariant import Invariant
from .invariants import Invariants
from typing import List


class PythonedaApplication(abc.ABC, BaseObject):
    """
    Represents an application.

    Class name: PythonedaApplication

    Responsibilities:
        - Marker for PythonEDA applications.

    Collaborators:
        - None
    """

    def __init__(self, name: str):
        """
        Creates a new PythonedaApplication instance.
        :param name: The name of the application.
        :type name: str
        """
        super().__init__()
        self._name = name
        Invariants.instance().bind(
            Invariant[PythonedaApplication](
                self, "pythoneda.shared.PythonedaApplication"
            ),
            None,
        )
        PythonedaApplication.logger().info(f"Running {self.name}")

    @property
    def name(self) -> str:
        """
        Gets the name of the application.
        :return: The name of the application.
        :rtype: str
        """
        return self._name

    @abc.abstractmethod
    async def accept(self, eventOrEvents) -> List:
        """
        Accepts and processes an event, potentially generating others in response.
        :param eventOrEvents: The event(s) to process.
        :type eventOrEvents: Union[pythoneda.shared.Event, collections.abc.Iterable]
        :return: The generated events in response.
        :rtype: List[pythoneda.shared.Event]
        """
        pass

    @classmethod
    @property
    def invariant_type(cls) -> str:
        """
        Retrieves the invariant type.
        :return: Such information.
        :rtype: str
        """
        return "pythoneda.shared.PythonedaApplication"

    def __str__(self):
        """
        Returns a string representation of the PythonedaApplication instance.
        :return: Such representation.
        :rtype: str
        """
        return self.name if self.name is not None else ""

    def __repr__(self):
        """
        Returns a string representation of the PythonedaApplication instance.
        :return: Such representation.
        :rtype: str
        """
        return self.__str__()


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

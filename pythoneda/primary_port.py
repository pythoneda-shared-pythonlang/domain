"""
pythoneda/primary_port.py

This script defines the PrimaryPort class.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythoneda/domain

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
from pythoneda import Port


class PrimaryPort(Port, abc.ABC):
    """
    Input ports to the domain.

    Class name: PrimaryPort

    Responsibilities:
        - Mark Ports accepting incoming events from the outside.

    Collaborators:
        - Application that resolves the adapters for PrimaryPorts.
    """

    def __init__(self):
        """
        Creates a new instance.
        """
        super().__init__()

    @abc.abstractmethod
    async def entrypoint(self, app):
        """
        Accepts input on behalf of the given application.
        :param app: The application.
        :type app: pythoneda.application.PythonEDA
        """
        raise NotImplementedError(
            "entrypoint(app:pythoneda.application.PythonEDA) must be implemented by subclasses"
        )

    @classmethod
    @property
    def is_one_shot_compatible(cls) -> bool:
        """
        Retrieves whether this primary port should be instantiated when
        "one-shot" behavior is active.
        It should return False if the port listens to future messages
        from outside.
        :return: True in such case.
        :rtype: bool
        """
        return False

    @classmethod
    def priority(cls) -> int:
        """
        Retrieves the default priority of the primary port.
        :return: The priority. The higher the value, the lower the priority.
        :rtype: int
        """
        return 100

# vim: set fileencoding=utf-8
"""
pythoneda/shared/primary_port.py

This script defines the PrimaryPort class.

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
from .port import Port
import abc


class PrimaryPort(Port, abc.ABC):
    """
    Input ports to the domain.

    Class name: PrimaryPort

    Responsibilities:
        - Mark Ports accepting incoming events from the outside.

    Collaborators:
        - Application that resolves the adapters for PrimaryPorts.
    """

    def __init__(self, app):
        """
        Creates a new instance.
        :param app: The application instance.
        :type app: pythoneda.shared.application.PythonEDA
        """
        super().__init__(app)

    @abc.abstractmethod
    async def entrypoint(self, app):
        """
        Accepts input on behalf of the given application.
        :param app: The application.
        :type app: pythoneda.application.PythonEDA
        """
        raise NotImplementedError(
            "entrypoint(app:pythoneda.shared.application.PythonEDA) must be implemented by subclasses"
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


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

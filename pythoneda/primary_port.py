"""
pythoneda/primary_port.py

This script defines the PrimaryPort class.

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
from pythoneda.port import Port

class PrimaryPort(Port):
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

    def priority(self) -> int:
        """
        Retrieves the priority of the primary port.
        :return: The priority. The higher the value, the lower the priority.
        :rtype: int
        """
        raise NotImplementedError("priority() must be implemented by subclasses")

    async def accept(self, app):
        """
        Accepts input on behalf of the given application.
        :param app: The application.
        :type app: PythonEDA
        """
        raise NotImplementedError("accept() must be implemented by subclasses")

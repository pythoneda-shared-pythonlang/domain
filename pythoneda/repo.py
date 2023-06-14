"""
pythoneda/repo.py

This script defines the Repo class.

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

from typing import Dict, List


class Repo(Port):
    """
    A repository for a specific entity class.

    Class name: Repo

    Responsibilities:
        - Provides access to persisted Entities.

    Collaborators:
        - Entity: The items persisted outside.
    """
    def __init__(self, entityClass):
        """
        Creates a new instance.
        :param entityClass: The associated Entity class.
        :type entityClass: Type[Entity]
        """
        self._entity_class = entityClass

    @property
    def entity_class(self):
        """
        Retrieves the associated Entity class.
        :return: Such class.
        :rtype: Type[Entity]
        """
        return self._entity_class

    def find_by_id(self, id: str):
        """Must be implemented by subclasses"""
        raise NotImplementedError("find_by_id() must be implemented by subclasses")


    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """Must be implemented by subclasses"""
        raise NotImplementedError("find_by_attribute() must be implemented by subclasses")


    def filter(self, dictionary: Dict):
        """Must be implemented by subclasses"""
        raise NotImplementedError("filter() must be implemented by subclasses")


    def insert(self, item):
        """Must be implemented by subclasses"""
        raise NotImplementedError("insert() must be implemented by subclasses")


    def update(self, item):
        """Must be implemented by subclasses"""
        raise NotImplementedError("update() must be implemented by subclasses")


    def delete(self, id: str):
        """Must be implemented by subclasses"""
        raise NotImplementedError("delete() must be implemented by subclasses")


    def find_by_pk(self, pk: Dict):
        """Must be implemented by subclasses"""
        raise NotImplementedError("find_by_pk() must be implemented by subclasses")


    def list(self) -> List:
        """Must be implemented by subclasses"""
        raise NotImplementedError("list() must be implemented by subclasses")

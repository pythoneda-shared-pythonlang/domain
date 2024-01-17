# vim: set fileencoding=utf-8
"""
pythoneda/shared/repo.py

This script defines the Repo class.

Copyright (C) 2023-today rydnr's pythoneda-shared/domain

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
from typing import Dict, List


class Repo(Port, abc.ABC):
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
        super().__init__()
        self._entity_class = entityClass

    @property
    def entity_class(self):
        """
        Retrieves the associated Entity class.
        :return: Such class.
        :rtype: Type[Entity]
        """
        return self._entity_class

    @abc.abstractmethod
    def find_by_id(self, identifier: str):
        """
        Retrieves an entity by its id.
        :param identifier: The id.
        :type identifier: str
        :return: An instance of the EntityClass type, or None if none found.
        :rtype: pythoneda.Entity
        """
        raise NotImplementedError("find_by_id() must be implemented by subclasses")

    @abc.abstractmethod
    def find_by_attribute(self, attributeName: str, attributeValue: str):
        """
        Retrieves the entities matching given attribute criteria.
        :param attributeName: The name of the attribute.
        :type attributeName: str
        :param attributeValue: The name of the attribute.
        :type attributeValue: str
        :return: The instances of the EntityClass matching given criteria, or an empty list if none found.
        :rtype: List[pythoneda.Entity]
        """
        raise NotImplementedError(
            "find_by_attribute() must be implemented by subclasses"
        )

    @abc.abstractmethod
    def filter(self, dictionary: Dict):
        """
        Retrieves the entities matching given criteria.
        :param dictionary: The filter.
        :type dictionary: Dict
        :return: The instances of the EntityClass matching given criteria, or an empty list if none found.
        :rtype: List[pythoneda.Entity]
        """
        raise NotImplementedError("filter() must be implemented by subclasses")

    @abc.abstractmethod
    def insert(self, item):
        """
        Persists a new Entity.
        :param item: The entity.
        :type item: pythoneda.Entity
        """
        raise NotImplementedError("insert() must be implemented by subclasses")

    @abc.abstractmethod
    def update(self, item):
        """
        Updates an existing Entity.
        :param item: The entity.
        :type item: pythoneda.Entity
        """
        raise NotImplementedError("update() must be implemented by subclasses")

    @abc.abstractmethod
    def delete(self, identifier: str):
        """
        Deletes an existing Entity.
        :param identifier: The identifier of the entity.
        :type identifier: str
        """
        raise NotImplementedError("delete() must be implemented by subclasses")

    @abc.abstractmethod
    def find_by_pk(self, pk: Dict):
        """
        Retrieves an entity matching a primary key filter.
        :param pk: The primary key values.
        :type pk: str
        :return: An instance of the EntityClass type, or None if none found.
        :rtype: pythoneda.Entity
        """
        raise NotImplementedError("find_by_pk() must be implemented by subclasses")

    @abc.abstractmethod
    def list(self) -> List:
        """
        Retrieves all entities.
        :return: The list of all entities.
        :rtype: List[Entity]
        """
        raise NotImplementedError("list() must be implemented by subclasses")
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

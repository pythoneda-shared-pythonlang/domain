"""
pythoneda/entity_in_progress.py

This script defines the EntityInProgress class.

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
from pythoneda.value_object import attribute, primary_key_attribute, ValueObject


class EntityInProgress(ValueObject):

    """
    Represents an Entity which doesn't have all information yet.

    Class name: EntityInProgress

    Responsibilities:
        - Temporary realization of an incomplete Entity.
        - Holds a registry of instances.

    Collaborators:
        - Entity: It mimics a specific Entity subclass.
    """

    _pending = {}

    def __init__(self):
        """
        Creates a new EntityInProgress instance.
        """
        super().__init__()
        self.__class__.register(self)

    @classmethod
    def register(cls, entityInProgress):
        """
        Registers a new instance.
        :param entityInProgress: The instance to register.
        :type entityInProgress: EntityInProgress
        """
        if entityInProgress not in cls._pending:
            cls._pending[cls.build_key_from_entity(entityInProgress)] = entityInProgress

    @classmethod
    def matching(cls, **kwargs):
        """
        Retrieves the EntityInProgress matching given criteria.
        :param kwargs: The criteria to use.
        :type kwargs: Dict
        :return: True if there's an EntityInProgress matching given criteria; False otherwise.
        :rtype: bool
        """
        return cls._pending.get(cls.build_key_from_attributes(**kwargs), None)

    @classmethod
    def build_key_from_attributes(cls, **kwargs) -> str:
        """
        Builds a key from the provided attributes.
        :param kwargs: The attribute information.
        :type kwargs: Dict
        :return: The key.
        :rtype: str
        """
        items = []
        for key in cls.primary_key():
            items.append(f'"{key}": "{kwargs.get(key, "")}"')
        return f'{{ {", ".join(items)} }}'

    @classmethod
    def build_key_from_entity(cls, entityInProgress) -> str:
        """
        Builds a key for given entity (in progress).
        :param entityInProgress: The entity in progress.
        :type entityInProgress: EntityInProgress
        :return: The key.
        :rtype: str
        """
        items = []
        for key in cls.primary_key():
            items.append(f'"{key}": "{getattr(entityInProgress, key, "")}"')
        return f'{{ {", ".join(items)} }}'

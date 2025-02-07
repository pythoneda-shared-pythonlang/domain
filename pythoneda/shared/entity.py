# vim: set fileencoding=utf-8
"""
pythoneda/shared/entity.py

This script defines the Entity class.

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
from datetime import datetime
from .event import Event
from .event_reference import EventReference
from .value_object import internal_attribute, ValueObject
from typing import List, Optional


class Entity(ValueObject, abc.ABC):
    """
    Represents an Entity: something meaningful, unique, with set of attributes, and, in good designs, behavior.

    Class name: Entity

    Responsibilities:
        - Defines uniqueness constraints.
        - A cohesive group of related attribute values.
        - Specifies attributes, including primary key's and those used for filtering, using ValueObject's decorators.

    Collaborators:
        - ValueObject: Provides attribute decorators, and __str__(), repr__(), __eq__() and __hash__().
        - Repo: To rebuild them from persistence layers.
    """

    def __init__(self, eventHistory: List[EventReference]):
        """
        Creates a new Entity instance.
        :param eventHistory: The event history.
        :type eventHistory: List[pythoneda.shared.EventReference]
        """
        self._event_history = eventHistory
        self._created_event = None
        self._deleted_event = None
        super().__init__()

    @property
    @internal_attribute
    def event_history(self) -> List[EventReference]:
        """
        Returns the event history.
        :return: The event history.
        :rtype: List[pythoneda.shared.EventReference]
        """
        return self._event_history

    @property
    def created_event(self) -> Optional[Event]:
        """
        Returns the event that created this entity.
        :return: The event that created this entity.
        :rtype: Optional[pythoneda.shared.Event]
        """
        return self._created_event

    @property
    def deleted_event(self) -> Optional[Event]:
        """
        Returns the event that deleted this entity.
        :return: The event that deleted this entity.
        :rtype: Optional[pythoneda.shared.Event]
        """
        return self._deleted_event

    @classmethod
    @abc.abstractmethod
    def _create_instance_from(cls, event: Event) -> "Entity":
        """
        Creates a new instance from a request.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: A new instance.
        :rtype: pythoneda.shared.Entity
        """
        pass

    @abc.abstractmethod
    def create_created_event(self, createRequested: Event) -> Event:
        """
        Creates a new client created event.
        :param createRequested: The request.
        :type createRequested: pythoneda.shared.Event
        :return: The event.
        :rtype: pythoneda.shared.Event
        """
        pass

    @classmethod
    def create_from(cls, event: Event) -> ValueObject:
        """
        Creates a new instance from a create-request event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: A new instance.
        :rtype: pythoneda.shared.ValueObject
        """
        result = cls._create_instance_from(event)

        result._created_event = result.create_created_event(event)

        result._event_history.append(
            EventReference(
                result._created_event.id, result._created_event.__class__.__name__
            )
        )

        return result

    @abc.abstractmethod
    def create_deleted_event(self, deleteRequest: Event) -> Event:
        """
        Creates a deleted event.
        :param deleteRequest: The request.
        :type deleteRequest: pythoneda.shared.Event
        :return: The event.
        :rtype: pythoneda.shared.Event
        """

    def delete(self, deleteRequest: Event) -> Event:
        """
        Deletes this instance.
        :param deleteRequest: The request.
        :type deleteRequest: pythoneda.shared.Event
        :return: The deleted event.
        :rtype: pythoneda.shared.Event
        """
        self._deleted_event = self.create_deleted_event(deleteRequest)

        self._event_history.append(
            EventReference(deleteRequest.id, deleteRequest.__class__.__name__)
        )
        self._event_history.append(
            EventReference(
                self._deleted_event.id, self._deleted_event.__class__.__name__
            )
        )

        self._deleted = datetime.now()

        return self._deleted_event


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:

# vim: set fileencoding=utf-8
"""
pythoneda/shared/flow.py

This script defines the Flow class.

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
from . import Entity, Event
import abc
from typing import Any, List


class Flow(Entity, abc.ABC):
    """
    Represents a Flow: a sequence of events.

    Class name: Flow

    Responsibilities:
        - Defines a sequence of events.

    Collaborators:
        - Event
    """

    def __init__(self, firstEvent: Event = None):
        """
        Creates a new Flow instance.
        :param firstEvent: The first event of the flow.
        :type firstEvent: pythoneda.shared.Event
        """
        super().__init__()
        self._first_event = None
        self._events = []
        self.add_event(firstEvent)

    @property
    def first_event(self) -> Event:
        """
        Retrieves the first event.
        :return: Such event.
        :rtype: pythoneda.Event
        """
        return self._first_event

    @property
    def events(self) -> List[Event]:
        """
        Retrieves the list of events of the flow.
        :return: Such list.
        :rtype: List[pythoneda.shared.Event]
        """
        return self._events

    def add_event(self, event: Event):
        """
        Adds a new event to the flow.
        :param event: The event.
        :type event: pythoneda.shared.Event
        """
        if event is not None:
            if self._first_event is None:
                self._first_event = event
            if event not in self._events:
                self._events.insert(0, event)

    async def resume(self, event: Event) -> List[Event]:
        """
        Resumes the flow with a new event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: The event resulting from resuming this flow.
        :rtype: List[pythoneda.shared.Event]
        """
        result = None

        my_event_ids = [evt.id for evt in self._events]
        incoming_event_ids = [event.id] + event.previous_event_ids
        if self.first_continued_second(incoming_event_ids, my_event_ids):
            result = await self.continue_flow(event)
        else:
            Flow.logger().debug(
                f"Cannot resume {incoming_event_ids} from the flow: {my_event_ids}"
            )

        return result

    def first_continued_second(self, first: List[str], second: List[str]) -> bool:
        """
        Check if the first list is a continuation of the second list.
        :param first: The first list.
        :type first: List[str]
        :param second: The second list.
        :type second: List[str]
        :return: True if the first list is a continuation of the second list, False otherwise.
        :rtype: bool
        """
        if first == second:
            return True

        # Check if first has at least one item not in second
        if not any(item not in second for item in first):
            return False

        # Find common items
        common_items = [item for item in first if item in second]

        # Check if there is at least one common item
        if not common_items:
            return False

        # Check if the order of common items is the same in both lists
        second_indices = [second.index(item) for item in common_items]
        if second_indices != sorted(second_indices):
            return False

        return True

    def is_subsequence(self, first: List[Any], second: List[Any]) -> bool:
        """
        Check if first is a subsequence of second.
        The order of elements in first must match their order in second.

        Example:
        first = [3, 5, 6]
        second = [3, 2, 5, 9, 6, 10]
        is_subsequence(first, second) -> True
        :param first: The first list.
        :type first: List[Any]
        :param second: The second list.
        :type second: List[Any]
        :return: True if the first list is a subsequence of the second list, False otherwise.
        :rtype: bool
        """
        # Index to track our progress in first
        idx = 0

        # Iterate over all items in second
        for item in second:
            # If current item matches the next needed item in first, move to the next needed item
            if item == first[idx]:
                idx += 1
                # If we've matched all items of first, return True
                if idx == len(first):
                    return True

                # If we exit the loop without matching all items of first, return False
        return idx == len(first)

    def find_latest_event(self, eventClass: type) -> Event:
        """
        Finds the latest event of the given class.
        :param eventClass: The class of the event.
        :type eventClass: type
        :return: Such event.
        :rtype: pythoneda.shared.Event
        """
        for event in reversed(self._events):
            if isinstance(event, eventClass):
                return event
        return None

    @abc.abstractmethod
    async def continue_flow(self, event: Event) -> List[Event]:
        """
        Continues the flow with a new event.
        :param event: The event.
        :type event: pythoneda.shared.Event
        :return: The events resulting from resuming this flow.
        :rtype: List[pythoneda.shared.Event]
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

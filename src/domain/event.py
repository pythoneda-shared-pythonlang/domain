from domain.value_object import ValueObject


class Event(ValueObject):
    """
    The base event class.
    """
    def __init__(self):
        """Creates a new event instance"""
        super().__init__()

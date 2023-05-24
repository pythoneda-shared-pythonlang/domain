class UnsupportedEvent(Exception):
    """
    An unsupported event was emitted.
    """

    def __init__(self, event):
        super().__init__(f'Unsupported event: {event}')

class Formatting:
    """
    Marks formatting wrappers.
    """
    def __init__(self, fmt):
        """Creates a new instance"""
        self._fmt = fmt

    @property
    def _formatted(self):
        return self._fmt

    def __getattr__(self, attr):
        """
        Delegate any method call to the wrapped instance.
        """
        return getattr(self._fmt, attr)

    def __str__(self):
        return self._fmt.__str__()

    def __repr__(self):
        return self._fmt.__repr__()

    def __eq__(self, other):
        return self._fmt.__eq__(other)

    def __hash__(self):
        return self._fmt.__hash__()

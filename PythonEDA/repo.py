from PythonEDA.port import Port

class Repo(Port):
    """
    A repository for a specific entity class.
    """
    def __init__(self, entity_class):
        self._entity_class = entity_class

    @property
    def entity_class(self):
        return self._entity_class

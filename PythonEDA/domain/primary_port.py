from domain.port import Port

class PrimaryPort(Port):
    """
    Input ports to the domain.
    """
    def priority(self) -> int:
        """Retrieves the priority of the primary port."""
        raise NotImplementedError("priority() must be implemented by subclasses")

    async def accept(self, app):
        """Accepts input on behalf of the given application."""
        raise NotImplementedError("accept() must be implemented by subclasses")

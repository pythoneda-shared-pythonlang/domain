from PythonEDA.event import Event

class EventEmitter:

    _receivers = []

    @classmethod
    def receivers(cls):
        return EventEmitter._receivers

    @classmethod
    def register_receiver(cls, receiver):
        if receiver not in EventEmitter._receivers:
            EventEmitter._receivers.append(receiver)

    @classmethod
    def unregister_receiver(cls, receiver):
        if receiver in EventEmitter._receivers:
            EventEmitter._receivers.remove(receiver)

    @classmethod
    async def emit(cls, event: Event):
        """
        Emits given event.
        """
        for receiver in EventEmitter._receivers:
            await receiver.accept(event)

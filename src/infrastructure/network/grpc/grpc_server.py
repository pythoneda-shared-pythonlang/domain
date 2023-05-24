from domain.event import Event
from domain.primary_port import PrimaryPort

from concurrent import futures
import grpc

import asyncio
import time
import json
import logging
from typing import Dict

class GrpcServer(PrimaryPort):

    _default_insecure_port = '[::]:50051'

    def __init__(port=None):
        super().__init__()
        if port:
            self._insecure_port = port
        else:
            self._insecure_port = self.__class__._default_insecure_port

    @property
    def app(self):
        return self._app

    @property
    def insecure_port(self) -> str:
        return self._insecure_port

    def priority(self) -> int:
        return 999

    def add_servicers(self, server, app):
        raise NotImplementedError("add_servicers() not implemented by {self.__class__}")

    async def accept(self, app):
        self._app = app
        serve_task = asyncio.create_task(self.serve(app))
        asyncio.ensure_future(serve_task)
        try:
            await serve_task
        except KeyboardInterrupt:
            serve_task.cancel()
            try:
                await serve_task
            except asyncio.CancelledError:
                pass

    async def serve(self, app):
        server = grpc.aio.server()
        add_servicers(self, server, app)
        server.add_insecure_port(self._insecure_port)
        logging.getLogger(__name__).info(f'gRPC server listening at {self.insecure_port}')
        await server.start()
        await server.wait_for_termination()

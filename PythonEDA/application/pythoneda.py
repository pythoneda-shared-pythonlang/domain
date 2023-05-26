#!/usr/bin/env python3

from PythonEDA.application.bootstrap import get_interfaces, get_implementations

import asyncio
import importlib
import importlib.util
import logging
import os
import sys
from typing import Callable, Dict

class PythonEDA():

    _singleton = None

    def __init__(self):
        super().__init__()
        self._primaryPorts = []

    def get_primary_ports(self):
        return self._primaryPorts

    @classmethod
    async def main(cls):
        cls._singleton = PythonEDA()
        mappings = {}
        for port in cls.get_port_interfaces():
            implementations = get_implementations(port)
            if len(implementations) == 0:
                logging.getLogger(__name__).critical(f'No implementations found for {port}')
            else:
                mappings.update({ port: implementations[0]() })
        Ports.initialize(mappings)
        cls._singleton._primaryPorts = get_implementations(PrimaryPort)
        EventListener.find_listeners()
        EventEmitter.register_receiver(cls._singleton)
        loop = asyncio.get_running_loop()
        loop.run_until_complete(await PythonEDA.instance().accept_input())

    @classmethod
    def get_port_interfaces(cls):
        # this is to pass the domain module, so I can get rid of the `import domain`
        return get_interfaces(Port, importlib.import_module('.'.join(Event.__module__.split('.')[:-1])))

    @classmethod
    def instance(cls):
        return cls._singleton

    @classmethod
    def delegate_priority(cls, primaryPort) -> int:
        return primaryPort().priority()

    async def accept_input(self):
        for primaryPort in sorted(self.get_primary_ports(), key=PythonEDA.delegate_priority):
            port = primaryPort()
            await port.accept(self)

    async def accept(self, event): # : Event) -> Event:
        result = []
        if event:
            firstEvents = []
            logging.getLogger(__name__).info(f'Accepting event {event}')
            for listenerClass in EventListener.listeners_for(event.__class__):
                resultingEvents = await listenerClass.accept(event)
                if resultingEvents and len(resultingEvents) > 0:
                    firstEvents.extend(resultingEvents)
            if len(firstEvents) > 0:
                result.extend(firstEvents)
                for event in firstEvents:
                    result.extend(await self.accept(event))
        return result

    async def accept_configure_logging(self, logConfig: Dict[str, bool]):
        module_function = self.__class__.get_log_config()
        module_function(logConfig["verbose"], logConfig["trace"], logConfig["quiet"])

    @classmethod
    def get_log_config(cls) -> Callable:
        result = None

        spec = importlib.util.spec_from_file_location("_log_config", os.path.join("PythonEDA", os.path.join("infrastructure", f"_log_config.py")))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        entry = {}
        configure_logging_function = getattr(module, "configure_logging", None)
        if callable(configure_logging_function):
            result = configure_logging_function
        else:
            print(f"Error in PythonEDA/infrastructure/_log_config.py: configure_logging")
        return result

from PythonEDA.event import Event
from PythonEDA.event_emitter import EventEmitter
from PythonEDA.event_listener import EventListener
from PythonEDA.port import Port
from PythonEDA.ports import Ports
from PythonEDA.primary_port import PrimaryPort

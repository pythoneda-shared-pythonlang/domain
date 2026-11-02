---
okf_version: "0.2"
---

# pythoneda-shared-pythonlang/domain

* [domain](pythoneda-shared-pythonlang-domain.md) - Shared Kernel: This package provides support for event-driven architectures in Python, following the hexagonal architecture layout, and encouraging domain-driven design.

## Application
* [PythonedaApplication](pythoneda-application.md) - Represents an application.

## Entity
* [Entity](entity.md) - Represents an Entity: something meaningful, unique, with set of attributes, and, in good designs, behavior.
* [Flow](flow.md) - Represents a Flow: a sequence of events.

## Event
* [Event](event.md) - The base event class.

## Event Emitter
* [EventEmitter](event-emitter.md) - Port able to emit Events.

## Event Listener
* [EventListener](event-listener.md) - This class can listen / receive events.

## Port
* [EventListenerPort](event-listener-port.md) - Port able to receive Events.
* [LoggingPort](logging-port.md) - Port for logging mechanisms.
* [Port](port.md) - Represents a primary or secondary port.
* [Ports](ports.md) - Registry of available ports.
* [PrimaryPort](primary-port.md) - Input ports to the domain.
* [Repo](repo.md) - A repository for a specific entity class.

## Value Object
* [BaseObject](base-object.md) - Ancestor of all PythonEDA classes.
* [DomainException](domain-exception.md) - The parent class of all domain exceptions.
* [EntityInProgress](entity-in-progress.md) - Represents an Entity which doesn't have all information yet.
* [EventReference](event-reference.md) - Represents a reference to an event.
* [Formatting](formatting.md) - Marks formatting wrappers.
* [Invariant](invariant.md) - Represents a kind of invariant value that can be
* [Invariants](invariants.md) - Represents a way to interact with the "invariant world".
* [LoggingFallback](logging-fallback.md) - Fallback logging.
* [LoggingPortFallback](logging-port-fallback.md) - Fallback logging.
* [SensitiveValue](sensitive-value.md) - Prevents sensitive values to be exposed.
* [UnsupportedEvent](unsupported-event.md) - An unsupported event was emitted.
* [ValueObject](value-object.md) - A value object.

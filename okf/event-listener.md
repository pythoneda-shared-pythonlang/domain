---
type: Event Listener
title: "EventListener"
description: "This class can listen / receive events."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/event_listener.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/event_listener.py
    title: pythoneda/shared/event_listener.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

This class can listen / receive events.

Class name: EventListener

Responsibilities:
    - Offers itself to be notified of new Events.
    - Provides a list of types of Events it supports.
    - Maintains a registry of listeners.

Collaborators:
    - Event: The message emitted.
    - EventEmitter: Those which emit events.

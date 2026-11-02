---
type: Event
title: "Event"
description: "The base event class."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/event.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/event.py
    title: pythoneda/shared/event.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

The base event class.

Class name: Event

Responsibilities:
    - Represents a change in the system state.
    - It's the only way to communicate among PythonEDA domains.

Collaborators:
    - EventEmitter: Emits Events.
    - EventListener: Listens to Events.

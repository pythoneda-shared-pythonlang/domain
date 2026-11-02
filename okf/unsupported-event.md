---
type: Value Object
title: "UnsupportedEvent"
description: "An unsupported event was emitted."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/unsupported_event.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/unsupported_event.py
    title: pythoneda/shared/unsupported_event.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

An unsupported event was emitted.

Class name: UnsupportedEvent

Responsibilities:
    - Contain context information about the event that was received and was not supported.

Collaborators:
    - PrimaryPort: Ports that accept events and detect unsupported ones.

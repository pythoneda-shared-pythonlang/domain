---
type: Port
title: "Ports"
description: "Registry of available ports."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/ports.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/ports.py
    title: pythoneda/shared/ports.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

Registry of available ports.

Class name: Ports

Responsibilities:
    - Maintain a registry of available ports.
    - Act as a singleton

Collaborators:
    - Port: The resolved interfaces.
    - Adapter implementations in the infrastructure layer.
    - Application that provides the adapters when running the bounded context.

---
type: Port
title: "Port"
description: "Represents a primary or secondary port."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/port.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/port.py
    title: pythoneda/shared/port.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

Represents a primary or secondary port.

Class name: Port

Responsibilities:
    - They are interfaces that get implemented by adapters in the infrastructure layer.
    - Port implementations interact with the outside.

Collaborators:
    - Adapter implementations in the infrastructure layer.
    - Application that resolve Ports with adapters when running the bounded context.
    - Ports maintain a registry of Port instances.

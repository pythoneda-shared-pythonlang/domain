---
type: Value Object
title: "Formatting"
description: "Marks formatting wrappers."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/formatting.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/formatting.py
    title: pythoneda/shared/formatting.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

Marks formatting wrappers.

Class name: Formatting

Responsibilities:
    - Wraps another instance's attributes.
    - Exposes only other instance's data, not behavior.

Collaborators:
    - PythonEDA/ValueObject: It uses this class to determine the behavior
      of its "__eq__()", "__str__()", "__repr__()" and "__hash__()".

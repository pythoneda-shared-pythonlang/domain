---
type: Value Object
title: "SensitiveValue"
description: "Prevents sensitive values to be exposed."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/sensitive_value.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/sensitive_value.py
    title: pythoneda/shared/sensitive_value.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

Prevents sensitive values to be exposed.

Class name: SensitiveValue

Responsibilities:
    - Wraps a sensitive value.
    - Overrides "__eq__()", "__str__()", "__repr__()" and "__hash__()" to avoid leaking the sensitive value,
    while preserving identity invariants.

Collaborators:
    - Any primitive type or class to protect.

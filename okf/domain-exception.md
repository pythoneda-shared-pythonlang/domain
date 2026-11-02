---
type: Value Object
title: "DomainException"
description: "The parent class of all domain exceptions."
resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/domain_exception.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/pythoneda/shared/domain_exception.py
    title: pythoneda/shared/domain_exception.py
  - id: readme
    resource: https://github.com/pythoneda-shared-pythonlang/domain/blob/main/README.md
    title: README.md
status: draft
---

The parent class of all domain exceptions.

Class name: Exception

Responsibilities:
    - Represents an error in a domain.
    - Subclasses should provide as much context as possible.

Collaborators:
    - Exception: Python's built-in exception class.
    - ValueObject: Overrides Python's default methods.

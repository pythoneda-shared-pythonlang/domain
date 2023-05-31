# PythonEDA/base

This package provides support for event-driven architectures in Python, following the hexagonal architecture layout, and encouraging domain-driven design.

In summary, PythonEDA helps you to focus on your domain, and assume all interaction with the outside is through events. For each domain, [this organization](https://github.com/pythoneda "PythonEDA") will host its model, [PythonEDA-Infrastructure](https://github.com/pythoneda-infrastructure "PythonEDA Infrastructure") you the infrastructure (grpc, d-bus, https, relational databases), and [PythonEDA-Application](https://github.com/pythoneda-application "PythonEDA Application") the glue that binds both layers together, and resolve the ports (in DDD jargon).

PythonEDA/base provides:
- Event support: Event, EventListener, EventEmitter;
- Port and PrimaryPort interfaces;
- Abstract entity class to derive yours from;
- ValueObject with decorators to provide `__str__()`, `__repr__()`, `__hash__()` and `__eq__()` for you.

Currenty domains modelled so far:
- [Python packages](https://github.com/pythoneda/python-packages "Python packages' github repository"): Domain of Python packages.
- [Git repositories](https://github.com/pythoneda/git-repositories "Git repositories' github repository"): Domain of Git repositories.
- [Nix flakes' github repository](https://github.com/pythoneda/nix-flakes "Nix flakes' github repository"): Domain of Nix flakes.


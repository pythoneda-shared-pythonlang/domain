# domain

This package provides support for event-driven architectures in Python, following the hexagonal architecture layout, and encouraging domain-driven design.

In summary, PythonEDA helps you to focus on your domain, and assume all interaction with the outside is through events. For each domain, [this organization](https://github.com/pythoneda "PythonEDA") will host its model, [PythonEDA-Infrastructure](https://github.com/pythoneda-infrastructure "PythonEDA Infrastructure") you the infrastructure (grpc, d-bus, https, relational databases), and [PythonEDA-Application](https://github.com/pythoneda-application "PythonEDA Application") the glue that binds both layers together, and resolve the ports (in DDD jargon).

PythonEDA/base provides:
- Event support: Event, EventListener, EventEmitter;
- Port and PrimaryPort interfaces;
- A Ports class to dynamically resolve port adapters (IoC);
- Abstract entity class to derive yours from;
- ValueObject with decorators to provide `__str__()`, `__repr__()`, `__hash__()` and `__eq__()` for you.

## How to declare it in your flake

Check the latest tag of the definition repository: https://github.com/pythoneda-shared-pythoneda-def/domain/tags, and use it instead of the `[version]` placeholder below.

```nix
{
  description = "[..]";
  inputs = rec {
    [..]
    pythoneda-shared-pythoneda-domain = {
      [optional follows]
      url =
        "github:pythoneda-shared-pythoneda-def/domain/[version]";
    };
  };
  outputs = [..]
};
```

If your project depends upon [https://github.com/nixos/nixpkgs](nixpkgs "nixpkgs") and/or [https://github.com/numtide/flake-utils](flake-utils "flake-utils"), you might want to pin them under the `[optional follows]` above.

The Nix flake is provided by the [https://github.com/pythoneda-shared-pythoneda-def/domain](pythoneda-shared-pythoneda-def/domain "pythoneda-shared-pythoneda-def/domain") repository.

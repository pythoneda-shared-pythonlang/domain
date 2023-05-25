from domain.port import Port

import importlib
from typing import Dict

class Ports():

    _singleton = None

    def __init__(self, mappings):
        self._mappings = mappings

    @classmethod
    def initialize(cls, mappings: Dict[Port, Port]):
        cls._singleton = Ports(mappings)

    @classmethod
    def instance(cls):
        return cls._singleton

    def resolve(self, port: Port) -> Port:
        return self._mappings.get(port, None)

    def resolve_by_module_name(self, module_name: str, port_name: str):
        module = importlib.import_module(module_name)
        port = getattr(module, port_name)
        return self.resolve(port)

    def resolvePythonPackageMetadataRepo(self):
        return self.resolve_by_module_name("domain.python.python_package_metadata_repo", "PythonPackageMetadataRepo")

    def resolveFlakeRepo(self):
        return self.resolve_by_module_name("domain.flake.flake_repo", "FlakeRepo")

    def resolveFlakeRecipeRepo(self):
        return self.resolve_by_module_name("domain.flake.recipe.flake_recipe_repo", "FlakeRecipeRepo")

    def resolveNixTemplateRepo(self):
        return self.resolve_by_module_name("domain.nix.nix_template_repo", "NixTemplateRepo")

    def resolveNixPythonPackageRepo(self):
        return self.resolve_by_module_name("domain.nix.python.nix_python_package_repo", "NixPythonPackageRepo")

    def resolveGitRepoRepo(self):
        return self.resolve_by_module_name("domain.git.git_repo_repo", "GitRepoRepo")

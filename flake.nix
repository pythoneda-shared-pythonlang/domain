{
  description = "Support for event-driven architectures in Python";

  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
    poetry2nix = {
      url = "github:nix-community/poetry2nix/v1.28.0";
      inputs.nixpkgs.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
    };
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixos { inherit system; };
        description = "Support for event-driven architectures in Python";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/pythoneda/base";
        maintainers = with pkgs.lib.maintainers; [ ];
        nixpkgsRelease = "nixos-23.05";
        shared = import ./nix/devShells.nix;
        pythoneda-base-for = { version, python }:
          python.pkgs.buildPythonPackage rec {
            pname = "pythoneda-base";
            inherit version;
            projectDir = ./.;
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [
              build
              pkgs.poetry
              poetry-core
            ];

            buildInputs = [ ];

            propagatedBuildInputs = [ ];

            checkInputs = with python.pkgs; [ pytest ];

            pythonImportsCheck = [ "pythoneda" ];

            postInstall = ''
              mkdir $out/dist
              cp dist/*.whl $out/dist
            '';

            meta = with pkgs.lib; {
              inherit description license homepage maintainers;
            };
          };
        pythoneda-base-0_0_1a12-for = python:
          pythoneda-base-for {
            version = "0.0.1a12";
            inherit python;
          };
      in rec {
        packages = rec {
          pythoneda-base-0_0_1a12-python38 =
            pythoneda-base-0_0_1a12-for pkgs.python38;
          pythoneda-base-0_0_1a12-python39 =
            pythoneda-base-0_0_1a12-for pkgs.python39;
          pythoneda-base-0_0_1a12-python310 =
            pythoneda-base-0_0_1a12-for pkgs.python310;
          pythoneda-base-0_0_1a12-python311 =
            pythoneda-base-0_0_1a12-for pkgs.python311;
          pythoneda-base-latest-python38 = pythoneda-base-0_0_1a12-python38;
          pythoneda-base-latest-python39 = pythoneda-base-0_0_1a12-python39;
          pythoneda-base-latest-python310 = pythoneda-base-0_0_1a12-python310;
          pythoneda-base-latest-python311 = pythoneda-base-0_0_1a12-python311;
          pythoneda-base-latest = pythoneda-base-latest-python311;
          default = pythoneda-base-latest;
        };
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-base-0_0_1a12-python38 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a12-python38;
            python = pkgs.python38;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-0_0_1a12-python39 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a12-python39;
            python = pkgs.python39;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-0_0_1a12-python310 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a12-python310;
            python = pkgs.python310;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-0_0_1a12-python311 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a12-python311;
            python = pkgs.python311;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-latest-python38 = pythoneda-base-0_0_1a12-python38;
          pythoneda-base-latest-python39 = pythoneda-base-0_0_1a12-python39;
          pythoneda-base-latest-python310 = pythoneda-base-0_0_1a12-python310;
          pythoneda-base-latest-python311 = pythoneda-base-0_0_1a12-python311;
          pythoneda-base-latest = pythoneda-base-latest-python310;
          default = pythoneda-base-latest;
        };
      });
}

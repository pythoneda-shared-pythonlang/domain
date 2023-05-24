{
  description = "Support for event-driven architectures in Python";

  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
    };
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixos { inherit system; };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
      in rec {
        packages = {
          pythoneda = mkPoetryApplication rec {
            pname = "pythoneda";
            version = "0.0.alpha.1";
            format = "pyproject";
            projectDir = ./.;

            pythonImportsCheck = [ ];

            meta = with pkgs.lib; {
              description = "Support for event-driven architectures in Python";
              license = licenses.gpl3;
              homepage = "https://github.com/rydnr/pythoneda";
              maintainers = with maintainers; [ ];
            };
          };
          default = packages.pythoneda;
          meta = with lib; {
            description = "Support for event-driven architectures in Python";
            license = licenses.gpl3;
            homepage = "https://github.com/rydnr/pythoneda";
            maintainers = with maintainers; [ ];
          };
        };
        defaultPackage = packages.default;
        devShell = pkgs.mkShell {
          buildInputs = with pkgs.python3Packages; [ packages.default ];
        };
        shell = flake-utils.lib.mkShell {
          packages = system: [ self.packages.${system}.default ];
        };
      });
}

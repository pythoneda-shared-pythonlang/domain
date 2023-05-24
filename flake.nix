{
  description = "Support for event-driven architectures in Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlay ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in rec {
        packages = {
          pythoneda-0_0_1 = (import ./pythoneda-0.0.1.nix) {
            inherit (pythonPackages)
              buildPythonApplication grpcio grpcio-tools requests packaging toml
              beautifulsoup4 mistune;
            inherit (pkgs) lib gnumake;
            mkPoetryApplication = pkgs.poetry2nix.mkPoetryApplication;
          };
          pythoneda = packages.pythoneda-0_0_1;
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

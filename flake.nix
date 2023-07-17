{
  description = "Support for event-driven architectures in Python";
  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixos { inherit system; };
        pname = "pythoneda";
        description = "Support for event-driven architectures in Python";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/pythoneda-shared/pythoneda";
        maintainers = with pkgs.lib.maintainers; [ ];
        nixpkgsRelease = "nixos-23.05";
        shared = import ./nix/shared.nix;
        pythonpackage = "pythoneda-shared-pythoneda";
        pythoneda-for = { version, python }:
          let
            pythonVersionParts = builtins.splitVersion python.version;
            pythonMajorVersion = builtins.head pythonVersionParts;
            pythonMajorMinorVersion =
              "${pythonMajorVersion}.${builtins.elemAt pythonVersionParts 1}";
            pnameWithUnderscores =
              builtins.replaceStrings [ "-" ] [ "_" ] pname;
            wheelName =
              "${pnameWithUnderscores}-${version}-py${pythonMajorVersion}-none-any.whl";
          in python.pkgs.buildPythonPackage rec {
            inherit pname version;
            projectDir = ./.;
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [ pkgs.jq poetry-core ];

            checkInputs = with python.pkgs; [ pytest ];

            pythonImportsCheck = [ pythonpackage ];

            postInstall = ''
              mkdir $out/dist $out/scripts
              cp dist/${wheelName} $out/dist
              cp scripts/* $out/scripts
              jq ".url = \"$out/dist/${wheelName}\"" $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json > temp.json && mv temp.json $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json
            '';

            meta = with pkgs.lib; {
              inherit description homepage license maintainers;
            };
          };
        pythoneda-0_0_1a21-for = python:
          pythoneda-for {
            version = "0.0.1a21";
            inherit python;
          };
      in rec {
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-0_0_1a21-python38 = shared.devShell-for {
            package = packages.pythoneda-0_0_1a21-python38;
            pythoneda = packages.pythoneda-0_0_1a21-python38;
            python = pkgs.python38;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-0_0_1a21-python39 = shared.devShell-for {
            package = packages.pythoneda-0_0_1a21-python39;
            pythoneda = packages.pythoneda-0_0_1a21-python39;
            python = pkgs.python39;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-0_0_1a21-python310 = shared.devShell-for {
            package = packages.pythoneda-0_0_1a21-python310;
            pythoneda = packages.pythoneda-0_0_1a21-python310;
            python = pkgs.python310;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-0_0_1a21-python311 = shared.devShell-for {
            package = packages.pythoneda-0_0_1a21-python311;
            pythoneda = packages.pythoneda-0_0_1a21-python311;
            python = pkgs.python311;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-latest-python38 = pythoneda-0_0_1a21-python38;
          pythoneda-latest-python39 = pythoneda-0_0_1a21-python39;
          pythoneda-latest-python310 = pythoneda-0_0_1a21-python310;
          pythoneda-latest-python311 = pythoneda-0_0_1a21-python311;
          pythoneda-latest = pythoneda-latest-python310;
          default = pythoneda-latest;
        };
        packages = rec {
          default = pythoneda-latest;
          pythoneda-0_0_1a21-python38 = pythoneda-0_0_1a21-for pkgs.python38;
          pythoneda-0_0_1a21-python39 = pythoneda-0_0_1a21-for pkgs.python39;
          pythoneda-0_0_1a21-python310 = pythoneda-0_0_1a21-for pkgs.python310;
          pythoneda-0_0_1a21-python311 = pythoneda-0_0_1a21-for pkgs.python311;
          pythoneda-latest = pythoneda-latest-python311;
          pythoneda-latest-python38 = pythoneda-0_0_1a21-python38;
          pythoneda-latest-python39 = pythoneda-0_0_1a21-python39;
          pythoneda-latest-python310 = pythoneda-0_0_1a21-python310;
          pythoneda-latest-python311 = pythoneda-0_0_1a21-python311;
        };
      });
}

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
        description = "Support for event-driven architectures in Python";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/pythoneda/base";
        maintainers = with pkgs.lib.maintainers; [ ];
        nixpkgsRelease = "nixos-23.05";
        shared = import ./nix/devShells.nix;
        pythoneda-base-for = { version, python }:
          let
            pname = "pythoneda-base";
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

            pythonImportsCheck = [ "pythoneda" ];

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
        pythoneda-base-0_0_1a16-for = python:
          pythoneda-base-for {
            version = "0.0.1a16";
            inherit python;
          };
      in rec {
        packages = rec {
          pythoneda-base-0_0_1a16-python38 =
            pythoneda-base-0_0_1a16-for pkgs.python38;
          pythoneda-base-0_0_1a16-python39 =
            pythoneda-base-0_0_1a16-for pkgs.python39;
          pythoneda-base-0_0_1a16-python310 =
            pythoneda-base-0_0_1a16-for pkgs.python310;
          pythoneda-base-0_0_1a16-python311 =
            pythoneda-base-0_0_1a16-for pkgs.python311;
          pythoneda-base-latest-python38 = pythoneda-base-0_0_1a16-python38;
          pythoneda-base-latest-python39 = pythoneda-base-0_0_1a16-python39;
          pythoneda-base-latest-python310 = pythoneda-base-0_0_1a16-python310;
          pythoneda-base-latest-python311 = pythoneda-base-0_0_1a16-python311;
          pythoneda-base-latest = pythoneda-base-latest-python311;
          default = pythoneda-base-latest;
        };
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-base-0_0_1a16-python38 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a16-python38;
            pythoneda-base = packages.pythoneda-base-0_0_1a16-python38;
            python = pkgs.python38;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-0_0_1a16-python39 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a16-python39;
            pythoneda-base = packages.pythoneda-base-0_0_1a16-python39;
            python = pkgs.python39;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-0_0_1a16-python310 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a16-python310;
            pythoneda-base = packages.pythoneda-base-0_0_1a16-python310;
            python = pkgs.python310;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-0_0_1a16-python311 = shared.devShell-for {
            package = packages.pythoneda-base-0_0_1a16-python311;
            pythoneda-base = packages.pythoneda-base-0_0_1a16-python311;
            python = pkgs.python311;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-base-latest-python38 = pythoneda-base-0_0_1a16-python38;
          pythoneda-base-latest-python39 = pythoneda-base-0_0_1a16-python39;
          pythoneda-base-latest-python310 = pythoneda-base-0_0_1a16-python310;
          pythoneda-base-latest-python311 = pythoneda-base-0_0_1a16-python311;
          pythoneda-base-latest = pythoneda-base-latest-python310;
          default = pythoneda-base-latest;
        };
      });
}

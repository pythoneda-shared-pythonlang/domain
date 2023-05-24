{ buildPythonApplication, lib, mkPoetryApplication, grpcio, grpcio-tools
, requests, packaging, toml, beautifulsoup4, mistune, gnumake }:

mkPoetryApplication rec {
  pname = "pythoneda";
  version = "0.0.1";
  format = "pyproject";
  projectDir = ./.;

  nativeBuildInputs = [ grpcio grpcio-tools gnumake ];

  propagatedBuildInputs = [ requests packaging toml beautifulsoup4 mistune ];

  buildInputs = [ ];

  pythonImportsCheck = [ ];
  meta = with lib; {
    description = "Support for event-driven architectures in Python";
    license = licenses.gpl3;
    homepage = "https://github.com/rydnr/pythoneda";
    maintainers = with maintainers; [ ];
  };
}

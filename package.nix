{
  buildPythonPackage,
  flit-core,
  gunicorn,
  lib,
  nixVersions,
  # optuna-dashboard,
  optuna,
  psutil,
  pydantic,
  pyright,
  pythonOlder,
  rich,
  ruff,
  scipy,
}:
let
  inherit (lib.fileset) toSource unions;
  inherit (lib.trivial) importTOML;
  pyprojectAttrs = importTOML ./pyproject.toml;
  finalAttrs = {
    pname = pyprojectAttrs.project.name;
    inherit (pyprojectAttrs.project) version;
    pyproject = true;
    disabled = pythonOlder "3.12";
    src = toSource {
      root = ./.;
      fileset = unions [
        ./pyproject.toml
        ./tune_nix_eval
      ];
    };
    build-system = [ flit-core ];
    dependencies = [
      gunicorn
      optuna
      psutil
      pydantic
      rich
      scipy
    ];
    # Not packaged.
    pythonRemoveDeps = [
      "optuna-dashboard"
    ];
    propagatedBuildInputs = [
      nixVersions.latest
    ];
    pythonImportsCheck = [ finalAttrs.pname ];
    nativeCheckInputs = [
      pyright
      ruff
    ];
    passthru.optional-dependencies.dev = [
      pyright
      ruff
    ];
    doCheck = true;
    checkPhase =
      # preCheck
      ''
        runHook preCheck
      ''
      # Check with ruff
      + ''
        echo "Linting with ruff"
        ruff check
        echo "Checking format with ruff"
        ruff format --diff
      ''
      # Check with pyright
      + ''
        echo "Typechecking with pyright"
        pyright --warnings
        echo "Verifying type completeness with pyright"
        pyright --verifytypes ${finalAttrs.pname} --ignoreexternal
      ''
      # postCheck
      + ''
        runHook postCheck
      '';
    meta = with lib; {
      inherit (pyprojectAttrs.project) description;
      homepage = pyprojectAttrs.project.urls.Homepage;
      maintainers = with maintainers; [ connorbaker ];
      mainProgram = "tune-nix-eval";
    };
  };
in
buildPythonPackage finalAttrs

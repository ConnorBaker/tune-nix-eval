{
  fetchFromGitHub,
  lib,
  stdenv,
}:
let
  heap-layers = fetchFromGitHub {
    owner = "emeryberger";
    repo = "Heap-Layers";
    rev = "a2048eae91b531dc5d72be7a194e0b333c06bd4c";
    hash = "sha256-vl3z30CBX7hav/DM/UE0EQ9lLxZF48tMJrYMXuSulyA=";
  };
in
stdenv.mkDerivation {
  strictDeps = true;

  pname = "hoard";
  version = "3.13-unstable-2024-08-02";

  src = fetchFromGitHub {
    owner = "emeryberger";
    repo = "Hoard";
    rev = "f021bdb810332c9c9f5a11ae5404aaa38fe129c0";
    hash = "sha256-Ui134VZyb5wUg20yXmPzTCle8aCevLVFyE0SCWSuM94=";
  };

  sourceRoot = "source/src";

  # Don't download dependencies.
  postPatch = ''
    substituteInPlace ./GNUmakefile \
      --replace-fail \
        'git clone https://github.com/emeryberger/Heap-Layers' \
        "" \
      --replace-fail \
        'PREFIX ?= /usr/lib' \
        "PREFIX ?= $out/lib"
    ln -s "${heap-layers}" ./Heap-Layers
  '';

  preInstall = ''
    mkdir -p "$out/lib"
  '';

  makeFlags = [
    "Linux-gcc-x86_64"
  ];

  doCheck = false;

  meta = {
    description = "A Fast, Scalable, and Memory-efficient Malloc for Linux, Windows, and Mac";
    homepage = "https://github.com/emeryberger/Hoard";
    license = lib.licenses.asl20;
    platforms = [ "x86_64-linux" ];
    maintainers = with lib.maintainers; [ connorbaker ];
  };
}

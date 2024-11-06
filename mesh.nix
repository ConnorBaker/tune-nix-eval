{
  buildBazelPackage,
  buildPackages,
  fetchFromGitHub,
  lib,
}:
buildBazelPackage {
  strictDeps = true;

  pname = "mesh";
  version = "0-unstable-2024-07-06";

  src = fetchFromGitHub {
    owner = "plasma-umass";
    repo = "Mesh";
    rev = "d45d6deec627b7d46de98dfb5415c30b7c1db9c6";
    hash = "sha256-fVph5EkQusbDVtZK5kLCqoW9EDyy2v1ACUe7QzrksTw=";
  };

  fetchAttrs.hash = "sha256-IZBQ1ICxOBo1p9JDNJsbdYyAvVqTnIRu510SibSk79g=";

  bazel = buildPackages.bazel_5;

  bazelBuildFlags = [
    "--config=modern-amd64"
    "--compilation_mode=opt"
  ];

  bazelTargets = [ "//src:mesh" ];

  removeRulesCC = false;

  removeLocalConfigCC = false;

  postPatch =
    ''
      rm -f .bazelversion
      rm -f ./tools/bazel
      rm -f ./bazel
    ''
    # Increase the arena size to 128 GB.
    # --replace-fail \
    #       'kArenaSize = 64ULL * 1024ULL * 1024ULL * 1024ULL;  // 64 GB' \
    #       'kArenaSize = 1024ULL * 1024ULL * 1024ULL * 1024ULL;  // 1024 GB' \
    #     --replace-fail \
    #       'static constexpr double kMeshesPerMap = .33;' \
    #       'static constexpr double kMeshesPerMap = .0001;' \
    + ''
      substituteInPlace ./src/common.h \
        --replace-fail \
          'static constexpr size_t kMinArenaExpansion = 4096;  // 16 MB in pages' \
          'static constexpr size_t kMinArenaExpansion = 2048;  // 8 MB in pages'
      substituteInPlace ./src/runtime.cc \
        --replace-fail \
          'const auto meshCount = static_cast<size_t>(kMeshesPerMap * mapCount);' \
          'const auto meshCount = static_cast<size_t>(kMeshesPerMap * 1048576.0);'
    '';

  buildAttrs.installPhase = ''
    runHook preInstall
    mkdir -p "$out/lib"
    install -c -m 0755 bazel-bin/src/libmesh.so "$out/lib/libmesh.so"
    mkdir -p "$out/include/plasma"
    install -c -m 0755 src/plasma/mesh.h "$out/include/plasma/mesh.h"
    runHook postInstall
  '';

  doCheck = false;

  meta = {
    description = "A memory allocator that automatically reduces the memory footprint of C/C++ applications";
    homepage = "https://github.com/plasma-umass/Mesh";
    license = lib.licenses.asl20;
    platforms = [ "x86_64-linux" ];
    maintainers = with lib.maintainers; [ connorbaker ];
  };
}

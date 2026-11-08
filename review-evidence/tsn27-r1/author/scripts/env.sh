# Pinned toolchain for the tsn-c-stack gates (sourced).
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$VALIDATION_TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
# The shared clang-18 wrapper names a removed directory; the scratch bin runs the same pinned binary,
# and clang-tidy from the CI image's package (clang-tidy-18 18.1.3-1ubuntu1, deb sha256 4880055c...b6b70363).
export PATH=$VALIDATION_STORAGE/tsn27-a751/bin:$VALIDATION_TOOLS/clang-18/bin:$PATH
# Mermaid CLI for the graph gate, with its node runtime.
export PATH=$HOME/.local/bin:$HOME/.hermes/node/bin:$PATH
export TMPDIR=$VALIDATION_STORAGE/tsn27-a751/tmp
mkdir -p "$TMPDIR"

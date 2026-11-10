# The pinned tsn-c-stack gate toolchain (sourced): GoogleTest/GMock 1.14.0, Clang 18.1.3, clang-tidy 18.1.3, Mermaid CLI 11.16.0.
export PATH=$TOOLS/clang-18/bin:$TOOLS/clang-tidy-18/bin:$TMP/pp210-a708/mermaid-cli/node_modules/.bin:$HOME/.hermes/node/bin:/usr/local/bin:/usr/bin:/bin
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export TMPDIR=$SCRATCH/donor/tmp
mkdir -p "$TMPDIR"

# Pinned tsn-c-stack gate toolchain (sourced). Needs TOOLS (pinned toolchain root) and SCRATCH (disposable dir).
# Clang 18.1.3 as clang-18 (lexing gates), clang-tidy 18.1.3, GoogleTest/GMock 1.14.0; host gcc/clang/cmake/cppcheck/
# riscv64-elf-gcc/qemu; Mermaid CLI from the user's PATH.
: "${TOOLS:?set TOOLS}" "${SCRATCH:?set SCRATCH}"
export PATH=$TOOLS/clang-18/bin:$TOOLS/clang-tidy-18/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export TMPDIR=$SCRATCH/tmp; mkdir -p "$TMPDIR"

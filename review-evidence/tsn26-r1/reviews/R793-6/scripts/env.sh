# Pinned toolchain environment for the tsn-c-stack gates (set TOOLS to the pinned tool root).
# GoogleTest 1.14.0, clang-tidy 18.1.3 and clang-18 (lexing) are pinned; the sanitizer arm uses the host clang.
TOOLS=${TOOLS:?set TOOLS to the pinned tool root}
export PATH="$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH"
export PKG_CONFIG_PATH="$TOOLS/gtest-1.14.0/lib/pkgconfig" CMAKE_PREFIX_PATH="$TOOLS/gtest-1.14.0" LD_LIBRARY_PATH="$TOOLS/gtest-1.14.0/lib"

# Source from the packet's scripts directory. Set TOOLS to the root holding the pinned
# gtest-1.14.0, clang-18 and clang-tidy-18 trees (the gates refuse other versions).
P=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
: "${TOOLS:?set TOOLS to the pinned toolchain root}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
# scratch/bin holds clang, clang++ and clang-18 wrappers that exec $TOOLS/clang-18/bin/clang-18.
mkdir -p "$P/scratch/bin"
for n in clang clang-18; do printf '#!/bin/sh\nexec %s/clang-18/bin/clang-18 "$@"\n' "$TOOLS" > "$P/scratch/bin/$n"; done
printf '#!/bin/sh\nexec %s/clang-18/bin/clang-18 --driver-mode=g++ "$@"\n' "$TOOLS" > "$P/scratch/bin/clang++"
chmod +x "$P/scratch/bin/"*
export PATH=$P/scratch/bin:$TOOLS/clang-tidy-18/bin:$PATH
export ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1

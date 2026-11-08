#!/bin/bash
# One variant tree of the exact head: build every hosted binary and run ctest; list failing tests.
# usage: escape.sh TAG [variant.py options...]
set -u; . "$(dirname "$0")/env.sh"
TAG=$1; shift
O=$RCP/escape/$TAG; D=$SCR/escape/$TAG; mkdir -p "$O"
tree HEAD "$D/src"
python3 -I "$(dirname "$0")/variant.py" "$D/src" "$@" > "$O/edit.log" 2>&1; e=$?
(cd "$D/src" && git diff --no-index -- "$REPO/include/wire.h" include/wire.h) > "$O/wire.diff" 2>&1
cmake -S "$D/src" -B "$D/build" -DCMAKE_BUILD_TYPE=Debug > "$D/configure.log" 2>&1; c=$?
cmake --build "$D/build" -j2 > "$D/build.log" 2>&1; b=$?
ctest --test-dir "$D/build" --output-on-failure -j2 > "$D/ctest.log" 2>&1; t=$?
fails=$(grep -E '^\[  FAILED  \] [A-Za-z0-9_]+\.[A-Za-z0-9_/]+$' "$D/ctest.log" | awk '{print $4}' | sort -u | tr '\n' ' ')
bins=$(grep -E '\(Failed\)|\*\*\*Failed' "$D/ctest.log" | grep -oE '[a-z_]+_tests' | sort -u | tr '\n' ' ')
echo "$TAG edit=$e configure=$c build=$b ctest=$t $(grep -E 'tests passed' "$D/ctest.log") failing_binaries=[$bins] failing_tests=[$fails]" | tee "$O/result.txt"

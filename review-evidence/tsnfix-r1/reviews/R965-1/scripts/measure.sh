#!/bin/bash
# measure.sh PACKET REPO COMMIT OUT JOBS: export COMMIT's tree, GCC coverage build, ctest, the commit's own coverage.py, arcs.py.
P=$1; R=$2; C=$3; O=$4; J=${5:-8}
. "$P/scripts/env.sh" "$P"
rm -rf "$O"; mkdir -p "$O/src"
git -C "$R" archive "$C" | tar -x -C "$O/src"
echo "commit $(git -C "$R" rev-parse "$C") tree $(git -C "$R" rev-parse "$C^{tree}")"
grep -E '^(src|include)/' "$O/src/tests/coverage.ratchet" | sed 's/^/ratchet at commit: /'
cmake -S "$O/src" -B "$O/build" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DTSN_COVERAGE=ON > "$O/configure.log" 2>&1 || { echo "configure rc $?"; exit 1; }
cmake --build "$O/build" -j"$J" > "$O/build.log" 2>&1 || { echo "build rc $?"; exit 1; }
find "$O/build" -name '*.gcda' -delete
ctest --test-dir "$O/build" --output-on-failure -j"$J" > "$O/ctest.log" 2>&1; echo "ctest rc $? : $(grep -E 'tests passed' "$O/ctest.log")"
(cd "$O/src" && python3 scripts/coverage.py "$O/build"); echo "coverage.py rc $?"
python3 "$P/scripts/arcs.py" "$O/src" "$O/build" > "$O/arcs.txt"; echo "arcs.py rc $?"
grep ' raw: ' "$O/arcs.txt"

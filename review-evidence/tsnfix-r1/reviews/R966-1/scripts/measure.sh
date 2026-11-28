#!/bin/sh
# Measure GCC coverage of one commit in a disposable export of it.
# usage: measure.sh <clone> <commit> <scratch-dir> <receipt-dir> <jobs>
set -u
here=$(cd "$(dirname "$0")" && pwd)
. "$here/env.sh"
clone=$1; commit=$2; scratch=$3; out=$4; jobs=$5
full=$(git -C "$clone" rev-parse "$commit^{commit}") || exit 2
short=$(printf %s "$full" | cut -c1-8)
tree=$scratch/tree-$short; build=$scratch/build-$short
rm -rf "$tree" "$build"; mkdir -p "$tree" "$out"
git -C "$clone" archive "$full" | tar -x -C "$tree" || exit 2
log=$out/measure-$short.txt
{
  echo "commit $full"
  echo "gcc $(gcc -dumpfullversion) gcov $(gcov --version | head -1)"
  echo "gtest $(pkg-config --modversion gtest)"
  cmake -S "$tree" -B "$build" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DTSN_COVERAGE=ON > "$build.configure.log" 2>&1; echo "configure rc $?"
  cmake --build "$build" -j"$jobs" > "$build.build.log" 2>&1; echo "build rc $?"
  find "$build" -name '*.gcda' -delete
  ctest --test-dir "$build" -j"$jobs" > "$build.ctest.log" 2>&1; echo "ctest rc $?"
  tail -4 "$build.ctest.log"
  echo "--- scripts/coverage.py (this commit's reader, exclusions and ratchet)"
  (cd "$tree" && python3 scripts/coverage.py "$build"); echo "coverage rc $?"
  echo "--- recorded ratchet at this commit"
  cat "$tree/tests/coverage.ratchet"
} > "$log" 2>&1
python3 "$here/arcs.py" "$build" src/adp.c "$tree/src/adp.c" > "$out/arcs-adp-$short.txt" 2>&1
python3 "$here/arcs.py" "$build" src/acmp.c "$tree/src/acmp.c" > "$out/arcs-acmp-$short.txt" 2>&1
echo "$short done"

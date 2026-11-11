#!/bin/bash
# Run the head's CTest suite (GCC Debug) with a planted src/acmp.c. usage: suite_on_plant.sh REPO HEAD PLANT.c OUT
set -u
REPO=$1 HEAD=$2 P=$3 O=$4
D=$(cd "$(dirname "$0")" && pwd); S=$D/../scratch; . "$D/env.sh"
rm -rf "$O"; git clone -q --no-local "$REPO" "$O/src" && git -C "$O/src" checkout -q --detach "$HEAD" || exit 3
cp "$P" "$O/src/src/acmp.c"
cmake -S "$O/src" -B "$O/b" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ > "$O/configure.log" 2>&1 || exit 4
cmake --build "$O/b" -j8 > "$O/build.log" 2>&1 || exit 5
for t in "$O"/b/acmp_tests "$O"/b/acmp_wide "$O"/b/acmp_walk; do
  n=$(basename "$t"); "$t" --gtest_brief=1 > "$O/$n.log" 2>&1; rc=$?; echo "$n rc=$rc"
  grep -h "^\[  FAILED  \]" "$O/$n.log" | sort -u | head -8
done

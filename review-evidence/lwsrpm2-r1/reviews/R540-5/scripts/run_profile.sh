#!/bin/sh
# Usage: run_profile.sh SRC PKT PROFILE(OFF|ON) CGREEN_PREFIX
# Runs the published tester.md suite commands for one profile; one rc line per step.
SRC=$1; PKT=$2; P=$3; CG=$4
B=$PKT/scratch/build-$P; R=$PKT/receipts/profile-$P; mkdir -p "$R"
export PYTHONDONTWRITEBYTECODE=1 CMAKE_PREFIX_PATH=$CG LD_LIBRARY_PATH=$CG/lib CPATH=$CG/include LIBRARY_PATH=$CG/lib
cd "$SRC" || exit 2
: > "$R/rc.txt"
step() { n=$1; shift; "$@" > "$R/$n.log" 2>&1; echo "$n rc=$?" >> "$R/rc.txt"; }
step configure cmake -S . -B "$B" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$P
step build cmake --build "$B" --parallel 16
step ctest ctest --test-dir "$B" --output-on-failure
step unit "$B/unit_tests"
step behave env SHLAN_LIBRARY="$B/libshlan.so" behave
step behave-dry behave --dry-run
echo done >> "$R/rc.txt"

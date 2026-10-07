#!/usr/bin/env bash
# Build and run both registrar profiles of the reviewed checkout concurrently.
# Usage: run_profiles.sh <checkout> <cgreen-prefix> <work-dir> <receipt-dir>
set -u
SRC=$1; CG=$2; WORK=$3; OUT=$4
mkdir -p "$WORK" "$OUT"
export CMAKE_PREFIX_PATH="$CG" LD_LIBRARY_PATH="$CG/lib"
run_profile() {
    local name=$1 milan=$2 b="$WORK/build-$1" log="$OUT/profile-$1.log"
    rm -rf "$b"
    {
        echo "## profile $name LWSRP_MILAN=$milan"
        cmake -S "$SRC" -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN="$milan"; echo "rc_configure=$?"
        cmake --build "$b" --parallel 8; echo "rc_build=$?"
        ctest --test-dir "$b" --output-on-failure; echo "rc_ctest=$?"
        "$b/unit_tests"; echo "rc_unit=$?"
        (cd "$SRC" && SHLAN_LIBRARY="$b/libshlan.so" behave --no-color); echo "rc_behave=$?"
        (cd "$SRC" && behave --dry-run --no-color) >/dev/null 2>&1; echo "rc_behave_dry=$?"
    } > "$log" 2>&1
}
run_profile default OFF &
run_profile milan ON &
wait
grep -h -E '^## profile|^rc_|Completed|tests? passed|passed,|scenarios? passed|steps? passed|feature' "$OUT"/profile-*.log

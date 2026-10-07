#!/usr/bin/env bash
# Run both unit profiles, scenarios, embedded/freestanding checks and both
# reversal drivers concurrently against a checkout. Each job writes its own
# log and rc file under OUT. Usage: run_suites.sh CHECKOUT CGREEN_PREFIX OUT
set -u
SRC=$(cd "$1" && pwd); PREFIX=$(cd "$2" && pwd); OUT=$3
mkdir -p "$OUT"; WORK="$OUT/work"; rm -rf "$WORK"; mkdir -p "$WORK"
export CMAKE_PREFIX_PATH="$PREFIX" LD_LIBRARY_PATH="$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export CPATH="$PREFIX/include" LIBRARY_PATH="$PREFIX/lib"

profile() { # $1 = OFF|ON
    local b="$WORK/build-$1"
    cmake -S "$SRC" -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN="$1" &&
    cmake --build "$b" --parallel 4 &&
    ctest --test-dir "$b" --output-on-failure &&
    "$b/unit_tests" &&
    (cd "$SRC" && SHLAN_LIBRARY="$b/libshlan.so" behave -f plain --no-capture) &&
    (cd "$SRC" && behave --dry-run)
}
job() { # $1 = name, rest = command
    local n=$1; shift
    ( "$@" ) > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc"
}
cd "$SRC"
job profile-OFF profile OFF &
job profile-ON profile ON &
job embedded python3 tests/check_embedded.py --work-dir "$WORK/embedded" &
job freestanding-OFF python3 tests/check_freestanding.py &
job freestanding-ON env CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py &
job reversals-OFF python3 tests/check_reversals.py --work-dir "$WORK/rev-OFF" --prefix "$PREFIX" &
job reversals-ON python3 tests/check_reversals.py --work-dir "$WORK/rev-ON" --prefix "$PREFIX" --milan ON &
wait
for f in "$OUT"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done

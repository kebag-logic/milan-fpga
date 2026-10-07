#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Reviewer probe campaign for lwSRP PR #3 (issue #2).
# Usage: probe.sh <lwsrp-clone> <cgreen-prefix> <work-dir> <receipt-dir>
# Each probe runs in its own git-archive copy of the reviewed head (or base),
# so the clone itself is never modified.  Probes run concurrently.
set -u
SRC=$1; CG=$2; WORK=$3; OUT=$4
HEAD=e4f9995b791489c53b8ccb8a8dc09ec508e32e6b
BASE=19f5796b63652eb1151906de73cb827d4980a53f
mkdir -p "$WORK" "$OUT"

copy() { # name rev
    rm -rf "$WORK/$1"; mkdir -p "$WORK/$1"
    git -C "$SRC" archive "$2" | tar -x -C "$WORK/$1"
}

# build <dir> [extra cmake args...]; records configure/build rc
build() {
    local d=$1; shift
    ( cd "$d" && cmake -B build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$CG" "$@" ) > "$d.configure.log" 2>&1
    echo "configure_rc=$?" >> "$d.rc"
    cmake --build "$d/build" -j4 > "$d.build.log" 2>&1
    echo "build_rc=$?" >> "$d.rc"
}
run_ctest() {
    ( cd "$1" && LD_LIBRARY_PATH="$CG/lib" ctest --test-dir build --output-on-failure ) > "$1.ctest.log" 2>&1
    echo "ctest_rc=$?" >> "$1.rc"
}
run_ctest_v() {
    ( cd "$1" && LD_LIBRARY_PATH="$CG/lib" ctest --test-dir build -V ) > "$1.ctest-v.log" 2>&1
    echo "ctest_v_rc=$?" >> "$1.rc"
}
run_behave() {
    ( cd "$1" && behave --no-color ) > "$1.behave.log" 2>&1
    echo "behave_rc=$?" >> "$1.rc"
}

probe() { # name rev mutation-function checks...
    local n=$1 rev=$2 mut=$3; shift 3
    local d="$WORK/$n"
    rm -f "$d.rc"
    copy "$n" "$rev"
    ( cd "$d" && $mut ) > "$d.mutate.log" 2>&1
    echo "mutate_rc=$?" >> "$d.rc"
    if [ "$rev" = "$HEAD" ]; then
        ( cd "$WORK" && diff -ru pristine_head "$n" ) > "$d.mutation.diff.log" 2>&1
    fi
    build "$d"
    for c in "$@"; do "$c" "$d"; done
}

none() { true; }
r1_drop_bindings() { sed -i '\#tests/features/switch_bindings.c#d' CMakeLists.txt && ! grep -q switch_bindings CMakeLists.txt; }
r2_old_env() { git -C "$SRC" show "$BASE:tests/features/environment.py" > tests/features/environment.py; }
r3_placeholder() {
    git -C "$SRC" show "$BASE:tests/unit/placeholder.c" > tests/unit/placeholder.c &&
    sed -i 's#add_executable(unit_tests tests/unit/main.c tests/unit/mrp_pdu_test.c)#add_executable(unit_tests tests/unit/placeholder.c)#' CMakeLists.txt &&
    grep -q 'unit_tests tests/unit/placeholder.c)' CMakeLists.txt
}
r4_empty_runner() { sed -i 's#TestSuite \*suite = mrp_pdu_suite();#TestSuite *suite = create_test_suite();#' tests/unit/main.c && grep -q 'suite = create_test_suite()' tests/unit/main.c; }
r5_wrong_byte() { sed -i 's#assert_that(packed, is_equal_to(215));#assert_that(packed, is_equal_to(214));#' tests/unit/mrp_pdu_test.c && grep -q 'is_equal_to(214)' tests/unit/mrp_pdu_test.c; }
x2_no_guard_empty_runner() { r4_empty_runner && sed -i '/FAIL_REGULAR_EXPRESSION/d' CMakeLists.txt && ! grep -q FAIL_REGULAR CMakeLists.txt; }
x3_disable_calls_enable() { sed -i 's#return shlan_port_disable(sw, port_id);#return shlan_port_enable(sw, port_id);#' tests/features/switch_bindings.c && grep -c 'shlan_port_enable(sw' tests/features/switch_bindings.c | grep -q 2; }
x4_enable_returns_zero() { sed -i 's#return shlan_port_enable(sw, port_id);#(void)shlan_port_enable(sw, port_id); return 0;#' tests/features/switch_bindings.c && grep -q 'return 0;' tests/features/switch_bindings.c; }
x5_connect_noop() { sed -i 's#return shlan_connect(sw);#(void)sw; return 0;#' tests/features/switch_bindings.c && grep -q '(void)sw; return 0;' tests/features/switch_bindings.c; }

copy pristine_head "$HEAD"
# Reviewed head and base (before) baselines.
probe p0_head  "$HEAD" none run_ctest run_ctest_v run_behave &
probe p1_base  "$BASE" none run_ctest run_ctest_v run_behave &
# The five planted reversals named in the author evidence.
probe r1_drop_bindings "$HEAD" r1_drop_bindings run_behave &
probe r2_old_env       "$HEAD" r2_old_env       run_behave &
probe r3_placeholder   "$HEAD" r3_placeholder   run_ctest run_ctest_v &
probe r4_empty_runner  "$HEAD" r4_empty_runner  run_ctest run_ctest_v &
probe r5_wrong_byte    "$HEAD" r5_wrong_byte    run_ctest &
# Reviewer-own probes.
probe x2_no_guard_empty_runner "$HEAD" x2_no_guard_empty_runner run_ctest &
probe x3_disable_calls_enable  "$HEAD" x3_disable_calls_enable  run_behave &
probe x4_enable_returns_zero   "$HEAD" x4_enable_returns_zero   run_behave &
probe x5_connect_noop          "$HEAD" x5_connect_noop          run_behave &
wait

# x1: configure without any cgreen on the search path must fail.
copy x1_no_cgreen "$HEAD"
( cd "$WORK/x1_no_cgreen" && cmake -B build ) > "$WORK/x1_no_cgreen.configure.log" 2>&1
echo "configure_rc=$?" > "$WORK/x1_no_cgreen.rc"

for f in "$WORK"/*.rc; do echo "== $(basename "$f" .rc)"; cat "$f"; done > "$OUT/probe-rc.txt"
for f in "$WORK"/*.log; do cp "$f" "$OUT/"; done

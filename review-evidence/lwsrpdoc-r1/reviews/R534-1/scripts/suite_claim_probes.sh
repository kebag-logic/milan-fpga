#!/bin/bash
# Disposable probes of tester/integrator claims, each in its own export of HEAD, run concurrently.
#  A empty-suite: runner executes an empty cgreen suite -> ctest must FAIL (tester.md:31).
#  B no-cgreen: configure without the cgreen prefix -> configure must FAIL (integrator.md:20).
#  C wrong-disable-binding: shlan_test_port_disable calls enable -> does behave detect it? (tester.md:87-88)
#  D noop-connect + wrong-enable: connect no-op, enable binding calls disable -> does behave detect it?
# Usage: suite_claim_probes.sh <clone> <workdir> <cgreen-prefix> <logdir>
set -u
CLONE=$1; W=$2; DEPS=$3; L=$4; mkdir -p "$L"
mk() { rm -rf "$W/$1"; mkdir -p "$W/$1"; git -C "$CLONE" archive HEAD | tar -x -C "$W/$1"; }
mk A; mk B; mk C; mk D
cat > "$W/A/tests/unit/main.c" <<'C'
#include <cgreen/cgreen.h>
int main(void)
{
    TestSuite *suite = create_test_suite();
    return run_test_suite(suite, create_text_reporter());
}
C
sed -i 's/return shlan_port_disable(sw, port_id);/return shlan_port_enable(sw, port_id);/' "$W/C/tests/features/switch_bindings.c"
sed -i 's/return shlan_port_enable(sw, port_id);/return 0;/; s/return shlan_connect(sw);/return 0;/' "$W/D/tests/features/switch_bindings.c"
( cd "$W/A" && CMAKE_PREFIX_PATH=$DEPS cmake -S . -B build >"$L/A-cfg.log" 2>&1 && cmake --build build -j16 >"$L/A-build.log" 2>&1 && LD_LIBRARY_PATH=$DEPS/lib ctest --test-dir build --output-on-failure >"$L/A-ctest.log" 2>&1; echo "A empty-suite ctest rc=$? (expect nonzero)" ) &
( cd "$W/B" && env -u CMAKE_PREFIX_PATH -u CPATH -u LIBRARY_PATH cmake -S . -B build >"$L/B-cfg.log" 2>&1; echo "B no-cgreen configure rc=$? (expect nonzero)" ) &
( cd "$W/C" && CMAKE_PREFIX_PATH=$DEPS cmake -S . -B build >"$L/C-cfg.log" 2>&1 && cmake --build build -j16 >"$L/C-build.log" 2>&1 && LD_LIBRARY_PATH=$DEPS/lib behave >"$L/C-behave.log" 2>&1; echo "C wrong-disable-binding behave rc=$? ($(grep -E 'scenarios passed' "$L/C-behave.log"))" ) &
( cd "$W/D" && CMAKE_PREFIX_PATH=$DEPS cmake -S . -B build >"$L/D-cfg.log" 2>&1 && cmake --build build -j16 >"$L/D-build.log" 2>&1 && LD_LIBRARY_PATH=$DEPS/lib behave >"$L/D-behave.log" 2>&1; echo "D noop-enable/connect behave rc=$? ($(grep -E 'scenarios passed' "$L/D-behave.log"))" ) &
wait
grep -h -E 'No assertions|Could NOT|CGREEN|not found' "$L/A-ctest.log" "$L/B-cfg.log" | head -6
grep -n -E 'shlan_test_port_(enable|disable)|return' "$W/C/tests/features/switch_bindings.c" "$W/D/tests/features/switch_bindings.c" | head -12

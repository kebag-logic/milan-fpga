#!/usr/bin/env bash
# Run the PR's listed offline gates concurrently in a clone; one log and rc file each.
# usage: gates.sh <clone> <receipt-dir>
set -u
C="$1"; R="$2"; mkdir -p "$R"; cd "$C" || exit 2
run() { local n="$1"; shift; ( "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
run gate_workflows_check python3 scripts/ci_gate_workflows.py --check
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run gate_workflows_selftest python3 scripts/ci_gate_workflows_selftest.py
run litex_legs_selftest python3 scripts/ci_litex_legs_selftest.py
run run_litex_sims_selftest scripts/run_litex_sims.sh --selftest
run litex_legs_legs python3 scripts/ci_litex_legs.py legs
run ci_scope_selftest python3 scripts/ci_scope.py --selftest
run diff_check git diff --check e61a4afaa54a598ceec08b7b5879285256cc60b6 aa3e2d85024c0aa17b32ed1165e23e65cfad49b0
run behave bash -c 'cd tests && behave --no-capture -f plain'
wait
for f in "$R"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done

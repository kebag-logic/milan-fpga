#!/usr/bin/env bash
# Run the contract checks and the native two-leg control (fixed, --shared, dev base)
# concurrently. Usage: run_checks_and_controls.sh <repo clone> <packet dir> <venv python> <CPython prefix>
set -u
REPO="$1"; P="$2"; VPY="$3"; PLANT="$4"
R="$P/receipts"; S="$P/scratch"
mkdir -p "$R"
cd "$REPO" || exit 2
run() {  # name, command...
  local name="$1"; shift
  ( "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) &
}
run gate_workflows_check  "$VPY" scripts/ci_gate_workflows.py --check
run gate_workflows_selftest "$VPY" scripts/ci_gate_workflows_selftest.py
run events_check "$VPY" scripts/ci_events.py --check
run events_selftest "$VPY" scripts/ci_events.py --selftest
run control_fix "$VPY" scripts/ci_toolcache_isolation.py --python "$PLANT" --work "$S/ctl-fix" --report "$R/control_fix.json"
run control_shared "$VPY" scripts/ci_toolcache_isolation.py --python "$PLANT" --work "$S/ctl-shared" --shared --report "$R/control_shared.json"
run control_dev "$VPY" scripts/ci_toolcache_isolation.py --python "$PLANT" --work "$S/ctl-dev" --rev 9ef717727e6fdac11ee7f01672fefae948452343 --report "$R/control_dev.json"
wait
for f in "$R"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done

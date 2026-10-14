#!/bin/sh
# Usage: gates.sh <repo-root> <receipt-dir>
# Runs the capture input gate, its five mutation arms, and the CI scope/event
# self-checks concurrently in the foreground; one log and rc file per job.
set -u
REPO=$1; OUT=$2
mkdir -p "$OUT"
cd "$REPO" || exit 2
job() { name=$1; shift; ( "$@" >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc" ) & }
job capture_gate python3 scripts/check_nvm_capture.py
for m in bytes records clock ignore-off-timing receipt-opt-out; do
  job capture_mut_$m python3 scripts/check_nvm_capture.py --mutation $m
done
job ci_scope_selftest python3 scripts/ci_scope.py --selftest
job ci_events_check python3 scripts/ci_events.py --check
wait
for f in "$OUT"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done

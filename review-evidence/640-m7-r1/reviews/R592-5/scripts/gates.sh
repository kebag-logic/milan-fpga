#!/usr/bin/env bash
# Usage: gates.sh <checkout> <receipt-dir>. Runs the round-5 gates concurrently, rc per gate.
set -u
src=$1; out=$2; mkdir -p "$out"; cd "$src" || exit 2
run() { local n=$1; shift; ( "$@" >"$out/$n.log" 2>&1; echo $? >"$out/$n.rc" ) & }
run suite_shards_selftest python3 scripts/suite_shards.py --selftest
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run ci_scope_selftest python3 scripts/ci_scope.py --selftest
wait
for n in 0 1 2 3 4 5; do scripts/run_all_suites.sh --shard $n/6 --list >"$out/list_$n.of6" 2>&1; echo $? >"$out/list_$n.of6.rc"; done
scripts/run_all_suites.sh --list >"$out/list_serial" 2>&1; echo $? >"$out/list_serial.rc"
for f in "$out"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done

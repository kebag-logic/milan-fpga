#!/usr/bin/env bash
# Usage: preflight.sh <head-checkout> <receipt-dir>. Runs the eight serial-sweep
# preflight gates of scripts/run_all_suites.sh concurrently, one rc each.
set -u; ROOT=$1; OUT=$2; mkdir -p "$OUT"; cd "$ROOT" || exit 2
g() { local n=$1; shift; ( "$@" >"$OUT/$n.log" 2>&1; echo $? >"$OUT/$n.rc" ) & }
g test_suite_cancellation python3 "$ROOT/scripts/test_suite_cancellation.py"
g suite_tally python3 "$ROOT/scripts/suite_tally.py" --selftest
g suite_shards python3 "$ROOT/scripts/suite_shards.py" --selftest
g check_merge_containment python3 "$ROOT/scripts/check_merge_containment.py" --selftest
g check_results_fresh python3 "$ROOT/scripts/check_results_fresh.py" --self-test
g check_list_hermetic bash "$ROOT/syn/yosys/check_list_hermetic.sh"
g xvlog_gate python3 "$ROOT/scripts/xvlog_gate.py" --selftest
g check_merge_review_integrity python3 "$ROOT/scripts/check_merge_review_integrity.py" --selftest
wait
for f in "$OUT"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done

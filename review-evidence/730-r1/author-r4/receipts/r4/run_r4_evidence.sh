#!/usr/bin/env bash
# Round 4 evidence for lane 730: reviewer mutants and probes, unchanged, plus own order mutants, in parallel.
set -u
P=$VALIDATION_STORAGE/730-a607/r4-packet
O=$VALIDATION_STORAGE/730-a607/r4-out
OWN=$VALIDATION_STORAGE/730-a607/r4-own
mkdir -p "$O"
( python3 -I "$P/scripts/mutants_r2.py" "$P" "$P/head" --jobs 5 > "$O/mutants-r2-at-head.txt" 2>&1; echo $? > "$O/mutants-r2-at-head.rc" ) &
( python3 -I "$OWN/mutants_r4_order.py" "$P" "$P/head" --jobs 3 > "$O/mutants-r4-order.txt" 2>&1; echo $? > "$O/mutants-r4-order.rc" ) &
( SANDBOX_TREE_RO=1 SANDBOX_RO="$P/scripts" "$P/scripts/sandbox.sh" "$P/head" python3 -I "$P/scripts/probe_r3.py" "$P/head" 300 > "$O/probe-r3-at-head.txt" 2>&1; echo $? > "$O/probe-r3-at-head.rc" ) &
( SANDBOX_TREE_RO=1 SANDBOX_RO="$P/scripts" "$P/scripts/sandbox.sh" "$P/head" python3 -I "$P/scripts/probe_shutdown.py" "$P/head" > "$O/probe-shutdown-at-head.txt" 2>&1; echo $? > "$O/probe-shutdown-at-head.rc" ) &
wait
for f in "$O"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") | $(tail -1 "${f%.rc}.txt")"; done

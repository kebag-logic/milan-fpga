#!/usr/bin/env bash
# Runs tb/adp_engine/mutants.py (the lane's own driver, unmodified) in six
# disjoint --only chunks, 6 concurrent jobs on 8 CPUs, one output dir each.
set -u
source "$(dirname "$0")/env.sh"
OUT="$PKT/receipts/adp_mutants"; mkdir -p "$OUT"
chunks=(
 "cfg-dependent-field-top,cfg-frozen-at-top,cfg-overlay-only,cfg-nonzero-for-valid"
 "cfg-valid-not-sticky,cfg-valid-any-selector,cfg-valid-ucpu-bus"
 "cfg-valid-hard-reset,cfg-valid-no-reset,gate-enable-dropped-top"
 "cfg-read-live,cfg-dependent-field,gate-enable-dropped,walk-down-answers-discover,walk-delay-ignores-link-down"
 "walk-down-answers-gm-change,walk-down-shutdown-departs,walk-delay-answers-discover,walk-delay-shutdown-silent,walk-stale-draw-arms,walk-departing-keeps-index,walk-foreign-discover-answered,walk-link-down-keeps-timer"
 "disc-fresh-checks-gm,disc-not-discovered-checks-index,disc-not-discovered-checks-interface,disc-restart-not-rediscovered,disc-departing-ignores-interface,disc-stray-noadp-departs,disc-unbind-keeps-timer"
)
pids=()
for i in "${!chunks[@]}"; do
  ( cd "$CLONE/tb/adp_engine" && $CAP python3 mutants.py --output "$PKT/scratch/adp_mut_logs_$i" --only "${chunks[$i]}" > "$OUT/chunk$i.txt" 2>&1; echo "rc=$?" >> "$OUT/chunk$i.txt" ) &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
cat "$OUT"/chunk*.txt | grep -E ' (KILLED|UNPROVEN)$|^control|^rc=|checks:' 

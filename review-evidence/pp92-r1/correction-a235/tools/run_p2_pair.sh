#!/usr/bin/env bash
# Probe P2 (re-anchored copy) at the fixed head and at the reviewed head, in parallel.
set -u
P=$REVIEWS/pp92-a235-packet
LANE=$LANES/pp92-93-boot-restore
export VERILATOR=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
run() {  # rev outdir log
  bash "$P/tools/run_p2_rebased.sh" "$LANE" "$1" "$2" > "$3" 2>&1
  echo "rc=$?" >> "$3"
}
run f8d30ec "$P/scratch/p2-final" "$P/logs/probes/R278-P2-final.log" &
run 156c206 "$P/scratch/p2-head-rebased" "$P/logs/repro/p2-head-rebased.log" &
wait
for f in "$P/logs/probes/R278-P2-final.log" "$P/logs/repro/p2-head-rebased.log"; do
  echo "== $f"; head -1 "$f"; grep -E "PROBE|rc=" "$f"
done

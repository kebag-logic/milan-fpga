#!/bin/bash
# Arm A's aecp group at one point (1x1 or 8x8), at the review clone's head, to the measurement.
# Usage: arm_a_aecp.sh <1x1|8x8>. The build directory is disposable scratch.
. "$(dirname "$0")/env.sh"
P=$1; B=$PACKET/scratch/builds/armA-aecp-$P; rm -rf "$B"; mkdir -p "$(dirname "$B")"
cd "$CHECKOUT" && echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain | wc -l)"
start=$(date +%s)
python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$B" --record-budget-findings \
  --groups aecp --jobs 4
rc=$?; echo "elapsed=$(( $(date +%s) - start ))s rc=$rc"
echo "tree after: $(git status --porcelain | wc -l) changed path(s)"
for f in "$B"/results/table.md "$B"/image/ctrl_app.elf; do [ -f "$f" ] && sha256sum "$f"; done
python3 -c "import json,sys; s=json.load(open('$B/soc.json')); print('soc.json ledgered:', json.dumps(s).count('8x8-two-interfaces')>0)" 2>/dev/null
grep -c PINMISSING "$B/verilate.log" 2>/dev/null

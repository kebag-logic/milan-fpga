#!/bin/bash
# The isolation control with --gate-legs at a given head, plus a memory sampler.
# Usage: run.sh <head sha> <out dir>
set -uo pipefail
H=$1; OUT=$2
LANE=$LANES/748-elab-race
PY=$VALIDATION_STORAGE/748-a623/gatevenv/bin/python3
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
mkdir -p "$OUT"
( while :; do echo "$(date +%s) $(cat "$CG/memory.current")" >> "$OUT/memory.txt"; sleep 15; done ) &
sampler=$!
began=$(date +%s)
"$PY" -I "$LANE/scripts/ci_toolcache_isolation.py" \
  --python $VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu \
  --pip-cache $VALIDATION_STORAGE/748-a623/pipwarm/home/.cache/pip \
  --work $VALIDATION_STORAGE/748-a623/r2/gatelegs/run --rev "$H" \
  --gate-legs --rv32-sdk "$HOME/br-milan-rv32" --tool-dir $VALIDATION_TOOLS/sv2v-v0.0.12 \
  --report "$OUT/gate-legs.json" > "$OUT/gate-legs.log" 2>&1
echo $? > "$OUT/gate-legs.rc"
echo "wall $(( $(date +%s) - began )) s" > "$OUT/wall.txt"
kill $sampler
echo done > "$OUT/done"

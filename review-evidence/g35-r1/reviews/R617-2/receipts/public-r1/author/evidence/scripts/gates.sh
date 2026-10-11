#!/usr/bin/env bash
# Run the four donor gates concurrently in the lane, each with its own log
# and rc file. Usage: gates.sh <label>  (logs under $VALIDATION_STORAGE/g35-a599/gates-<label>)
set -u
label="$1"
LANE=$LANES/g35-rx-err
OUT=$VALIDATION_STORAGE/g35-a599/gates-$label
mkdir -p "$OUT"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export TMPDIR=$VALIDATION_STORAGE/g35-a599/tmp
mkdir -p "$TMPDIR"
cd "$LANE" || exit 2
{ git rev-parse HEAD; git status --short; verilator --version; } > "$OUT/identity.txt" 2>&1
for g in tb contract lint docs; do
  (
    if [ "$g" = tb ]; then make -j16 tb > "$OUT/$g.log" 2>&1
    else make "$g" > "$OUT/$g.log" 2>&1
    fi
    echo $? > "$OUT/$g.rc"
  ) &
done
wait
for g in tb contract lint docs; do echo "$g rc=$(cat "$OUT/$g.rc")"; done

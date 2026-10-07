#!/bin/sh
# Usage: run_render_campaign.sh <tree> <outdir>
# Runs the full tdm8render-mutants campaign from the suite directory with the
# pinned Verilator; writes full.log, rc, tool identity and timing to <outdir>.
set -u
TREE=$1; OUT=$2
mkdir -p "$OUT" "$OUT/tmp"
: "${VERILATOR:?set VERILATOR to the pinned 5.050 wrapper}"
export VERILATOR VERILATOR_JOBS=${VERILATOR_JOBS:-4} TMPDIR="$OUT/tmp" PYTHONHASHSEED=0
{ "$VERILATOR" --version; make --version | head -1; git -C "$TREE" rev-parse HEAD; git -C "$TREE/protocol-processor" rev-parse HEAD; git -C "$TREE" status --short; date -Is; } > "$OUT/identity.txt" 2>&1
cd "$TREE/tb/verilator/milan_dp_render" || exit 99
make tdm8render-mutants > "$OUT/full.log" 2>&1
echo $? > "$OUT/rc"
date -Is >> "$OUT/identity.txt"

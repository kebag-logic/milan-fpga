#!/bin/bash
# Usage: differential.sh <repo> <scratch> <outdir>; runs the MAAP C/RTL differential self-test with scratch-only outputs
set -u
R=$1; S=$2; O=$3
export PATH="$S/bin:$PATH" VERILATOR="$S/bin/verilator" TMPDIR="$S/tmp/differential"
mkdir -p "$TMPDIR"; rm -rf "$S/differential"
cd "$R"
{ echo "head $(git rev-parse HEAD) start $(date -u +%FT%TZ)"; python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$S/differential"; rc=$?; echo "end $(date -u +%FT%TZ) rc=$rc"; } > "$O/differential.log" 2>&1
grep -o 'rc=[0-9]*$' "$O/differential.log" | tail -1 | cut -d= -f2 > "$O/differential.rc"

#!/usr/bin/env bash
# Scratch: the AECP wire comparison of one tree at one interface count.
# usage: aecpwire.sh <tree> <reference> <interfaces> <output>
set -u
tree=$1; ref=$2; n=$3; out=$4
export TMPDIR=$VALIDATION_STORAGE/697c-a583/tmpdir VERILATOR_JOBS=2
rm -rf "$out"; mkdir -p "$out"
cd "$tree" || exit 2
date -u +%FT%TZ
python3 -B sw/firmware/ctrl/test/aecp_wire.py --reference "$ref" --interfaces "$n" --output "$out" \
  --verilator $VALIDATION_TOOLS/pinned-verilator-5.050/verilator
echo "exit=$?"
date -u +%FT%TZ

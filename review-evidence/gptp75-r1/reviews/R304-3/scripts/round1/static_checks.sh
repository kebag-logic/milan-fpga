#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R304-1 static receipts for FPGA-gPTP PR #76 (#75).
# usage: static_checks.sh REPO_CLONE BASE HEAD SCRATCH
#   REPO_CLONE  a clone containing both commits (read-only use: git show/archive)
#   SCRATCH     a disposable directory for exported trees and regenerated images
# Prints: ROM regeneration versus the four tracked images, and every
# KL_gptp_engine.sv line anchor in docs/SOURCE_EVIDENCE.md at base and head.
set -eu
REPO=$1 BASE=$2 HEAD=$3 S=$4
mkdir -p "$S"
rm -rf "$S/st_head" && mkdir -p "$S/st_head"
git -C "$REPO" archive "$HEAD" | tar -x -C "$S/st_head"
cd "$S/st_head"
G=hdl/ucode/gen_gptp_ucode.py
echo "== ROM regeneration at $HEAD"
python3 $G -o "$S/rg_ooc.hex"
python3 $G -o "$S/rg_ucpu.hex"
python3 $G --clk-hz 2000000 -o "$S/rg_tsngen.hex"
python3 $G --clk-hz 2000000 --cease-ms 3000 -o "$S/rg_engine.hex"
for pair in ooc:syn/ooc/work ucpu:tb/verilator/ucpu tsngen:tb/tsngen \
            engine:tb/verilator/engine; do
  k=${pair%%:*} d=${pair#*:}
  if cmp -s "$S/rg_$k.hex" "$d/gptp_ucode.hex"; then r=MATCH; else r=DIFFER; fi
  echo "$r $(sha256sum "$d/gptp_ucode.hex" | cut -d' ' -f1) $d/gptp_ucode.hex"
done
echo "== SOURCE_EVIDENCE.md KL_gptp_engine.sv anchors (base line text -> head)"
git -C "$REPO" show "$HEAD:docs/SOURCE_EVIDENCE.md" |
  grep -o 'KL_gptp_engine.sv#L[0-9]*' | sort -u | sed 's/.*#L//' | sort -n |
while read -r L; do
  b=$(git -C "$REPO" show "$BASE:hdl/top/KL_gptp_engine.sv" | sed -n "${L}p")
  h=$(git -C "$REPO" show "$HEAD:hdl/top/KL_gptp_engine.sv" | sed -n "${L}p")
  moved=$(git -C "$REPO" show "$HEAD:hdl/top/KL_gptp_engine.sv" |
          grep -nFx -- "$b" | cut -d: -f1 | tr '\n' ' ')
  if [ "$b" = "$h" ]; then st=EXACT; else st="STALE(now at line ${moved% })"; fi
  echo "L$L $st :: base='$b' head='$h'"
done
echo "== SOURCE_EVIDENCE.md changed by the PR?"
if git -C "$REPO" diff --quiet "$BASE" "$HEAD" -- docs/SOURCE_EVIDENCE.md; then
  echo "unchanged"; else echo "changed"; fi

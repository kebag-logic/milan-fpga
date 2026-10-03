#!/usr/bin/env bash
# Reproduce the PR body's "syntax fault planted in all.v inside KL_srp_top" row
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"; S="$P/scratch"; V="$S/bin/verilator"
# at this head with R448-2's unchanged plant.py (allv-syntax), to read the
# all.v line the gate cites now.
set -u
w=$S/allv-row; rm -rf "$w"; mkdir -p "$w"; cp -a $S/head-tree/. "$w/"
python3 $P/scripts/round2/r448-2/plant.py "$w" allv-syntax KL_srp_top
( cd "$w" && ./syn/yosys/run.sh ) > $P/receipts/allv_syntax_row.log 2>&1; echo "rc=$?"
grep -m1 'YOSYS FAIL all.v' $P/receipts/allv_syntax_row.log

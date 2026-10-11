#!/bin/sh
# Run the donor gates at the exact head, each with its own log and rc file.
# Usage: run_gates.sh <checkout> <receipts-dir> <pinned-verilator-dir>
# make tb runs in the given checkout; contract/lint/docs/ooc-selftest too.
CO=$1; OUT=$2; VDIR=$3
export PATH="$VDIR:$PATH"
cd "$CO" || exit 2
verilator --version > "$OUT/verilator_version.txt" 2>&1
for t in contract lint docs; do
  ( make $t > "$OUT/make_$t.log" 2>&1; echo $? > "$OUT/make_$t.rc" ) &
done
( python3 -I syn/ooc/check_ooc_clock.py --selftest > "$OUT/ooc_selftest.log" 2>&1; echo $? > "$OUT/ooc_selftest.rc"
  python3 -I syn/ooc/check_ooc_clock.py > "$OUT/ooc_static.log" 2>&1; echo $? > "$OUT/ooc_static.rc" ) &
( make -j16 tb > "$OUT/make_tb.log" 2>&1; echo $? > "$OUT/make_tb.rc" ) &
wait

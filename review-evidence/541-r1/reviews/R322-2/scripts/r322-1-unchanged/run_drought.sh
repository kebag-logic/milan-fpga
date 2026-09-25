#!/bin/sh
# Usage: run_drought.sh <extracted-head-root> <work-dir> <verilator>
# Builds scripts/probe_drought.cpp against the head KL_crf_rx.sv and against
# the P2 mutant (validation error refreshes the timeout); head must pass,
# the mutant must fail.
set -u
ROOT=$1; WORK=$2; V=$3
HERE=$(cd "$(dirname "$0")" && pwd)
RTL=$ROOT/hdl/ieee1722/crf/KL_crf_rx.sv
mkdir -p "$WORK"
python3 - "$RTL" "$WORK/p2.sv" <<'EOF'
import sys
s = open(sys.argv[1]).read()
a = "wire w_acc_run_w = w_acc && !stop_i;"
assert s.count(a) == 1
open(sys.argv[2], "w").write(s.replace(a, "wire w_acc_run_w = w_hit && !stop_i;"))
EOF
rc_all=0
for case in head:"$RTL" p2_refresh:"$WORK/p2.sv"; do
  name=${case%%:*}; src=${case#*:}
  "$V" --cc --exe --build -j 8 --top-module KL_crf_rx -Mdir "$WORK/obj_$name" \
    -GCLK_FREQ_HZ_P=200000 -GIVAL_CYC_P=200 -Wno-fatal -Wno-WIDTHEXPAND \
    -Wno-WIDTHTRUNC -CFLAGS "-std=c++17 -O2" "$src" "$HERE/probe_drought.cpp" \
    -o Vdrought >"$WORK/build_$name.log" 2>&1 || { echo "$name: BUILD FAILED"; rc_all=1; continue; }
  "$WORK/obj_$name/Vdrought"; rc=$?
  echo "== $name rc=$rc"
done
exit $rc_all

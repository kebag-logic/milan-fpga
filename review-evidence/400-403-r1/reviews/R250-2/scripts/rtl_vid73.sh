#!/bin/sh
# Rerun of R2/R3 from rtl_mutants.sh with the fixture flags quoted as one
# make variable. Usage: rtl_vid73.sh PACKET_DIR PINNED_VERILATOR
set -eu
P="$1"; export VL_REAL="$2"; export VL_JOBS=4
S="$P/scripts"; R="$P/receipts"; T="$P/scratch"; VL="$S/vl-capped.sh"
FIX="$T/fixture-vid73"
grep -q "16'd73;" "$FIX/gen/adp_shape_defaults.svh"
DP=hdl/milan/milan_datapath.sv
BIND='      .SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C),\n'
PP73="rm -rf tb/verilator/pp_shadow/obj_dir; make -C tb/verilator/pp_shadow VERILATOR=$VL 'SHAPE_1x1=+incdir+$FIX -CFLAGS -DDECLARATION_VID=73'"
( cd "$T/rtl2" && sh -c "$PP73" ) > "$R/rtl-R2.log" 2>&1 && rc=0 || rc=$?
echo "RESULT R2-vid73-head-control: exit=$rc" >> "$R/rtl-R2.log" &
python3 "$S/mutant.py" "$T/rtl1" R3-vid-binding-removed-vid73-recipe detect \
  $DP "$BIND" "" -- sh -c "$PP73" > "$R/rtl-R3.log" 2>&1 || true
wait
grep -h '^RESULT' "$R/rtl-R2.log" "$R/rtl-R3.log"

#!/bin/sh
# RTL mutants for the csr and pp_shadow suites, four disposable trees in
# parallel at VL_JOBS=2 each (8 jobs total). Usage:
#   rtl_mutants.sh PACKET_DIR PINNED_VERILATOR
# Each tree is a copy of PACKET_DIR/scratch/probe (the reviewed head).
set -eu
P="$1"; export VL_REAL="$2"; export VL_JOBS=2
S="$P/scripts"; R="$P/receipts"; T="$P/scratch"
VL="$S/vl-capped.sh"
for n in 1 2 3 4; do
  rm -rf "$T/rtl$n"; cp -a "$T/probe" "$T/rtl$n"
done
# VID-73 fixture header: the committed arty_current header, VID changed only.
FIX="$T/fixture-vid73"; mkdir -p "$FIX/gen"
sed "s/ADP_SRP_DOM_DEF_VID_C = 16'd2;/ADP_SRP_DOM_DEF_VID_C = 16'd73;/" \
  "$T/probe/configs/generated/endstation_arty_current/gen/adp_shape_defaults.svh" \
  > "$FIX/gen/adp_shape_defaults.svh"
grep -q "16'd73;" "$FIX/gen/adp_shape_defaults.svh"
DP=hdl/milan/milan_datapath.sv
BIND='      .SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C),\n'
PPM="make -C tb/verilator/pp_shadow VERILATOR=$VL"
PP73="make -C tb/verilator/pp_shadow VERILATOR=$VL 'SHAPE_1x1=+incdir+$FIX -CFLAGS -DDECLARATION_VID=73'"
CSRM="make -C tb/verilator/csr VERILATOR=$VL"
{
  # R1: generated VID binding removed; the committed recipe (VID 2).
  python3 "$S/mutant.py" "$T/rtl1" R1-vid-binding-removed-default-recipe survive \
    $DP "$BIND" "" -- sh -c "$PPM" > "$R/rtl-R1.log" 2>&1
  # R3: the same mutant under the VID-73 fixture recipe.
  python3 "$S/mutant.py" "$T/rtl1" R3-vid-binding-removed-vid73-recipe detect \
    $DP "$BIND" "" -- sh -c "rm -rf tb/verilator/pp_shadow/obj_dir; $PP73" > "$R/rtl-R3.log" 2>&1
} &
{
  # R2: positive control, VID-73 fixture at the reviewed head.
  (cd "$T/rtl2" && sh -c "$PP73") > "$R/rtl-R2.log" 2>&1; echo "RESULT R2-vid73-head-control: exit=$?" >> "$R/rtl-R2.log"
} &
{
  # R4: TCAM_CTRL real reset arms the station filter (default_pass 0).
  python3 "$S/mutant.py" "$T/rtl3" R4-tcam-reset-filtering detect \
    hdl/common/csr/milan_csr.sv "tcam_ctrl <= 32'h1;" "tcam_ctrl <= 32'h2;" -- sh -c "$PPM" > "$R/rtl-R4.log" 2>&1
} &
{
  # R5/R6: non-neutral AAF / MAAP real reset restored (readback table unchanged).
  python3 "$S/mutant.py" "$T/rtl4" R5-aaf-real-reset-vid2 detect \
    hdl/common/csr/milan_csr.sv "aaf_ctrl <= AAF_CTRL_RST_C;" "aaf_ctrl <= 32'h0002_0000;" -- sh -c "$CSRM" > "$R/rtl-R5.log" 2>&1
  python3 "$S/mutant.py" "$T/rtl4" R6-maap-readback-default-0x800 detect \
    hdl/common/csr/milan_csr.sv "A_MAAP_CTRL[10:0]:  csr_default = MAAP_CTRL_RST_C;" "A_MAAP_CTRL[10:0]:  csr_default = 32'h0000_0800;" -- sh -c "$CSRM" > "$R/rtl-R6.log" 2>&1
} &
wait
grep -h '^RESULT' "$R"/rtl-R*.log

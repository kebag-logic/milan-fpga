#!/usr/bin/env bash
# Base-versus-candidate equivalence of KL_pp_event_router at one N_SRC_P,
# by induction over matched state: every port and every register is matched
# by name; internal combinational wires (*_w, which differ by design) are
# hidden first so only ports and registers are compared.
# usage: evr_equiv.sh <base.sv> <cand.sv> <N_SRC_P> <workdir>
set -u
base=$1; cand=$2; n=$3; wd=$4
SV2V=${SV2V:-$VALIDATION_TOOLS/sv2v-v0.0.12/sv2v}
YOSYS=${YOSYS:-yosys}
mkdir -p "$wd"
"$SV2V" "$base" | sed 's/module KL_pp_event_router/module evr_gold/' >"$wd/gold.v" || exit 3
"$SV2V" "$cand" | sed 's/module KL_pp_event_router/module evr_gate/' >"$wd/gate.v" || exit 3
cat >"$wd/induct.ys" <<EOF
read_verilog $wd/gold.v
read_verilog $wd/gate.v
chparam -set N_SRC_P $n evr_gold evr_gate
proc; memory; opt_clean; flatten; opt -fast
rename -hide w:*_w
opt_clean
equiv_make evr_gold evr_gate equiv
hierarchy -top equiv
equiv_simple -seq 2
equiv_induct -seq 2
equiv_status -assert
EOF
"$YOSYS" -q -l "$wd/induct.log" "$wd/induct.ys" >/dev/null 2>&1; r1=$?
v1=$(grep -E "Of those cells|Found [0-9]+ unproven" "$wd/induct.log" | tail -1)
echo "N=$n induct_rc=$r1 [$v1]"
exit $r1

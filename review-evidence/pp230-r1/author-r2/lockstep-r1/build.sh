#!/usr/bin/env bash
# Scratch: build one lockstep shape. usage: build.sh <new_srp_dir> <out> <N_SRC> <N_SNK> <SLOT_AW> <JOIN> <PER> <LEAVE>
set -euo pipefail
L=$VALIDATION_STORAGE/pp230-a523/lockstep
NEW=$1; OUT=$2; NS=$3; NK=$4; AW=$5; J=$6; P=$7; LV=$8
TK=8; LS=$((8 + NS))
B=$VALIDATION_STORAGE/pp230-a523/basetree/hdl
mkdir -p "$OUT"
python3 $L/gen_top.py "$NEW/KL_srp_top.sv" "$OUT/lockstep_top.sv" > "$OUT/gen.log"
$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --cc --exe --build -j 4 --top-module lockstep_top \
  -Wno-fatal -Wno-lint -Wno-style -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  --x-initial unique --x-assign unique \
  -GN_SOURCES_P=$NS -GN_SINKS_P=$NK -GSLOT_AW_P=$AW -GTK_SLOT_BASE_P=$TK -GLS_SLOT_BASE_P=$LS \
  -GJOIN_MS_P=$J -GPERIODIC_MS_P=$P -GLEAVE_MS_P=$LV \
  -CFLAGS "-std=c++17 -O2 -DN_SRC=$NS -DN_SNK=$NK -DSLOT_AW=$AW" \
  --Mdir "$OUT/obj" -o Vlockstep \
  $B/common/pp_pkg.sv $B/srp/srp_pkg.sv \
  $L/ref/KL_srp_decoder_ref.sv $L/ref/KL_srp_domain_ref.sv $L/ref/KL_srp_vlan_ref.sv $L/ref/KL_srp_admission_ref.sv \
  $L/ref/KL_srp_talker_fsm_ref.sv $L/ref/KL_srp_listener_fsm_ref.sv $L/ref/KL_srp_encoder_ref.sv $L/ref/KL_srp_top_ref.sv \
  $NEW/KL_srp_decoder.sv $NEW/KL_srp_domain.sv $NEW/KL_srp_vlan.sv $NEW/KL_srp_admission.sv \
  $NEW/KL_srp_talker_fsm.sv $NEW/KL_srp_listener_fsm.sv $NEW/KL_srp_encoder.sv $NEW/KL_srp_top.sv \
  "$OUT/lockstep_top.sv" $L/lockstep_main.cpp > "$OUT/build.log" 2>&1
echo built "$OUT"

#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# build.sh HDL_DIR LS_DIR OUT_DIR M N CADENCE(default|compressed) [HEAD_SRP_DIR]
# Builds the random lockstep model: head KL_srp_top (from HDL_DIR/srp, or
# from HEAD_SRP_DIR when given, for planted controls) with the generated
# checker of LS_DIR (base modules renamed _ref) bound into it.
set -eu
HDL=$1; LS=$2; OUT=$3; M=$4; N=$5; CAD=$6; HEADSRP=${7:-$HDL/srp}
V=${VERILATOR:-verilator}   # Verilator 5.050 (set VERILATOR to override)
HERE=$(cd "$(dirname "$0")" && pwd)
G="-GN_SOURCES_P=$M -GN_SINKS_P=$N -GSLOT_AW_P=7 -GTK_SLOT_BASE_P=8 -GLS_SLOT_BASE_P=24"
[ "$CAD" = compressed ] && G="$G -GJOIN_MS_P=20 -GPERIODIC_MS_P=100 -GLEAVE_MS_P=500"
mkdir -p "$OUT"
SRCS="$HDL/common/pp_pkg.sv $HDL/srp/srp_pkg.sv"
for m in KL_srp_decoder KL_srp_domain KL_srp_vlan KL_srp_talker_fsm KL_srp_listener_fsm KL_srp_admission KL_srp_encoder KL_srp_top; do
  SRCS="$SRCS $HEADSRP/$m.sv $LS/ref/${m}_ref.sv"
done
SRCS="$SRCS $LS/lockstep_chk.sv $LS/lockstep_bind.sv"
"$V" --cc --exe --build -j 4 --top-module KL_srp_top --prefix Vtop -Mdir "$OUT/obj" \
  --x-assign unique --x-initial unique $G \
  -Wno-fatal -Wno-lint -Wno-style -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -CFLAGS "-std=c++17 -O2 -DNSRC=$M -DNSNK=$N" \
  $SRCS "$HERE/main.cpp" -o Vtop > "$OUT/build.log" 2>&1
echo "built $OUT"

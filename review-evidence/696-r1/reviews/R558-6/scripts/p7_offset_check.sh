#!/bin/bash
# Build the real-CSR datapath MAAP harness, with one added print of each MAAP
# frame's requested_start, against a given KL_maap.sv. Mirrors the build recipe
# of tb/verilator/maap/integration.mk (same derived sources and flags).
# usage: p7_offset_check.sh <repo> <KL_maap.sv> <harness.cpp> <out-dir> <dp_srcs.txt> <dp_flags.txt>
set -euo pipefail
repo=$1 rtl=$2 harness=$3 out=$4 srcs_file=$5 flags_file=$6
cd "$repo/tb/verilator/maap"
srcs=$(sed "s|../../../hdl/ieee1722/maap/KL_maap.sv|$rtl|" "$srcs_file")
grep -q -- "$rtl" <<<"$srcs"
mkdir -p "$out"
python3 ../../../protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o "$out/ltn_rom.hex"
python3 ../../../protocol-processor/hdl/aecp/ucode/gen_ucode.py -o "$out/ucode.hex"
# The derived flags carry one quoted -CFLAGS word; split them as make's shell does.
eval "flags=($(cat "$flags_file"))"
# shellcheck disable=SC2086
"${VERILATOR:-verilator}" +incdir+../../../configs/generated/endstation_ax7101_1x1_tdm8 \
  "${flags[@]}" --Mdir "$out" -GMAAP_CLK_HZ_P=10000 \
  -GN_STREAMS=1 -GTALKER_WIRE_CHANS_P=8 -GAUDIO_IF_SLOTS_P=8 \
  -GAUDIO_IF_MASTER_P=1 -GLOOPBACK_P=1 -GI2SPB_P=0 -GLPF_P=0 \
  -CFLAGS "-I$repo/tb/verilator/maap" \
  $srcs "$harness" -o maap_integration
cd "$out" && ./maap_integration

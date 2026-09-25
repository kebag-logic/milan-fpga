#!/usr/bin/env bash
# Elaborate protocol_processor_top with -G overrides for every parameter the
# guide lists (restating the implemented defaults, so behaviour is unchanged)
# and once with a bogus name, to show each listed name is an overridable
# top-level parameter. Usage: override_probe.sh <repo-root> <verilator>
set -uo pipefail
cd "$1" || exit 2
V=$2
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
G=(-GN_STREAM_IN_P=8 -GN_STREAM_OUT_P=8 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOMAIN_P=1
   -GN_CONTROL_P=1 -GRX_SLOTS_P=4 -GRX_SLOT_BYTES_P=576 -GTX_STD_SLOTS_P=4
   -GTX_OVERSIZE_BYTES_P=1600 -GCLK_HZ_P=100000000 -GTIM_DIV_US_P=100
   -GTIM_DIV_MS_P=1000 '-GTROM_HEX_P="ltn_rom.hex"' '-GUCODE_HEX_P="ucode.hex"'
   "-GDESC_BASE_P=32'h20000000" -GDESC_LINE_BYTES_P=576 -GDESC_IDX_ENTRIES_P=32
   -GDESC_NAME_ENTRIES_P=32 -GDESC_MEM_TMO_CYC_P=4096 -GNVM_RS_TMO_CYC_P=2000000
   -GREG_TL_TIMEOUT_MS_P=300000 -GLOCK_TIMEOUT_MS_P=60000
   "-GRESP_BASE_P=32'h20100000" "-GSRP_DOM_DEF_VID_P=16'd2")
echo "overrides: ${#G[@]}"
for mode in all24 bogus localparam; do
  extra=()
  [ "$mode" = bogus ] && extra=(-GNOT_A_TOP_PARAM_P=1)
  [ "$mode" = localparam ] && extra=(-GTMR_AW_C=7)
  # shellcheck disable=SC2086
  out=$("$V" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
        --top-module protocol_processor_top "${G[@]}" "${extra[@]}" $pkgs $all 2>&1)
  rc=$?
  echo "=== $mode rc=$rc"
  grep -E '%(Warning|Error)' <<<"$out" | head -8
done

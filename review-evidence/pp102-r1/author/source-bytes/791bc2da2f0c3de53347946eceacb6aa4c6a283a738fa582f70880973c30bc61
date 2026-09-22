#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Device portability: sv2v + yosys must elaborate every top (hdl/README rule 2).
# The tops array is the authoritative list — extend it with every new top.
# `pipefail` completes the trio the other two thirds of which were already
# here. It reaches only the `find | sort` pairs on the source line below, both
# of which must succeed for that line to mean anything; the yosys verdicts are
# AND-OR lists that `set -e` deliberately leaves alone.
set -euo pipefail
cd "$(dirname "$0")/../.."
tops=(KL_aecp_ucpu KL_aecp_desc_store KL_aecp_dyn_state KL_aecp_resp_buf KL_aecp_engine KL_aecp_notify KL_aecp_ca_originator KL_pp_timer_service KL_pp_prng KL_pp_rx_slots KL_pp_tx_slots KL_pp_release_merge
      KL_pp_rx_validator KL_pp_normalizer KL_pp_dispatch KL_pp_scoreboard
      KL_pp_event_router KL_pp_originator KL_pp_tx_arbiter KL_pp_trace_ring
      KL_pp_side_port KL_pp_nvm_port KL_adp_engine KL_pp_acmp_listener
      KL_acmp_talker KL_pp_maap KL_srp_decoder KL_srp_encoder KL_srp_domain
      KL_srp_vlan KL_srp_talker_fsm KL_srp_listener_fsm)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
# The two substitutions below are split on purpose - sv2v takes one file per
# word - and stay on one line, which is the form Rule 9 kept for source lists.
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"  # shellcheck disable=SC2086 # deliberate word split of two source lists
( cd hdl/aecp/ucode && python3 gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null 2>&1 || python3 gen_ltn_rom.py > /dev/null; cp ltn_rom.hex "$work/" 2>/dev/null || true )
cd "$work"
for t in "${tops[@]}"; do
  yosys -q -p "read_verilog all.v; hierarchy -check -top $t; proc; opt_clean" \
    && echo "YOSYS OK  $t" || { echo "YOSYS FAIL $t"; exit 1; }
done

# Elaboration alone does not prove that inferred memories map onto the target
# FPGA. KL_aecp_engine contains the largest mixed-control RAM in this block, so
# carry it through the complete Xilinx memory-mapping flow as a regression gate.
# Six RAMB36 is the current engine shape: five existing stores plus exactly
# one staging store. Assert both facts so losing inference and expanding byte
# lanes fail in opposite directions.
yosys -q -p "read_verilog all.v; hierarchy -check -top KL_aecp_engine; synth_xilinx -family xc7 -flatten -top KL_aecp_engine; select -module KL_aecp_engine; select -assert-count 1 c:amap_stage_r* t:RAMB36E1 %i; select -assert-count 6 t:RAMB36E1" \
  && echo "YOSYS XILINX OK  KL_aecp_engine" \
  || { echo "YOSYS XILINX FAIL KL_aecp_engine"; exit 1; }

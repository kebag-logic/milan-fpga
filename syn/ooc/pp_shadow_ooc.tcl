# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context synthesis of the protocol-processor SHADOW plane as the
# consumer instantiates it: KL_pp_shadow, which contains the whole
# protocol_processor_top (packet engine + ADP + ACMP + SRP + side port + NVM
# port) plus the consumer-side RX classifier, control-frame FIFO and byte
# serializer.
#
# This is the SAME INSTRUMENT as syn/ooc/ucpu_ooc.tcl in the protocol-processor
# repo (post-synthesis hierarchical utilization, ship part, 100 MHz OOC), so
# the number it produces is directly comparable to that document's anchors and
# to the 1,068 LUT uCPU skeleton measurement of record.
#
# It answers the one question no estimate in docs/10_RESOURCE_AND_EFFORT.md
# could: what does this plane ACTUALLY cost on the die this board ships, given
# the board is LUT-bound at ~97.7% and the conformance cliff sits at 84.77%.
#
#   cd <workdir>
#   python3 <pp>/hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex
#   vivado -mode batch -source <repo>/syn/ooc/pp_shadow_ooc.tcl -nojournal -log ooc.log

set REPO [file normalize [file dirname [info script]]/../..]
set PP   $REPO/protocol-processor/hdl
set AXIS $REPO/third_party/verilog-axis/rtl

# packages first, then the engines, then the consumer wrapper — tb/pp_top order
read_verilog -sv \
  $PP/common/pp_pkg.sv $PP/srp/srp_pkg.sv $PP/acmp/acmp_pkg.sv $PP/adp/adp_pkg.sv \
  $PP/common/KL_pp_prng.sv $PP/common/KL_pp_timer_service.sv \
  $PP/packet_engine/KL_pp_rx_validator.sv \
  $PP/packet_engine/KL_pp_rx_slots.sv \
  $PP/packet_engine/KL_pp_normalizer.sv \
  $PP/packet_engine/KL_pp_dispatch.sv \
  $PP/packet_engine/KL_pp_tx_slots.sv \
  $PP/packet_engine/KL_pp_tx_arbiter.sv \
  $PP/packet_engine/KL_pp_scoreboard.sv \
  $PP/packet_engine/KL_pp_event_router.sv \
  $PP/packet_engine/KL_pp_originator.sv \
  $PP/packet_engine/KL_pp_trace_ring.sv \
  $PP/packet_engine/KL_pp_side_port.sv \
  $PP/packet_engine/KL_pp_nvm_port.sv \
  $PP/adp/KL_adp_engine.sv \
  $PP/acmp/KL_acmp_listener.sv $PP/acmp/KL_acmp_talker.sv \
  $PP/acmp/KL_acmp_nvm_shadow.sv \
  $PP/srp/KL_srp_decoder.sv $PP/srp/KL_srp_domain.sv \
  $PP/srp/KL_srp_vlan.sv $PP/srp/KL_srp_admission.sv \
  $PP/srp/KL_srp_talker_fsm.sv $PP/srp/KL_srp_listener_fsm.sv \
  $PP/srp/KL_srp_encoder.sv $PP/srp/KL_srp_top.sv \
  $PP/top/KL_mrp_strip.sv $PP/top/protocol_processor_top.sv \
  $REPO/hdl/milan/KL_pp_shadow.sv

# the Forencich frame FIFO is plain Verilog-2001
read_verilog $AXIS/axis_fifo.v

# Shape. Defaults to the wrapper's own 8/8 — the FULL-shape, pessimistic,
# decision-relevant end. Override for the shape a given board actually flashes:
#   PP_N_IN=1 PP_N_OUT=1 vivado -mode batch -source .../pp_shadow_ooc.tcl
# The two numbers are read ONCE here and printed with the result, because a
# utilization figure quoted without its shape is a figure that gets misapplied.
set N_IN  [expr {[info exists ::env(PP_N_IN)]  ? $::env(PP_N_IN)  : 8}]
set N_OUT [expr {[info exists ::env(PP_N_OUT)] ? $::env(PP_N_OUT) : 8}]
puts "pp_shadow OOC shape: N_STREAM_IN_P=$N_IN N_STREAM_OUT_P=$N_OUT"

synth_design -mode out_of_context -top KL_pp_shadow -part xc7a100tfgg484-2 \
  -generic N_STREAM_IN_P=$N_IN -generic N_STREAM_OUT_P=$N_OUT

create_clock -period 10.000 -name clk [get_ports clk_i]
report_utilization -hierarchical -file util_hier.rpt
report_utilization -file util.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing.rpt

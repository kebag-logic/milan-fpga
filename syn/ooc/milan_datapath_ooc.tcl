# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context synthesis of the WHOLE milan_datapath — the baseline against
# which a substituted datapath (shipping 1722.1/SRP planes deleted, protocol
# processor in their place) is differenced.
#
# Same instrument as syn/ooc/pp_shadow_ooc.tcl and syn/ooc/old_planes_ooc.tcl
# (post-synthesis utilization, ship part, 100 MHz OOC), because a net figure
# built from two different instruments is not a net figure.
#
# The per-block OOC numbers those two scripts produce are STANDALONE costs;
# they do not carry the datapath's own interconnect to each plane. This script
# is what closes that gap: it prices the assembled design, so
# (substituted - baseline) is the number that actually decides the campaign.
#
#   PP=0 vivado -mode batch -source .../milan_datapath_ooc.tcl -nojournal   ;# baseline
#   PP=1 ...                                                               ;# plane ON
#
# The shape include MUST be named (milan_datapath and milan_csr both
# `include gen/adp_shape_defaults.svh); the 1x1 arty config is the default
# elaboration shape the yosys gate also uses.

set REPO [file normalize [file dirname [info script]]/../..]
set PP   [expr {[info exists ::env(PP)] ? $::env(PP) : 0}]
set TAG  [expr {[info exists ::env(TAG)] ? $::env(TAG) : "base"}]
puts "milan_datapath OOC: PP_PLANE_P=$PP tag=$TAG"

# The source list comes from syn/yosys/run.sh via dp_srcs.py — the ONE list
# the portability gate proves elaborates. A copy of it here would drift.
set SRC_LINES [split [string trim [exec python3 $REPO/syn/ooc/dp_srcs.py]] "\n"]
set SV {}
set V  {}
foreach f $SRC_LINES {
  if {[string match "*.sv" $f]} { lappend SV $f } else { lappend V $f }
}
puts "milan_datapath OOC: [llength $SV] SystemVerilog + [llength $V] Verilog sources"
read_verilog -sv $SV
read_verilog $V

if {$PP} {
  set P $REPO/protocol-processor/hdl
  read_verilog -sv \
    $P/common/pp_pkg.sv $P/srp/srp_pkg.sv $P/acmp/pp_acmp_pkg.sv $P/adp/pp_adp_pkg.sv \
    $P/common/KL_pp_prng.sv $P/common/KL_pp_timer_service.sv \
    $P/packet_engine/KL_pp_rx_validator.sv $P/packet_engine/KL_pp_rx_slots.sv \
    $P/packet_engine/KL_pp_normalizer.sv $P/packet_engine/KL_pp_dispatch.sv \
    $P/packet_engine/KL_pp_tx_slots.sv $P/packet_engine/KL_pp_tx_arbiter.sv \
    $P/packet_engine/KL_pp_scoreboard.sv $P/packet_engine/KL_pp_event_router.sv \
    $P/packet_engine/KL_pp_originator.sv $P/packet_engine/KL_pp_trace_ring.sv \
    $P/packet_engine/KL_pp_side_port.sv $P/packet_engine/KL_pp_nvm_port.sv \
    $P/adp/KL_adp_engine.sv $P/acmp/KL_pp_acmp_listener.sv $P/acmp/KL_acmp_talker.sv \
    $P/acmp/KL_acmp_nvm_shadow.sv $P/srp/KL_srp_decoder.sv $P/srp/KL_srp_domain.sv \
    $P/srp/KL_srp_vlan.sv $P/srp/KL_srp_admission.sv $P/srp/KL_srp_talker_fsm.sv \
    $P/srp/KL_srp_listener_fsm.sv $P/srp/KL_srp_encoder.sv $P/srp/KL_srp_top.sv \
    $P/top/KL_mrp_strip.sv $P/top/protocol_processor_top.sv \
    $REPO/hdl/milan/KL_pp_shadow.sv
}

set INCS [list $REPO/hdl/common $REPO/hdl/common/csr \
               $REPO/hdl/common/eth_event_counter $REPO/hdl/ieee17221/adp \
               $REPO/hdl/ieee8021q/ts $REPO/hdl/ieee8021as/ptp_timestamp \
               $REPO/hdl/ieee17221/aecp $REPO/hdl/ieee17221/aecp/gen \
               $REPO/configs/generated/endstation_arty_current]

synth_design -mode out_of_context -top milan_datapath -part xc7a100tfgg484-2 \
  -include_dirs $INCS -generic PP_PLANE_P=$PP

create_clock -period 10.000 -name clk [get_ports -quiet axis_clk]
report_utilization -hierarchical -file util_hier_$TAG.rpt
report_utilization -file util_$TAG.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing_$TAG.rpt

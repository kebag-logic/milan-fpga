# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context synthesis of the SHIPPING 1722.1 + SRP control planes — the
# ones scenario B proposes to DELETE and replace with the protocol processor.
#
# This is the other half of syn/ooc/pp_shadow_ooc.tcl. That script prices what
# the new plane COSTS; this one prices what the old planes GIVE BACK, with the
# same instrument (post-synthesis utilization, ship part, 100 MHz OOC), so the
# two can be subtracted honestly. A net figure built from two different
# instruments would not be a net figure.
#
#   PLANE=aecp  vivado -mode batch -source .../old_planes_ooc.tcl -nojournal
#   PLANE=lwsrp | acmp_lstn | acmp_tlkr | adp
#
# The shape include is REQUIRED: milan_csr and the AECP response builder both
# `include gen/adp_shape_defaults.svh, and an unnamed shape resolves to
# whichever config last ran --write-rtl.

set REPO [file normalize [file dirname [info script]]/../..]
set H    $REPO/hdl
set A    $REPO/third_party/verilog-axis/rtl
set C    $H/common
set K    $H/ieee17221/aecp
set M    $H/ieee17221/acmp
set D    $H/ieee17221/adp
set S    $H/ieee8021q/srp

set PLANE [expr {[info exists ::env(PLANE)] ? $::env(PLANE) : "aecp"}]
puts "old-plane OOC: PLANE=$PLANE"

set INCS [list $C $H/common/csr $C/eth_event_counter $D $K $K/gen \
               $REPO/configs/generated/endstation_arty_current]

switch $PLANE {
  aecp {
    set TOP KL_aecp_top
    set SRCS [list $C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $D/adp_pkg.sv \
      $K/aecp_pkg.sv $K/KL_aecp_ingress.sv $K/KL_aecp_packet_validator.sv \
      $K/KL_aecp_common_parser.sv $K/KL_aecp_l0_state.sv $K/KL_aecp_timers.sv \
      $K/KL_aecp_accessor.sv $K/KL_aecp_aem_store.sv $K/KL_aem_patch.sv \
      $K/KL_aecp_aem_dyn_mux.sv $K/KL_aecp_response_builder.sv $K/KL_aecp_top.sv]
  }
  lwsrp {
    set TOP KL_lwsrp_top
    set SRCS [list $S/lwsrp_pkg.sv $S/KL_lwsrp_timers.sv $S/KL_lwsrp_tx.sv \
      $S/KL_lwsrp_ingress.sv $S/KL_lwsrp_walker.sv $S/KL_lwsrp_registrar.sv \
      $S/KL_lwsrp_ta_registrar.sv $S/KL_lwsrp_rx.sv $S/KL_lwsrp_bw_gate.sv \
      $S/KL_lwsrp_ctx.sv $S/KL_lwsrp_ctx_tx.sv $S/KL_lwsrp_top.sv]
  }
  acmp_lstn {
    set TOP KL_acmp_listener
    set SRCS [list $M/acmp_pkg.sv $M/KL_acmp_lstn_ctx.sv $M/KL_acmp_listener.sv]
  }
  acmp_tlkr {
    set TOP KL_acmp_responder
    set SRCS [list $M/acmp_pkg.sv $M/KL_acmp_tlkr_ctx.sv $M/KL_acmp_responder.sv]
  }
  adp {
    set TOP adp_advertiser
    set SRCS [list $D/adp_pkg.sv $D/adp_advertiser.sv]
  }
  default { error "unknown PLANE '$PLANE'" }
}

read_verilog -sv $SRCS
read_verilog $A/axis_fifo.v

synth_design -mode out_of_context -top $TOP -part xc7a100tfgg484-2 \
  -include_dirs $INCS

create_clock -period 10.000 -name clk [get_ports -quiet clk_i]
report_utilization -hierarchical -file util_hier_$PLANE.rpt
report_utilization -file util_$PLANE.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing_$PLANE.rpt

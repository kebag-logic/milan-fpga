# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context synthesis of the WHOLE milan_datapath — the assembled,
# substituted design: the shipping 1722.1/SRP planes are deleted and the
# protocol processor stands in their place, instantiated unconditionally.
#
# Same instrument as syn/ooc/pp_shadow_ooc.tcl (post-synthesis utilization,
# ship part, 100 MHz OOC), because a net figure built from two different
# instruments is not a net figure.
#
# The per-block OOC number pp_shadow_ooc.tcl produces is a STANDALONE cost; it
# does not carry the datapath's own interconnect to the plane. This script is
# what closes that gap: it prices the assembled design, so a difference against
# a stored baseline is the number that actually decides the campaign.
#
#   vivado -mode batch -source .../milan_datapath_ooc.tcl -nojournal
#   TAG=<name> ...     ;# names the .rpt files
#
# There is no PP switch any more. milan_datapath instantiates KL_pp_shadow
# unconditionally (PP_PLANE_P is gone with the plane it used to gate), so
# "the datapath" and "the datapath with the processor" are the same design.
#
# The shape include MUST be named (milan_datapath and milan_csr both
# `include gen/adp_shape_defaults.svh); the 1x1 arty config is the default
# elaboration shape the yosys gate also uses.

set REPO [file normalize [file dirname [info script]]/../..]
set TAG  [expr {[info exists ::env(TAG)] ? $::env(TAG) : "base"}]
puts "milan_datapath OOC: tag=$TAG"

# The source list is printed by syn/yosys/run.sh itself (`--emit`) and relayed
# by dp_srcs.py -- the ONE list the portability gate proves elaborates. A copy
# here would drift, and since the processor's files are part of that list now, a
# copy would drift a whole control plane. Nothing is read outside it, and
# nothing re-reads run.sh: dp_srcs.py checks the record run.sh hands it.
set SRC_LINES [split [string trim [exec python3 $REPO/syn/ooc/dp_srcs.py]] "\n"]
set SV {}
set V  {}
foreach f $SRC_LINES {
  if {[string match "*.sv" $f]} { lappend SV $f } else { lappend V $f }
}
puts "milan_datapath OOC: [llength $SV] SystemVerilog + [llength $V] Verilog sources"
read_verilog -sv $SV
read_verilog $V

# protocol_processor_top $readmemh's its ACMP listener transition ROM by the
# RELATIVE name "ltn_rom.hex", which Vivado resolves against ITS OWN run
# directory. Generate it into that directory and hand synth_design the absolute
# path, so the utilization report cannot depend on where vivado was launched
# from — and cannot quietly measure an all-zero ROM.
set TROM [file normalize ltn_rom.hex]
exec python3 $REPO/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o $TROM
# UG901: a STRING generic's value must reach -generic wrapped in literal
# double quotes, or Vivado takes it for an integer/bit-vector and drops it.
set TROM_GENERIC "PP_TROM_HEX_P=\"$TROM\""

set INCS [list $REPO/hdl/common $REPO/hdl/common/csr \
               $REPO/hdl/common/eth_event_counter $REPO/hdl/ieee17221/adp \
               $REPO/hdl/ieee8021q/ts $REPO/hdl/ieee8021as/ptp_timestamp \
               $REPO/hdl/ieee1722/avtp \
               $REPO/configs/generated/endstation_arty_current]

synth_design -mode out_of_context -top milan_datapath -part xc7a100tfgg484-2 \
  -include_dirs $INCS -generic $TROM_GENERIC

create_clock -period 10.000 -name clk [get_ports -quiet axis_clk]
report_utilization -hierarchical -file util_hier_$TAG.rpt
report_utilization -file util_$TAG.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing_$TAG.rpt

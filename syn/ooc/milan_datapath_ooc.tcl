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

# BOTH control-plane $readmemh images, generated into the run directory FIRST,
# before anything slow. protocol_processor_top reads its ACMP listener
# transition ROM by the RELATIVE name "ltn_rom.hex" and KL_aecp_ucpu its
# microcode by "ucode.hex" (UCODE_HEX_P); Vivado resolves both against ITS OWN
# run directory. This recipe is documented to run from an EMPTY directory, so
# it must generate what it requires: until #246 it generated only
# ltn_rom.hex, and Vivado read the absent ucode.hex as an all-zero ROM behind
# one CRITICAL WARNING (Synth 8-4445), constant-folded the AECP uCPU, and
# completed rc=0 with a full, plausible utilization report 7,923 LUT under
# the shipping design. `exec` takes each generator's exit status (a failed
# generator aborts the script); the check after it refuses an image a
# generator left missing or empty, exactly pp_shadow_ooc.tcl's contract.
foreach {img gen} [list \
    ltn_rom.hex $REPO/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py \
    ucode.hex   $REPO/protocol-processor/hdl/aecp/ucode/gen_ucode.py] {
  exec python3 $gen -o $img
  if {![file exists $img] || [file size $img] == 0} {
    error "milan_datapath OOC: $img is missing or empty in [pwd] after its\
generator ($gen) exited 0. Refusing to synthesize: an area report built on a\
ROM Vivado could not open is not a measurement (#246)."
  }
}

# The absolute paths reach synth_design as generics, so the figure cannot
# depend on where vivado was launched from and cannot quietly measure an
# all-zero ROM. UG901: a STRING generic's value must reach -generic wrapped
# in literal double quotes, or Vivado takes it for an integer/bit-vector and
# drops it.
set TROM_GENERIC  "PP_TROM_HEX_P=\"[file normalize ltn_rom.hex]\""
set UCODE_GENERIC "PP_UCODE_HEX_P=\"[file normalize ucode.hex]\""

# And the refusal the tool itself already offers: a $readmem image Vivado
# cannot open is CRITICAL WARNING Synth 8-4445 and a completed run with a
# wrong number -- the one failure of this instrument that still returns a
# figure. Promote it to an ERROR so any image this preflight does not cover
# (a future option-ON gptp_ucode.hex, a renamed image) fails the run outright
# instead of shaping the report.
set_msg_config -id {Synth 8-4445} -new_severity ERROR

# The source list is printed by syn/yosys/run.sh itself (`--emit`) and relayed
# by dp_srcs.py -- the ONE list the portability gate proves elaborates. A copy
# here would drift, and since the processor's files are part of that list now, a
# copy would drift a whole control plane. Nothing is read outside it, and
# nothing re-reads run.sh: dp_srcs.py checks the record run.sh hands it, and
# resolves $TOP in it through `sv2v --top`, so sv2v is required to run this
# script as well as the Yosys gate (README.md's tool table).
set SRC_LINES [split [string trim [exec python3 $REPO/syn/ooc/dp_srcs.py]] "\n"]
set SV {}
set V  {}
foreach f $SRC_LINES {
  if {[string match "*.sv" $f]} { lappend SV $f } else { lappend V $f }
}
puts "milan_datapath OOC: [llength $SV] SystemVerilog + [llength $V] Verilog sources"
read_verilog -sv $SV
read_verilog $V

set INCS [list $REPO/hdl/common $REPO/hdl/common/csr \
               $REPO/hdl/common/eth_event_counter $REPO/hdl/ieee17221/adp \
               $REPO/hdl/ieee8021q/ts $REPO/hdl/ieee8021as/ptp_timestamp \
               $REPO/hdl/ieee1722/avtp \
               $REPO/configs/generated/endstation_arty_current]

synth_design -mode out_of_context -top milan_datapath -part xc7a100tfgg484-2 \
  -include_dirs $INCS -generic $TROM_GENERIC -generic $UCODE_GENERIC

create_clock -period 10.000 -name clk [get_ports -quiet axis_clk]
report_utilization -hierarchical -file util_hier_$TAG.rpt
report_utilization -file util_$TAG.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing_$TAG.rpt

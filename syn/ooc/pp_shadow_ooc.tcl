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
#   python3 <pp>/hdl/aecp/ucode/gen_ucode.py -o ucode.hex
#   vivado -mode batch -source <repo>/syn/ooc/pp_shadow_ooc.tcl -nojournal -log ooc.log
#
# BOTH images, and both by RELATIVE name, because their modules $readmemh them
# that way and Vivado resolves the name against ITS OWN working directory, not
# against the source file. A missing one is a CRITICAL WARNING ending in
# "ignoring", not an error, so the run completes and reports an area for a ROM
# full of X. ucode.hex became necessary when this file stopped naming a subset
# of the plane by hand: the AECP uCPU was one of the eight sources the old
# literal had gone stale by. syn/yosys/run.sh generates both, for this reason.
# The check below refuses to synthesize without them, because that CRITICAL
# WARNING is the one failure of this instrument that still returns a number.

set REPO [file normalize [file dirname [info script]]/../..]

# The top is named ONCE. It reaches synth_design and the source-list generator
# from the same variable, so the module this script synthesizes and the module
# it reads cannot be two different strings.
set TOP KL_pp_shadow

# The read set is what syn/yosys/run.sh ITSELF PRINTS for the "KL_pp_shadow|..."
# entry -- the same list the portability gate elaborates on every run. dp_srcs.py
# runs `run.sh --emit KL_pp_shadow` and checks the record; it does not read the
# script, because a reader of a build file accepts what it has modelled and bash
# accepts something else, and four such disagreements were measured on the
# reading version ([R0] on PR #240, round two). Now a run.sh edit either moves
# this read set exactly as it moves the Yosys one, or fails both.
#
# This file used to assemble its own list instead: scripts/pp_srcs.py for the
# submodule half plus a hand-named axis_fifo.v. That covered every source except
# one, and the one was $TOP itself, so the documented plane-area recipe read 41
# sources and stopped at `ERROR: [Synth 8-439] module 'KL_pp_shadow' not found`
# (Issue #235). What replaces it is not a tidier spelling of the same list:
# dp_srcs.py refuses to emit a list unless the top RESOLVES in it -- its model of
# the directive layer must see the declaration (a commented, `ifdef`-guarded or
# unexpanded-macro one is not one), and sv2v, when installed, must resolve it
# too. On a host without sv2v the model alone still refuses; only the
# cross-check is lost, and `--require-front-end` (which CI passes and this file
# does not) turns that loss into a failure.
set SRC_LINES [split [string trim [exec python3 $REPO/syn/ooc/dp_srcs.py --top $TOP]] "\n"]
set SV {}
set V  {}
foreach f $SRC_LINES {
  if {[string match "*.sv" $f]} { lappend SV $f } else { lappend V $f }
}
puts "pp_shadow OOC: [llength $SV] SystemVerilog + [llength $V] Verilog sources"

# Both $readmemh images, BEFORE anything slow. Vivado resolves the relative
# name against the working directory, so this check has to ask the same
# question the same way: from here, by relative name. An absent or empty image
# is a CRITICAL WARNING and a completed run whose utilization figure is for a
# ROM of X -- the only way this script returns a wrong number instead of no
# number, which is the worse half of the pair Issue #235 is the other half of.
foreach {img gen} [list \
    ltn_rom.hex "protocol-processor/hdl/acmp/rom/gen_ltn_rom.py (KL_pp_acmp_listener's F05.3 transition ROM)" \
    ucode.hex   "protocol-processor/hdl/aecp/ucode/gen_ucode.py (KL_aecp_ucpu's microcode)"] {
  if {![file exists $img] || [file size $img] == 0} {
    error "pp_shadow OOC: $img is missing or empty in [pwd]. Generate it here\
with $gen before running this script. Vivado would report the missing\
\$readmemh image as a CRITICAL WARNING ending in \"ignoring\", synthesize a ROM\
full of X and print a utilization number for it."
  }
}

read_verilog -sv $SV
read_verilog $V

# Shape. Defaults to the wrapper's own 8/8 - the FULL-shape, pessimistic,
# decision-relevant end. Override for the shape a given board actually flashes:
#   PP_N_IN=1 PP_N_OUT=1 vivado -mode batch -source .../pp_shadow_ooc.tcl
# The two numbers are read ONCE here and printed with the result, because a
# utilization figure quoted without its shape is a figure that gets misapplied.
set N_IN  [expr {[info exists ::env(PP_N_IN)]  ? $::env(PP_N_IN)  : 8}]
set N_OUT [expr {[info exists ::env(PP_N_OUT)] ? $::env(PP_N_OUT) : 8}]
puts "pp_shadow OOC shape: N_STREAM_IN_P=$N_IN N_STREAM_OUT_P=$N_OUT"

synth_design -mode out_of_context -top $TOP -part xc7a100tfgg484-2 \
  -generic N_STREAM_IN_P=$N_IN -generic N_STREAM_OUT_P=$N_OUT

create_clock -period 10.000 -name clk [get_ports clk_i]
report_utilization -hierarchical -file util_hier.rpt
report_utilization -file util.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing.rpt

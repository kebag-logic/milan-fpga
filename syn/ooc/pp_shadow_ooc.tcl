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

set REPO [file normalize [file dirname [info script]]/../..]
set PP   $REPO/protocol-processor/hdl
set AXIS $REPO/third_party/verilog-axis/rtl

# The submodule sources are DERIVED (scripts/pp_srcs.py), not listed here. This
# file used to carry a sixth hand-written copy of that list and it was stale by
# eight sources, the whole AECP engine among them, which Vivado reports only as
# `module not found`. Packages come first because a package must be declared
# before its importers; the generator guarantees that ordering.
set PP_SRCS [exec python3 $REPO/scripts/pp_srcs.py --prefix $PP]
read_verilog -sv {*}$PP_SRCS

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

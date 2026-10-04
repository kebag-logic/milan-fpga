# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Vivado calibration anchor for the issue #649 parameter sweep: synthesize one
# top out of context at one sweep point, with the shipping image's synthesis
# and optimization directives, and report it twice (after synth_design and
# after opt_design) at full hierarchy depth.
#
# Everything that names a design input comes from ONE file the sweep driver
# writes, syn/resmap/yosys_sweep.py `vivado-point`, so the Yosys and Vivado
# halves of a calibration pair read the same derived record:
#
#   top=<module>             exactly one
#   part=<part>              exactly one
#   clock_ns=<period>        exactly one; constrains the axis_clk port
#   incdir=<dir>             in order; the point's shape directory first
#   define=<NAME>            each one
#   src=<file>               in the derived record's order
#   generic=<NAME>=<value>   each parameter the point binds, ROM paths included
#
# A key this file does not know is a refusal, as is a missing one, and a
# $readmem image Vivado cannot open is promoted to an error (Synth 8-4445), so
# no report is written for a ROM read as zeros.
#
#   vivado -mode batch -source datapath_ooc.tcl -nojournal -log ooc.log \
#     -tclargs <point file>
#
# Writes, in the run directory: synth_hierarchy.rpt, synth_utilization.rpt,
# opt_hierarchy.rpt, opt_utilization.rpt, opt_cells.tsv (the census
# route_map.tcl writes, for CARRY4) and timing_opt.rpt.

if {[llength $argv] != 1} {
  error "datapath_ooc.tcl: expected exactly one argument, the point file"
}
set fh [open [lindex $argv 0] r]
set lines [split [string trim [read $fh]] "\n"]
close $fh
array set one {}
set incdirs {}
set defines {}
set srcs {}
set generics {}
foreach line $lines {
  if {![regexp {^([a-z_]+)=(.*)$} $line -> key value] || $value eq ""} {
    error "datapath_ooc.tcl: unreadable point line \"$line\""
  }
  switch -- $key {
    top - part - clock_ns {
      if {[info exists one($key)]} { error "datapath_ooc.tcl: $key given twice" }
      set one($key) $value
    }
    incdir { lappend incdirs $value }
    define { lappend defines -verilog_define $value }
    src { lappend srcs $value }
    generic { lappend generics -generic $value }
    default { error "datapath_ooc.tcl: unknown point key \"$key\"" }
  }
}
foreach key {top part clock_ns} {
  if {![info exists one($key)]} { error "datapath_ooc.tcl: the point names no $key" }
}
if {[llength $srcs] == 0 || [llength $incdirs] == 0} {
  error "datapath_ooc.tcl: the point names no sources or no include directory"
}
# Two threads, where the shipping route uses 32: the build host is shared,
# and each parallel-synthesis helper holds about 2 GB.
set_param general.maxThreads 2
set_msg_config -id {Synth 8-4445} -new_severity ERROR

# Read in the record's own order, one call per run of same-language files,
# as syn/ooc/milan_datapath_ooc.tcl does: compilation-unit scope moves with it.
set batch {}
set batch_sv -1
foreach f [concat $srcs {{}}] {
  set is_sv [string match "*.sv" $f]
  if {$f eq "" || ($batch_sv != -1 && $is_sv != $batch_sv)} {
    if {[llength $batch]} {
      if {$batch_sv} { read_verilog -sv $batch } else { read_verilog $batch }
    }
    set batch {}
  }
  if {$f eq ""} break
  set batch_sv $is_sv
  lappend batch $f
}

synth_design -mode out_of_context -top $one(top) -part $one(part) \
  -directive AreaOptimized_high -include_dirs $incdirs {*}$defines {*}$generics
set clk [get_ports -quiet axis_clk]
if {[llength $clk] != 1} {
  error "datapath_ooc.tcl: expected exactly one axis_clk port, found [llength $clk]"
}
create_clock -period $one(clock_ns) -name clk $clk
report_utilization -hierarchical -hierarchical_depth 64 \
  -hierarchical_min_primitive_count 0 -file synth_hierarchy.rpt
report_utilization -file synth_utilization.rpt

opt_design -directive ExploreArea
report_utilization -hierarchical -hierarchical_depth 64 \
  -hierarchical_min_primitive_count 0 -file opt_hierarchy.rpt
report_utilization -file opt_utilization.rpt
report_timing_summary -max_paths 3 -file timing_opt.rpt

set cells [get_cells -hierarchical -filter {IS_PRIMITIVE == 1}]
set out [open opt_cells.tsv w]
puts $out "cell\tprimitive\tlevel\tsite\tbel"
foreach name [get_property NAME $cells] ref [get_property REF_NAME $cells] \
    level [get_property PRIMITIVE_LEVEL $cells] {
  puts $out "$name\t$ref\t$level\t-\t-"
}
close $out
puts "datapath_ooc: [llength $cells] primitive cells"

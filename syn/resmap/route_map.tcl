# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Whole-image resource map, Vivado half (issue #649): reopen a ROUTED
# checkpoint and write the three inputs syn/resmap/resmap_map.py ties:
#
#   map_hierarchy.rpt  report_utilization -hierarchical at a depth no instance
#                      reaches, with the small-instance filter off, so every
#                      instance of the rebuilt hierarchy is a row
#   map_utilization.rpt  the flat report, whose totals are the image's
#   map_cells.tsv      every primitive cell: name, REF_NAME, PRIMITIVE_LEVEL,
#                      placed site and BEL. CARRY4 per block and the slice
#                      attribution are read from it, because the hierarchical
#                      report carries neither.
#
# It changes no netlist and writes no checkpoint. Run it from an empty
# directory:
#
#   vivado -mode batch -source route_map.tcl -nojournal -log route_map.log \
#     -tclargs <routed.dcp>
#
# The depth is 64. The parser refuses the report as truncated unless its
# deepest row lies above the depth the report's own command line names; the
# census plays no part in that check.

if {[llength $argv] != 1} {
  error "route_map.tcl: expected exactly one argument, the routed checkpoint"
}
set CHECKPOINT [file normalize [lindex $argv 0]]
if {![file isfile $CHECKPOINT]} {
  error "route_map.tcl: no checkpoint at $CHECKPOINT"
}
set_param general.maxThreads 8
open_checkpoint $CHECKPOINT
puts "route_map: design state [get_property STATUS [current_design]]"

report_utilization -hierarchical -hierarchical_depth 64 \
  -hierarchical_min_primitive_count 0 -file map_hierarchy.rpt
report_utilization -file map_utilization.rpt

# One property query per column over the whole cell list, in one order: a
# per-cell get_property over about 130,000 cells is minutes, a list query is
# seconds, and the lists come back in the order of the cell list they read.
set cells [get_cells -hierarchical -filter {IS_PRIMITIVE == 1}]
set names [get_property NAME $cells]
set refs [get_property REF_NAME $cells]
set levels [get_property PRIMITIVE_LEVEL $cells]
set sites [get_property LOC $cells]
set bels [get_property BEL $cells]
set n [llength $names]
foreach column [list $refs $levels $sites $bels] {
  if {[llength $column] != $n} {
    error "route_map.tcl: a property list is [llength $column] long for $n\
 cells; an empty property collapses a list, so the columns no longer align"
  }
}
# A parallel foreach, never lindex by position: the property lists are not
# plain Tcl lists until converted, and indexing them one position at a time
# measured 64 lines a second (12,248 lines in 190 s before that run was
# stopped), about 34 minutes of held lock for one census.
set fh [open map_cells.tsv w]
puts $fh "cell\tprimitive\tlevel\tsite\tbel"
foreach name $names ref $refs level $levels site $sites bel $bels {
  if {$site eq ""} { set site "-" }
  if {$bel eq ""} { set bel "-" }
  puts $fh "$name\t$ref\t$level\t$site\t$bel"
}
close $fh
puts "route_map: $n primitive cells written"

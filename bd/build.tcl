# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Non-interactive project build for the Milan TSN NIC: RTL + block design ->
# synthesis -> implementation -> bitstream. Needs a valid Vivado tool license
# (free "Vivado ML Standard / basic" tier covers xc7z020clg400-1).
#
#   cd bd && vivado -mode batch -source build.tcl
#     [-tclargs <stage>]        stage in: bd | synth | impl | bit (default bit)
#
# Everything lands in bd/build/ (git-ignored). The block design comes from the
# generated milan-dma.tcl; its 2025.1 version-guard is neutralised at source
# time (we run 2026.1) without touching the committed file.

set REPO   [file normalize [file dirname [info script]]/..]
set BD_TCL [file join $REPO bd milan-dma.tcl]
set BUILD  [file join $REPO bd build]
set PART   xc7z020clg400-1
set TOP    milan_top

set stage bit
if {[llength $argv] > 0} { set stage [lindex $argv 0] }

file mkdir $BUILD
cd $BUILD

# --------------------------------------------------------------------------
# 1. Project + RTL sources
# --------------------------------------------------------------------------
create_project -force milan_dma_project $BUILD -part $PART

# All synthesizable RTL under hdl/ (packages/headers first is not required —
# Vivado orders by dependency during elaboration).
set rtl {}
foreach ext {svh sv v} {
    # sources live up to three levels under hdl/ (hdl/<family>/<block>[/gen]/*.ext)
    foreach f [glob -nocomplain \
                   [file join $REPO hdl * * * *.$ext] \
                   [file join $REPO hdl * * *.$ext] \
                   [file join $REPO hdl * *.$ext] \
                   [file join $REPO hdl *.$ext]] {
        lappend rtl $f
    }
}
set rtl [lsort -unique $rtl]
if {[llength $rtl] == 0} { error "no RTL sources found under [file join $REPO hdl]" }
add_files -norecurse $rtl
set_property file_type {SystemVerilog} [get_files -quiet *.sv]
set_property file_type {Verilog Header} [get_files -quiet *.svh]

# --------------------------------------------------------------------------
# 2. Block design (milan_dma) from the generated tcl, version-guard defused
# --------------------------------------------------------------------------
set fh [open $BD_TCL r]; set bd_src [read $fh]; close $fh
# Make the embedded version match the running tool so the guard's `return 1`
# never fires. `version -short` -> e.g. 2026.1
set here [version -short]
regsub {set scripts_vivado_version [0-9]+\.[0-9]+} $bd_src "set scripts_vivado_version $here" bd_src
eval $bd_src

set bd_file [get_files -quiet *milan_dma.bd]
if {$bd_file eq ""} { error "block design milan_dma.bd was not created by $BD_TCL" }
generate_target all [get_files $bd_file]
# Do NOT make_wrapper: the repo ships a hand-edited hdl/milan/milan_dma_wrapper.v
# (adds m_axi_csr + irq_csr) that instantiates the BD directly.

set_property top $TOP [current_fileset]
update_compile_order -fileset sources_1
puts "== top = [get_property top [current_fileset]] ; part = $PART =="
puts "== BD milan_dma created; sources ready =="
if {$stage eq "bd"} { puts "== stage=bd: stopping after elaboration setup =="; return }

# --------------------------------------------------------------------------
# 3. Synthesis
# --------------------------------------------------------------------------
launch_runs synth_1 -jobs [expr {[llength [get_param general.maxThreads]] ? 4 : 4}]
wait_on_run synth_1
if {[get_property PROGRESS [get_runs synth_1]] ne "100%"} {
    error "SYNTHESIS FAILED — see [file join $BUILD milan_dma_project.runs synth_1 runme.log]"
}
puts "== synthesis complete =="
if {$stage eq "synth"} { return }

# --------------------------------------------------------------------------
# 4. Implementation (+ bitstream unless stage=impl)
# --------------------------------------------------------------------------
if {$stage eq "bit"} {
    launch_runs impl_1 -to_step write_bitstream -jobs 4
} else {
    launch_runs impl_1 -jobs 4
}
wait_on_run impl_1
if {[get_property PROGRESS [get_runs impl_1]] ne "100%"} {
    error "IMPLEMENTATION FAILED — see [file join $BUILD milan_dma_project.runs impl_1 runme.log]"
}
puts "== implementation complete =="

set bit [glob -nocomplain [file join $BUILD milan_dma_project.runs impl_1 *.bit]]
if {$bit ne ""} { puts "== BITSTREAM: $bit ==" } else { puts "== no .bit produced (stage=$stage) ==" }

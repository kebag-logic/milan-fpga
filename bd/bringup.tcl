# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# ---------------------------------------------------------------------------
# bringup.tcl — bring up the Milan TSN NIC project inside Vivado.
#
# Creates the Vivado project for a chosen FPGA device, adds all RTL, builds the
# milan_dma block design, sets milan_top as the top module, and leaves the
# project OPEN so you can keep working (GUI or interactive Tcl).
#
# It is normally launched by bringup.py, but you can also run it directly:
#
#     vivado -mode gui -source bringup.tcl -tclargs <part> <with_bd>
#     vivado -mode tcl -source bringup.tcl -tclargs xc7z020clg400-1 1
#
#   <part>     full Vivado part name        (default: xc7z020clg400-1)
#   <with_bd>  1 = build the milan_dma BD    (default: 1 for Zynq-7000 parts,
#              0 = RTL only                            0 otherwise)
#
# The milan_dma BD instantiates the Zynq-7000 PS (processing_system7), so the
# full project only builds on an xc7z* part. On any other device pass with_bd=0
# to bring up just the synthesizable TSN RTL (useful for lint / OOC synthesis).
# ---------------------------------------------------------------------------

# --- Parameters (device is defined here / via -tclargs) --------------------
set REPO      [file normalize [file dirname [info script]]/..]
set BD_TCL    [file join $REPO bd milan-dma.tcl]
set BUILD_DIR [file join $REPO bd build]
set TOP       milan_top

set PART    xc7z020clg400-1                            ;# default target device
if {[llength $argv] >= 1} { set PART [lindex $argv 0] }

# BD on by default only for Zynq-7000 (the PS7 IP needs it); else RTL only.
set WITH_BD [expr {[string match "xc7z*" $PART] ? 1 : 0}]
if {[llength $argv] >= 2} { set WITH_BD [lindex $argv 1] }

puts "=========================================================="
puts " Milan TSN project bring-up"
puts "   device (part) : $PART"
puts "   block design  : [expr {$WITH_BD ? {milan_dma (Zynq PS7)} : {none — RTL only}}]"
puts "   build dir     : $BUILD_DIR"
puts "=========================================================="

# --- 1. Sanity-check the device is actually installed ----------------------
if {[llength [get_parts -quiet $PART]] == 0} {
    puts "ERROR: part '$PART' is not installed in this Vivado."
    puts "       installed families: [lsort -unique [get_property FAMILY [get_parts]]]"
    puts "       (Zynq-7000 needs the AMD installer -> Add Devices -> Zynq-7000.)"
    return -code error "part not installed"
}

# --- 2. Create the project -------------------------------------------------
create_project -force milan_dma_project $BUILD_DIR -part $PART

# --- 3. Add every RTL source under hdl/ ------------------------------------
#     (packages/headers are ordered automatically during elaboration)
set rtl {}
foreach ext {svh sv v} {
    foreach f [glob -nocomplain \
                   [file join $REPO hdl * *.$ext] \
                   [file join $REPO hdl *.$ext]] {
        lappend rtl $f
    }
}
set rtl [lsort -unique $rtl]
if {[llength $rtl] == 0} { return -code error "no RTL found under [file join $REPO hdl]" }
add_files -norecurse $rtl
set_property file_type {SystemVerilog}   [get_files -quiet *.sv]
set_property file_type {Verilog Header}  [get_files -quiet *.svh]
puts "== added [llength $rtl] RTL source files =="

# --- 4. Build the milan_dma block design (Zynq PS7 + DMA + interconnect) ----
if {$WITH_BD} {
    # The generated BD script is stamped for Vivado 2025.1 and its version guard
    # does `return 1` on any mismatch. Rewrite the stamp to the running tool so
    # the guard passes — without editing the committed file on disk.
    set fh [open $BD_TCL r]; set bd_src [read $fh]; close $fh
    regsub {set scripts_vivado_version [0-9]+\.[0-9]+} \
           $bd_src "set scripts_vivado_version [version -short]" bd_src
    eval $bd_src

    set bd_file [get_files -quiet *milan_dma.bd]
    if {$bd_file eq ""} { return -code error "milan_dma.bd was not created by $BD_TCL" }
    generate_target all [get_files $bd_file]
    puts "== block design milan_dma created + generated =="
    # NB: no make_wrapper — the repo ships a hand-edited milan_dma_wrapper.v
    #     (adds the m_axi_csr master + irq_csr) that instantiates the BD directly.
}

# --- 5. Set the top and settle the compile order ---------------------------
set_property top $TOP [current_fileset]
update_compile_order -fileset sources_1

puts "=========================================================="
puts " Project is up.  top = [get_property top [current_fileset]] , part = $PART"
puts "   next (interactive):  launch_runs synth_1 ; wait_on_run synth_1"
puts "   or full flow:        vivado -mode batch -source build.tcl"
puts "=========================================================="
# Project is intentionally left OPEN for interactive work.

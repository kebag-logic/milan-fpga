# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# FAIL THE BUILD WHEN A PORT CONSTRAINED `IOB TRUE` DID NOT PACK (issue #475).
#
# `set_property IOB TRUE` asks the placer to put a port's register in the
# OLOGIC/ILOGIC site of its own IOB. When that register cannot go there - it
# has a fabric load, its D is an inversion, or there is no register at all -
# Vivado raises CRITICAL WARNING [Place 30-722] and the build carries on. The
# bitstream then launches or samples that pin from a slice, and the pin-to-pin
# skew the constraint was bought for (the TDM bus, the GMII launch and
# capture) is a placement lottery again with no red line anywhere. So this
# check runs on the PLACED design, before routing, and turns that into an
# error that names the port.
#
# milan_soc.py sources this file and calls the proc from the flow's
# pre-routing commands:
#
#   kl_iob_pack_check <build_name>_iob_pack.rpt
#
# Every port whose IOB property is TRUE gets one verdict line, in the report
# and in the log:
#
#   PASS    OUT: the one cell driving the pad buffer sits in an OLOGIC site.
#           IN: every register reading the pad sits in an ILOGIC site. The
#           input is followed through the ILOGIC's own delay elements
#           (ZHOLD_DELAY, which opt_design inserts in front of an input flop,
#           and IDELAYE2). Combinational fabric loads beside that register
#           are allowed and counted in the line (eth0_rx_dv has four);
#   INERT   there is nothing to pack: an output driven by a constant (a
#           pruned render lane parks tdm_dout low) or an input nothing reads;
#   FAIL    anything else: the register sits in a slice or is unplaced, the
#           pad is driven, or only read, by logic that is not a register, or
#           the port is bidirectional, which this check does not model.
#
# One FAIL is a Tcl error, and a Tcl error ends the batch run: no routing, no
# bitstream. A port with no IOB constraint (tdm_mclk, tdm_din today) is not
# looked at. Vivado object lists are passed whole between the queries below,
# never rebuilt from names: `-of_objects` takes objects, not names.
# sw/litex/iob_pack_selftest.py drives this file in tclsh with the Vivado
# netlist queries stubbed; that is its gate outside Vivado.

# The cells on the far side of `pins` (their net's leaf pins facing `dir`).
proc kl_iob_net_cells {pins dir} {
    set net [get_nets -quiet -of_objects $pins]
    if {[llength $net] == 0} {
        return {}
    }
    return [get_cells -quiet -of_objects \
        [get_pins -quiet -leaf -of_objects $net -filter "DIRECTION == $dir"]]
}

# The cells driving (OUT) or reading (IN) the pad buffer `bufs`, as a list of
# object lists: for an input, the loads that are not delay elements and the
# loads behind those delay elements.
proc kl_iob_far_groups {bufs dir} {
    if {$dir eq "OUT"} {
        return [list [kl_iob_net_cells \
            [get_pins -quiet -of_objects $bufs -filter {REF_PIN_NAME == I}] OUT]]
    }
    set loads [kl_iob_net_cells \
        [get_pins -quiet -of_objects $bufs -filter {REF_PIN_NAME == O}] IN]
    set delays [filter -quiet $loads {REF_NAME == ZHOLD_DELAY || REF_NAME == IDELAYE2}]
    return [list \
        [filter -quiet $loads {REF_NAME != ZHOLD_DELAY && REF_NAME != IDELAYE2}] \
        [kl_iob_net_cells [get_pins -quiet -of_objects $delays -filter {DIRECTION == OUT}] IN]]
}

# One port's verdict: a list {VERDICT detail}.
proc kl_iob_port_verdict {port} {
    set dir [get_property DIRECTION $port]
    if {$dir ni {IN OUT}} {
        return [list FAIL "direction $dir is not checked; only IN and OUT ports are"]
    }
    set site [expr {$dir eq "OUT" ? "OLOGIC" : "ILOGIC"}]
    set bufs [get_cells -quiet -of_objects \
        [get_pins -quiet -leaf -of_objects [get_nets -quiet -of_objects $port]]]
    set regs {}
    set logic {}
    set wrong {}
    foreach group [kl_iob_far_groups $bufs $dir] {
        foreach cell $group {
            set ref [get_property REF_NAME $cell]
            if {$ref eq "GND" || $ref eq "VCC"} {
                continue
            }
            set loc [get_property LOC $cell]
            set what "$cell ($ref @ [expr {$loc eq {} ? {unplaced} : $loc}])"
            if {$dir eq "IN" && ![string is true -strict [get_property IS_SEQUENTIAL $cell]]} {
                lappend logic $what
                continue
            }
            lappend regs $what
            if {![string match "${site}_*" $loc]} {
                lappend wrong $what
            }
        }
    }
    if {[llength $regs] == 0 && [llength $logic] == 0} {
        return [list INERT "$dir, nothing behind the pad to pack"]
    }
    if {[llength $regs] == 0} {
        return [list FAIL "$dir, no register reads the pad, only: [join $logic {, }]"]
    }
    if {[llength $wrong] > 0} {
        return [list FAIL "$dir, not in an $site site: [join $wrong {, }]"]
    }
    set also [expr {[llength $logic] ? "; also read by [llength $logic] fabric cell(s)" : ""}]
    return [list PASS "$dir, [join $regs {, }]$also"]
}

proc kl_iob_pack_check {report} {
    set rows {}
    set failed {}
    foreach port [get_ports -quiet] {
        if {[string toupper [get_property -quiet IOB $port]] ne "TRUE"} {
            continue
        }
        lassign [kl_iob_port_verdict $port] verdict detail
        lappend rows [format "%-5s %s: %s" $verdict $port $detail]
        if {$verdict eq "FAIL"} {
            lappend failed $port
        }
    }
    set rows [lsort $rows]
    set fh [open $report w]
    puts $fh "# issue #475: every port constrained IOB TRUE, after placement"
    foreach row $rows {
        puts $fh $row
    }
    close $fh
    foreach row $rows {
        puts "IOB-PACK $row"
    }
    if {[llength $failed] > 0} {
        error "IOB-PACK FAIL: [llength $failed] port(s) constrained IOB TRUE are not in an IOB register after placement: [join [lsort $failed] {, }]. This is CRITICAL WARNING Place 30-722 made fatal; see $report."
    }
    puts "IOB-PACK OK: [llength $rows] port(s) constrained IOB TRUE checked, none unpacked ($report)"
}

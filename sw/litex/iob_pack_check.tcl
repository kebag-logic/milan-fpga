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
#           An OBUFT's tristate driver is held to the same test, since its
#           register packs into the same OLOGIC. IN: every register reading
#           the pad sits in an ILOGIC site. The input is followed through the
#           ILOGIC's own delay elements (ZHOLD_DELAY, which opt_design
#           inserts in front of an input flop, and IDELAYE2), by their DATA
#           outputs only - an IDELAYE2 CNTVALUEOUT read back by a CSR flop is
#           not a capture path. Combinational fabric loads beside the capture
#           register are allowed and counted in the line (eth0_rx_dv has
#           four);
#   INERT   there is verifiably nothing to pack, and the row says what was
#           seen: a port synthesis kept no buffer and no net for, because
#           nothing reads or drives the pin (eth0_rx_er); an output whose
#           only driver is a constant cell (a pruned render lane parks
#           tdm_dout low);
#   FAIL    anything else: the register sits in a slice or is unplaced, the
#           pad is driven, or only read, by logic that is not a register, the
#           port is bidirectional, which this check does not model, or a hop
#           of the traversal answered nothing where the netlist must hold
#           something - a pad whose buffer, buffer pin, net, far side, or
#           anything behind one of the ILOGIC delay elements cannot be found
#           is NOT a port with nothing to pack.
#
# That last clause is the #475 review finding, and the rule it gives is
# uniform. Past the no-net test below, an IN port can NEVER read INERT: an
# empty answer on ANY hop behind the pad buffer - the hop behind a delay
# element, and a load the delay partition did not account for, included - is
# a FAIL naming the port. An OUT port reads INERT only when every pin this
# file followed answered a driver and every one of those drivers is a
# constant cell. So INERT is reachable from two structures only, each of them
# seen rather than assumed: a port with no net, and an output whose drivers
# are all constants.
#
# What holds that rule up is the grading below, not the absence of `-quiet`:
# an unknown or renamed property is answered EMPTY by Vivado, with the flag
# or without it, measured on this design. `-of_objects` handed a name, or an
# empty list, DOES raise, and a raise ends the batch run rather than reading
# as an absence (the first cut of this check handed it a name and read every
# input INERT). So every step below tests its input first, grades the
# emptiness itself, and passes Vivado object lists whole, never rebuilt from
# names. The one `-quiet` left is marked where it is read, and crossed
# against two counts that do not depend on it.
#
# One FAIL is a Tcl error, and a Tcl error ends the batch run: no routing, no
# bitstream. A port with no IOB constraint (tdm_mclk, tdm_din today) is not
# looked at. sw/litex/iob_pack_selftest.py drives this file in tclsh with the
# Vivado netlist queries stubbed; that is its gate outside Vivado.

# The cells on the far side of `pins` (their net's leaf pins facing `dir`), as
# {reached cells}. `reached` is 0 when the pins carry no net: their far side
# does not exist, which is not the same as a net whose far side is empty, and
# the caller must not read the two the same way. `pins` must not be empty.
proc kl_iob_net_cells {pins dir} {
    set net [get_nets -of_objects $pins]
    if {[llength $net] == 0} {
        return [list 0 {}]
    }
    set far [get_pins -leaf -of_objects $net -filter "DIRECTION == $dir"]
    if {[llength $far] == 0} {
        return [list 1 {}]
    }
    return [list 1 [get_cells -of_objects $far]]
}

# The cells driving (OUT) or reading (IN) the pad buffer `bufs`, as {reached
# groups}: for an input, the loads that are not delay elements and the loads
# behind those delay elements. `reached` is 0 when a hop answered nothing
# where a placed buffer must hold something - no data pin, no net on it, no
# driver, no load, nothing behind a delay element, or a load the delay
# partition lost. That is a FAIL for the caller, never an INERT.
proc kl_iob_far_groups {bufs dir} {
    if {$dir eq "OUT"} {
        set pins [get_pins -of_objects $bufs \
            -filter {REF_PIN_NAME == I || REF_PIN_NAME == T}]
        if {[llength $pins] == 0} {
            return [list 0 {}]
        }
        # one followed pin at a time: an OBUFT whose T answers a grounded
        # driver must not answer for an I whose net came back empty.
        set drivers {}
        foreach pin $pins {
            lassign [kl_iob_net_cells $pin OUT] reached cells
            if {!$reached || [llength $cells] == 0} {
                return [list 0 {}]
            }
            lappend drivers {*}$cells
        }
        return [list 1 [list $drivers]]
    }
    set pins [get_pins -of_objects $bufs -filter {REF_PIN_NAME == O}]
    if {[llength $pins] == 0} {
        return [list 0 {}]
    }
    lassign [kl_iob_net_cells $pins IN] reached loads
    if {!$reached || [llength $loads] == 0} {
        return [list 0 {}]
    }
    set delays [filter $loads {REF_NAME == ZHOLD_DELAY || REF_NAME == IDELAYE2}]
    set direct [filter $loads {REF_NAME != ZHOLD_DELAY && REF_NAME != IDELAYE2}]
    if {[llength $delays] + [llength $direct] != [llength $loads]} {
        # the two halves must account for every load, and they do not when
        # the property itself answered nothing: an unknown or renamed one is
        # empty for == and for != alike, so both halves come back empty and
        # the loads that are really there would go ungraded.
        return [list 0 {}]
    }
    if {[llength $delays] == 0} {
        return [list 1 [list $direct]]
    }
    set taps [get_pins -of_objects $delays -filter \
        {REF_PIN_NAME == DATAOUT || REF_PIN_NAME == DLYIFF || REF_PIN_NAME == DLYFABRIC}]
    if {[llength $taps] == 0} {
        return [list 0 {}]
    }
    lassign [kl_iob_net_cells $taps IN] reached behind
    if {!$reached || [llength $behind] == 0} {
        return [list 0 {}]
    }
    return [list 1 [list $direct $behind]]
}

# One port's verdict: a list {VERDICT detail}.
proc kl_iob_port_verdict {port} {
    set dir [get_property DIRECTION $port]
    if {$dir ni {IN OUT}} {
        return [list FAIL "direction $dir is not checked; only IN and OUT ports are"]
    }
    set site [expr {$dir eq "OUT" ? "OLOGIC" : "ILOGIC"}]
    set nets [get_nets -of_objects $port]
    if {[llength $nets] == 0} {
        # nothing drives or reads the pin, so synthesis kept neither net nor
        # buffer for it (eth0_rx_er): there is no launch or capture edge the
        # constraint could protect. The query itself worked - a failed one
        # would have raised - so this is a seen absence, not a silent one.
        return [list INERT "$dir, the port has no net: nothing drives or reads the pin"]
    }
    set bufs {}
    set pins [get_pins -leaf -of_objects $nets]
    if {[llength $pins] > 0} {
        set bufs [get_cells -of_objects $pins]
    }
    if {[llength $bufs] == 0} {
        return [list FAIL "$dir, net [join $nets {, }] reaches no cell: this port could not be traversed"]
    }
    lassign [kl_iob_far_groups $bufs $dir] reached groups
    if {!$reached} {
        return [list FAIL "$dir, nothing answered behind [join $bufs {, }]: this port could not be traversed"]
    }
    set regs {}
    set logic {}
    set wrong {}
    set fixed {}
    foreach group $groups {
        foreach cell $group {
            set ref [get_property REF_NAME $cell]
            if {$ref eq "GND" || $ref eq "VCC"} {
                lappend fixed "$cell ($ref)"
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
        # the second of the two structures INERT is returned for: every pin
        # followed above answered a driver, and every one of them is a
        # constant cell. An input cannot arrive here - each hop behind its
        # pad buffer answered something or the traversal already failed - and
        # an output with no driver at all is the ungradable case, not a pad
        # with nothing to pack.
        if {$dir eq "OUT" && [llength $fixed] > 0} {
            return [list INERT "$dir, nothing to pack behind [join $bufs {, }]: driven by [join $fixed {, }]"]
        }
        return [list FAIL "$dir, no cell answered behind [join $bufs {, }]: this port could not be traversed"]
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

# How many `set_property IOB TRUE` lines the constraint files beside `report`
# carry: what the build ASKED for, read outside the netlist. -1 when no .xdc
# sits there, so nothing vouches for a run that selected no port.
proc kl_iob_constraint_lines {report} {
    set files [glob -nocomplain -directory [file dirname $report] *.xdc]
    if {[llength $files] == 0} {
        return -1
    }
    set lines 0
    foreach path $files {
        set fh [open $path r]
        set text [read $fh]
        close $fh
        foreach line [split $text "\n"] {
            if {[regexp -nocase {^[ \t]*set_property[ \t]+IOB[ \t]+TRUE} $line]} {
                incr lines
            }
        }
    }
    return $lines
}

proc kl_iob_pack_check {report} {
    set rows {}
    set failed {}
    set graded {}
    foreach port [get_ports] {
        # the only -quiet read in this file, because an empty answer is the
        # NORMAL one here: most ports carry no IOB property at all. The two
        # counts crossed below are what keeps it honest.
        if {[string toupper [get_property -quiet IOB $port]] ne "TRUE"} {
            continue
        }
        lappend graded $port
        # re-raised, never swallowed: a query that fails inside the verdict
        # ends the build either way, but a bare Tcl trace does not say which
        # port it was grading.
        if {[catch {kl_iob_port_verdict $port} answer]} {
            error "IOB-PACK ERROR: grading $port ended the run: $answer"
        }
        lassign $answer verdict detail
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
        error "IOB-PACK FAIL: [llength $failed] port(s) constrained IOB TRUE are not in an IOB register after placement, or could not be traversed: [join [lsort $failed] {, }]. An unpacked register is CRITICAL WARNING Place 30-722 made fatal; the other rows are this check refusing to grade what it could not see. See $report."
    }
    # A run that selected no port would otherwise report a clean result while
    # checking nothing. Cross the per-port property read above against the
    # same question asked as one filter, and both against the constraints the
    # build wrote: the three cannot disagree on a design that packed.
    set constrained [get_ports -filter {IOB == TRUE || IOB == true}]
    set lines [kl_iob_constraint_lines $report]
    if {[llength $rows] != [llength $constrained]} {
        set disputed {}
        foreach port $constrained {
            if {[lsearch -exact $graded $port] < 0} {
                lappend disputed $port
            }
        }
        foreach port $graded {
            if {[lsearch -exact $constrained $port] < 0} {
                lappend disputed $port
            }
        }
        error "IOB-PACK ERROR: [llength $rows] port(s) answered IOB TRUE one at a time, but [llength $constrained] match the same filter; the two reads disagree on: [join [lsort $disputed] {, }]. The netlist did not read the same way twice, so this run graded nothing; see $report."
    }
    if {[llength $rows] == 0 && $lines != 0} {
        set why "$lines set_property IOB TRUE line(s) sit in the constraints beside it"
        if {$lines < 0} {
            set why "no .xdc file sits beside it to say whether that is right"
        }
        error "IOB-PACK ERROR: no port answered IOB TRUE, so nothing was checked, and $why. A run that selects no port is not a pass; see $report."
    }
    puts "IOB-PACK OK: [llength $rows] port(s) constrained IOB TRUE checked, none unpacked ($report)"
}

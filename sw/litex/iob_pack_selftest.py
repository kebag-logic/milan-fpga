#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive sw/litex/iob_pack_check.tcl's verdicts without Vivado (issue #475).

The check runs only inside a Vivado build, after placement, so nothing else
would notice if it stopped failing. This script sources THE REAL .TCL in
`tclsh` with the six Vivado netlist queries it uses (get_ports, get_nets,
get_pins, get_cells, get_property, filter) stubbed over a small placed
netlist, one netlist per arm. The netlists copy what Vivado placed for the
AX7101 TDM8 build: an output flop in an OLOGIC, and an input flop in an
ILOGIC behind the ZHOLD_DELAY that opt_design inserts in front of it.

  - the shipping shape, every constrained port packed: exit 0, and tdm_mclk /
    tdm_din, which carry no IOB constraint, are never looked at even though
    their registers sit in slices;
  - a pruned render lane (tdm_dout driven by a constant) and eth0_rx_er,
    which synthesis kept no net for because nothing reads the pin: INERT,
    exit 0;
  - eth0_rx_dv as it places: its flop in the ILOGIC and four fabric LUTs
    reading the same pad. PASS: the register packed, and the LUTs are
    counted in the line, not failed;
  - one planted defect per arm - the bclk pad flop left in a slice (the
    fabric-load case Place 30-722 reports), an unplaced flop, a LUT on the
    pad, an input flop in the fabric with and without the ILOGIC delay in
    front of it, an input read by a second fabric flop, an input read only
    by LUTs, and a bidirectional port: exit 1, the error names exactly that
    port and the report carries its FAIL row;
  - one hop of the traversal answering nothing while the port's register
    sits in a slice - no pin on the port's net, no data pin on the pad
    buffer, no load on the buffer's net, no driver on it, nothing behind the
    ILOGIC delay element, and a REF_NAME the tool cannot answer, which loses
    every load of the delay partition - and the per-port IOB read answering
    nothing for every port, or no .xdc beside the report: exit 1 each. These
    are the cases that read INERT, or "0 port(s) checked", before the #475
    review; a query that answers nothing must not be the verdict that lets a
    build through;
  - a query answering NAMES instead of objects, which is what `{*}` does to
    an answer live: the next query raises, the run ends, and the error says
    which port was being graded. Nothing packs a name back into an object,
    so this arm holds only while the traversal carries objects end to end.

The stubs mirror the three answers Vivado gives. Nothing MATCHED is an empty
list. A query handed no object at all raises (Common 17-697). And a query
handed a NAME where an object is required raises too (Common 17-161), which
is what ended a real build at this check: an object here is its name behind
a marker byte no netlist name carries, every stub answers objects, every
stub rejects a name, and the harness strips the marker from what the check
prints. `-quiet` is ignored, so the flag is counted in the file instead
(`quiet_reads`).

One thing no stub can see, because Tcl values carry no object identity: live,
REBUILDING a query answer by value turns its objects back into names.
Measured on the placed checkpoint: `{*}` expansion, `eval`, `lmap` and
`join` then `split` all do; `foreach`, `lindex`, `lassign`, `lsort`, `filter`
and `lappend` of the whole answer keep the objects. So the file is read as
text for the measured spellings (`rebuilt_answers`). A text rule sees only
the spellings it lists: the live run on a placed checkpoint that
docs/integration/BUILDING.md requires for any change to the check is what
covers the class.

Every mutant of the .tcl in MUTANTS must then be noticed by an arm that
stops holding or by one of those two counts, which is what shows the checks
here can fail for the defects they name.
Needs `tclsh` (package `tcl`); exits 2 without it.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

CHECK_TCL = Path(__file__).resolve().parent / "iob_pack_check.tcl"

#: The marker an object carries and a name does not. \x02 cannot appear in a
#: netlist name, and the harness strips it from everything the check prints,
#: so a report row and an error read exactly as they do live.
OBJ = "\x02"

#: The Vivado queries the check uses, answered from the ::PORT, ::PIN and
#: ::CELL arrays each arm fills in. A pin's net is its NET field; a net is
#: nothing but the name its pins and its port share. Every query ANSWERS
#: objects and every query REJECTS a name, as the live tool does.
STUBS = r"""
set ::KL_OBJ "\x02"
proc kl_stub_obj {name} {
    return "$::KL_OBJ$name"
}
proc kl_stub_mint {names} {
    set out {}
    foreach name $names { lappend out [kl_stub_obj $name] }
    return $out
}
# The name behind an object, and a raise when there is no object there: a
# name in an object's place is Common 17-161 live, which ends the run.
proc kl_stub_name {cmd what value} {
    if {[string index $value 0] ne $::KL_OBJ} {
        error "stub $cmd: Invalid option value '$value' specified for\
               '$what' (Vivado: Common 17-161)"
    }
    return [string range $value 1 end]
}
proc kl_stub_match {obj filter} {
    foreach alt [split [string map {"||" "\x01"} $filter] "\x01"] {
        set ok 1
        foreach atom [split [string map {"&&" "\x01"} $alt] "\x01"] {
            lassign $atom key op want
            if {($op eq "==") != ([get_property $key $obj] eq $want)} { set ok 0 }
        }
        if {$ok} { return 1 }
    }
    return 0
}
proc filter {args} {
    lassign [lsearch -all -inline -not -exact $args -quiet] objs filter
    set out {}
    foreach o $objs { if {[kl_stub_match $o $filter]} { lappend out $o } }
    return $out
}
proc kl_stub_args {argv} {
    set of {}; set filter ""
    for {set i 0} {$i < [llength $argv]} {incr i} {
        switch -- [lindex $argv $i] {
            -of_objects { incr i; set of [lindex $argv $i] }
            -filter { incr i; set filter [lindex $argv $i] }
        }
    }
    return [list $of $filter]
}
proc get_ports {args} {
    lassign [kl_stub_args $args] of filter
    set all [kl_stub_mint [lsort [array names ::PORT]]]
    if {$filter eq ""} { return $all }
    return [filter $all $filter]
}
proc get_property {args} {
    set argv [lsearch -all -inline -not -exact $args -quiet]
    lassign $argv key obj
    set name [kl_stub_name get_property object $obj]
    foreach arr {::PORT ::PIN ::CELL} {
        if {[info exists ${arr}($name)]} {
            set d [set ${arr}($name)]
            if {[dict exists $d $key]} { return [dict get $d $key] }
            return ""
        }
    }
    error "stub get_property: no object '$name'"
}
# The names behind `-of_objects`: no object at all is Common 17-697 live, a
# name where an object belongs is 17-161, and both end the run.
proc kl_stub_objs {cmd of} {
    if {[llength $of] == 0} {
        error "stub $cmd: -of_objects with no object (Vivado: Common 17-697)"
    }
    set out {}
    foreach o $of { lappend out [kl_stub_name $cmd objects $o] }
    return $out
}
proc get_nets {args} {
    lassign [kl_stub_args $args] of
    set out {}
    foreach o [kl_stub_objs get_nets $of] {
        foreach arr {::PORT ::PIN} {
            if {[info exists ${arr}($o)]} {
                set net [dict get [set ${arr}($o)] NET]
                if {$net ne ""} { lappend out $net }
            }
        }
    }
    return [kl_stub_mint [lsort -unique $out]]
}
proc get_pins {args} {
    lassign [kl_stub_args $args] of filter
    set names [kl_stub_objs get_pins $of]
    set out {}
    foreach p [array names ::PIN] {
        set d $::PIN($p)
        if {[dict get $d NET] in $names || [dict get $d CELL] in $names} {
            lappend out $p
        }
    }
    set out [kl_stub_mint [lsort $out]]
    if {$filter eq ""} { return $out }
    return [filter $out $filter]
}
proc get_cells {args} {
    lassign [kl_stub_args $args] of
    set out {}
    foreach p [kl_stub_objs get_cells $of] {
        lappend out [dict get $::PIN($p) CELL]
    }
    return [kl_stub_mint [lsort -unique $out]]
}
"""

#: A cell as (primitive, placed site); "" is unplaced.
Cell = tuple[str, str]


@dataclass
class Netlist:
    """A placed netlist in the shape the stubs read: ports, pins, cells."""

    ports: dict[str, tuple[str, str, str]] = field(default_factory=dict)
    pins: dict[str, tuple[str, str, str, str]] = field(default_factory=dict)
    cells: dict[str, Cell] = field(default_factory=dict)

    def pin(self, cell: str, ref_pin: str, direction: str, net: str) -> None:
        """Connect pin `ref_pin` of `cell` to `net`."""
        self.pins[f"{cell}/{ref_pin}"] = (cell, ref_pin, direction, net)

    def drop(self, port: str) -> None:
        """Disconnect every cell built for `port`, before rebuilding it."""
        for name in [p for p, v in self.pins.items() if v[0].startswith(port)]:
            del self.pins[name]

    def blind(self, *pins: str) -> None:
        """Delete `pins`, so the query that asks for them answers nothing.

        This is how a netlist query that came back empty looks to the check:
        the structure the traversal needs is not there to be found.
        """
        for name in pins:
            del self.pins[name]

    def dangling_port(self, port: str, direction: str, iob: str) -> None:
        """A constrained port with no net and no buffer at all.

        How eth0_rx_er really places: the pin is read by nothing, so
        synthesis keeps no IBUF and `get_nets -of_objects` on the port
        answers nothing (probed on the AX7101 TDM8 placed checkpoint).
        """
        self.ports[port] = (direction, iob, "")

    def out_port(self, port: str, iob: str, driver: Cell) -> None:
        """An output port through an OBUF from `driver`."""
        buf, inner = f"{port}_OBUF_inst", f"{port}_OBUF"
        self.ports[port] = ("OUT", iob, port)
        self.cells[buf] = ("OBUF", f"IOB_{port}")
        self.pin(buf, "O", "OUT", port)
        self.pin(buf, "I", "IN", inner)
        self.cells[f"{port}_src"] = driver
        self.pin(f"{port}_src", "Q" if driver[0].startswith("FD") else "O",
                 "OUT", inner)

    def in_port(self, port: str, iob: str, loads: list[Cell],
                zhold: str = "") -> None:
        """An input port through an IBUF into `loads`.

        With a `zhold` site the IBUF feeds a ZHOLD_DELAY there and the loads
        hang off its DLYIFF output, which is how an ILOGIC input flop places.
        """
        buf, inner = f"{port}_IBUF_inst", f"{port}_IBUF"
        self.ports[port] = ("IN", iob, port)
        self.cells[buf] = ("IBUF", f"IOB_{port}")
        self.pin(buf, "I", "IN", port)
        self.pin(buf, "O", "OUT", inner)
        if zhold:
            dly = f"{port}_zhold"
            self.cells[dly] = ("ZHOLD_DELAY", zhold)
            self.pin(dly, "DLYIN", "IN", inner)
            self.pin(dly, "DLYIFF", "OUT", f"{port}_dly")
            inner = f"{port}_dly"
        for index, load in enumerate(loads):
            self.cells[f"{port}_dst{index}"] = load
            self.pin(f"{port}_dst{index}", "D" if load[0].startswith("FD")
                     else "I0", "IN", inner)

    def tcl(self) -> str:
        """The array assignments the stubs answer from.

        The whole variable name is braced, so a bus bit such as
        `eth0_rx_data[0]` is an array key and never a command substitution.
        """
        lines = []
        for name, (direction, iob, net) in self.ports.items():
            lines.append(f"set {{::PORT({name})}} "
                         f"{{DIRECTION {direction} IOB {{{iob}}} NET {{{net}}}}}")
        for name, (cell, ref_pin, direction, net) in self.pins.items():
            lines.append(f"set {{::PIN({name})}} {{CELL {cell} REF_PIN_NAME "
                         f"{ref_pin} DIRECTION {direction} NET {net}}}")
        for name, (ref, loc) in self.cells.items():
            seq = int(ref.startswith("FD"))
            lines.append(f"set {{::CELL({name})}} "
                         f"{{REF_NAME {ref} LOC {{{loc}}} IS_SEQUENTIAL {seq}}}")
        return "\n".join(lines) + "\n"


RX = "eth0_rx_data[0]"


def shipping() -> Netlist:
    """The AX7101 TDM8 shape as it places, every constrained port packed."""
    net = Netlist()
    net.out_port("tdm_bclk", "TRUE", ("FDRE", "OLOGIC_X0Y168"))
    net.out_port("tdm_fsync", "TRUE", ("FDSE", "OLOGIC_X0Y164"))
    net.out_port("tdm_dout", "TRUE", ("FDRE", "OLOGIC_X0Y167"))
    net.out_port("eth0_tx_en", "TRUE", ("FDRE", "OLOGIC_X0Y151"))
    net.in_port(RX, "TRUE", [("FDRE", "ILOGIC_X0Y120")], zhold="ILOGIC_X0Y120")
    # rx_er is constrained and read by nothing, so it keeps no net at all
    net.dangling_port("eth0_rx_er", "IN", "TRUE")
    # no IOB constraint: registers in slices, and the check must not care
    net.out_port("tdm_mclk", "", ("FDRE", "SLICE_X0Y170"))
    net.in_port("tdm_din", "FALSE", [("FDRE", "SLICE_X5Y16")])
    return net


def planted_out(port: str, driver: Cell) -> Netlist:
    """The shipping netlist with output `port` driven by `driver` instead."""
    net = shipping()
    net.drop(port)
    net.out_port(port, "TRUE", driver)
    return net


def planted_in(port: str, loads: list[Cell], zhold: str = "") -> Netlist:
    """The shipping netlist with input `port` read by `loads` instead."""
    net = shipping()
    net.drop(port)
    net.in_port(port, "TRUE", loads, zhold)
    return net


def rx_dv() -> Netlist:
    """eth0_rx_dv as the AX7101 build places it (dev ab823fe6, every seed).

    Its flop sits behind the ZHOLD_DELAY in the ILOGIC, and four LUTs in
    slices read the same pad through the ILOGIC bypass.
    """
    net = shipping()
    net.in_port("eth0_rx_dv", "TRUE", [("FDRE", "ILOGIC_X0Y119")],
                zhold="ILOGIC_X0Y119")
    for index, site in enumerate(("SLICE_X0Y122", "SLICE_X0Y122",
                                  "SLICE_X0Y49", "SLICE_X1Y49")):
        net.cells[f"eth0_rx_dv_lut{index}"] = ("LUT5", site)
        net.pin(f"eth0_rx_dv_lut{index}", "I0", "IN", "eth0_rx_dv_IBUF")
    return net


def inout() -> Netlist:
    """A bidirectional port carrying IOB TRUE, which the check does not model."""
    net = shipping()
    net.ports["eth0_mdio"] = ("INOUT", "TRUE", "eth0_mdio")
    net.cells["eth0_mdio_IOBUF_inst"] = ("IOBUF", "IOB_eth0_mdio")
    net.pin("eth0_mdio_IOBUF_inst", "IO", "INOUT", "eth0_mdio")
    return net


def blinded_out(port: str, pin: str) -> Netlist:
    """`port`'s register in a slice, and one hop of the traversal deleted.

    Without that hop every query about it answers nothing, which is what a
    query that ERRORED looked like while they all carried -quiet. The
    register is left unpacked, so only the traversal rule can catch it.
    """
    net = planted_out(port, ("FDRE", "SLICE_X1Y168"))
    net.blind(pin)
    return net


def blinded_in(port: str) -> Netlist:
    """`port`'s capture flop in the fabric, and nothing reading the pad net."""
    net = planted_in(port, [("FDRE", "SLICE_X0Y90")])
    net.blind(f"{port}_dst0/D")
    return net


def blinded_delay_in(port: str) -> Netlist:
    """`port`'s flop in a slice behind the delay, whose net answers no load.

    IBUF, ZHOLD_DELAY, capture flop is the shape every GMII RX input really
    takes, so the hop behind the delay element is the one this board's
    inputs are graded on: an empty answer there must fail exactly as an
    empty answer on the hop in front of it does.
    """
    net = planted_in(port, [("FDRE", "SLICE_X0Y120")], zhold="ILOGIC_X0Y120")
    net.blind(f"{port}_dst0/D")
    return net


def unconstrained() -> Netlist:
    """The shipping shape with every IOB property answering nothing."""
    net = shipping()
    for name, (direction, _iob, port_net) in list(net.ports.items()):
        net.ports[name] = (direction, "", port_net)
    return net


#: Three `set_property IOB TRUE` lines, as LiteX writes the generated .xdc
#: beside the report: what the build ASKED for, outside the netlist.
XDC_IOB_TRUE = """set_property IOSTANDARD LVCMOS33 [get_ports tdm_bclk]
set_property IOB TRUE [get_ports {eth0_tx_data[*]}]
set_property IOB TRUE [get_ports eth0_tx_en]
set_property IOB TRUE [get_ports tdm_bclk]
"""

#: The per-port IOB read answers nothing for tdm_bclk alone, the way a query
#: that errored answered under -quiet. The port drops out of the loop, and
#: only the second opinion (the same question as one filter) still sees it.
BLIND_ONE_IOB_READ = r"""
rename get_property kl_stub_real_get_property
proc get_property {args} {
    if {[lindex $args 0] eq "-quiet" && [lindex $args 1] eq "IOB"
        && [lindex $args 2] eq [kl_stub_obj tdm_bclk]} { return "" }
    return [kl_stub_real_get_property {*}$args]
}
"""

#: get_cells answers NAMES instead of objects, which is what `{*}` expansion
#: of an answer does to it live. Nothing downstream can pack a name back
#: into an object, so the next query raises Common 17-161 and the run ends -
#: the failure a real build hit, reproduced where tclsh can see it.
CELLS_ANSWER_NAMES = r"""
rename get_cells kl_stub_real_get_cells
proc get_cells {args} {
    set out {}
    foreach obj [kl_stub_real_get_cells {*}$args] {
        lappend out [kl_stub_name get_cells object $obj]
    }
    return $out
}
"""

#: REF_NAME answered for no cell, which is how Vivado answers an unknown or
#: renamed property: empty for `==` and for `!=` alike, with no warning and
#: no raise. Both halves of the check's delay partition then come back empty
#: while the loads are really there, so the flop below goes ungraded unless
#: the partition is required to account for every load.
BLIND_REF_NAME_FILTER = r"""
rename filter kl_stub_real_filter
proc filter {args} {
    lassign [lsearch -all -inline -not -exact $args -quiet] objs want
    if {[string match {*REF_NAME*} $want]} { return {} }
    return [kl_stub_real_filter {*}$args]
}
"""


@dataclass
class Arm:
    """One netlist, the exit status it must give, and the port it must name."""

    name: str
    netlist: Netlist
    status: int
    failed: str = ""
    rows: tuple[str, ...] = ()
    #: extra Tcl between the netlist and the check: a query made to answer
    #: nothing, which no netlist can express.
    twist: str = ""
    #: constraints written beside the report, for the rules that cross the
    #: netlist against what the build asked for.
    xdc: str = ""
    #: text the error must carry, where no single port is at fault.
    says: str = ""


ARMS = (
    Arm("shipping shape, all packed", shipping(), 0,
        rows=("PASS  tdm_bclk:", f"PASS  {RX}: IN, {RX}_dst0 (FDRE @ ILOGIC",
              "INERT eth0_rx_er:")),
    Arm("pruned render lane: tdm_dout from a constant",
        planted_out("tdm_dout", ("GND", "")), 0, rows=("INERT tdm_dout:",)),
    Arm("bclk pad flop left in a slice (fabric load, Place 30-722)",
        planted_out("tdm_bclk", ("FDRE", "SLICE_X1Y168")), 1, "tdm_bclk",
        ("FAIL  tdm_bclk: OUT, not in an OLOGIC site",)),
    Arm("fsync pad flop unplaced", planted_out("tdm_fsync", ("FDSE", "")),
        1, "tdm_fsync", ("FAIL  tdm_fsync:", "@ unplaced")),
    Arm("dout driven by a LUT, no register at all",
        planted_out("tdm_dout", ("LUT2", "SLICE_X2Y167")), 1, "tdm_dout",
        ("FAIL  tdm_dout:",)),
    Arm("rx capture flop in the fabric",
        planted_in(RX, [("FDRE", "SLICE_X0Y90")]), 1, RX,
        (f"FAIL  {RX}: IN, not in an ILOGIC site",)),
    Arm("rx capture flop in the fabric behind the ILOGIC delay",
        planted_in(RX, [("FDRE", "SLICE_X0Y120")], zhold="ILOGIC_X0Y120"), 1,
        RX, (f"FAIL  {RX}: IN, not in an ILOGIC site: {RX}_dst0",)),
    Arm("rx pin read by the IOB flop and a fabric flop",
        planted_in(RX, [("FDRE", "ILOGIC_X0Y90"), ("FDRE", "SLICE_X3Y90")]),
        1, RX, (f"FAIL  {RX}:",)),
    Arm("rx_dv as it places: ILOGIC flop plus four fabric LUTs", rx_dv(), 0,
        rows=("PASS  eth0_rx_dv: IN, eth0_rx_dv_dst0 (FDRE @ ILOGIC_X0Y119); "
              "also read by 4 fabric cell(s)",)),
    Arm("rx pin read only by LUTs, no register",
        planted_in(RX, [("LUT3", "SLICE_X0Y122")]), 1, RX,
        (f"FAIL  {RX}: IN, no register reads the pad, only:",)),
    Arm("bidirectional port", inout(), 1, "eth0_mdio",
        ("FAIL  eth0_mdio: direction INOUT",)),
    Arm("unpacked output, and the port's net answers no pin",
        blinded_out("tdm_bclk", "tdm_bclk_OBUF_inst/O"), 1, "tdm_bclk",
        ("FAIL  tdm_bclk: OUT, net tdm_bclk reaches no cell",)),
    Arm("unpacked output, and the pad buffer answers no data pin",
        blinded_out("tdm_bclk", "tdm_bclk_OBUF_inst/I"), 1, "tdm_bclk",
        ("FAIL  tdm_bclk: OUT, nothing answered behind tdm_bclk_OBUF_inst",)),
    Arm("unpacked input, and the pad buffer's net answers no load",
        blinded_in(RX), 1, RX,
        (f"FAIL  {RX}: IN, nothing answered behind {RX}_IBUF_inst",)),
    Arm("unpacked input behind the ILOGIC delay, whose net answers no load",
        blinded_delay_in(RX), 1, RX,
        (f"FAIL  {RX}: IN, nothing answered behind {RX}_IBUF_inst",)),
    Arm("unpacked output, and the pad buffer's net answers no driver",
        blinded_out("tdm_bclk", "tdm_bclk_src/Q"), 1, "tdm_bclk",
        ("FAIL  tdm_bclk: OUT, nothing answered behind tdm_bclk_OBUF_inst",)),
    Arm("unpacked input, and REF_NAME answers for no cell",
        planted_in(RX, [("FDRE", "SLICE_X0Y90")], zhold="ILOGIC_X0Y120"), 1,
        RX, (f"FAIL  {RX}: IN, nothing answered behind {RX}_IBUF_inst",),
        twist=BLIND_REF_NAME_FILTER),
    Arm("unpacked output whose IOB read answers nothing: it leaves the loop",
        planted_out("tdm_bclk", ("FDRE", "SLICE_X1Y168")), 1,
        twist=BLIND_ONE_IOB_READ, xdc=XDC_IOB_TRUE,
        says="did not read the same way twice"),
    Arm("no port answers IOB TRUE, but the constraints carry it",
        unconstrained(), 1, xdc=XDC_IOB_TRUE,
        says="no port answered IOB TRUE"),
    Arm("no port answers IOB TRUE, and no .xdc sits beside the report",
        unconstrained(), 1, says="no .xdc file sits beside it"),
    Arm("a query answers names, not objects: the next one raises",
        shipping(), 1, twist=CELLS_ANSWER_NAMES,
        says="Invalid option value"),
)

#: (name, original text, replacement): each must make some arm stop holding.
MUTANTS = (
    ("site test always true", '![string match "${site}_*" $loc]', "0"),
    ("final error removed", '        error "IOB-PACK FAIL:',
     '        puts "IOB-PACK FAIL:'),
    ("delay elements not looked through",
     "[filter $loads {REF_NAME == ZHOLD_DELAY || REF_NAME == IDELAYE2}]",
     "{}"),
    ("a port whose net reaches no cell taken for INERT",
     'return [list FAIL "$dir, net [join $nets {, }] reaches no cell',
     'return [list INERT "$dir, net [join $nets {, }] reaches no cell'),
    ("a far side that answered nothing taken for INERT",
     'return [list FAIL "$dir, nothing answered behind',
     'return [list INERT "$dir, nothing answered behind'),
    ("the two counts of constrained ports not crossed",
     "[llength $rows] != [llength $constrained]", "0"),
    ("a run that selected no port taken for a clean one",
     "[llength $rows] == 0 && $lines != 0", "0"),
    ("every input load taken for a register",
     "![string is true -strict [get_property IS_SEQUENTIAL $cell]]", "0"),
    ("an input with no register taken for INERT",
     "[llength $regs] == 0 && [llength $logic] == 0", "[llength $regs] == 0"),
    ("an empty answer behind a delay element taken for reached",
     "if {!$reached || [llength $behind] == 0} {", "if {!$reached} {"),
    ("the delay partition not made to account for every load",
     "[llength $delays] + [llength $direct] != [llength $loads]", "0"),
    ("an output pin whose net answers no driver taken for reached",
     "if {!$reached || [llength $cells] == 0} {", "if {!$reached} {"),
    ("an output parked by a constant taken for untraversable",
     '$dir eq "OUT" && [llength $fixed] > 0', "0"),
    ("a missing .xdc taken for a constraint-free build",
     "        return -1", "        return 0"),
    ("-quiet back on the port's net query", "set nets [get_nets -of_objects $port]",
     "set nets [get_nets -quiet -of_objects $port]"),
    ("a per-pin answer taken apart and rebuilt", "lappend groups $cells",
     "lappend groups {*}$cells"),
    ("the same rebuild spelled with eval", "lappend groups $cells",
     "eval lappend groups [list $cells]"),
    ("the same rebuild spelled with lmap", "lappend groups $cells",
     "set groups [lmap g [concat $groups [list $cells]] {set g}]"),
    ("the same rebuild spelled with join and split", "lappend groups $cells",
     "lappend groups [split [join $cells] { }]"),
    ("a query that raised while grading a port taken for INERT",
     'error "IOB-PACK ERROR: grading $port ended the run: $answer"',
     'set answer [list INERT "the query raised"]'),
)

PORTS = ("tdm_bclk", "tdm_fsync", "tdm_dout", "tdm_mclk", "tdm_din",
         "eth0_tx_en", RX, "eth0_rx_er", "eth0_rx_dv", "eth0_mdio")


def run_arm(tclsh: str, check: Path, arm: Arm, work: Path) -> list[str]:
    """Run one arm against `check`; return what did not hold (empty = held)."""
    report = work / "iob_pack.rpt"
    report.unlink(missing_ok=True)
    xdc = work / "arm.xdc"
    xdc.unlink(missing_ok=True)
    if arm.xdc:
        xdc.write_text(arm.xdc, encoding="utf-8")
    driver = work / "arm.tcl"
    driver.write_text(
        STUBS + arm.netlist.tcl() + arm.twist + f"source {{{check}}}\n"
        f"if {{[catch {{kl_iob_pack_check {{{report}}}}} msg]}} "
        "{ puts stderr $msg; exit 1 }\nexit 0\n", encoding="utf-8")
    proc = subprocess.run([tclsh, str(driver)], capture_output=True, text=True,
                          check=False)
    # what the check printed, with the stub's object marker taken back off:
    # live, an object prints as its bare name.
    stderr = proc.stderr.replace(OBJ, "")
    problems = []
    if proc.returncode != arm.status:
        problems.append(f"exit {proc.returncode}, want {arm.status}: "
                        f"{stderr.strip() or proc.stdout.replace(OBJ, '').strip()}")
    if arm.failed:
        named = [p for p in PORTS if f" {p}." in stderr or f" {p}," in stderr]
        if named != [arm.failed]:
            problems.append(f"error names {named}, want [{arm.failed!r}]")
    if arm.says and arm.says not in stderr:
        problems.append(f"error does not say {arm.says!r}: "
                        f"{stderr.strip()!r}")
    text = (report.read_text(encoding="utf-8").replace(OBJ, "")
            if report.is_file() else "")
    problems += [f"report lacks {row!r}" for row in arm.rows if row not in text]
    problems += [f"report looks at {p}, which carries no IOB constraint"
                 for p in ("tdm_mclk", "tdm_din") if f" {p}:" in text]
    return problems


def quiet_reads(source: str) -> list[str]:
    """The `-quiet` reads the check's code lines carry: exactly one is right.

    The stubs ignore the flag, so no arm notices it coming back to a netlist
    query, while the one verdict that does not fail the build rests on those
    queries answering an absence rather than a failure.
    """
    code = [line for line in source.splitlines()
            if not line.lstrip().startswith("#")]
    found = sum(line.count("-quiet") for line in code)
    if found == 1:
        return []
    return [f"the check carries {found} -quiet read(s) in its code lines, "
            "want exactly one (the per-port IOB property)"]


#: Tcl spellings MEASURED on the placed checkpoint under 2026.1 to hand a
#: Vivado query answer back as plain names, with the number of times each may
#: stand in the check's code lines. `split` is allowed once: the report text
#: cut into lines, which is no query answer.
REBUILD_FORMS = (
    ("{*}", re.compile(r"\{\*\}"), 0),
    ("eval", re.compile(r"(?<![\w$])eval(?!\w)"), 0),
    ("lmap", re.compile(r"(?<![\w$])lmap(?!\w)"), 0),
    ("split", re.compile(r"(?<![\w$])split(?!\w)"), 1),
)


def rebuilt_answers(source: str) -> list[str]:
    """The measured spellings that rebuild a query answer by value.

    Measured on the placed checkpoint under 2026.1: `foreach`, `lindex`,
    `lassign`, `lsort`, `lrange`, `lreverse`, `filter`, `concat`, and
    `lappend` of a whole answer or of elements taken out of it, all keep a
    Vivado object list's objects; `{*}` expansion (`list {*}` included),
    `eval lappend`, `lmap` over an answer, and `join` then `split` all hand
    back plain NAMES, the next query raises Common 17-161, and the check
    re-raises it uncaught, so the build stops at this check. No Tcl value
    carries that difference, so no stub here can see it - a marked object
    survives every one of them in tclsh. The check's code lines are read for
    the spellings instead. The list is what was measured, not a closure:
    another spelling of the same rebuild passes here, and only the live run
    stops it.
    """
    code = [line for line in source.splitlines()
            if not line.lstrip().startswith("#")]
    problems = []
    for form, pattern, allowed in REBUILD_FORMS:
        lines = [line.strip() for line in code if pattern.search(line)]
        if len(lines) > allowed:
            problems.append(
                f"the check carries `{form}` on {len(lines)} code line(s), "
                f"want at most {allowed}: {lines!r}. A Vivado object list is "
                "passed whole or not at all; rebuilt by value, its elements "
                "come back as names the next query rejects")
    return problems


def mutant_arms(tclsh: str, work: Path) -> list[str]:
    """Every mutant must be noticed: by an arm, or by one of the two counts."""
    failures = []
    source = CHECK_TCL.read_text(encoding="utf-8")
    for name, old, new in MUTANTS:
        if source.count(old) != 1:
            failures.append(f"mutant '{name}': its target text is not in the "
                            "check exactly once")
            continue
        mutant = work / "mutant.tcl"
        text = source.replace(old, new)
        mutant.write_text(text, encoding="utf-8")
        caught = [a.name for a in ARMS if run_arm(tclsh, mutant, a, work)]
        caught += ["the -quiet count"] if quiet_reads(text) else []
        caught += ["the rebuild count"] if rebuilt_answers(text) else []
        print(f"  [{'KILL' if caught else 'LIVE'}] mutant '{name}': "
              f"{len(caught)} check(s) notice it")
        if not caught:
            failures.append(f"mutant '{name}' survives every arm")
    return failures


def main() -> int:
    """Run every arm and every mutant; exit 0 only if all held."""
    tclsh = shutil.which("tclsh")
    if tclsh is None:
        print("iob_pack_selftest: tclsh not found (install the `tcl` package)",
              file=sys.stderr)
        return 2
    source = CHECK_TCL.read_text(encoding="utf-8")
    failures = quiet_reads(source)
    print(f"  [{'FAIL' if failures else 'PASS'}] one -quiet read in the "
          "check's code lines")
    rebuilt = rebuilt_answers(source)
    print(f"  [{'FAIL' if rebuilt else 'PASS'}] no measured rebuild of a query "
          "answer in the check's code lines")
    failures += rebuilt
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for arm in ARMS:
            problems = run_arm(tclsh, CHECK_TCL, arm, work)
            print(f"  [{'FAIL' if problems else 'PASS'}] {arm.name}")
            failures += [f"{arm.name}: {p}" for p in problems]
        failures += mutant_arms(tclsh, work)
    for failure in failures:
        print(f"iob_pack_selftest: {failure}", file=sys.stderr)
    print(f"iob_pack_selftest: {len(ARMS)} arms, {len(MUTANTS)} mutants, "
          f"{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

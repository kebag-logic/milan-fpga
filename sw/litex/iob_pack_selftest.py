#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive sw/litex/iob_pack_check.tcl's verdicts without Vivado (issue #475).

The check runs only inside a Vivado build, after placement, so nothing else
would notice if it stopped failing. This script sources THE REAL .TCL in
`tclsh` with the five Vivado netlist queries it uses (get_ports, get_nets,
get_pins, get_cells, get_property) stubbed over a small placed netlist, one
netlist per arm. The netlists copy what Vivado placed for the AX7101 TDM8
build: an output flop in an OLOGIC, and an input flop in an ILOGIC behind the
ZHOLD_DELAY that opt_design inserts in front of it.

  - the shipping shape, every constrained port packed: exit 0, and tdm_mclk /
    tdm_din, which carry no IOB constraint, are never looked at even though
    their registers sit in slices;
  - a pruned render lane (tdm_dout driven by a constant) and an input nothing
    reads: INERT, exit 0;
  - eth0_rx_dv as it places: its flop in the ILOGIC and four fabric LUTs
    reading the same pad. PASS: the register packed, and the LUTs are
    counted in the line, not failed;
  - one planted defect per arm - the bclk pad flop left in a slice (the
    fabric-load case Place 30-722 reports), an unplaced flop, a LUT on the
    pad, an input flop in the fabric with and without the ILOGIC delay in
    front of it, an input read by a second fabric flop, an input read only
    by LUTs, and a bidirectional port: exit 1, the error names exactly that
    port and the report carries its FAIL row.

Every mutant of the .tcl in MUTANTS must then make at least one arm stop
holding, which is what shows the arms can fail for the defects they name.
Needs `tclsh` (package `tcl`); exits 2 without it.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

CHECK_TCL = Path(__file__).resolve().parent / "iob_pack_check.tcl"

#: The Vivado queries the check uses, answered from the ::PORT, ::PIN and
#: ::CELL arrays each arm fills in. A pin's net is its NET field; a net is
#: nothing but the name its pins and its port share.
STUBS = r"""
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
proc get_ports {args} { return [lsort [array names ::PORT]] }
proc get_property {args} {
    set argv [lsearch -all -inline -not -exact $args -quiet]
    lassign $argv key obj
    foreach arr {::PORT ::PIN ::CELL} {
        if {[info exists ${arr}($obj)]} {
            set d [set ${arr}($obj)]
            if {[dict exists $d $key]} { return [dict get $d $key] }
            return ""
        }
    }
    error "stub get_property: no object '$obj'"
}
proc get_nets {args} {
    lassign [kl_stub_args $args] of
    set out {}
    foreach o $of {
        if {[info exists ::PORT($o)]} { lappend out [dict get $::PORT($o) NET] }
        if {[info exists ::PIN($o)]} { lappend out [dict get $::PIN($o) NET] }
    }
    return [lsort -unique $out]
}
proc get_pins {args} {
    lassign [kl_stub_args $args] of filter
    set out {}
    foreach p [array names ::PIN] {
        set d $::PIN($p)
        if {[dict get $d NET] in $of || [dict get $d CELL] in $of} {
            lappend out $p
        }
    }
    if {$filter eq ""} { return [lsort $out] }
    return [filter [lsort $out] $filter]
}
proc get_cells {args} {
    lassign [kl_stub_args $args] of
    set out {}
    foreach p $of { lappend out [dict get $::PIN($p) CELL] }
    return [lsort -unique $out]
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
                         f"{{DIRECTION {direction} IOB {{{iob}}} NET {net}}}")
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
    # rx_er is constrained and read by nothing: no register, nothing to pack
    net.in_port("eth0_rx_er", "TRUE", [])
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


@dataclass
class Arm:
    """One netlist, the exit status it must give, and the port it must name."""

    name: str
    netlist: Netlist
    status: int
    failed: str = ""
    rows: tuple[str, ...] = ()


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
)

#: (name, original text, replacement): each must make some arm stop holding.
MUTANTS = (
    ("site test always true", '![string match "${site}_*" $loc]', "0"),
    ("final error removed", '        error "IOB-PACK FAIL:',
     '        puts "IOB-PACK FAIL:'),
    ("delay elements not looked through",
     "[filter -quiet $loads {REF_NAME == ZHOLD_DELAY || REF_NAME == IDELAYE2}]",
     "{}"),
    ("every input load taken for a register",
     "![string is true -strict [get_property IS_SEQUENTIAL $cell]]", "0"),
    ("an input with no register taken for INERT",
     "[llength $regs] == 0 && [llength $logic] == 0", "[llength $regs] == 0"),
)

PORTS = ("tdm_bclk", "tdm_fsync", "tdm_dout", "tdm_mclk", "tdm_din",
         "eth0_tx_en", RX, "eth0_rx_er", "eth0_rx_dv", "eth0_mdio")


def run_arm(tclsh: str, check: Path, arm: Arm, work: Path) -> list[str]:
    """Run one arm against `check`; return what did not hold (empty = held)."""
    report = work / "iob_pack.rpt"
    report.unlink(missing_ok=True)
    driver = work / "arm.tcl"
    driver.write_text(
        STUBS + arm.netlist.tcl() + f"source {{{check}}}\n"
        f"if {{[catch {{kl_iob_pack_check {{{report}}}}} msg]}} "
        "{ puts stderr $msg; exit 1 }\nexit 0\n", encoding="utf-8")
    proc = subprocess.run([tclsh, str(driver)], capture_output=True, text=True,
                          check=False)
    problems = []
    if proc.returncode != arm.status:
        problems.append(f"exit {proc.returncode}, want {arm.status}: "
                        f"{proc.stderr.strip() or proc.stdout.strip()}")
    if arm.failed:
        named = [p for p in PORTS if f" {p}." in proc.stderr
                 or f" {p}," in proc.stderr]
        if named != [arm.failed]:
            problems.append(f"error names {named}, want [{arm.failed!r}]")
    text = report.read_text(encoding="utf-8") if report.is_file() else ""
    problems += [f"report lacks {row!r}" for row in arm.rows if row not in text]
    problems += [f"report looks at {p}, which carries no IOB constraint"
                 for p in ("tdm_mclk", "tdm_din") if f" {p}:" in text]
    return problems


def mutant_arms(tclsh: str, work: Path) -> list[str]:
    """Every mutant must be caught: some arm must stop holding under it."""
    failures = []
    source = CHECK_TCL.read_text(encoding="utf-8")
    for name, old, new in MUTANTS:
        if source.count(old) != 1:
            failures.append(f"mutant '{name}': its target text is not in the "
                            "check exactly once")
            continue
        mutant = work / "mutant.tcl"
        mutant.write_text(source.replace(old, new), encoding="utf-8")
        caught = [a.name for a in ARMS if run_arm(tclsh, mutant, a, work)]
        print(f"  [{'KILL' if caught else 'LIVE'}] mutant '{name}': "
              f"{len(caught)} arm(s) notice it")
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
    failures = []
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

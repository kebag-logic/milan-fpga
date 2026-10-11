#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""publication_census.py - every class-D value of the processor, followed through the elaborated datapath.

THE QUESTION. In the split placement the fabric datapath no longer has the
protocol processor: the firmware owns ADP, ACMP, MAAP and SRP and writes what
the datapath consumes into the mailbox's publication block (#665, ruling
6088423771, decision 2 (a)). Which values the block must carry is decided by
what ``hdl/milan/milan_datapath.sv`` reads, and a list copied by hand missed
two of them (#665, comment 6092086337). This check derives the list from the
datapath every time, in every shape the builder builds, and fails closed
(#665, comments 6094461419 and 6100024293).

THE NETLIST, not the text (#665, comment 6097292237). census_elab.py
elaborates the datapath with the recipe, the sv2v and the Yosys of CI's
elaboration gate, every other module a blackbox cell, its processes turned
into cells by the passes ``proc`` runs (``insbuf`` before each that would
rename a read, the closing ``opt_expr`` left out, as census_elab.py says), and
reads the netlist back.

THE SHAPES. ``--check`` elaborates the recipe's own shape (run.sh's
milan_datapath row: the module's default parameters, define ``SYNTHESIS``,
the all-fabric header ``configs/generated/endstation_arty_current``) and the
shape of every ``configs/*.yaml``: its generated header directory, the
integer parameters ``endstation_builder.datapath_params()`` states for it,
which test_builder gate 23m holds to the Instance milan_soc.py builds, and
``SYNTHESIS``. Today that is endstation_arty_4x4, _arty_8ch, _arty_current,
_ax7101_1x1_tdm8 and _ax7101_8x8, from one to eight streams, with and without
the loopback lane and the optional blocks; a configuration the builder gains
is elaborated with no edit here. Each shape is censused on its own, and then
the shapes are compared: a generate branch one shape builds is in that
shape's netlist, and a read it holds is found there.

The census follows values through each netlist alone, so how a read is written (a
procedural block with or without ``begin``, a case label, a compound
assignment, an event control, a function, a port connected by position or by
``.name``, a macro, an escaped name) does not matter: what the elaborator
built is what is counted. A form the front end or the elaborator refuses is
refused, and so is an escaped name holding ``//`` or ``/*``, which sv2v reads
as a comment (census_elab.py says why).

THE POPULATION is the nets the processor wrapper cell's class-D output ports
drive. ``CLASS_D_PORTS`` lists that face and must equal the outputs the
wrapper declares under its class-D sections: the elaborated wrapper names its
outputs, and its port list places each under a section heading, so a port
added to, renamed in or moved out of the face fails until it is reviewed here.
``aecp_strm_started_o``, each sink's started level, joins them by the ruling
of comment 6092086337. The datapath must hold one ``KL_pp_shadow`` cell, named
``pp_shadow``. Each of these ports must drive one whole named net that no
other port drives, and be that net's only driver: a port left unconnected, a
port driving part of a net or more than one, and a second driver of the net
(an ``assign``, a declaration's initialiser, another cell's output) fail. No
bit of the datapath may have two drivers.

THE READS. From a population net's bits the census follows every cell they
enter (a buffer for an assignment, an operator, a multiplexer, a flop, a
latch, any cell the elaborator produced) to the bits that cell drives, until
it reaches a net with a name the source gave it. That net is the read's
consumer; an instance's input port reached first makes ``instance.port`` the
consumer. A read is keyed by (population net, consumer).

THE CONE of a read is everything its consumer's bits reach, followed through
every cell the same way, named nets included. A cell leads from each of its
input bits to every one of its output bits, so no cell's function is trusted
to drop a dependency, and a memory's write leads to its reads. Each end is:

  csr        an input port of the CSR cell ``csr`` that ``CSR_READBACK`` names
  processor  an input port of the wrapper cell ``pp_shadow`` that
             ``PROCESSOR_FACE`` names, its GET_STREAM_INFO and GET_AVB_INFO
             answer face
  the wire   any other input port of any cell, those two included, any
             datapath output, and a cell with no output (a print or an
             assertion)

So a terminal is a cell and a port, never a port's name, and a path the
census cannot rule out reaches the wire.

THE CENSUS. ``CENSUS`` names every read once:

  field      the read reaches the wire; the block field that carries the
             value in the split placement, which the contract must define
  status     the read reaches CSR read-back only, through the ports
             ``CSR_READBACK`` lists (a field may be named: published anyway)
  processor  the read reaches the wrapper's own GET_STREAM_INFO face only
             (``PROCESSOR_FACE``), which needs no publication (ruling
             6088423771, decision 2): F5's AECP owner answers GET_STREAM_INFO
             and GET_AVB_INFO from firmware state, a STREAM_INPUT's binding,
             started and registration fields from the ACMP view
             (sw/firmware/ctrl/app/ctrl_app_aecp.c) and the rest through its
             platform's stream and avb ports, none from the block

and fails, in any shape, on a read the census does not name, a row no read
matches, a status or processor read whose cone reaches the wire, a status read
whose cone reaches the processor wrapper, a field read whose cone does not
reach the wire, and a field the contract does not define. Across the shapes it
fails on a population, an unread net, a read or a read's classes of cone end
(wire, CSR read-back, the processor's face) that is not the same in every
shape. Which CSR input or which instance's input a cone ends at may differ:
from four streams up, the AAF stream gate also reaches the CSR read-back
input ``i_tlk_lobs_v``.

    python3 sw/mailbox/publication_census.py --check --jobs 4
    python3 sw/mailbox/publication_census.py --list
    python3 sw/mailbox/publication_census.py --selftest --jobs 4

THE RULES. census_rules.py names every rule above, the shapes' and the
tools' included, and each is enforced only where ``live()`` names it.

``--selftest`` (census_selftest.py) elaborates a planted copy of the datapath,
the wrapper or an included file for each defect of ``census_plants.PLANTS``,
at a shape that builds the plant's branch, and requires each to be refused by
its own words: every reviewer probe of review rounds 2 to 5 of #665 that
escaped the census, each beside its plain-assign control, the census's own
defects, every wrong connection of the wrapper's class-D face, the forms the
front end refuses, and a plant for each rule. The tracked sources, and a copy
whose only change is a comment naming a class-D wire, must pass. Then it
removes each rule in turn and requires every arm planted against it to be
accepted.
"""

from __future__ import annotations

import argparse
import multiprocessing
import re
import sys
import time
from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mailbox_model  # noqa: E402
from census_elab import (REPO, RECIPE, WORK, Cell, CensusError, Netlist, Shape, elaborate,  # noqa: E402
                         recipe, shapes, toolchain)
from census_rules import live  # noqa: E402

DATAPATH = REPO / "hdl/milan/milan_datapath.sv"
WRAPPER_SV = REPO / "hdl/milan/KL_pp_shadow.sv"

WRAPPER = "KL_pp_shadow"
CSR = "milan_csr"
#: The two cells whose named ports end a cone, by instance name.
WRAPPER_CELL = "pp_shadow"
CSR_CELL = "csr"
#: The wrapper's class-D face: each a 1:1 pass-through of protocol_processor_top's own output.
CLASS_D_PORTS = frozenset({
    "srp_class_a_prio_o", "srp_class_a_vid_o", "srp_domain_adopted_o", "srp_domain_change_o",
    "srp_tk_decl_state_o", "srp_lstn_reg_state_o", "srp_active_o", "srp_sr_admitted_o",
    "srp_granted_slope_bps_o", "srp_src_fail_code_o", "srp_src_fail_bridge_o", "srp_sum_slope_bps_o",
    "srp_over_limit_o", "srp_tk_reg_state_o", "srp_lstn_decl_state_o", "srp_acc_latency_o",
    "srp_snk_fail_code_o", "acmp_declaring_o", "acmp_bound_o", "acmp_bound_eid_o", "acmp_bound_sid_o",
    "acmp_bound_dmac_o", "acmp_bound_vlan_o", "adp_next_avail_index_o",
})
#: Each sink's started level, which the ruling of comment 6092086337 adds, and the wire the rows name it by.
STARTED_PORT = "aecp_strm_started_o"
STARTED = "pp_aecp_strm_started_w"


@dataclass(frozen=True)
class Row:
    """How one read of a class-D wire is accounted for."""

    kind: str          # "field", "status" or "processor"
    field: str         # REGISTER.FIELD of the publication block, or ""
    why: str


#: (wire, consumer) -> Row. The consumer is the named net the read drives, or
#: instance.port.
CENSUS: dict[tuple[str, str], Row] = {
    # ---- read on the wire: carried by the publication block -----------------
    ("pp_cd_acmp_declaring_w", "acmp_talker_active_v"):
        Row("field", "DA_GATE.OPEN", "the AAF talker admission gate; DA validity only, see the design page's "
            "choices (#665, comment 6092086337)"),
    ("pp_cd_srp_active_w", "lwsrp_stream_gate"):
        Row("field", "LICENCE.ACTIVE", "the SRP stream gate of the AAF and CRF talkers"),
    ("pp_cd_srp_sr_admitted_w", "lwsrp_stream_gate"):
        Row("field", "LICENCE.ACTIVE", "the SRP stream gate of the AAF and CRF talkers"),
    ("pp_cd_srp_class_a_prio_w", "lwsrp_op_prio"):
        Row("field", "SR_DOMAIN.PRIORITY", "the C-TAG PCP of the AAF and CRF talkers"),
    ("pp_cd_srp_class_a_vid_w", "lwsrp_op_vid"):
        Row("field", "SR_DOMAIN.VID", "the C-TAG VID of the AAF and CRF talkers"),
    ("pp_cd_srp_domain_adopted_w", "lwsrp_adopt_valid"):
        Row("field", "SR_DOMAIN.ADOPTED", "selects the adopted Domain for the C-TAG"),
    ("pp_cd_srp_tk_decl_state_w", "crft_class_a_w"):
        Row("field", "TALKER_DECL.DECLARED", "the CRF talker's C-TAG enable (802.1Q 35.1.2)"),
    ("pp_cd_acmp_bound_w", "acmpl_bound_v_w"):
        Row("field", "BINDING.BOUND", "the listener accept, the stream table and the CRF sink"),
    ("pp_cd_acmp_bound_sid_w", "acmpl_sid_v_w"):
        Row("field", "SID_LO.SID", "the stream table's and the CRF sink's stream_id, with SID_HI and "
            "BINDING.SID_VALID"),
    (STARTED, "acmpl_stopped_v_w"):
        Row("field", "BINDING.STARTED", "the listener accept and the CRF sink's stop (Milan v1.2 5.3.8.7)"),
    # ---- read back as CSR status only --------------------------------------
    ("pp_cd_srp_sum_slope_bps_w", "lwsrp_idle_slope"):
        Row("status", "IDLE_SLOPE.BPS", "LWSRP_SLOPE; no shaper consumes it, published as ruled"),
    ("pp_cd_srp_active_w", "lwsrp_res_active"): Row("status", "", "LWSRP_STATUS"),
    ("pp_cd_srp_sr_admitted_w", "lwsrp_slope_en"): Row("status", "", "LWSRP_STATUS"),
    ("pp_cd_srp_domain_adopted_w", "lwsrp_domain_ok"): Row("status", "", "LWSRP_STATUS"),
    ("pp_cd_srp_over_limit_w", "lwsrp_over_limit"): Row("status", "", "LWSRP_STATUS"),
    ("pp_cd_srp_src_fail_code_w", "lwsrp_tfail_code"): Row("status", "", "LWSRP_STATUS"),
    ("pp_cd_srp_src_fail_code_w", "lwsrp_tfail_valid"): Row("status", "", "LWSRP_STATUS"),
    ("pp_cd_srp_tk_decl_state_w", "lwsrp_talker_declared"): Row("status", "", "LWSRP_STATUS"),
    ("pp_cd_srp_lstn_reg_state_w", "lwsrp_lstn_reg0_w"):
        Row("status", "", "LWSRP_STATUS and the snapshot window's listener-observed bit"),
    ("pp_cd_srp_tk_reg_state_w", "lwsrp_ta_registered"): Row("status", "", "ACMPL_STATE"),
    ("pp_cd_srp_snk_fail_code_w", "lwsrp_ta_failed"): Row("status", "", "ACMPL_STATE"),
    ("pp_cd_srp_snk_fail_code_w", "lwsrp_ta_fail_code"): Row("status", "", "ACMPL_TUID"),
    ("pp_cd_acmp_bound_vlan_w", "acmpl_vlan_w"): Row("status", "", "ACMPL_STATE"),
    ("pp_cd_adp_avail_index_w", "adp_available_index"): Row("status", "", "ADP_STATUS"),
    # ---- the wrapper's own GET_STREAM_INFO face -----------------------------
    ("pp_cd_acmp_bound_w", "gsi_bnd_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_acmp_bound_sid_w", "gsi_sid_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_acmp_bound_dmac_w", "gsi_ans_raw_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_acmp_bound_vlan_w", "gsi_ans_raw_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_acmp_declaring_w", "gsi_decl_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_tk_reg_state_w", "gsi_tkreg_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_lstn_reg_state_w", "gsi_lreg_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_tk_decl_state_w", "gsi_tkdcl_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_acc_latency_w", "gsi_ans_raw_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_src_fail_code_w", "gsi_ans_raw_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_src_fail_bridge_w", "gsi_ans_raw_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_class_a_vid_w", "gsi_ans_raw_w"): Row("processor", "", "GET_STREAM_INFO"),
    ("pp_cd_srp_class_a_prio_w", "gsi_prio_snap_r"): Row("processor", "", "GET_AVB_INFO's Domain snapshot"),
    ("pp_cd_srp_class_a_vid_w", "gsi_vid_snap_r"): Row("processor", "", "GET_AVB_INFO's Domain snapshot"),
    (STARTED, "gsi_flags_w"): Row("processor", "", "GET_STREAM_INFO, Milan v1.2 Table 5.9 bit 28"),
}

#: The CSR block's inputs the status reads reach: each is read back through
#: milan_csr's live register mux or its 0x800 snapshot window, never into
#: anything that leaves the station.
CSR_READBACK = frozenset({
    "i_lwsrp_status", "i_lwsrp_slope", "i_lwsrp_dom", "i_acmpl_state", "i_acmpl_tuid", "i_tlk_lobs_v",
    "i_adp_available_index", "i_crft_stat",
})

#: The wrapper's GET_STREAM_INFO and GET_AVB_INFO answer face: its answer
#: data, the wait it holds, and the change strobes behind its notifications.
PROCESSOR_FACE = frozenset({"gsi_data_i", "gsi_wait_i", "gsi_avb_chg_i", "gsi_asp_chg_i"})

#: A section heading of the wrapper's port list, `//! ---- title ----`.
SECTION = re.compile(r"^[ \t]*//!?[ \t]*-{4}[ \t]*(.*?)[ \t]*-{4,}[ \t]*$")
NAME = re.compile(r"(?<![\w$\\])[A-Za-z_][\w$]*")
#: The Yosys memory cells that write: each leads to the cells reading its memory.
MEM_WRITES = ("$memwr", "$meminit")
#: The inputs of a Yosys cell that select, enable, clock or reset rather than
#: carry a value; each leads to the cell's outputs like any other.
CONTROL_PORTS = frozenset({"S", "EN", "CLK", "ARST", "SRST", "CLR", "SET"})
INCLUDE = re.compile(r"`include\s+\"([^\"]+)\"")


@dataclass(frozen=True)
class Sources:
    """What the census elaborates: the datapath, the wrapper, and every copy of each
    file the datapath includes, the one the front end reads first."""

    datapath: str
    wrapper: str
    included: dict[str, tuple[tuple[str, str], ...]]


@dataclass(frozen=True)
class Read:
    """One (wire, consumer) read and the ends of its cone."""

    wire: str
    consumer: str
    ends: frozenset[tuple[str, str]]


@dataclass
class Survey:
    """One shape's census: the population, its reads, the nets nothing reads, every
    way the netlist breaks the census's rules, and the netlist's size."""

    population: dict[str, str]
    reads: list[Read]
    unread: list[str]
    problems: list[str]
    size: str
    shape: str = RECIPE.name


@dataclass
class Flow:
    """The netlist as edges: where each bit leads, what drives it, and each cell's output bits."""

    net: Netlist
    fanout: dict[int, list[tuple[str, ...]]]
    drivers: dict[int, list[tuple[str, str]]]   # bit -> (cell, port), or ("", port) for a datapath input
    outs: dict[str, tuple[int, ...]]
    readers: dict[str, list[str]]        # a memory -> the cells reading it


def edge_of(name: str, c: Cell, dirs: dict[str, str]) -> tuple[str, str] | None:
    """Where a bit entering cell c leads: a memory write to that memory's reads, a
    Yosys cell with an output to all its output bits; None for an instance's port
    or a cell with no output, which ends the path."""
    if c.memid and c.kind.startswith(MEM_WRITES):
        return "mem", c.memid
    if c.kind.startswith("$") and any(d != "input" for d in dirs.values()):
        return "cell", name
    return None


def flow(net: Netlist) -> Flow:
    """Every edge of the netlist. A Yosys cell ($...) with an output leads from each
    input bit to all its output bits; a memory write leads to the memory's reads;
    an instance's input port, a datapath output and a cell with no output end a path."""
    fl = Flow(net, defaultdict(list), defaultdict(list), {}, defaultdict(list))
    every = live("every-input")
    for name, c in net.cells.items():
        dirs = {p: c.dirs.get(p, "inout") for p in c.conns}       # an unknown direction is both
        fl.outs[name] = tuple(b for p, bits in c.conns.items() if dirs[p] != "input" for b in bits
                              if isinstance(b, int))
        if c.memid and c.kind.startswith("$mem") and not c.kind.startswith(MEM_WRITES):
            fl.readers[c.memid].append(name)
        edge = edge_of(name, c, dirs)
        for p, bits in c.conns.items():
            for b in (b for b in bits if isinstance(b, int)):
                if dirs[p] != "input":
                    fl.drivers[b].append((name, p))
                if dirs[p] != "output" and (every or not edge or p not in CONTROL_PORTS):
                    fl.fanout[b].append(edge or ("pin", name, p))
    for p, (d, bits) in net.ports.items():
        for b in (b for b in bits if isinstance(b, int)):
            if d != "output":
                fl.drivers[b].append(("", p))
            if d != "input":
                fl.fanout[b].append(("out", p))
    return fl


def step(fl: Flow, bit: int) -> list[tuple[str, ...]]:
    """Where one bit leads: ("bit", b) for each bit a cell drives from it, else the end it reaches."""
    out = []
    for e in fl.fanout.get(bit, ()):
        if e[0] == "cell":
            out += [("bit", o) for o in fl.outs[e[1]]]
        elif e[0] == "mem":
            out += [("bit", o) for r in fl.readers.get(e[1], ()) for o in fl.outs[r]] if live("memory") else []
        else:
            out.append(e)
    return out


def named(net: Netlist, bit: int) -> str:
    """The name the source gave the net a bit belongs to, or "" for one the elaborator made."""
    name = net.bit_name[bit][0]
    return "" if name in net.hidden else name


def terminal(net: Netlist, end: tuple[str, ...]) -> tuple[str, str] | None:
    """(class, name) of a cone end. Only the two named faces stop it: an input of
    the cell csr that CSR_READBACK names, an input of the cell pp_shadow that
    PROCESSOR_FACE names. Every other port, and a datapath output, is the wire.
    None only where a rule the mutation check removed no longer makes it an end."""
    if end[0] == "out":
        return ("wire", f"the datapath output {end[1]}") if live("output-is-wire") else None
    cell, port = end[1], end[2]
    kind = net.cells[cell].kind
    any_cell = not live("terminal-cell")
    if kind == CSR and (cell == CSR_CELL or any_cell) and (port in CSR_READBACK or not live("csr-readback")):
        return "csr", port
    if kind == WRAPPER and (cell == WRAPPER_CELL or any_cell) and (port in PROCESSOR_FACE or
                                                                  not live("processor-face")):
        return "processor", port
    if kind.startswith("$"):
        return ("wire", f"{cell}.{port} ({kind}, which has no output)") if live("no-output-end") else None
    return "wire", f"{cell}.{port}"


def driver(net: Netlist, d: tuple[str, str]) -> str:
    """What one driver of a bit is, in the source's terms."""
    cell, port = d
    if not cell:
        return f"the datapath input {port}"
    c = net.cells[cell]
    if c.kind == "$_BUF_":                          # an assignment, which insbuf made a buffer
        b = c.conns.get("A", ("x",))[0]
        if not isinstance(b, int):
            return f"an assignment of the constant {b}"
        name, i = net.bit_name[b]
        return "an assignment of an expression" if name in net.hidden else f"an assignment of {name}[{i}]"
    return f"a {c.kind} cell" if c.kind.startswith("$") else f"{cell}.{port}"


def first_hop(fl: Flow, wire: str) -> dict[str, set]:
    """consumer -> what of it a population net's value lands on first: the bits of
    the first named net on each path, or the end reached before any."""
    start = [b for b in fl.net.names[wire] if isinstance(b, int)]
    seen, todo, hits = set(start), deque(start), defaultdict(set)
    while todo:
        for e in step(fl, todo.popleft()):
            if e[0] != "bit":
                hits[f"{e[1]}.{e[2]}" if e[0] == "pin" else e[1]].add(e)
            elif e[1] not in seen:
                seen.add(e[1])
                name = named(fl.net, e[1])
                if name and name != wire:
                    hits[name].add(e[1])
                else:
                    todo.append(e[1])
    return hits


def cone(fl: Flow, start: set) -> frozenset[tuple[str, str]]:
    """Every end a read's consumer reaches, through every cell and named net."""
    ends = {terminal(fl.net, e) for e in start if not isinstance(e, int)}
    bits = [b for b in start if isinstance(b, int)]
    seen, todo = set(bits), deque(bits)
    while todo:
        for e in step(fl, todo.popleft()):
            if e[0] != "bit":
                ends.add(terminal(fl.net, e))
            elif e[1] not in seen:
                seen.add(e[1])
                todo.append(e[1])
    return frozenset(ends - {None})


def class_d_face(wrapper: str, outputs: set[str]) -> tuple[set[str], list[str]]:
    """(the outputs the wrapper's port list declares under a class-D section heading,
    every output it cannot place). The elaborated wrapper names its outputs; the
    source only says which section each is declared under."""
    lines = wrapper.splitlines()
    start = next((i for i, s in enumerate(lines) if re.match(rf"\s*module\s+{WRAPPER}\b", s)), None)
    if start is None:
        raise CensusError(f"the wrapper source declares no module {WRAPPER}")
    end = next((i for i in range(start, len(lines)) if re.match(r"\s*\)\s*;", lines[i])), len(lines))
    section, where = "", defaultdict(list)
    for s in lines[start:end + 1]:
        head = SECTION.match(s)
        section = head.group(1) if head else section
        for n in NAME.findall("" if head else s.split("//")[0]):
            if n in outputs:
                where[n].append(section)
    problems = [f"the wrapper's port list declares output {n} {len(where[n])} times, or never: the census "
                f"cannot tell its section" for n in sorted(outputs) if len(where[n]) != 1 and live("face-placed")]
    face = {n for n in outputs if len(where[n]) == 1 and where[n][0].startswith("class-D")}
    if not face:
        raise CensusError(f"{WRAPPER} declares no output under a class-D section of its port list")
    return face, problems


def population(fl: Flow, wrapper: str) -> tuple[dict[str, str], list[str]]:
    """net -> the class-D port that drives it, and every way the wrapper's face, its
    cell or the population's drivers break the rules."""
    net = fl.net
    cells = sorted(n for n, c in net.cells.items() if c.kind == WRAPPER)
    if cells != [WRAPPER_CELL] and live("one-wrapper"):
        raise CensusError(f"the datapath holds {WRAPPER} cell(s) {cells or 'none'}; the census reads one, "
                          f"{WRAPPER_CELL}")
    if (CSR_CELL not in net.cells or net.cells[CSR_CELL].kind != CSR) and live("csr-cell"):
        raise CensusError(f"the datapath holds no {CSR} cell named {CSR_CELL}")
    outputs = {p for p, d in net.modules.get(WRAPPER, {}).items() if d == "output"}
    face, out = class_d_face(wrapper, outputs)
    out += [f"the wrapper declares class-D output {p}, which CLASS_D_PORTS does not list: review it"
            for p in sorted(face - CLASS_D_PORTS) if live("face-listed")]
    out += [f"CLASS_D_PORTS lists {p}, which the wrapper's class-D face does not declare"
            for p in sorted(CLASS_D_PORTS - face) if live("face-declared")]
    if STARTED_PORT not in outputs and live("started-port"):
        out.append(f"the wrapper declares no output {STARTED_PORT}")
    pop: dict[str, str] = {}
    cell = net.cells[WRAPPER_CELL]
    for port in sorted((face | CLASS_D_PORTS | {STARTED_PORT}) & outputs):
        bits = cell.conns.get(port, ())
        names = sorted({net.bit_name[b][0] for b in bits if isinstance(b, int)})
        if not names and live("port-connected"):
            out.append(f"class-D port {port} is not connected")
        elif (len(names) != 1 or net.names[names[0]] != bits or names[0] in net.hidden) and live("port-one-net"):
            out.append(f"class-D port {port} drives {', '.join(names)}, not one whole named net")
        elif names and names[0] in pop and live("ports-distinct"):
            out.append(f"class-D ports {pop[names[0]]} and {port} drive one net, {names[0]}")
        elif names:
            pop[names[0]] = port
            others = sorted({driver(net, d) for b in bits for d in fl.drivers[b] if d != (WRAPPER_CELL, port)})
            out += [f"{names[0]} is driven by {', '.join(others)} besides the wrapper's class-D port {port}: a "
                    f"second driver"] if others and live("sole-driver") else []
    return pop, out


def multiple(fl: Flow, skip: set[str]) -> list[str]:
    """Each net outside skip with a bit that has two drivers: the census cannot tell which value its readers see."""
    out: dict[str, set[str]] = defaultdict(set)
    for b, ds in fl.drivers.items():
        if len(ds) > 1 and fl.net.bit_name[b][0] not in skip and live("two-drivers"):
            out[fl.net.bit_name[b][0]] |= {driver(fl.net, d) for d in ds}
    return [f"{n} has two drivers, {', '.join(sorted(ds))}: the census cannot tell which its readers see"
            for n, ds in sorted(out.items())]


def survey(src: Sources, shape: Shape = RECIPE, net: Netlist | None = None) -> Survey:
    """The population, its reads and their cones, from the datapath as elaborated in
    shape, or from net when that elaboration is already done."""
    net = net or elaborate(overlay(src), shape)
    fl = flow(net)
    pop, problems = population(fl, src.wrapper)
    problems += multiple(fl, set(pop))
    reads, unread = [], []
    for wire in sorted(pop):
        hits = first_hop(fl, wire)
        unread += [wire] if not hits else []
        reads += [Read(wire, c, cone(fl, at)) for c, at in sorted(hits.items())]
    size = f"{len(net.cells)} cells, {len(net.names) - len(net.hidden)} named nets"
    return Survey(pop, reads, unread, problems, size, shape.name)


def surveyed(job: tuple[Sources, Shape]) -> Survey:
    """survey() of one shape in a worker process, a refusal naming the shape."""
    src, shape = job
    try:
        return survey(src, shape)
    except CensusError as exc:
        raise CensusError(f"in the shape {shape.name}: {exc}") from exc


def overlay(src: Sources) -> dict[Path, str]:
    """Each file whose text in src differs from the checkout's, by path."""
    out = {}
    for path, text in ((DATAPATH, src.datapath), (WRAPPER_SV, src.wrapper),
                       *((REPO / p, t) for copies in src.included.values() for p, t in copies)):
        if path.read_text(encoding="utf-8") != text:
            out[path] = text
    return out


def fields(contract: mailbox_model.Contract) -> set[str]:
    """REGISTER.FIELD of every publication register."""
    return {f"{r.name}.{f.name}" for r in contract.pub_registers + contract.pub_sink_registers for f in r.fields}


def judge(sv: Survey, table: dict[tuple[str, str], Row], known: set[str]) -> list[str]:
    """Every way one shape's survey and the census disagree."""
    out = list(sv.problems)
    for r in sv.reads:
        row = table.get((r.wire, r.consumer))
        where = f"{r.wire} -> {r.consumer}"
        kinds = {k for k, _ in r.ends}
        if row is None:
            reach = "the wire" if "wire" in kinds else ", ".join(sorted(kinds)) or "nothing"
            out += [f"unmapped read: {where} reaches {reach}; name its block field or its ruled exclusion"
                    ] if live("unmapped") else []
            continue
        if row.field and row.field not in known and live("unknown-field"):
            out.append(f"{where}: the census names {row.field}, which the publication block does not define")
        if row.kind == "field" and "wire" not in kinds and live("field-on-wire"):
            out.append(f"{where}: mapped to {row.field} as read on the wire, but it reaches no wire")
        if row.kind in ("status", "processor"):
            # what keeps the read off the wire: only the ports terminal()
            # names, the CSR read-back face and the wrapper's answer face
            wires = sorted(n for k, n in r.ends if k == "wire")
            if wires and live("off-wire"):
                out.append(f"{where}: counted as {row.kind}, but it reaches the wire at {'; '.join(wires)}")
            if row.kind == "status" and "processor" in kinds and live("status-not-processor"):
                out.append(f"{where}: counted as status, but it reaches the processor wrapper")
    seen = {(r.wire, r.consumer) for r in sv.reads}
    out += [f"stale row: the datapath no longer reads {w} into {c}" for w, c in table
            if (w, c) not in seen and live("stale-row")]
    return out


def compare(svs: list[Survey]) -> list[str]:
    """Every way the shapes disagree: the population, the unread nets, and the reads
    with each read's classes of cone end, each item not found in every shape."""
    if len(svs) < 2 or not live("same-across-shapes"):
        return []
    views = {"the population": lambda sv: {f"{n} from {p}" for n, p in sv.population.items()},
             "the unread nets": lambda sv: set(sv.unread),
             "the reads": lambda sv: {f"{r.wire} -> {r.consumer} reaching "
                                      f"{', '.join(sorted({k for k, _ in r.ends})) or 'nothing'}" for r in sv.reads}}
    out = []
    for what, view in views.items():
        seen = {sv.shape: view(sv) for sv in svs}
        odd = set().union(*seen.values()) - set.intersection(*seen.values())
        out += [f"{what} differ between the shapes: {item} only in {', '.join(s for s, v in seen.items() if item in v)}"
                for item in sorted(odd)]
    return out


def verdict(svs: list[Survey], table: dict[tuple[str, str], Row], known: set[str]) -> list[str]:
    """Every shape's findings, each once with the shapes it holds in, then the shapes' disagreements."""
    grouped: dict[str, list[str]] = defaultdict(list)
    for sv in svs:
        for f in judge(sv, table, known):
            grouped[f].append(sv.shape)
    out = [f if len(svs) == 1 else f"{f} [{'every shape' if len(at) == len(svs) else ', '.join(at)}]"
           for f, at in grouped.items()]
    return out + compare(svs)


def census(src: Sources, table: dict[tuple[str, str], Row], known: set[str], at: tuple[Shape, ...] | None = None,
           jobs: int = 1, nets: dict[str, Netlist] | None = None) -> tuple[list[str], list[Survey]]:
    """Every finding over the shapes at (every shape the builder builds when None), and
    each shape's survey. jobs elaborate at once; nets, when given, holds each shape's
    netlist by name, elaborated only when missing."""
    at = shapes() if at is None else at
    if nets is None and jobs > 1 and len(at) > 1:
        # the most streams first: the largest netlist is the longest elaboration
        order = sorted(at, key=lambda s: -dict(s.params).get("N_STREAMS", 1))
        WORK.roms()                    # once, here: the workers share this process's scratch directory
        with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context("fork")) as pool:
            done = dict(zip((s.name for s in order), pool.map(surveyed, [(src, s) for s in order])))
        svs = [done[s.name] for s in at]
    else:
        svs = []
        for shape in at:
            net = nets.get(shape.name) if nets is not None else None
            if net is None:
                net = elaborate(overlay(src), shape)
                if nets is not None:
                    nets[shape.name] = net
            svs.append(survey(src, shape, net))
    return verdict(svs, table, known), svs


def findings(src: Sources, table: dict[tuple[str, str], Row], known: set[str]) -> tuple[list[str], Survey]:
    """census() over every shape the builder builds, one at a time, and the recipe's survey."""
    out, svs = census(src, table, known)
    return out, svs[0]


def load(datapath: Path, wrapper: Path) -> Sources:
    """The sources as tracked, with each file the datapath includes: every copy the
    front end could read, the one it reads first leading (the datapath's own
    directory, then the recipe's include directories in order)."""
    text = datapath.read_text(encoding="utf-8")
    roots = [DATAPATH.parent, *recipe().incdirs]
    found = {}
    for name in dict.fromkeys(INCLUDE.findall(text)):
        hits = [Path(r) / name for r in roots if (Path(r) / name).is_file()]
        found[name] = tuple((p.resolve().relative_to(REPO).as_posix(), p.read_text(encoding="utf-8"))
                            for p in dict.fromkeys(h.resolve() for h in hits))
    return Sources(text, wrapper.read_text(encoding="utf-8"), found)


def report(svs: list[Survey], out: list[str], listing: bool, checking: bool) -> None:
    """Print --list's population and reads (the first shape's; --check fails where
    another differs) and each shape, and --check's findings and tally."""
    first, params = svs[0], {s.name: s.params for s in shapes()}
    if listing:
        for wire, port in sorted(first.population.items(), key=lambda kv: kv[1]):
            print(f"{port:26} -> {wire}" + ("   (unread)" if wire in first.unread else ""))
        for r in first.reads:
            row = CENSUS.get((r.wire, r.consumer))
            ends = ", ".join(sorted({k for k, _ in r.ends})) or "nothing"
            print(f"{r.wire:30} -> {r.consumer:24} reaches {ends:22} "
                  f"{row.kind + ' ' + row.field if row else 'UNMAPPED'}")
    for sv in svs:
        bound = " ".join(f"{k}={v}" for k, v in params.get(sv.shape, ())) or "the module's defaults"
        print(f"shape {sv.shape}: {sv.size}; {len(sv.reads)} read(s), {len(sv.unread)} unread net(s); {bound}")
    if checking:
        for f in out:
            print(f"[FAIL] {f}")
        wires = len({r.wire for r in first.reads})
        print(f"== publication census: {len(svs)} shape(s), checks: {sum(len(sv.reads) for sv in svs)}   "
              f"failures: {len(out)} ==")
        print(f"{len(first.population)} class-D net(s) from the wrapper cell's ports, {len(first.unread)} unread; "
              f"{len(first.reads)} read(s) of {wires} class-D net(s) in each shape; "
              f"RESULT: {'PASS' if not out else 'FAIL'}")


def main(argv: list[str] | None = None) -> int:
    """--check, --list and --selftest over the elaborated datapath; the exit status."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--check", action="store_true", help="fail on any read the census does not account for")
    ap.add_argument("--list", action="store_true", help="print the population, and every read, its cone and its row")
    ap.add_argument("--selftest", action="store_true", help="prove the check refuses each planted defect")
    ap.add_argument("--jobs", type=int, default=1, help="elaborations run at once")
    ap.add_argument("--datapath", type=Path, default=DATAPATH, help="the datapath to elaborate in its place")
    ap.add_argument("--wrapper", type=Path, default=WRAPPER_SV,
                    help="the processor wrapper to elaborate in its place")
    args = ap.parse_args(argv)
    if not (args.check or args.list or args.selftest) or args.jobs < 1:
        ap.error("name --check, --list or --selftest, and --jobs of 1 or more")
    known = fields(mailbox_model.load())
    rc, began = 0, time.monotonic()
    try:
        print(f"publication census: elaborating {DATAPATH.relative_to(REPO)} with {toolchain()}")
        src = load(args.datapath, args.wrapper)
        if args.check or args.list:
            out, svs = census(src, CENSUS, known, None, args.jobs)
            report(svs, out, args.list, args.check)
            print(f"publication census: {len(svs)} shape(s) elaborated and classified in "
                  f"{time.monotonic() - began:.0f} s at --jobs {args.jobs}")
            rc |= bool(out) and args.check
        if args.selftest:
            # census_selftest imports this module by name: hand it this one, not a second copy
            sys.modules.setdefault("publication_census", sys.modules[__name__])
            import census_selftest
            rc |= bool(census_selftest.selftest(src, known, args.jobs))
    except CensusError as exc:
        print(f"[FAIL] the census cannot read {args.datapath}: {exc}")
        return 2
    return int(rc)


if __name__ == "__main__":
    sys.exit(main())

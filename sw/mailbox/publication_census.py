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
datapath every time and fails closed (#665, comment 6094461419).

THE NETLIST, not the text (#665, comment 6097292237). census_elab.py
elaborates the datapath in the all-fabric shape with the recipe, the sv2v and
the Yosys of CI's elaboration gate, every other module a blackbox cell, its
processes turned into cells by the passes ``proc`` runs (``insbuf`` before
each that would rename a read, the closing ``opt_expr`` left out, as
census_elab.py says), and reads the netlist back. The
census follows values through that netlist alone, so how a read is written (a
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

and fails on a read the census does not name, a row no read matches, a status
or processor read whose cone reaches the wire, a status read whose cone
reaches the processor wrapper, a field read whose cone does not reach the
wire, and a field the contract does not define.

    python3 sw/mailbox/publication_census.py --check
    python3 sw/mailbox/publication_census.py --list
    python3 sw/mailbox/publication_census.py --selftest --jobs 4

``--selftest`` elaborates a planted copy of the datapath, the wrapper or an
included file for each defect of ``census_plants.PLANTS`` and requires each to
be refused by its own words: every reviewer probe of rounds 2 to 5 of #665
that escaped the text census, each beside its plain-assign control, the
census's own defects, every wrong connection of the wrapper's class-D face,
and the forms the front end refuses. The tracked sources, and a copy whose
only change is a comment naming a class-D wire, must pass.
"""

from __future__ import annotations

import argparse
import multiprocessing
import re
import sys
import time
from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mailbox_model  # noqa: E402
from census_elab import REPO, Cell, CensusError, Netlist, elaborate, recipe, toolchain  # noqa: E402
from census_plants import PLANTS, apply  # noqa: E402

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
    """One elaboration's census: the population, its reads, the nets nothing reads,
    every way the netlist breaks the census's rules, and the netlist's size."""

    population: dict[str, str]
    reads: list[Read]
    unread: list[str]
    problems: list[str]
    size: str


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
                if dirs[p] != "output":
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
            out += [("bit", o) for r in fl.readers.get(e[1], ()) for o in fl.outs[r]]
        else:
            out.append(e)
    return out


def named(net: Netlist, bit: int) -> str:
    """The name the source gave the net a bit belongs to, or "" for one the elaborator made."""
    name = net.bit_name[bit][0]
    return "" if name in net.hidden else name


def terminal(net: Netlist, end: tuple[str, ...]) -> tuple[str, str]:
    """(class, name) of a cone end. Only the two named faces stop it: an input of
    the cell csr that CSR_READBACK names, an input of the cell pp_shadow that
    PROCESSOR_FACE names. Every other port, and a datapath output, is the wire."""
    if end[0] == "out":
        return "wire", f"the datapath output {end[1]}"
    cell, port = end[1], end[2]
    kind = net.cells[cell].kind
    if cell == CSR_CELL and kind == CSR and port in CSR_READBACK:
        return "csr", port
    if cell == WRAPPER_CELL and kind == WRAPPER and port in PROCESSOR_FACE:
        return "processor", port
    return "wire", f"{cell}.{port}" + ("" if not kind.startswith("$") else f" ({kind}, which has no output)")


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
    return frozenset(ends)


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
                f"cannot tell its section" for n in sorted(outputs) if len(where[n]) != 1]
    face = {n for n in outputs if len(where[n]) == 1 and where[n][0].startswith("class-D")}
    if not face:
        raise CensusError(f"{WRAPPER} declares no output under a class-D section of its port list")
    return face, problems


def population(fl: Flow, wrapper: str) -> tuple[dict[str, str], list[str]]:
    """net -> the class-D port that drives it, and every way the wrapper's face, its
    cell or the population's drivers break the rules."""
    net = fl.net
    cells = sorted(n for n, c in net.cells.items() if c.kind == WRAPPER)
    if cells != [WRAPPER_CELL]:
        raise CensusError(f"the datapath holds {WRAPPER} cell(s) {cells or 'none'}; the census reads one, "
                          f"{WRAPPER_CELL}")
    if CSR_CELL not in net.cells or net.cells[CSR_CELL].kind != CSR:
        raise CensusError(f"the datapath holds no {CSR} cell named {CSR_CELL}")
    outputs = {p for p, d in net.modules.get(WRAPPER, {}).items() if d == "output"}
    face, out = class_d_face(wrapper, outputs)
    out += [f"the wrapper declares class-D output {p}, which CLASS_D_PORTS does not list: review it"
            for p in sorted(face - CLASS_D_PORTS)]
    out += [f"CLASS_D_PORTS lists {p}, which the wrapper's class-D face does not declare"
            for p in sorted(CLASS_D_PORTS - face)]
    if STARTED_PORT not in outputs:
        out.append(f"the wrapper declares no output {STARTED_PORT}")
    pop: dict[str, str] = {}
    cell = net.cells[WRAPPER_CELL]
    for port in sorted((face | CLASS_D_PORTS | {STARTED_PORT}) & outputs):
        bits = cell.conns.get(port, ())
        names = sorted({net.bit_name[b][0] for b in bits if isinstance(b, int)})
        if not names:
            out.append(f"class-D port {port} is not connected")
        elif len(names) != 1 or net.names[names[0]] != bits or names[0] in net.hidden:
            out.append(f"class-D port {port} drives {', '.join(names)}, not one whole named net")
        elif names[0] in pop:
            out.append(f"class-D ports {pop[names[0]]} and {port} drive one net, {names[0]}")
        else:
            pop[names[0]] = port
            others = sorted({driver(net, d) for b in bits for d in fl.drivers[b] if d != (WRAPPER_CELL, port)})
            out += [f"{names[0]} is driven by {', '.join(others)} besides the wrapper's class-D port {port}: a "
                    f"second driver"] if others else []
    return pop, out


def multiple(fl: Flow, skip: set[str]) -> list[str]:
    """Each net outside skip with a bit that has two drivers: the census cannot tell which value its readers see."""
    out: dict[str, set[str]] = defaultdict(set)
    for b, ds in fl.drivers.items():
        if len(ds) > 1 and fl.net.bit_name[b][0] not in skip:
            out[fl.net.bit_name[b][0]] |= {driver(fl.net, d) for d in ds}
    return [f"{n} has two drivers, {', '.join(sorted(ds))}: the census cannot tell which its readers see"
            for n, ds in sorted(out.items())]


def survey(src: Sources) -> Survey:
    """The population, its reads and their cones, from the datapath as elaborated."""
    net = elaborate(overlay(src))
    fl = flow(net)
    pop, problems = population(fl, src.wrapper)
    problems += multiple(fl, set(pop))
    reads, unread = [], []
    for wire in sorted(pop):
        hits = first_hop(fl, wire)
        unread += [wire] if not hits else []
        reads += [Read(wire, c, cone(fl, at)) for c, at in sorted(hits.items())]
    size = f"{len(net.cells)} cells, {len(net.names) - len(net.hidden)} named nets"
    return Survey(pop, reads, unread, problems, size)


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


def findings(src: Sources, table: dict[tuple[str, str], Row], known: set[str]) -> tuple[list[str], Survey]:
    """Every way the elaborated sources and the census disagree."""
    sv = survey(src)
    out = list(sv.problems)
    for r in sv.reads:
        row = table.get((r.wire, r.consumer))
        where = f"{r.wire} -> {r.consumer}"
        kinds = {k for k, _ in r.ends}
        if row is None:
            reach = "the wire" if "wire" in kinds else ", ".join(sorted(kinds)) or "nothing"
            out.append(f"unmapped read: {where} reaches {reach}; name its block field or its ruled exclusion")
            continue
        if row.field and row.field not in known:
            out.append(f"{where}: the census names {row.field}, which the publication block does not define")
        if row.kind == "field" and "wire" not in kinds:
            out.append(f"{where}: mapped to {row.field} as read on the wire, but it reaches no wire")
        if row.kind in ("status", "processor"):
            # what keeps the read off the wire: only the ports terminal()
            # names, the CSR read-back face and the wrapper's answer face
            wires = sorted(n for k, n in r.ends if k == "wire")
            if wires:
                out.append(f"{where}: counted as {row.kind}, but it reaches the wire at {'; '.join(wires)}")
            if row.kind == "status" and "processor" in kinds:
                out.append(f"{where}: counted as status, but it reaches the processor wrapper")
    seen = {(r.wire, r.consumer) for r in sv.reads}
    out += [f"stale row: the datapath no longer reads {w} into {c}" for w, c in table if (w, c) not in seen]
    return out, sv


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


def arm(job: tuple) -> tuple[bool, str]:
    """One self-test arm: (refused by its words, the line saying so)."""
    what, planted, table, word, known = job
    if isinstance(planted, str):
        return False, f"[BAD] planted {what}: {planted}"
    try:
        got, _ = findings(planted, table, known)
    except CensusError as exc:
        got = [f"the census cannot read it: {exc}"]
    words = (word,) if isinstance(word, str) else word
    hit = [f for f in got if all(w in f for w in words)]
    return bool(hit), f"[{'ok' if hit else 'BAD'}] planted {what}: " + (f"refused ({hit[0]})" if hit else
                                                                        f"accepted ({got[:1] or 'no finding'})")


def selftest(src: Sources, known: set[str], jobs: int) -> int:
    """Each plant elaborated and refused by its own words, the controls clean; the number of failed arms."""
    began, failed = time.monotonic(), 0
    clean, _ = findings(src, CENSUS, known)
    print(f"[{'ok' if not clean else 'BAD'}] positive control, the tracked sources: {len(clean)} finding(s)"
          + "".join(f"\n    {f}" for f in clean))
    failed += bool(clean)
    note = replace(src, datapath=src.datapath.replace(
        "  wire crft_class_a_w =", "  // pp_cd_srp_over_limit_w is not read here\n  wire crft_class_a_w =", 1))
    quiet, _ = findings(note, CENSUS, known)
    print(f"[{'ok' if not quiet else 'BAD'}] negative control, a class-D wire named in a comment: "
          f"{len(quiet)} finding(s)")
    failed += bool(quiet)
    arms = [(p.what, apply(src, p), CENSUS, p.word, known) for p in PLANTS]
    key = ("pp_cd_srp_tk_decl_state_w", "crft_class_a_w")
    arms.append(("a field the contract lacks", src, {**CENSUS, key: Row("field", "TALKER_DECL.DECLARE", "")},
                 "which the publication block does not define", known))
    arms.append(("a stale row", src, {**CENSUS, ("pp_cd_srp_granted_slope_bps_w", "lwsrp_idle_slope"):
                                      Row("status", "", "planted")},
                 "stale row: the datapath no longer reads pp_cd_srp_granted_slope_bps_w", known))
    with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context("fork")) as pool:
        for ok, line in pool.map(arm, arms):
            print(line, flush=True)
            failed += not ok
    print(f"selftest: {failed} of {len(arms) + 2} arm(s) failed; {len(arms) + 2} elaborations in "
          f"{time.monotonic() - began:.0f} s at --jobs {jobs}")
    return failed


def report(sv: Survey, out: list[str], listing: bool, checking: bool) -> None:
    """Print --list's population and reads, and --check's findings and tally."""
    if listing:
        for wire, port in sorted(sv.population.items(), key=lambda kv: kv[1]):
            print(f"{port:26} -> {wire}" + ("   (unread)" if wire in sv.unread else ""))
        for r in sv.reads:
            row = CENSUS.get((r.wire, r.consumer))
            ends = ", ".join(sorted({k for k, _ in r.ends})) or "nothing"
            print(f"{r.wire:30} -> {r.consumer:24} reaches {ends:22} "
                  f"{row.kind + ' ' + row.field if row else 'UNMAPPED'}")
    if checking:
        for f in out:
            print(f"[FAIL] {f}")
        wires = len({r.wire for r in sv.reads})
        print(f"== publication census: checks: {len(sv.reads)}   failures: {len(out)} ==")
        print(f"{len(sv.population)} class-D net(s) from the wrapper cell's ports, {len(sv.unread)} unread; "
              f"netlist: {sv.size}")
        print(f"{len(sv.reads)} read(s) of {wires} class-D net(s); RESULT: {'PASS' if not out else 'FAIL'}")


def main(argv: list[str] | None = None) -> int:
    """--check, --list and --selftest over the elaborated datapath; the exit status."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--check", action="store_true", help="fail on any read the census does not account for")
    ap.add_argument("--list", action="store_true", help="print the population, and every read, its cone and its row")
    ap.add_argument("--selftest", action="store_true", help="prove the check refuses each planted defect")
    ap.add_argument("--jobs", type=int, default=1, help="elaborations the self-test runs at once")
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
        out, sv = findings(src, CENSUS, known)
        report(sv, out, args.list, args.check)
        print(f"publication census: elaborated and classified in {time.monotonic() - began:.0f} s")
        rc |= bool(out) and args.check
        if args.selftest:
            rc |= bool(selftest(src, known, args.jobs))
    except CensusError as exc:
        print(f"[FAIL] the census cannot read {args.datapath}: {exc}")
        return 2
    return int(rc)


if __name__ == "__main__":
    sys.exit(main())

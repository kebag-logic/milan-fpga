#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""publication_census.py - every occurrence of the processor's class-D wires, accounted for.

THE QUESTION. In the split placement the fabric datapath no longer has the
protocol processor: the firmware owns ADP, ACMP, MAAP and SRP and writes what
the datapath consumes into the mailbox's publication block (#665, ruling
6088423771, decision 2 (a)). Which values the block must carry is decided by
what ``hdl/milan/milan_datapath.sv`` reads, and a list copied by hand missed
two of them (#665, comment 6092086337). This check derives the list from the
datapath every time and fails closed: an occurrence it cannot account for
fails, whatever its form (#665, comment 6094461419).

THE POPULATION comes from the processor wrapper's instance, never from a
name. ``CLASS_D_PORTS`` lists the class-D face of ``KL_pp_shadow`` and must
equal the outputs the wrapper's own class-D sections declare, so a port added
to, renamed in or moved out of that face fails until it is reviewed here.
``aecp_strm_started_o``, each sink's started level, joins them by the ruling
of comment 6092086337. The datapath's one ``KL_pp_shadow`` instance must
connect each of these ports by name, once, to a bare wire, and that wire joins
the population whatever it is called. A port left unconnected, connected to an
expression, or connected positionally or by an implicit ``.name`` fails.

THE OCCURRENCES. Comments and strings are blanked first. Every remaining
occurrence of a population wire in the datapath must be exactly one of:

  its declaration     the name one ``wire`` or ``logic`` declaration declares
  its connection      the wrapper's class-D output connection above
  a read              a read (below), which ``CENSUS`` must then map

Any other occurrence fails: a case item label, a positional or implicit
``.name`` port connection, a function or task body, a second driver, and any
form not listed here. A form the parser does not understand is therefore
refused, never skipped. Three forms read a value without naming its wire, and
each fails wherever it appears: a wildcard ``.*`` port connection, a macro
token paste, and a hierarchical reference into the wrapper, the CSR block or
an instance a population read reaches. A file the datapath includes must not
name a population wire, and an include the census cannot find under ``hdl/``
or ``configs/`` fails.

THE READS. The datapath is cut into statements, and a statement into its
assignments (a comma outside brackets after the first '=' starts the next of a
list, ``assign a = x, b = y``). A read is an occurrence of a name in an
assignment's right-hand side, in an index of its target, in the parentheses
of an ``if``, ``case``, ``for`` or ``while`` that controls it, or in a named
module port connection, whatever the port is called. Declarations with an
initialiser (``wire x = ...``) are assignments like any other. A read of a
population wire is keyed by the wire and its consumer: the signal its
assignment drives, or ``instance.port``.

THE CONE fails closed at every node, as the occurrences do at the first hop:
any occurrence is an edge (#665, comment 6095903333). A read leads to every
signal its statement can drive: the targets of its assignment, every target
of the procedural block (``always``, ``initial``, ``final``) it lies in, or
its ``instance.port``. From each signal reached, every non-comment occurrence
of its name in the datapath is one of:

  its declaration     a name a net or variable declaration declares
  a place driving it  the target of an assignment
  a read              which leads on to every signal its statement can drive

and any other occurrence counts as reaching the wire: a positional or implicit
``.name`` port, a case item label, an event control, a member or hierarchical
name, anything inside a function, task, property or sequence declaration (a
``return`` among them), a read inside the arguments of a call to a function,
task, system function or macro (the census does not follow a value through
what it cannot see), and any form not listed here. A signal that a file the
datapath includes names counts as reaching the wire too. Only two terminals
stop the cone, each named by instance and port, never by a port's name:

  csr        a port of the ``milan_csr`` instance that ``CSR_READBACK`` names
  processor  a port of the ``KL_pp_shadow`` instance that ``PROCESSOR_FACE``
             names, its GET_STREAM_INFO and GET_AVB_INFO answer face

Every other port of every instance, those two included, and a module output
are the wire. So a path the census cannot rule out reaches the wire.

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
or processor read whose cone reaches the wire (any port the two lists do not
name among it), a status read whose cone reaches the processor wrapper, a field
read whose cone does not reach the wire, and a field the contract does not
define.

    python3 sw/mailbox/publication_census.py --check
    python3 sw/mailbox/publication_census.py --list
    python3 sw/mailbox/publication_census.py --selftest

``--selftest`` plants each defect of ``PLANTS`` into copies of the datapath,
the wrapper or an included file: the reviewers' escaping reads (a wire renamed
off the class-D prefix, a case item label, positional and implicit ``.name``
ports, a function's return) and the forms already refused; the reviewers'
escaping cone hops from a status consumer and a processor consumer (a
positional and an implicit ``.name`` port, a case item label, a function's
return, an event control, an input port named like an output), each with its
plain-assign control, and further hops (a relational ``<=`` in a case label,
a function's and a task's output argument, a macro's argument, the second
assignment of a list, another target of the block, a member, a CSR or wrapper
port outside its face); every wrong connection of the wrapper's class-D face,
each outright refusal, and the census's own defects (an unmapped read, a
status or processor read on the wire, a field the contract lacks, a stale
row). Each must be refused by its own words, a cone hop by its read's row and
the occurrence that reaches the wire; the tracked sources, and a copy whose
only change is a comment naming a class-D wire, must pass.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mailbox_model  # noqa: E402
from census_plants import PLANTS, apply  # noqa: E402
# the reader; DECL, always_blocks, lead_of and lvalues are the census's API
# too, which the reviewers' probes of #665 call
from census_netlist import (  # noqa: E402
    DECL, TOKEN, CensusError, Netlist, always_blocks, assignment, close_of, declarations, lead_of, lvalues,
    netlist, strip_comments, top_level)

REPO = HERE.parent.parent
DATAPATH = REPO / "hdl/milan/milan_datapath.sv"
WRAPPER_SV = REPO / "hdl/milan/KL_pp_shadow.sv"
#: Where an included file is looked for: every build's include directories lie under these.
INCLUDE_ROOTS = (REPO / "hdl", REPO / "configs")

WRAPPER = "KL_pp_shadow"
CSR = "milan_csr"
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


#: (wire, consumer) -> Row. The consumer is the signal the read drives, or
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
SECTION = re.compile(r"^[ \t]*//!?[ \t]*-{4}[ \t]*(.*?)[ \t]*-{4,}[ \t]*$", re.M)
PORT_DIRECTION = re.compile(r"\s*(input|output|inout)\b")
PORT_WORDS = frozenset("input output inout wire logic reg var tri uwire signed unsigned".split())
NAMED_PORT = re.compile(r"\s*\.\s*(\w+)\s*\(")
WILDCARD = re.compile(r"[(,]\s*\.\s*\*\s*(?=[,)])")
INCLUDE = re.compile(r"`include\b\s*(\")?")
#: A dotted path, each scope optionally indexed (a generate scope, an instance array).
SCOPE = r"[A-Za-z_][\w$]*(?:\s*\[[^\][]*\])*"
HIERARCHICAL = re.compile(rf"(?<![\w$.]){SCOPE}(?:\s*\.\s*{SCOPE})+")


def terminal(net: Netlist, node: str) -> tuple[str, str] | None:
    """(class, name) when node ends a cone. Only the two named faces stop it:
    a port of the CSR block that CSR_READBACK names, a port of the processor
    wrapper that PROCESSOR_FACE names. Any other instance's port, any other
    port of those two, and a module output are the wire."""
    if "." in node:
        inst, port = node.split(".", 1)
        kinds = net.instances.get(inst, set())
        if kinds == {CSR} and port in CSR_READBACK:
            return "csr", port
        if kinds == {WRAPPER} and port in PROCESSOR_FACE:
            return "processor", port
        return "wire", node
    if node in net.outputs:
        return "wire", node
    return None


def unclassified(net: Netlist, pos: int, node: str) -> tuple[str, str]:
    """The wire end an occurrence the census cannot classify counts as."""
    return "wire", f"`{net.text_at(pos)}` (line {net.line(pos)}), an occurrence of {node} it cannot classify"


def reach(net: Netlist, at: set[int], included: frozenset[str] = frozenset()) -> set[tuple[str, str]]:
    """Every terminal the reads of one (wire, consumer) reach: the cone of
    everything each read's statement or block drives. A read the census
    follows no further (one inside a function or task) is the wire."""
    out: set[tuple[str, str]] = set()
    for pos in sorted(at):
        if pos not in net.drives:
            out.add(unclassified(net, pos, net.code[pos:TOKEN.match(net.code, pos).end()]))
        for consumer in net.drives.get(pos, ()):
            out |= cone(net, consumer, included)
    return out


def cone(net: Netlist, start: str, included: frozenset[str] = frozenset()) -> set[tuple[str, str]]:
    """Every terminal a consumer reaches, failing closed: every occurrence of
    every node it visits is that node's declaration, a place that drives it,
    or a read, which leads on to everything its statement or block drives;
    any other occurrence, and a node an included file names, is the wire."""
    seen, stack, out = set(), [start], set()
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        end = terminal(net, node)
        if end:
            out.add(end)
            continue
        if node in included:
            out.add(("wire", f"an included file, which names {node}"))
        for pos in net.tokens.get(node, ()):
            if net.in_sub(pos):
                out.add(unclassified(net, pos, node))
                continue
            if pos in net.targets_at or pos in net.declared_at:
                continue
            if pos in net.drives:
                stack.extend(net.drives[pos])
            else:
                out.add(unclassified(net, pos, node))
    return out


@dataclass(frozen=True)
class Sources:
    """What the census reads: the datapath, the wrapper, and every copy of each file the datapath includes."""

    datapath: str
    wrapper: str
    included: dict[str, tuple[tuple[str, str], ...]]


@dataclass(frozen=True)
class Read:
    """One (wire, consumer) read: its lines and its cone."""

    wire: str
    consumer: str
    lines: tuple[int, ...]
    ends: frozenset[tuple[str, str]]


@dataclass
class Survey:
    """One reading of the sources: the population, its reads, the tally of its
    occurrences, and every way the sources break the census's rules."""

    population: dict[str, tuple[str, int]]
    reads: list[Read]
    tally: dict[str, int]
    problems: list[str]


def class_d_face(wrapper: str) -> tuple[set[str], set[str]]:
    """(the outputs the wrapper's class-D sections declare, every output it declares)."""
    code = strip_comments(wrapper)
    m = re.search(rf"\bmodule\s+{WRAPPER}\b", code)
    if not m:
        raise CensusError(f"the wrapper source declares no module {WRAPPER}")
    i = code.index("(", m.end())
    if code[m.end():i].strip() == "#":
        i = code.index("(", close_of(code, i))
    end = close_of(code, i)
    marks = [(i + s.start(), s.group(1)) for s in SECTION.finditer(wrapper[i:end])]
    direction, face, outputs = "", set(), set()
    for a, b in top_level(code[i + 1:end - 1]):
        item = code[i + 1 + a:i + 1 + b]
        cut = assignment(item)
        item = item[:cut[0]] if cut else item          # a port's default value is no name
        d = PORT_DIRECTION.match(item)
        direction = d.group(1) if d else direction    # ANSI: a bare name keeps the last direction
        bare = re.sub(r"\[[^\]]*\]", lambda x: " " * len(x.group()), item)
        names = [n for n in re.finditer(r"[A-Za-z_]\w*", bare) if n.group() not in PORT_WORDS]
        if direction != "output" or not names:
            continue
        outputs.add(names[-1].group())
        at = i + 1 + a + names[-1].start()
        if max((m for m in marks if m[0] < at), default=(0, ""))[1].startswith("class-D"):
            face.add(names[-1].group())
    if not face:
        raise CensusError(f"{WRAPPER} declares no output under a class-D section of its port list")
    return face, outputs


def population(net: Netlist, wrapper: str) -> tuple[dict[str, tuple[str, int]], list[str]]:
    """wire -> (its class-D port, the offset of the wrapper's connection), and
    every way the wrapper's face or its instance breaks the rules."""
    face, outputs = class_d_face(wrapper)
    out = [f"the wrapper declares class-D output {p}, which CLASS_D_PORTS does not list: review it"
           for p in sorted(face - CLASS_D_PORTS)]
    out += [f"CLASS_D_PORTS lists {p}, which the wrapper's class-D face does not declare"
            for p in sorted(CLASS_D_PORTS - face)]
    if STARTED_PORT not in outputs:
        out.append(f"the wrapper declares no output {STARTED_PORT}")
    shadows = [i for i, kinds in net.instances.items() if kinds == {WRAPPER}]
    if len(shadows) != 1:
        raise CensusError(f"the datapath instantiates {WRAPPER} {len(shadows)} times; the census reads one")
    base, body = net.bodies[shadows[0]]
    named: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for s, e in top_level(body):
        m = NAMED_PORT.match(body, s)
        close = close_of(body, m.end() - 1) if m and m.end() <= e else e + 1
        if close <= e and not body[close:e].strip():        # the item is .port(expr) and nothing else
            named[m.group(1)].append((m.end(), body[m.end():close - 1]))
        elif body[s:e].strip():
            out.append(f"the wrapper instance connects `{' '.join(body[s:e].split())}`, which is not a named "
                       f"port connection: the census cannot tell which port it drives")
    pop: dict[str, tuple[str, int]] = {}
    for port in sorted(face | CLASS_D_PORTS | {STARTED_PORT}):
        conns = named.get(port, [])
        if len(conns) != 1:
            out.append(f"class-D port {port} is not connected" if not conns else
                       f"class-D port {port} is connected {len(conns)} times")
            continue
        at, expr = conns[0]
        m = re.fullmatch(r"\s*([A-Za-z_]\w*)\s*", expr)
        if not expr.strip():
            out.append(f"class-D port {port} is left unconnected")
        elif not m:
            out.append(f"class-D port {port} is connected to an expression, `{' '.join(expr.split())}`, not a wire")
        elif m.group(1) in pop:
            out.append(f"class-D ports {pop[m.group(1)][0]} and {port} drive one wire, {m.group(1)}")
        else:
            pop[m.group(1)] = (port, base + at + m.start(1))
    return pop, out


def includes(text: str, code: str) -> list[str]:
    """The path of every `include in text (code: text, its comments blanked); '' for one naming no quoted path."""
    out = []
    for m in INCLUDE.finditer(code):
        out.append(text[m.end():text.index('"', m.end())] if m.group(1) else "")
    return out


def outright(net: Netlist, pop: dict[str, tuple[str, int]], found: list[Read]) -> list[str]:
    """The forms that read a value without naming its wire, each refused wherever it appears."""
    out = [f"a wildcard port connection (.*) at line {net.line(m.start())} connects every same-named signal "
           f"without naming it: name each port" for m in WILDCARD.finditer(net.code)]
    out += [f"a macro token paste (``) at line {net.line(m.start())} can build a class-D wire's name the census "
            f"cannot see" for m in re.finditer("``", net.code)]
    watched = {i for i, kinds in net.instances.items() if kinds & {WRAPPER, CSR}}
    watched |= {c.split(".")[0] for _, name, c in net.reads_at if name in pop and "." in c}
    watched |= {n.split(".")[0] for r in found for k, n in r.ends if k == "wire" and re.fullmatch(r"\w+\.\w+", n)}
    for m in HIERARCHICAL.finditer(net.code):
        scopes = re.findall(r"[A-Za-z_][\w$]*", re.sub(r"\[[^\]]*\]", "", m.group()))[:-1]
        out += [f"a hierarchical reference into {s} at line {net.line(m.start())} reads it without naming the "
                f"wire: `{net.text_at(m.start())}`" for s in scopes if s in watched][:1]
    return out


def survey(src: Sources) -> Survey:
    """The population, its reads and cones, and every occurrence accounted for."""
    net = netlist(src.datapath)
    if not any(kinds == {CSR} for kinds in net.instances.values()):
        raise CensusError(f"the datapath instantiates no {CSR}")
    pop, problems = population(net, src.wrapper)
    connected = {at for _, at in pop.values()}
    included = frozenset(n for copies in src.included.values() for _, text in copies
                         for n in TOKEN.findall(strip_comments(text)))
    at_: dict[tuple[str, str], set[int]] = defaultdict(set)
    read_at: set[int] = set()
    for pos, name, consumer in net.reads_at:
        if name in pop and pos not in connected:
            at_[(name, consumer)].add(pos)
            read_at.add(pos)
    found = [Read(w, c, tuple(sorted({net.line(p) for p in at})), frozenset(reach(net, at, included)))
             for (w, c), at in sorted(at_.items())]
    declared = declarations(net, set(pop))
    problems += [f"{w} is declared {len(declared.get(w, []))} times; the census accounts for one declaration"
                 for w in sorted(pop) if len(declared.get(w, [])) != 1]
    tally = {"declaration": 0, "connection": 0, "read": 0}
    if pop:
        names = re.compile(r"(?<![A-Za-z0-9_$])(" + "|".join(map(re.escape, sorted(pop, key=len, reverse=True)))
                           + r")(?![A-Za-z0-9_$])")
        for m in names.finditer(net.code):
            kind = ("declaration" if m.start() in declared.get(m.group(1), ()) else
                    "connection" if m.start() in connected else "read" if m.start() in read_at else None)
            if kind:
                tally[kind] += 1
            else:
                problems.append(f"unaccounted occurrence of {m.group(1)} at `{net.text_at(m.start())}` (line "
                                f"{net.line(m.start())}): not its declaration, the wrapper's connection or a read")
        for rel in includes(src.datapath, net.code):
            copies = src.included.get(rel, ())
            if not copies:
                problems.append(f"the datapath includes {rel or 'a file'}, which the census cannot find under hdl/ "
                                f"or configs/: it cannot see what that file reads")
            for path, text in copies:
                problems += [f"{path}: an included file names class-D wire {w}"
                             for w in sorted(set(names.findall(strip_comments(text))))]
    problems += outright(net, pop, found)
    return Survey(pop, found, tally, problems)


def fields(contract: mailbox_model.Contract) -> set[str]:
    """REGISTER.FIELD of every publication register."""
    return {f"{r.name}.{f.name}" for r in contract.pub_registers + contract.pub_sink_registers for f in r.fields}


def findings(src: Sources, table: dict[tuple[str, str], Row], known: set[str]) -> tuple[list[str], Survey]:
    """Every way the sources and the census disagree."""
    sv = survey(src)
    out = list(sv.problems)
    for r in sv.reads:
        row = table.get((r.wire, r.consumer))
        where = f"{r.wire} -> {r.consumer} (line {', '.join(map(str, r.lines))})"
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
    """The sources as tracked: each included file found under INCLUDE_ROOTS, every copy of it."""
    text = datapath.read_text(encoding="utf-8")
    found = {}
    for rel in includes(text, strip_comments(text)):
        hits = [p for root in INCLUDE_ROOTS for p in sorted(root.rglob(Path(rel).name))
                if rel and p.as_posix().endswith("/" + rel)]
        found[rel] = tuple((p.relative_to(REPO).as_posix(), p.read_text(encoding="utf-8")) for p in hits)
    return Sources(text, wrapper.read_text(encoding="utf-8"), found)


def selftest(src: Sources, known: set[str]) -> int:
    """Each plant refused by its own words, the controls clean; the number of failed arms."""
    failed = 0
    clean, _ = findings(src, CENSUS, known)
    print(f"[{'ok' if not clean else 'BAD'}] positive control, the tracked sources: {len(clean)} finding(s)")
    failed += bool(clean)
    note = replace(src, datapath=src.datapath.replace(
        "  wire crft_class_a_w =", "  // pp_cd_srp_over_limit_w is not read here\n  wire crft_class_a_w =", 1))
    quiet, _ = findings(note, CENSUS, known)
    print(f"[{'ok' if not quiet else 'BAD'}] negative control, a class-D wire named in a comment: "
          f"{len(quiet)} finding(s)")
    failed += bool(quiet)
    arms = [(p.what, apply(src, p), CENSUS, p.word) for p in PLANTS]
    key = ("pp_cd_srp_tk_decl_state_w", "crft_class_a_w")
    arms.append(("a field the contract lacks", src, {**CENSUS, key: Row("field", "TALKER_DECL.DECLARE", "")},
                 "which the publication block does not define"))
    arms.append(("a stale row", src, {**CENSUS, ("pp_cd_srp_granted_slope_bps_w", "lwsrp_idle_slope"):
                                      Row("status", "", "planted")},
                 "stale row: the datapath no longer reads pp_cd_srp_granted_slope_bps_w"))
    for what, planted, table, word in arms:
        if isinstance(planted, str):
            print(f"[BAD] planted {what}: {planted}")
            failed += 1
            continue
        try:
            got, _ = findings(planted, table, known)
        except CensusError as exc:
            got = [f"the census cannot read it: {exc}"]
        words = (word,) if isinstance(word, str) else word
        hit = [f for f in got if all(w in f for w in words)]
        print(f"[{'ok' if hit else 'BAD'}] planted {what}: " + (f"refused ({hit[0]})" if hit else "accepted"))
        failed += not hit
    print(f"selftest: {failed} of {len(arms) + 2} arm(s) failed")
    return failed


def main(argv: list[str] | None = None) -> int:
    """--check, --list and --selftest over the datapath; the exit status."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--check", action="store_true", help="fail on any occurrence the census does not account for")
    ap.add_argument("--list", action="store_true", help="print the population, and every read, its cone and its row")
    ap.add_argument("--selftest", action="store_true", help="prove the check refuses each planted defect")
    ap.add_argument("--datapath", type=Path, default=DATAPATH, help="the datapath to read")
    ap.add_argument("--wrapper", type=Path, default=WRAPPER_SV,
                    help="the processor wrapper whose class-D face it reads")
    args = ap.parse_args(argv)
    if not (args.check or args.list or args.selftest):
        ap.error("name --check, --list or --selftest")
    known = fields(mailbox_model.load())
    rc = 0
    try:
        src = load(args.datapath, args.wrapper)
        out, sv = findings(src, CENSUS, known)
        if args.list:
            for wire, (port, _) in sorted(sv.population.items(), key=lambda kv: kv[1][0]):
                print(f"{port:26} -> {wire}")
            for r in sv.reads:
                row = CENSUS.get((r.wire, r.consumer))
                ends = ", ".join(sorted({k for k, _ in r.ends}))
                print(f"{r.wire:30} -> {r.consumer:24} lines {','.join(map(str, r.lines)):12} reaches {ends:22} "
                      f"{row.kind + ' ' + row.field if row else 'UNMAPPED'}")
        if args.check:
            for f in out:
                print(f"[FAIL] {f}")
            wires = len({r.wire for r in sv.reads})
            print(f"== publication census: checks: {len(sv.reads)}   failures: {len(out)} ==")
            print(f"{len(sv.population)} class-D wire(s) from the wrapper's ports; occurrences accounted: "
                  + ", ".join(f"{n} {k}(s)" for k, n in sv.tally.items()))
            print(f"{len(sv.reads)} read(s) of {wires} class-D wire(s); RESULT: {'PASS' if not out else 'FAIL'}")
            rc |= bool(out)
        if args.selftest:
            rc |= bool(selftest(src, known))
    except CensusError as exc:
        print(f"[FAIL] the census cannot read {args.datapath}: {exc}")
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())

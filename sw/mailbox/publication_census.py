#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""publication_census.py - every read of the processor's class-D outputs, mapped.

THE QUESTION. In the split placement the fabric datapath no longer has the
protocol processor: the firmware owns ADP, ACMP, MAAP and SRP and writes what
the datapath consumes into the mailbox's publication block (#665, ruling
6088423771, decision 2 (a)). Which values the block must carry is decided by
what ``hdl/milan/milan_datapath.sv`` reads, and a list copied by hand missed
two of them (#665, comment 6092086337). This check derives the list from the
datapath every time and fails when a read is not accounted for.

THE POPULATION. Every ``pp_cd_*_w`` wire, which the processor wrapper
(``KL_pp_shadow``) drives from its class-D face, and ``pp_aecp_strm_started_w``,
each sink's started level, which the ruling of comment 6092086337 adds: the
wrapper drives it from the ACMP binding record, and the listener accept reads
it.

THE READS. The datapath is cut into statements. A read is an occurrence of a
population wire in a statement's right-hand side, in an index of its target,
in the condition of an ``if``, ``case`` or ``for`` that controls it (inside an
``always`` block, every target of the block), or in a module instance's port
connection. Declarations with an initialiser (``wire x = ...``) are statements
like any other. Comments and strings are blanked first. A read is keyed by the
wire and its consumer: the signal the statement drives, or ``instance.port``.

THE CONE. From each consumer the check follows every statement that reads it,
transitively, to a terminal: a port of the CSR block (``milan_csr``, read-back
status), a port of the processor wrapper itself (its GET_STREAM_INFO answer
face), or anything else, which is the wire: another module's port or a module
output. Always blocks are followed as a whole, so the cone over-approximates:
a path it cannot rule out counts as reaching the wire.

THE CENSUS. ``CENSUS`` names every read once:

  field      the read reaches the wire; the block field that carries the
             value in the split placement, which the contract must define
  status     the read reaches CSR read-back only, through the ports
             ``CSR_READBACK`` lists (a field may be named: published anyway)
  processor  the read reaches the wrapper's own GET_STREAM_INFO face only
             (``PROCESSOR_FACE``), which needs no publication: after F5 the
             core answers it (ruling 6088423771, decision 2)

and fails on a read the census does not name, a row no read matches, a status
or processor read whose cone reaches the wire or a port the lists do not name,
a field read whose cone does not reach the wire, and a field the contract does
not define.

    python3 sw/mailbox/publication_census.py --check
    python3 sw/mailbox/publication_census.py --list
    python3 sw/mailbox/publication_census.py --selftest

``--selftest`` plants an unmapped read into copies of the datapath (on the
wire, in a declaration's initialiser, in an always block's condition), points
a status and a processor read at the wire, names a field the contract lacks
and adds a stale row, and requires each to be refused; the tracked datapath,
and a copy whose only change is a comment naming a class-D wire, must pass.
"""

from __future__ import annotations

import argparse
import bisect
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mailbox_model  # noqa: E402

REPO = HERE.parent.parent
DATAPATH = REPO / "hdl/milan/milan_datapath.sv"

#: The wrapper's class-D wires, and the started level the ruling adds.
POPULATION = re.compile(r"\bpp_cd_\w+_w\b")
STARTED = "pp_aecp_strm_started_w"
WRAPPER = "KL_pp_shadow"
CSR = "milan_csr"


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

KEYWORDS = frozenset("""
    assign wire logic reg begin end else if for case casez casex unique unique0 priority endcase default
    always always_comb always_ff always_latch posedge negedge or and generate endgenerate genvar localparam
    parameter input output inout signed unsigned int integer automatic function endfunction return initial
    typedef struct packed enum foreach while do module endmodule import export bit byte shortint longint
    string var const static""".split())
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_$]*)*")
LEAD = re.compile(r"\s*(begin|end|else|generate|endgenerate)\b(\s*:\s*\w+)?")
LEAD_COND = re.compile(r"\s*(if|for)\s*\(")
INST_TYPE = re.compile(r"\s*([A-Za-z_]\w*)\s*(#\s*\()?")
INST_NAME = re.compile(r"\s*([A-Za-z_]\w*)\s*\(")
CONTROL = re.compile(r"\b(if|case|casez|casex|for|while)\s*\(")
OUTPUT_DECL = re.compile(r"\boutput\s+(?:wire\s+|logic\s+|reg\s+)?(?:signed\s+)?(?:\[[^\]]*\]\s*)*(\w+)")


class CensusError(ValueError):
    """The datapath could not be read the way the census reads it."""


def strip_comments(text: str) -> str:
    """The text with comments and string bodies blanked, newlines kept."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append("".join(c if c == "\n" else " " for c in text[i:j]))
        elif text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            j = min(n, j + 1)
            out.append('"' + " " * max(0, j - i - 2) + ('"' if j - i >= 2 else ""))
        else:
            j = i + 1
            out.append(text[i])
        i = j
    return "".join(out)


def close_of(text: str, i: int) -> int:
    """The index just past the bracket group that opens at text[i]."""
    depth = 0
    for j in range(i, len(text)):
        if text[j] in "([{":
            depth += 1
        elif text[j] in ")]}":
            depth -= 1
            if depth == 0:
                return j + 1
    raise CensusError(f"an unbalanced bracket group opens at offset {i}")


def statements(code: str) -> list[tuple[int, int]]:
    """(start, end) of every statement: text up to a ';' outside brackets."""
    out, depth, start = [], 0, 0
    for i, c in enumerate(code):
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == ";" and depth == 0:
            out.append((start, i))
            start = i + 1
    if depth:
        raise CensusError("the datapath's brackets do not balance")
    return out


def assignment(text: str) -> tuple[int, int] | None:
    """(offset, length) of a statement's '=' or '<=' outside brackets."""
    depth = 0
    for i, c in enumerate(text):
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif depth == 0 and c == "=":
            prev = text[i - 1] if i else " "
            if text[i + 1:i + 2] == "=" or prev in "=!>":
                continue
            if prev == "<":
                if text[i - 2:i - 1] == "<":
                    continue
                return i - 1, 2
            return i, 1
    return None


def lvalues(lhs: str) -> tuple[list[str], int]:
    """The signals a left-hand side drives, and where they start in it."""
    k = len(lhs.rstrip())
    while k and lhs[k - 1] == "]":
        depth, m = 0, k - 1
        while m >= 0:
            depth += {"]": 1, "[": -1}.get(lhs[m], 0)
            if depth == 0:
                break
            m -= 1
        k = len(lhs[:m].rstrip())
    if k and lhs[k - 1] == "}":
        m = lhs.rfind("{", 0, k)
        return [t for t in IDENT.findall(lhs[m:k]) if t not in KEYWORDS], m
    m = k
    while m and (lhs[m - 1].isalnum() or lhs[m - 1] in "_$."):
        m -= 1
    name = lhs[m:k]
    return ([name] if name and name not in KEYWORDS else []), m


def reads(text: str, base: int) -> list[tuple[int, str]]:
    """Every signal named in text, at its absolute offset; literals' base
    letters and system names are not signals, and a.b reads a."""
    out = []
    for m in IDENT.finditer(text):
        name = m.group()
        before = text[m.start() - 1] if m.start() else " "
        if name in KEYWORDS or before in "'$`":
            continue
        out.append((base + m.start(), name.split(".")[0]))
    return out


@dataclass
class Netlist:
    """The datapath as statements: who reads what, and where it ends."""

    code: str
    edges: dict[str, set[str]]
    reads_at: list[tuple[int, str, str]]
    instances: dict[str, set[str]]
    outputs: set[str]
    newlines: list[int]

    def line(self, pos: int) -> int:
        """The 1-based source line of a character offset."""
        return bisect.bisect_right(self.newlines, pos)


def always_blocks(code: str, stmts: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """The extent of every always block: its begin to the matching end, or one statement."""
    toks = [(m.start(), m.group()) for m in re.finditer(r"\b(begin|end|always_comb|always_ff|always_latch|always)\b",
                                                         code)]
    out, i = [], 0
    while i < len(toks):
        pos, word = toks[i]
        if word.startswith("always"):
            ev = re.match(r"\s*(@\s*(\([^)]*\)|\*))?\s*", code[pos + len(word):])
            body = pos + len(word) + ev.end()
            if code.startswith("begin", body):
                depth, j = 0, i + 1
                while j < len(toks):
                    depth += {"begin": 1, "end": -1}.get(toks[j][1], 0)
                    if depth == 0:
                        break
                    j += 1
                out.append((pos, toks[j][0] + 3))
                i = j
            else:
                out.append((pos, next(e for s, e in stmts if e > body)))
        i += 1
    return out


def netlist(text: str) -> Netlist:
    """Read the datapath into statements, instances and read edges."""
    code = strip_comments(text)
    stmts = statements(code)
    blocks = always_blocks(code, stmts)
    edges: dict[str, set[str]] = defaultdict(set)
    reads_at: list[tuple[int, str, str]] = []
    instances: dict[str, set[str]] = defaultdict(set)
    block_targets: dict[tuple[int, int], set[str]] = defaultdict(set)
    block_ctrl: dict[tuple[int, int], list[tuple[int, str]]] = defaultdict(list)

    def read(pos: int, name: str, consumer: str) -> None:
        """Record that `consumer` reads `name` at offset `pos`."""
        reads_at.append((pos, name, consumer))
        edges[name].add(consumer)

    for s, e in stmts:
        text_s = code[s:e]
        op = assignment(text_s)
        if op is None:
            lead = text_s
            while True:
                m = LEAD.match(lead)
                if m:
                    lead = lead[m.end():]
                    continue
                m = LEAD_COND.match(lead)
                if m:
                    lead = lead[close_of(lead, m.end() - 1):]
                    continue
                break
            off = s + len(text_s) - len(lead)
            m = INST_TYPE.match(lead)
            if not m or m.group(1) in KEYWORDS:
                continue
            j = close_of(lead, m.end() - 1) if m.group(2) else m.end()
            n = INST_NAME.match(lead, j)
            if not n or n.group(1) in KEYWORDS:
                continue
            inst = n.group(1)
            instances[inst].add(m.group(1))
            open_at = n.end() - 1
            body = lead[open_at + 1:close_of(lead, open_at) - 1]
            for c in re.finditer(r"\.\s*(\w+)\s*\(", body):
                port = c.group(1)
                if port.endswith("_o") or port.startswith("o_"):
                    continue              # an output: the instance drives it
                a = c.end() - 1
                for pos, name in reads(body[a + 1:close_of(body, a) - 1], off + open_at + 1 + a + 1):
                    read(pos, name, f"{inst}.{port}")
            continue
        at, width = op
        lhs = text_s[:at]
        targets, start = lvalues(lhs)
        blk = next((b for b in blocks if b[0] <= s + at < b[1]), None)
        for t in targets:
            for pos, name in reads(text_s[at + width:], s + at + width):
                read(pos, name, t)
            for pos, name in reads(lhs[start:], s + start):
                if name not in targets:
                    read(pos, name, t)
            if blk:
                block_targets[blk].add(t)
        ctrl = []
        for c in CONTROL.finditer(lhs[:start]):
            a = c.end() - 1
            ctrl += reads(lhs[a + 1:close_of(lhs, a) - 1], s + a + 1)
        if blk:
            block_ctrl[blk] += ctrl
        else:
            for t in targets:
                for pos, name in ctrl:
                    read(pos, name, t)
    for blk, ctrl in block_ctrl.items():
        for t in block_targets[blk]:
            for pos, name in ctrl:
                read(pos, name, t)
    newlines = [0] + [m.end() for m in re.finditer("\n", code)]
    return Netlist(code, edges, reads_at, instances, set(OUTPUT_DECL.findall(code)), newlines)


def terminal(net: Netlist, node: str) -> tuple[str, str] | None:
    """(class, name) when node ends a cone: a CSR port, a wrapper port, the wire."""
    if "." in node:
        inst, port = node.split(".", 1)
        kinds = net.instances.get(inst, set())
        if kinds == {CSR}:
            return "csr", port
        if kinds == {WRAPPER}:
            return "processor", port
        return "wire", node
    if node in net.outputs:
        return "wire", node
    return None


def cone(net: Netlist, start: str) -> set[tuple[str, str]]:
    """Every terminal a consumer reaches."""
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
        stack.extend(net.edges.get(node, ()))
    return out


@dataclass(frozen=True)
class Read:
    """One (wire, consumer) read: its lines and its cone."""

    wire: str
    consumer: str
    lines: tuple[int, ...]
    ends: frozenset[tuple[str, str]]


def census(text: str) -> tuple[list[Read], Netlist]:
    """Every read of a population wire in the datapath, with its cone."""
    net = netlist(text)
    if not any(kinds == {WRAPPER} for kinds in net.instances.values()):
        raise CensusError(f"the datapath instantiates no {WRAPPER}: nothing drives the class-D wires")
    if not any(kinds == {CSR} for kinds in net.instances.values()):
        raise CensusError(f"the datapath instantiates no {CSR}")
    population = set(POPULATION.findall(net.code)) | {STARTED}
    lines: dict[tuple[str, str], set[int]] = defaultdict(set)
    for pos, name, consumer in net.reads_at:
        if name in population:
            lines[(name, consumer)].add(net.line(pos))
    return [Read(w, c, tuple(sorted(ln)), frozenset(cone(net, c))) for (w, c), ln in sorted(lines.items())], net


def fields(contract: mailbox_model.Contract) -> set[str]:
    """REGISTER.FIELD of every publication register."""
    return {f"{r.name}.{f.name}" for r in contract.pub_registers + contract.pub_sink_registers for f in r.fields}


def findings(text: str, table: dict[tuple[str, str], Row], known: set[str]) -> tuple[list[str], list[Read]]:
    """Every way the datapath and the census disagree."""
    found, net = census(text)
    out = []
    for r in found:
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
            wires = sorted(n for k, n in r.ends if k == "wire")
            if wires:
                out.append(f"{where}: counted as {row.kind}, but it reaches the wire at {', '.join(wires[:4])}")
            if row.kind == "status" and "processor" in kinds:
                out.append(f"{where}: counted as status, but it reaches the processor wrapper")
            # what keeps the read off the wire: only ports reviewed as read-back
            # or as the wrapper's answer face
            for k, port in sorted(r.ends):
                if k == "csr" and port not in CSR_READBACK:
                    out.append(f"{where}: reaches CSR port {port}, which CSR_READBACK does not name")
                if k == "processor" and port not in PROCESSOR_FACE:
                    out.append(f"{where}: reaches wrapper port {port}, which PROCESSOR_FACE does not name")
    seen = {(r.wire, r.consumer) for r in found}
    out += [f"stale row: the datapath no longer reads {w} into {c}" for w, c in table if (w, c) not in seen]
    return out, found


#: (planted defect, old, new, a word the finding must carry): each applied to
#: a copy of the datapath, each old text occurring once.
DATAPATH_PLANTS = (
    ("an unmapped read on the wire",
     "(|pp_cd_srp_tk_decl_state_w[2*CRF_DECL_SLOT_C +: 2]);",
     "(|pp_cd_srp_tk_decl_state_w[2*CRF_DECL_SLOT_C +: 2]) & ~pp_cd_srp_over_limit_w;",
     "unmapped read: pp_cd_srp_over_limit_w -> crft_class_a_w"),
    ("an unmapped read in a declaration's initialiser",
     "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &",
     "  wire planted_w = |pp_cd_srp_granted_slope_bps_w;\n"
     "  wire crft_class_a_w = planted_w & (ACMP_SRC_C > N_STREAMS) &",
     "unmapped read: pp_cd_srp_granted_slope_bps_w -> planted_w"),
    ("an unmapped read in an always block's condition",
     "    crft_stat_c[4]     = 1'b0;",
     "    crft_stat_c[4]     = 1'b0;\n    if (pp_cd_srp_lstn_decl_state_w[0]) crft_stat_c[4] = 1'b1;",
     "unmapped read: pp_cd_srp_lstn_decl_state_w -> crft_stat_c"),
    ("a status read on the wire",
     "    .vlan_en_i  (crft_class_a_w),",
     "    .vlan_en_i  (lwsrp_talker_declared),",
     "counted as status, but it reaches the wire"),
    ("a GET_STREAM_INFO read on the wire",
     "    .vlan_en_i  (crft_class_a_w),",
     "    .vlan_en_i  (gsi_tkdcl_w[0]),",
     "counted as processor, but it reaches the wire"),
    ("the started level dropped from the accept",
     "  wire [ACMP_SINKS_C-1:0] acmpl_stopped_v_w = acmpl_bound_v_w\n"
     "                                              & ~pp_aecp_strm_started_w;",
     "  wire [ACMP_SINKS_C-1:0] acmpl_stopped_v_w = acmpl_bound_v_w\n"
     "                                              & ~pp_cd_acmp_bound_w;",
     "unmapped read: pp_cd_acmp_bound_w -> acmpl_stopped_v_w"),
)


def selftest(text: str, known: set[str]) -> int:
    """Each plant refused, the controls clean; the number of failed arms."""
    failed = 0
    clean, _ = findings(text, CENSUS, known)
    print(f"[{'ok' if not clean else 'BAD'}] positive control, the tracked datapath: {len(clean)} finding(s)")
    failed += bool(clean)
    note = text.replace("  wire crft_class_a_w =", "  // pp_cd_srp_over_limit_w is not read here\n"
                        "  wire crft_class_a_w =", 1)
    quiet, _ = findings(note, CENSUS, known)
    print(f"[{'ok' if not quiet else 'BAD'}] negative control, a class-D wire named in a comment: "
          f"{len(quiet)} finding(s)")
    failed += bool(quiet)
    arms = [(what, text.replace(old, new), CENSUS, word, text.count(old))
            for what, old, new, word in DATAPATH_PLANTS]
    key = ("pp_cd_srp_tk_decl_state_w", "crft_class_a_w")
    renamed = dict(CENSUS)
    renamed[key] = Row("field", "TALKER_DECL.DECLARE", CENSUS[key].why)
    arms.append(("a field the contract lacks", text, renamed, "which the publication block does not define", 1))
    stale = dict(CENSUS)
    stale[("pp_cd_srp_granted_slope_bps_w", "lwsrp_idle_slope")] = Row("status", "", "planted")
    arms.append(("a stale row", text, stale, "stale row: the datapath no longer reads pp_cd_srp_granted_slope_bps_w",
                 1))
    for what, planted, table, word, sites in arms:
        if sites != 1:
            print(f"[BAD] planted {what}: its fixture occurs {sites} times in the datapath")
            failed += 1
            continue
        got, _ = findings(planted, table, known)
        hit = [f for f in got if word in f]
        print(f"[{'ok' if hit else 'BAD'}] planted {what}: " + (f"refused ({hit[0]})" if hit else "accepted"))
        failed += not hit
    print(f"selftest: {failed} arm(s) failed")
    return failed


def main(argv: list[str] | None = None) -> int:
    """--check, --list and --selftest over the datapath; the exit status."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--check", action="store_true", help="fail on any read the census does not account for")
    ap.add_argument("--list", action="store_true", help="print every read, its cone and its row")
    ap.add_argument("--selftest", action="store_true", help="prove the check refuses each planted defect")
    ap.add_argument("--datapath", type=Path, default=DATAPATH, help="the datapath to read")
    args = ap.parse_args(argv)
    if not (args.check or args.list or args.selftest):
        ap.error("name --check, --list or --selftest")
    text = args.datapath.read_text(encoding="utf-8")
    known = fields(mailbox_model.load())
    rc = 0
    try:
        out, found = findings(text, CENSUS, known)
        if args.list:
            for r in found:
                row = CENSUS.get((r.wire, r.consumer))
                ends = ", ".join(sorted({k for k, _ in r.ends}))
                print(f"{r.wire:30} -> {r.consumer:24} lines {','.join(map(str, r.lines)):12} reaches {ends:22} "
                      f"{row.kind + ' ' + row.field if row else 'UNMAPPED'}")
        if args.check:
            for f in out:
                print(f"[FAIL] {f}")
            wires = len({r.wire for r in found})
            print(f"== publication census: checks: {len(found)}   failures: {len(out)} ==")
            print(f"{len(found)} read(s) of {wires} class-D wire(s); RESULT: {'PASS' if not out else 'FAIL'}")
            rc |= bool(out)
        if args.selftest:
            rc |= bool(selftest(text, known))
    except CensusError as exc:
        print(f"[FAIL] the census cannot read {args.datapath}: {exc}")
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())

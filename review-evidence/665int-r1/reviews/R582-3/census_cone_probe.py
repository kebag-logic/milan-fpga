#!/usr/bin/env python3
"""census_cone_probe.py - R582-3 probe of publication_census.py's cone (one hop past the population).

The census accounts for every occurrence of a POPULATION wire (fail closed).
A status or processor read is then cleared by its CONE: the statements that
read its consumer, followed transitively. This probe asks whether that cone is
fail closed too, i.e. whether a status consumer read on the wire through a form
the census's statement parser does not follow is refused.

Usage: census_cone_probe.py <tree>   (a checkout or export of the head)

Part 1 plants, into copies of the datapath text, a status consumer
(lwsrp_talker_declared, CENSUS row "status") and a processor consumer
(gsi_tkdcl_w, row "processor") routed onto the CRF talker's vlan_en_i (the
wire) through forms the census refuses for a population wire: a positional
port, an implicit .name port, a case item label, a function body's return,
and a plain assign as the control. Each arm prints REFUSED or ESCAPED.

Part 2 lists, at the unmodified head, every occurrence of every node the
status/processor cones traverse that the census netlist records neither as a
read, as an assignment target, nor as a declaration: places where the cone
could under-approximate at this head.
"""
import re
import sys
from dataclasses import replace
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import publication_census as pc  # noqa: E402

src = pc.load(tree / "hdl/milan/milan_datapath.sv", tree / "hdl/milan/KL_pp_shadow.sv")
known = pc.fields(pc.mailbox_model.load())
CRF_DECL = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
VLAN_EN = "    .vlan_en_i  (crft_class_a_w),"
PART1 = src.datapath.count(CRF_DECL) == 1 and src.datapath.count(VLAN_EN) == 1


def routed(decl):
    t = src.datapath.replace(CRF_DECL, decl + CRF_DECL, 1)
    return t.replace(VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),", 1)


def forms(sig):
    return [
        ("plain assign (control)", f"  wire probe_w;\n  assign probe_w = {sig}[0];\n"),
        ("positional port", f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({sig}, probe_w);\n"),
        ("implicit .name port", f"  wire probe_w;\n  KL_probe_buf u_probe_dot (.{sig}, .y_o(probe_w));\n"),
        ("case item label", "  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    unique case (1'b1)\n"
                            f"      {sig}[0]: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n  end\n"),
        ("function body return", f"  function automatic logic probe_f();\n    return {sig}[0];\n  endfunction\n"
                                 "  wire probe_w;\n  assign probe_w = probe_f();\n"),
    ]


clean, _ = pc.findings(src, pc.CENSUS, known)
print(f"control: tracked head -> {len(clean)} finding(s)")
escaped = 0
for sig, row in (("lwsrp_talker_declared", "status"), ("gsi_tkdcl_w", "processor")) if PART1 else ():
    for what, decl in forms(sig):
        got, _ = pc.findings(replace(src, datapath=routed(decl)), pc.CENSUS, known)
        verdict = "REFUSED" if got else "ESCAPED"
        escaped += (not got) and not what.startswith("plain")
        print(f"[{verdict}] {row} consumer {sig} routed to vlan_en_i by {what}: "
              + (got[0][:160] if got else "census reports 0 findings, PASS"))
print(f"part 1: {escaped} escaping arm(s) (controls excluded)")

# Part 2: un-modelled occurrences of the cone's intermediate nodes at the head.
net = pc.netlist(src.datapath)
sv = pc.survey(src)
nodes = set()
for r in sv.reads:
    row = pc.CENSUS.get((r.wire, r.consumer))
    if not row or row.kind == "field":
        continue
    seen, stack = set(), [r.consumer]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        if pc.terminal(net, n):
            continue
        stack.extend(net.edges.get(n, ()))
    nodes |= {n for n in seen if "." not in n}
read_pos = {p for p, _, _ in net.reads_at}
decl = pc.declarations(net, nodes)
decl_pos = {p for v in decl.values() for p in v}
target_pos = set()
for s, e in net.stmts:
    t = net.code[s:e]
    op = pc.assignment(t)
    if not op:
        continue
    lhs = t[:op[0]]
    names, start = pc.lvalues(lhs)
    for m in re.finditer(r"[A-Za-z_][\w$]*", lhs[start:]):
        if m.group() in names:
            target_pos.add(s + start + m.start())
gaps = []
for n in sorted(nodes):
    for m in re.finditer(rf"(?<![\w$]){re.escape(n)}(?![\w$])", net.code):
        if m.start() in read_pos or m.start() in decl_pos or m.start() in target_pos:
            continue
        gaps.append((n, net.line(m.start()), net.text_at(m.start())))
print(f"part 2: {len(nodes)} intermediate cone node(s) of status/processor reads; "
      f"{len(gaps)} occurrence(s) the netlist neither reads, targets nor declares:")
for n, ln, txt in gaps:
    print(f"  {n} line {ln}: {txt}")

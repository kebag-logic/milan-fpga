#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit the read-path lockstep top for one CSR shape (lane M5 of #640).

The lockstep leg runs the current hdl/common/csr/milan_csr.sv beside
milan_csr_ref.sv, a frozen copy of the block as dev e8454e27 shipped it, with
the read path that lane M5 restructured. Both instances see the SAME inputs
every cycle and every output of the two is compared every cycle, so the
reference is an oracle for the whole module, not only for the read path.

The top is generated at build time, into the build directory, from the
module's own port list, so it can never omit a port the block grows:
  * every input except aclk/aresetn is a slice of one stimulus vector `stim`
    the harness writes as a whole (randomised) or by field name;
  * every DUT output is a slice of `dout`, which the harness reads by name;
  * `mism[k]` is 1 while output k differs between the two instances.
lockstep_ports.h carries the field tables the harness addresses them by, and
the map's register addresses so random traffic can aim at mapped words.

The reference is refused unless it is the e8454e27 block byte for byte
(module name aside): its SHA-256 with `milan_csr_ref` read back as
`milan_csr` must be REF_SHA256_C. The two port lists must be identical too;
identical function behind a different interface is not this lane's claim.

usage: gen_lockstep.py <dut.sv> <ref.sv> <outdir> NAME=VALUE...
       (the NAME=VALUE pairs are the milan_csr parameters of the shape)
"""

import ast
import hashlib
import operator
import re
import sys
from pathlib import Path

#: SHA-256 of hdl/common/csr/milan_csr.sv at dev e8454e27 (git blob 3392e01a)
REF_SHA256_C = "c3106a1410035f33eef9e634750ffc534be4d04293263bdbfd4ea144dfd523d8"
REF_MODULE_C = "module milan_csr_ref #("
DUT_MODULE_C = "module milan_csr #("
#: inputs the harness drives as ports of their own, never through `stim`
OWN_PORTS_C = ("aclk", "aresetn")
PORT_RE = re.compile(r"^\s*(input|output)\s+(?:wire|logic)?\s*(\[[^\]]+\])?\s*(\w+)\s*,?",
                     re.M)
ADDR_RE = re.compile(r"\b(A_[A-Z0-9_]+)\s*=\s*'h([0-9A-Fa-f]+)")
ARITH = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
         ast.FloorDiv: operator.floordiv}


def arith(expr: str, params: dict[str, int]) -> int:
    """Evaluate a port-width bound: integers, parameters, + - * and /."""
    def walk(node: ast.AST) -> int:
        """One node of the bound's expression tree."""
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return node.value
        if isinstance(node, ast.Name) and node.id in params:
            return params[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in ARITH:
            return ARITH[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError(f"port width bound not understood: {expr!r}")
    return walk(ast.parse(expr.replace("/", "//"), mode="eval").body)


def ports(text: str, params: dict[str, int]) -> list[tuple[str, str, int]]:
    """[(direction, name, width)] of the module header in `text`.

    The header runs from its `)(` line to its own `);` line; a `);` inside a
    port comment does not end it.
    """
    start = re.search(r"^\)\(\s*$", text, re.M)
    end = re.search(r"^\);\s*$", text[start.end():], re.M) if start else None
    if not start or not end:
        raise SystemExit("gen_lockstep: no `)(` ... `);` port header found")
    head = text[start.end():start.end() + end.start()]
    found = []
    for m in PORT_RE.finditer(head):
        width = 1
        if m.group(2):
            hi, lo = m.group(2)[1:-1].split(":")
            width = arith(hi.strip(), params) - arith(lo.strip(), params) + 1
        found.append((m.group(1), m.group(3), width))
    declared = len(re.findall(r"^\s*(?:input|output)\b", head, re.M))
    if len(found) != declared:
        raise SystemExit(f"gen_lockstep: parsed {len(found)} ports of {declared} declared; "
                         f"a port the top omits is an output nobody compares")
    return found


def checked_reference(ref_text: str) -> None:
    """Refuse a reference that is not the frozen e8454e27 block."""
    if ref_text.count(REF_MODULE_C) != 1:
        raise SystemExit(f"gen_lockstep: the reference must declare {REF_MODULE_C!r} once")
    digest = hashlib.sha256(ref_text.replace(REF_MODULE_C, DUT_MODULE_C).encode()).hexdigest()
    if digest != REF_SHA256_C:
        raise SystemExit(f"gen_lockstep: milan_csr_ref.sv is not the e8454e27 block "
                         f"(sha256 {digest}, expected {REF_SHA256_C}); the oracle "
                         f"must be the implementation the lane replaced, unedited")


def emit_top(plist: list[tuple[str, str, int]], params: dict[str, int]) -> str:
    """The SystemVerilog lockstep top for one shape."""
    ins = [(n, w) for d, n, w in plist if d == "input" and n not in OWN_PORTS_C]
    outs = [(n, w) for d, n, w in plist if d == "output"]
    in_w = sum(w for _, w in ins)
    out_w = sum(w for _, w in outs)
    pmap = ", ".join(f".{k}({v})" for k, v in params.items())
    lines = ["// GENERATED by tb/verilator/csr/gen_lockstep.py - do not edit",
             "`default_nettype none", "module csr_lockstep_top (",
             "  input  wire aclk,", "  input  wire aresetn,",
             f"  input  wire [{in_w - 1}:0] stim,",
             f"  output wire [{out_w - 1}:0] dout,",
             f"  output wire [{len(outs) - 1}:0] mism", ");"]
    for n, w in outs:
        lines.append(f"  wire [{w - 1}:0] d_{n}, r_{n};")
    for inst, mod, pre in (("dut", "milan_csr", "d_"), ("ref_i", "milan_csr_ref", "r_")):
        conns = ["    .aclk(aclk)", "    .aresetn(aresetn)"]
        off = 0
        for n, w in ins:
            conns.append(f"    .{n}(stim[{off} +: {w}])")
            off += w
        conns += [f"    .{n}({pre}{n})" for n, _ in outs]
        lines.append(f"  {mod} #({pmap}) {inst} (")
        lines.append(",\n".join(conns))
        lines.append("  );")
    off = 0
    for k, (n, w) in enumerate(outs):
        lines.append(f"  assign dout[{off} +: {w}] = d_{n};")
        lines.append(f"  assign mism[{k}] = (d_{n} != r_{n});")
        off += w
    lines += ["endmodule", "`default_nettype wire", ""]
    return "\n".join(lines)


def emit_header(plist: list[tuple[str, str, int]], addrs: list[int]) -> str:
    """The C++ field tables the harness addresses the vectors by."""
    ins = [(n, w) for d, n, w in plist if d == "input" and n not in OWN_PORTS_C]
    outs = [(n, w) for d, n, w in plist if d == "output"]
    lines = ["// GENERATED by tb/verilator/csr/gen_lockstep.py - do not edit",
             "#pragma once",
             "struct LockField { const char* name; int off; int width; };"]
    for tag, fields in (("IN", ins), ("OUT", outs)):
        lines.append(f"static const LockField LOCK_{tag}[] = {{")
        off = 0
        for n, w in fields:
            lines.append(f"  {{\"{n}\", {off}, {w}}},")
            off += w
        lines.append("};")
        lines.append(f"static const int LOCK_{tag}_N = {len(fields)};")
        lines.append(f"static const int LOCK_{tag}_W = {off};")
    lines.append("static const unsigned LOCK_ADDRS[] = {")
    lines += [f"  0x{a:03X}u," for a in addrs]
    lines.append("};")
    lines.append(f"static const int LOCK_ADDRS_N = {len(addrs)};")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    """Check the reference, then write the top and the header for one shape."""
    if len(argv) < 4:
        print(__doc__)
        return 2
    dut_text = Path(argv[1]).read_text()
    ref_text = Path(argv[2]).read_text()
    outdir = Path(argv[3])
    params = {}
    for pair in argv[4:]:
        name, value = pair.split("=", 1)
        params[name] = int(value, 0)
    checked_reference(ref_text)
    plist = ports(dut_text, params)
    if plist != ports(ref_text, params):
        raise SystemExit("gen_lockstep: the block's port list differs from the reference's")
    addrs = sorted({int(v, 16) for _, v in ADDR_RE.findall(dut_text)})
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "csr_lockstep_top.sv").write_text(emit_top(plist, params))
    (outdir / "lockstep_ports.h").write_text(emit_header(plist, addrs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate a base-versus-head lockstep harness for one SRP module at one shape.

The base module is renamed B_<module> (a copy of the base RTL with its module
name prefixed); the head module keeps its name. Both see the same inputs every
cycle; the wrapper raises one mismatch bit per output port. The C++ driver
draws every input from a seeded PRNG, with small shared value pools for the
matcher keys so declarations and received values meet.

usage: gen_lockstep.py <head.sv> <module> <count-param> <N> <outdir>
"""
import math
import re
import sys
from pathlib import Path

head_sv, module, nparam, n, outdir = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
text = "\n".join(l.split("//")[0] for l in Path(head_sv).read_text().splitlines())
start = text.index(f"module {module}")
plist = text.index(") (", start)
end = text.index(");", plist)
ports_txt = text[plist + 3:end]

idx_w = max(1, math.ceil(math.log2(n))) if n > 1 else 1
env = {nparam: n, "SRC_W_C": idx_w, "SNK_W_C": idx_w, "SLOT_AW_P": 7, "N_VIDS_P": 4,
       "N_SOURCES_P": n, "N_SINKS_P": n}

port_re = re.compile(r"^\s*(input|output)\s+(?:wire|logic)\s*((?:\[[^\]]*\]\s*)*)(\w+)\s*,?", re.M)
ports = []
for line in ports_txt.splitlines():
    code = line.split("//")[0]
    m = port_re.match(code)
    if not m:
        continue
    width = 1
    for dim in re.findall(r"\[([^\]]*)\]", m.group(2)):
        msb, lsb = dim.split(":")
        width *= eval(msb, {}, env) - eval(lsb, {}, env) + 1
    ports.append((m.group(1), width, m.group(3)))

ins = [p for p in ports if p[0] == "input"]
outs = [p for p in ports if p[0] == "output"]
decl = lambda w: f"[{w - 1}:0] " if w > 1 else ""

sv = [f"module ls_wrap (\n    output logic [{len(outs) - 1}:0] mm_o,\n    output logic [{len(outs) - 1}:0] act_o,"]
sv += [f"    input  wire {decl(w)}{name}," for _, w, name in ins]
sv[-1] = sv[-1].rstrip(",")
sv.append(");")
for _, w, name in outs:
    sv.append(f"  wire {decl(w)}a_{name}, b_{name};")
for tag, mod in (("a", f"B_{module}"), ("b", module)):
    conns = [f".{name}({name})" for _, _, name in ins] + [f".{name}({tag}_{name})" for _, _, name in outs]
    sv.append(f"  {mod} #(.{nparam}({n})) u_{tag} (\n    " + ",\n    ".join(conns) + ");")
for i, (_, _, name) in enumerate(outs):
    sv.append(f"  assign mm_o[{i}] = (a_{name} != b_{name});")
    sv.append(f"  assign act_o[{i}] = |b_{name};")
sv.append("endmodule")
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "ls_wrap.sv").write_text("\n".join(sv) + "\n")

cpp = ['#include "drive.hpp"', "void drive_inputs(Vls_wrap* d, Drv& g) {"]
for _, w, name in ins:
    if name == "clk_i":
        continue
    if w > 64:
        cpp.append(f"  for (int i = 0; i < {(w + 31) // 32}; ++i) d->{name}[i] = g.word(\"{name}\", i, {w});")
    else:
        cpp.append(f"  d->{name} = g.value(\"{name}\", {w});")
cpp.append("}")
cpp.append("const char* OUT_NAMES[] = {" + ", ".join(f'"{name}"' for _, _, name in outs) + "};")
cpp.append(f"const int N_OUT = {len(outs)};")
cpp.append(f"const int N_CTX = {n};")
(outdir / "drive_gen.cpp").write_text("\n".join(cpp) + "\n")
print(f"{module} N={n}: {len(ins)} inputs, {len(outs)} outputs")

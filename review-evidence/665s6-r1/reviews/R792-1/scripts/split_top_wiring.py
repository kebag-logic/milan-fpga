#!/usr/bin/env python3
"""Reviewer probe: in a split SoC's generated top-level Verilog, are KL_mbx and milan_datapath
joined only through KL_mbx_cdc and the control-frame FIFOs, and is KL_mbx_cdc on the right clocks?

Usage: split_top_wiring.py <gateware/top.v>

Reads the three instances' port bindings, resolves plain `assign a = b;` aliases, and reports:
  - the clocks and resets each side of KL_mbx_cdc binds;
  - every net KL_mbx and milan_datapath share directly (after aliasing), which would be a
    crossing outside KL_mbx_cdc (the CSR/system nets are listed so a reader can judge them);
  - how many ctl ports bind KL_mbx_cdc, and which reach neither KL_mbx_cdc nor a FIFO net.
"""
import re
import sys
from collections import defaultdict

text = open(sys.argv[1], encoding="utf-8", errors="replace").read()


def instance(module):
    m = re.search(r"^\s*" + re.escape(module) + r"\b[^;]*?\(\s*\n(.*?)\n\s*\);", text, re.S | re.M)
    if not m:
        sys.exit(f"no instance of {module}")
    ports = {}
    for p, expr in re.findall(r"\.([A-Za-z_][A-Za-z0-9_]*)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)", m.group(1)):
        ports[p] = expr.strip()
    return ports


def nets(expr):
    return set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", re.sub(r"\d+'[bhdo][0-9a-fA-F_xz]+", "", expr)))


alias = defaultdict(set)
for a, b in re.findall(r"^\s*assign\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z_][A-Za-z0-9_]*)\s*;", text, re.M):
    alias[a].add(b)
    alias[b].add(a)


def closure(ns):
    out, todo = set(ns), list(ns)
    while todo:
        n = todo.pop()
        for m in alias.get(n, ()):
            if m not in out:
                out.add(m)
                todo.append(m)
    return out


mbx, cdc, dp = instance("KL_mbx"), instance("KL_mbx_cdc"), instance("milan_datapath")
print("KL_mbx_cdc clocks and resets:")
for p in ("sys_clk_i", "sys_rst_n", "dp_clk_i", "dp_rst_n"):
    print(f"  .{p}({cdc.get(p)})")
print(f"milan_datapath .axis_clk({dp.get('axis_clk')})   KL_mbx .clk_i({mbx.get('clk_i')})")

mbx_nets = closure(set().union(*(nets(e) for e in mbx.values())))
dp_nets = closure(set().union(*(nets(e) for e in dp.values())))
shared = sorted(mbx_nets & dp_nets)
print(f"\nnets KL_mbx and milan_datapath share directly: {len(shared)}")
for n in shared:
    print(f"  {n}")

ctl = {p: e for p, e in dp.items() if re.match(r"[io]_ctl_", p)}
cdc_nets = closure(set().union(*(nets(e) for p, e in cdc.items() if p.startswith("d_"))))
via_cdc = [p for p, e in ctl.items() if closure(nets(e)) & cdc_nets]
rest = sorted(set(ctl) - set(via_cdc))
print(f"\nctl ports on milan_datapath: {len(ctl)}; bound to KL_mbx_cdc's d_* side: {len(via_cdc)}")
print("ctl ports not bound to KL_mbx_cdc (the frame ports, which the FIFOs carry):")
for p in rest:
    print(f"  .{p}({ctl[p]})")
m_side = closure(set().union(*(nets(e) for p, e in cdc.items() if p.startswith("m_"))))
print(f"\nKL_mbx_cdc m_* ports whose net reaches KL_mbx's bindings: "
      f"{sum(1 for p, e in cdc.items() if p.startswith('m_') and closure(nets(e)) & mbx_nets)} of "
      f"{sum(1 for p in cdc if p.startswith('m_'))}")

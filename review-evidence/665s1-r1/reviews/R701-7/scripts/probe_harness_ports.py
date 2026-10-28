#!/usr/bin/env python3
"""Probe: KL_mbx's declared ports (hdl/milan/mailbox/KL_mbx.sv) against the ports the
CPU budget harness's split_soc.py instance connects. usage: probe_harness_ports.py <checkout>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
sv = (root / 'hdl/milan/mailbox/KL_mbx.sv').read_text()
head = sv[sv.index('module KL_mbx'):]
head = head[:head.index(');')]
decl = {n for n in re.findall(r'\b(?:input|output)\b[^;,]*?\b(\w+)\s*(?:,|$)', head, re.M) if n.endswith(('_i', '_o'))}
py = (root / 'tb/verilator/ctrl_service_budget/split_soc.py').read_text()
inst = py[py.index("Instance('KL_mbx',"):]
inst = inst[:inst.index('def FlashBoundary') if 'def FlashBoundary' in inst else len(inst)]
conn = {m[2:] for m in re.findall(r'\b([io]_\w+)=', inst)}
print('KL_mbx ports declared:', len(decl))
print('harness-connected:', len(conn & decl))
miss = sorted(decl - conn)
print('declared but not connected by the harness:', len(miss))
print('  inputs left unconnected:', ' '.join(p for p in miss if p.endswith('_i')))
print('  outputs left unconnected:', len([p for p in miss if p.endswith('_o')]))

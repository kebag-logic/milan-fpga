#!/usr/bin/env python3
"""cone_extract.py <netlist.v> <out-dir>: textual cone of the fetch and load PMA fault terms of module VexiiRiscv.

Independent of the PR's decode.py: copies every one-line `assign` (and its declaration) that the two fault
terms reach, stopping at the PMA command inputs, into a standalone module `pma_cone` for Verilator. Any signal
reached that has no one-line assign and is not a cut input is refused (it would be state or a port).
"""
import re, sys
from pathlib import Path

CUT = {'FetchL1Plugin_logic_ctrl_pmaPort_cmd_address': 32, 'LsuCachelessPlugin_logic_onPma_port_cmd_address': 32,
       'LsuCachelessPlugin_logic_onPma_port_cmd_size': None, 'LsuCachelessPlugin_logic_onPma_port_cmd_op': None}
OUTS = ('FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault', 'LsuCachelessPlugin_logic_onPma_port_rsp_fault')
text = Path(sys.argv[1]).read_text()
body = re.search(r'^module VexiiRiscv \((.*?)^endmodule', text, re.S | re.M).group(1)
assigns = dict(re.findall(r'^\s*assign (\w+) = (.*);\s*$', body, re.M))
decls = {m.group(3): m.group(0).strip() for m in
         re.finditer(r'^\s*(wire|reg)\s+(\[\d+:\d+\]\s+)?(\w+)\s*;', body, re.M)}
ident = re.compile(r"(?<!['\w])([A-Za-z_]\w*)")
need, todo = [], list(OUTS)
seen = set()
while todo:
    n = todo.pop()
    if n in seen or n in CUT:
        continue
    seen.add(n)
    if n not in assigns:
        sys.exit(f'REFUSED: {n} has no one-line assign (state, port or multi-line)')
    rhs = re.sub(r"\d+'[bhd][0-9a-fA-F_]+", ' ', assigns[n])
    todo += [i for i in ident.findall(rhs)]
    need.append(n)
widths = {}
for c in CUT:
    d = decls.get(c, '')
    m = re.search(r'\[(\d+):(\d+)\]', d)
    widths[c] = (int(m.group(1)) - int(m.group(2)) + 1) if m else 1
lines = ['/* verilator lint_off UNUSEDSIGNAL */', '/* verilator lint_off WIDTHEXPAND */', 'module pma_cone(']
ports = [f'  input wire [{w-1}:0] {c}' for c, w in widths.items()] + [f'  output wire {o}_o' for o in OUTS]
lines += [',\n'.join(ports), ');']
for n in need:
    lines.append('  ' + decls[n].replace('reg ', 'wire ', 1))
for n in reversed(need):
    lines.append(f'  assign {n} = {assigns[n]};')
lines += [f'  assign {o}_o = {o};' for o in OUTS] + ['endmodule']
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
(out / 'pma_cone.v').write_text('\n'.join(lines) + '\n')
print(f'cone: {len(need)} assigns; cut inputs {widths}')

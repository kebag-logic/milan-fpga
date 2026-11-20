#!/usr/bin/env python3
"""gateware17.py: does the SRP cut's head (92de01f7) change the split GATEWARE against the step-14 head (c1e95dc1), or only its firmware payload? For each point
(1x1/1if, 8x8/1if), the step-14 head's export (r5fit16) against the new head's export (r8fit): the firmware each carries, the
control memory's rom banks (their depths in the Verilog, their init files), the Verilog outside its comments, the
constraints (as written and as a set), and the placed utilisation of the integrated route (ExtraPostPlacementOpt)."""
import hashlib
import re
from pathlib import Path

S = Path('<scratch>')
POINTS = (('1x1/1if', 'route'), ('8x8/1if', 'route8'))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def code(p: Path, root: str) -> list[str]:
    t = re.sub(r'/\*.*?\*/', '', p.read_text().replace(root, '<S>'), flags=re.S)
    return [l.split('//', 1)[0].rstrip() for l in t.splitlines() if l.split('//', 1)[0].strip()]


def body(p: Path) -> list[str]:
    lines = p.read_text().splitlines()
    return lines[next(i for i, l in enumerate(lines) if l.startswith('1. Slice Logic')):]


print(__doc__.strip().replace('\n', ' '))
for point, w in POINTS:
    a, b = S / f'r5fit16/{w}', S / f'r8fit/{w}'
    ga, gb = a / 'split/gateware', b / 'split/gateware'
    print(f'\n== {point}')
    print(f'firmware (ctrl_app.elf): c1e95dc1 {sha(a / "image/ctrl_app.elf")[:16]}, new head {sha(b / "image/ctrl_app.elf")[:16]}')
    banks = lambda g: re.findall(r'reg +\[31:0\] +([a-z_]*rom_bank\d+\[0:\d+\])', (g / 'alinx_ax7101.v').read_text())
    print(f'rom banks: c1e95dc1 {" ".join(banks(ga))}; new head {" ".join(banks(gb))}'
          f' -> {"SAME depths" if banks(ga) == banks(gb) else "DEPTHS CHANGE"}')
    ca, cb = code(ga / 'alinx_ax7101.v', str(S / 'r5fit16')), code(gb / 'alinx_ax7101.v', str(S / 'r8fit'))
    diff = [(x, y) for x, y in zip(ca, cb) if x != y]
    print(f'Verilog outside comments: {"EQUAL" if ca == cb else f"{len(diff) + abs(len(ca) - len(cb))} line(s) differ"}')
    for x, y in diff[:8]:
        print(f'  - {x.strip()[:110]}\n  + {y.strip()[:110]}')
    for f in sorted(p.name for p in gb.glob('*.init')):
        print(f'init {f}: {"EQUAL" if (ga / f).is_file() and sha(ga / f) == sha(gb / f) else "DIFFERS"}'
              f' ({sum(1 for _ in (gb / f).open())} words written at the new head)')
    xa = (ga / 'alinx_ax7101.xdc').read_text().replace(str(S / 'r5fit16'), '<S>').splitlines()
    xb = (gb / 'alinx_ax7101.xdc').read_text().replace(str(S / 'r8fit'), '<S>').splitlines()
    norm = lambda ls: sorted(re.sub(r'set_clock_groups -group (\[[^]]*\]\]) -group (\[[^]]*\]\])',
                                    lambda m: 'set_clock_groups -group ' + ' -group '.join(sorted(m.groups())), l)
                             for l in ls)
    print(f'constraints: {"EQUAL" if xa == xb else ("the same set (only clock-group pairs written in another order; set_clock_groups -asynchronous is symmetric)" if norm(xa) == norm(xb) else "DIFFER")}')
    if not any(gb.glob('*utilization_place.rpt')):
        print('placed utilisation: not routed at the new head (export only)')
        continue
    ua, ub = body(next(ga.glob('*utilization_place.rpt'))), body(next(gb.glob('*utilization_place.rpt')))
    print(f'placed utilisation (integrated route): {"IDENTICAL, every line" if ua == ub else "differs"}')
    for row in ('Slice LUTs', 'LUT as Memory', 'Slice Registers', 'Block RAM Tile', 'RAMB36/FIFO', 'RAMB18'):
        ra = next((l for l in ua if l.startswith(f'| {row}') or l.startswith(f'|   {row}')), '')
        rb = next((l for l in ub if l.startswith(f'| {row}') or l.startswith(f'|   {row}')), '')
        if ra or rb:
            va, vb = (r.split('|')[2].strip() if r else '-' for r in (ra, rb))
            print(f'  {row}: {va} -> {vb}')

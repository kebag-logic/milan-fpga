#!/usr/bin/env python3
"""Each image's rom layout from its ELF (readelf -SW): .text's size, the padding .rodata's 8-byte alignment puts
after it, .rodata, the .data load image after its 4-byte alignment, and the rom end ctrl_memory.plan reads (the last
loaded section's load address plus its size). usage: rom_layout.py READELF QALL_DIR [QALL_DIR...]"""
import re
import subprocess
import sys
from pathlib import Path

readelf = sys.argv[1]
rows = {}
for top in map(Path, sys.argv[2:]):
    for d in sorted(p for p in top.iterdir() if (p / 'image/ctrl_app.elf').exists()):
        out = subprocess.run([readelf, '-lSW', str(d / 'image/ctrl_app.elf')], capture_output=True, text=True).stdout
        sec = {m[0]: (int(m[1], 16), int(m[2], 16)) for m in re.findall(r'\]\s+(\.\w+)\s+\w+\s+([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)', out)}
        loads = [(int(m[0], 16), int(m[1], 16)) for m in re.findall(r'LOAD\s+0x[0-9a-f]+ 0x[0-9a-f]+ (0x[0-9a-f]+) (0x[0-9a-f]+)', out)]
        text, rodata = sec['.text'], sec['.rodata']
        rom = max(lma + size for lma, size in loads if size)
        pad = rodata[0] - (text[0] + text[1])
        rows.setdefault(d.name, []).append((top.name, text[1], pad, rodata[1], rom))
        print(f'{top.name:>8} {d.name}: .text {text[1]}, pad {pad}, .rodata {rodata[1]}, rom {rom}')
names = [Path(t).name for t in sys.argv[2:]]
for a, b in zip(names, names[1:]):
    print(f'# {a} -> {b}: .text delta, padding delta, rom delta')
    for img, r in rows.items():
        x, y = dict((t[0], t) for t in r)[a], dict((t[0], t) for t in r)[b]
        print(f'#   {img}: .text {y[1]-x[1]:+d}, pad {y[2]-x[2]:+d}, rom {y[4]-x[4]:+d}')

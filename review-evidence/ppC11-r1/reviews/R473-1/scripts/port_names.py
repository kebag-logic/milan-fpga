#!/usr/bin/env python3
"""List every *_i / *_o token on the given Markdown pages and whether it is
declared as an input/output/inout port of some module under hdl/ (SystemVerilog,
comments stripped). Usage: port_names.py <repo> <page>... ; rc 1 if any is missing."""
import re, sys, pathlib
repo = pathlib.Path(sys.argv[1])
ports = {}
for f in sorted(repo.glob('hdl/**/*.sv')) + sorted(repo.glob('hdl/**/*.svh')):
    t = f.read_text(errors='replace')
    t = re.sub(r'/\*.*?\*/', ' ', t, flags=re.S)
    t = re.sub(r'//[^\n]*', ' ', t)
    # ANSI port declarations: direction keyword up to the next , ; or )
    for m in re.finditer(r'\b(input|output|inout)\b([^;,)]*)', t):
        for n in re.findall(r'\b([A-Za-z_]\w*_[io])\b', m.group(2)):
            ports.setdefault(n, set()).add(str(f.relative_to(repo)))
missing = 0
for page in sys.argv[2:]:
    txt = pathlib.Path(page).read_text()
    names = sorted(set(re.findall(r'(?<![\w/.-])([A-Za-z][A-Za-z0-9_]*_[io])\b(?!\w)', txt)))
    for n in names:
        lines = [i+1 for i, l in enumerate(txt.splitlines()) if re.search(r'(?<![\w/.-])'+re.escape(n)+r'\b', l)]
        ok = n in ports
        if not ok: missing += 1
        print(f"{'PORT' if ok else 'MISSING'}\t{page}\t{n}\tlines={lines[:8]}\t{"TOP" if "hdl/top/protocol_processor_top.sv" in ports.get(n, ()) else "internal"}	{sorted(ports.get(n, []))[:2]}")
print(f"summary: {missing} missing", file=sys.stderr)
sys.exit(1 if missing else 0)

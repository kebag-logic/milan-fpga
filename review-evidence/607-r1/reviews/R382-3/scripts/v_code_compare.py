#!/usr/bin/env python3
"""Compare two LiteX .v files with all // and /* */ comments removed (the LiteX hierarchy
tree inside the header block comment lists blackboxes in a run-dependent order).
Usage: v_code_compare.py <workdir from probe_vs_full.sh>"""
import hashlib, pathlib, re, sys
W = pathlib.Path(sys.argv[1])
def code(p):
    t = p.read_text()
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = "\n".join(l for l in t.splitlines() if not l.lstrip().startswith("//"))
    return t
for d in sorted(W.glob("probe-*")):
    if not d.is_dir():
        continue
    k = d.name[len("probe-"):]
    a = code(d / "gateware/alinx_ax7101.v.norm"); b = code(W / f"full-{k}" / "gateware/alinx_ax7101.v.norm")
    h = hashlib.sha256(a.encode()).hexdigest()[:16]
    print(f"{k} .v code (all comments stripped) probe vs full: {'IDENTICAL' if a == b else 'DIFFERS'} sha256={h} lines={len(a.splitlines())}")

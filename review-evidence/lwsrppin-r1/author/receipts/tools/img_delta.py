#!/usr/bin/env python3
"""img_delta.py BASE_DIR HEAD_DIR SIZE_TOOL: every image's sections and every object whose size differs."""
import hashlib, subprocess, sys
from pathlib import Path
base, head, size = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
def sections(p):
    out = subprocess.run([size, "-A", str(p)], capture_output=True, text=True, check=True).stdout
    rows = {}
    for line in out.splitlines()[2:]:
        f = line.split()
        if len(f) >= 2 and f[0].startswith(".") and f[1].isdigit():
            rows[f[0]] = int(f[1])
    return rows
def berkeley(p):
    f = subprocess.run([size, str(p)], capture_output=True, text=True, check=True).stdout.splitlines()[1].split()
    return int(f[0]), int(f[1]), int(f[2])
for elf in sorted(head.rglob("ctrl_app.elf")):
    rel = elf.relative_to(head); b = base / rel
    hb = hashlib.sha256(b.read_bytes()).hexdigest()[:16]; hh = hashlib.sha256(elf.read_bytes()).hexdigest()[:16]
    sb, sh = sections(b), sections(elf)
    print(f"== {rel.parent}  sha256 base {hb} head {hh}")
    for name in sorted(set(sb) | set(sh)):
        d = sh.get(name, 0) - sb.get(name, 0)
        print(f"   {name:24} base {sb.get(name,0):>8} head {sh.get(name,0):>8} delta {d:+d}")
    for o in sorted(elf.parent.glob("*.o")):
        ob = b.parent / o.name
        if ob.exists():
            x, y = berkeley(ob), berkeley(o)
            if x != y:
                print(f"   object {o.name}: text/data/bss base {x} head {y}")
        su_h, su_b = o.with_suffix(".su"), ob.with_suffix(".su")
        if su_h.exists() and su_b.exists() and su_h.read_text() != su_b.read_text():
            fb = {l.split("\t")[0].split(":")[-1]: l.split("\t")[1] for l in su_b.read_text().splitlines() if "\t" in l}
            fh = {l.split("\t")[0].split(":")[-1]: l.split("\t")[1] for l in su_h.read_text().splitlines() if "\t" in l}
            ch = {k: (fb.get(k), fh.get(k)) for k in set(fb) | set(fh) if fb.get(k) != fh.get(k)}
            print(f"   frames {o.with_suffix('.su').name}: {ch}")

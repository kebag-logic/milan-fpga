#!/usr/bin/env python3
"""Generate ucode.hex from a tree's gen_ucode.py and print its program map.

usage: rommap.py TREE OUT_HEX OUT_MAP
Each program's extent runs from its place() start to the next start or the
first unoccupied word; names are the module's E_* constants equal to a start.
"""
import hashlib, importlib.util, sys
from pathlib import Path
tree, out_hex, out_map = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("gu", tree / "hdl/aecp/ucode/gen_ucode.py")
gu = importlib.util.module_from_spec(spec); sys.argv = ["gen_ucode.py"]; spec.loader.exec_module(gu)
text = "".join(f"{w:012x}\n" for w in gu.rom)
out_hex.write_text(text)
starts = sorted(gu.placed)
names = {}
for k, v in vars(gu).items():
    if k.startswith("E_") and isinstance(v, int) and v in starts:
        names.setdefault(v, []).append(k)
lines = []
for i, s in enumerate(starts):
    nxt = starts[i + 1] if i + 1 < len(starts) else len(gu.rom)
    e = s
    while e < nxt and e in gu.occupied:
        e += 1
    lines.append(f"{s:5d} {e - 1:5d} {e - s:4d} {'/'.join(sorted(names.get(s, ['?'])))}")
out_map.write_text("\n".join(lines) + "\n")
print(f"{out_hex.name}: {len(gu.rom)} words, {len(starts)} programs, {len(gu.occupied)} occupied, "
      f"sha256 {hashlib.sha256(text.encode()).hexdigest()}")

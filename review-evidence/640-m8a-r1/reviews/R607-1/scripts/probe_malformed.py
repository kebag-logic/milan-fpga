#!/usr/bin/env python3
"""R607-1: ctrl_memory.read_elf/plan on malformed and boundary inputs.

    probe_malformed.py <tree> <good-elf> <workdir>
"""
import sys
from pathlib import Path
tree, good, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(tree / "sw/litex"))
import ctrl_memory
work.mkdir(parents=True, exist_ok=True)
data = good.read_bytes()
cases = {"empty": b"", "not-elf": b"hello world" * 10, "elf64": b"\x7fELF\x02\x01" + data[6:],
         "big-endian": b"\x7fELF\x01\x02" + data[6:], "truncated-64": data[:64],
         "truncated-half": data[:len(data) // 2], "x86-machine": data[:18] + b"\x03\x00" + data[20:]}
for name, blob in cases.items():
    p = work / f"{name}.elf"; p.write_bytes(blob)
    try:
        ctrl_memory.plan(ctrl_memory.read_elf(p)); out = "ACCEPTED"
    except ctrl_memory.Refusal as e:
        out = f"Refusal[{e.check}]"
    except Exception as e:
        out = f"{type(e).__name__} (unnamed): {str(e)[:80]}"
    print(f"{name}: {out}")
# budget boundary: an image whose planned banks are exactly 56 and 56.5 RAMB36
img = ctrl_memory.read_elf(good)
p = ctrl_memory.plan(img)
for budget in (p.tiles, p.tiles - 0.5):
    try:
        ctrl_memory.plan(img, budget=budget); out = "accepted"
    except ctrl_memory.Refusal as e:
        out = f"Refusal[{e.check}]"
    print(f"plan tiles {p.tiles} against budget {budget}: {out}")

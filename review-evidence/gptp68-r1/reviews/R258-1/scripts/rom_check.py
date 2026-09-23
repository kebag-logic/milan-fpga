#!/usr/bin/env python3
"""ROM evidence for R258-1, reviewer-owned.

1. Regenerate each tracked image from the HEAD generator with the arguments
   its own producer uses and require byte equality with the committed file.
2. Word-diff every tracked image, base -> head, and print the changed address
   ranges plus the SERVO leg base in each (read from the generator's
   leg-placement line).
3. For extra configurations a consumer may generate (125, 50, 25 MHz and the
   seeded regression images), generate base and head, and require that the
   changed words sit inside the head SERVO leg span and every other leg keeps
   its base.
Usage: rom_check.py <donor-head-tree> <donor-base-tree>"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TRACKED = {
    "tb/verilator/engine/gptp_ucode.hex": ["--clk-hz", "2000000", "--cease-ms", "3000"],
    "tb/tsngen/gptp_ucode.hex": ["--clk-hz", "2000000"],
    "tb/verilator/ucpu/gptp_ucode.hex": [],
    "syn/ooc/work/gptp_ucode.hex": [],
}
EXTRA = {
    "125MHz": ["--clk-hz", "125000000"],
    "50MHz": ["--clk-hz", "50000000"],
    "25MHz": ["--clk-hz", "25000000"],
    "2MHz-seq-seed": ["--clk-hz", "2000000", "--cease-ms", "3000", "--seq-seed", "0x200000"],
    "2MHz-sync-seed": ["--clk-hz", "2000000", "--cease-ms", "3000", "--sync-seq-seed", "0x10000"],
}


def gen(tree: Path, args: list[str], out: Path) -> dict[str, int]:
    """Run the tree's generator; return its leg bases."""
    res = subprocess.run([sys.executable, str(tree / "hdl/ucode/gen_gptp_ucode.py"), *args,
                          "-o", str(out)], check=True, capture_output=True, text=True)
    legs = re.search(r"legs: (.*)", res.stdout).group(1)
    return {k: int(v) for k, v in (x.split("@") for x in legs.split())}


def words(path: Path) -> list[str]:
    """The image's words, one per line."""
    return path.read_text().split()


def ranges(idx: list[int]) -> list[tuple[int, int]]:
    """Collapse sorted indices into inclusive ranges."""
    out: list[tuple[int, int]] = []
    for i in idx:
        if out and out[-1][1] == i - 1:
            out[-1] = (out[-1][0], i)
        else:
            out.append((i, i))
    return out


def main() -> int:
    """Print the evidence; exit nonzero on any violated expectation."""
    head, base = Path(sys.argv[1]), Path(sys.argv[2])
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for rel, args in TRACKED.items():
            out = tmp / "regen.hex"
            gen(head, args, out)
            same = out.read_bytes() == (head / rel).read_bytes()
            sha = hashlib.sha256((head / rel).read_bytes()).hexdigest()
            print(f"regen {rel}: {'IDENTICAL' if same else 'DIFFERS'} sha256 {sha}")
            bad += not same
        for rel in TRACKED:
            b, h = words(base / rel), words(head / rel)
            diff = [i for i, (x, y) in enumerate(zip(b, h)) if x != y]
            print(f"word-diff {rel}: len {len(b)}->{len(h)} changed {ranges(diff)}")
        cfgs = {**{f"tracked:{k}": v for k, v in TRACKED.items()}, **EXTRA}
        for name, args in cfgs.items():
            lb = gen(base, args, tmp / "b.hex")
            lh = gen(head, args, tmp / "h.hex")
            b, h = words(tmp / "b.hex"), words(tmp / "h.hex")
            diff = [i for i, (x, y) in enumerate(zip(b, h)) if x != y]
            moved = {k: (lb[k], lh[k]) for k in lb if lb[k] != lh.get(k)}
            sv = lh["SERVO"]
            # the SERVO span: from its base up to the next leg base above it
            above = sorted(v for v in lh.values() if v > sv)
            span_end = (above[0] - 1) if above else len(h) - 1
            outside = [i for i in diff if not sv <= i <= span_end]
            ok = not moved and not outside
            print(f"cfg {name}: SERVO@{sv} span {sv}..{span_end} changed {ranges(diff)} "
                  f"moved-legs {moved or 'none'} outside-servo {len(outside)} "
                  f"{'OK' if ok else 'VIOLATION'}")
            bad += not ok
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

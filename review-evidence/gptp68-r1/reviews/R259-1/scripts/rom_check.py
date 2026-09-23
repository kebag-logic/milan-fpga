#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ROM review for FPGA-gPTP PR #74.

1. Regenerate the four tracked images at the head with the arguments their
   own producers use and require byte equality with the committed files.
2. For the head and the base generator, generate a matrix of configurations
   (the tracked ones, both seeded regression images, other clocks, MAC and
   p1) and report, per configuration: SHA-256 of both, real-word counts, leg
   bases, and every differing word address. The SERVO leg range at the head
   is read from the generator's own `legs:` line, so "only the SERVO leg
   changes" is checked against the generator, not assumed.
Usage: rom_check.py <head checkout> <base checkout>
"""

from __future__ import annotations

import hashlib
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
MATRIX = {
    "engine": ["--clk-hz", "2000000", "--cease-ms", "3000"],
    "engine-seq-seed": ["--clk-hz", "2000000", "--cease-ms", "3000", "--seq-seed", "0x200000"],
    "engine-sync-seed": ["--clk-hz", "2000000", "--cease-ms", "3000", "--sync-seq-seed", "0x10000"],
    "tsngen": ["--clk-hz", "2000000"],
    "default": [],
    "clk25M": ["--clk-hz", "25000000"],
    "clk50M": ["--clk-hz", "50000000"],
    "clk125M": ["--clk-hz", "125000000"],
    "clk1M": ["--clk-hz", "1000000"],
    "mac-p1": ["--mac", "0x021122334455", "--p1", "100"],
}


def gen(tree: Path, args: list[str], out: Path) -> tuple[list[str], str]:
    """Run tree's generator; (image words, the generator's stdout)."""
    r = subprocess.run([sys.executable, str(tree / "hdl/ucode/gen_gptp_ucode.py"),
                        *args, "-o", str(out)], capture_output=True, text=True, check=True)
    return out.read_text().split(), r.stdout


def legs(stdout: str) -> dict[str, int]:
    """Parse `legs: NAME@base ...` into a dict."""
    line = next(ln for ln in stdout.splitlines() if ln.startswith("legs:"))
    return {k: int(v) for k, v in (t.split("@") for t in line.split()[1:])}


def main() -> int:
    head, base = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    ok = True
    with tempfile.TemporaryDirectory(prefix="r259-rom-") as td:
        tmp = Path(td)
        print("== 1. tracked images regenerate byte-identically at the head")
        for rel, args in TRACKED.items():
            out = tmp / "t.hex"
            gen(head, args, out)
            same = out.read_bytes() == (head / rel).read_bytes()
            ok &= same
            print(f"{'OK  ' if same else 'DIFF'} {rel} args={args} "
                  f"sha256={hashlib.sha256((head / rel).read_bytes()).hexdigest()}")
        print("== 2. base vs head per configuration")
        for tag, args in MATRIX.items():
            hw, hs = gen(head, args, tmp / "h.hex")
            bw, bs = gen(base, args, tmp / "b.hex")
            hl, bl = legs(hs), legs(bs)
            diff = [i for i, (a, b) in enumerate(zip(hw, bw)) if a != b]
            order = sorted(hl.items(), key=lambda kv: kv[1])
            servo = hl["SERVO"]
            nxt = min([v for v in hl.values() if v > servo] + [len(hw)])
            outside = [i for i in diff if not servo <= i < nxt]
            moved = {k: (bl[k], hl[k]) for k in hl if bl.get(k) != hl[k]}
            ok &= not outside and not moved
            print(f"[{tag}] args={args}")
            print(f"   head sha256={hashlib.sha256((tmp / 'h.hex').read_bytes()).hexdigest()} "
                  f"base sha256={hashlib.sha256((tmp / 'b.hex').read_bytes()).hexdigest()}")
            print(f"   {hs.splitlines()[0].split(': ', 1)[1]} (head) | "
                  f"{bs.splitlines()[0].split(': ', 1)[1]} (base)")
            print(f"   SERVO@{servo}, next leg or entry boundary at {nxt} "
                  f"(order: {' '.join(f'{k}@{v}' for k, v in order)})")
            rng = f"{diff[0]}..{diff[-1]}" if diff else "none"
            print(f"   differing words: {len(diff)} in {rng}; outside SERVO span: "
                  f"{outside if outside else 'none'}; leg bases moved: {moved if moved else 'none'}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

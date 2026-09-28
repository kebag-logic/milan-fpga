#!/usr/bin/env python3
"""Review probe R368-2: which record edge the partial-ownership fixture picks.

Usage: python3 -B edge_residues.py <repo-root> <work-dir>
Reproduces grade_partial_ownership's pair selection with the gate's own Bench
and reports, per shipped shape, the chosen edge residue (offset mod 4) and the
residues available among contiguous unaligned edges. A word store crossing
only one byte needs residue 3; two bytes need residue 2 or 3.
"""
from collections import Counter
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as gate  # noqa: E402

for cfg in sorted((root / "configs").glob("endstation_*.yaml")):
    bench = gate.make_bench(cfg, work / cfg.stem, gate.FIRMWARE.read_text())
    offsets = bench.offsets()
    rids = sorted(bench.frames, key=offsets.get)
    pairs = [(l, r) for l, r in zip(rids, rids[1:])
             if offsets[r] % 4 and offsets[l] + len(bench.frames[l]) == offsets[r]]
    chosen = pairs[0] if pairs else None
    res = Counter(offsets[r] % 4 for _, r in pairs)
    print(f"{cfg.stem:28s} chosen={chosen} chosen_residue="
          f"{offsets[chosen[1]] % 4 if chosen else None} available={dict(sorted(res.items()))}")

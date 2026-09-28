#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Reviewer probe: capture-copy edge mutants on every shipped shape.

Usage: edge_mutants.py <repo-root> <work-dir>
Plants each mutant into a copy of the unchanged firmware text and grades it
with the committed host bench (test_nvm_firmware.make_bench/grade) on every
configs/endstation_*.yaml. Prints, per shape, the residue of the first
unaligned closed->open boundary the partial-ownership grade uses, and per
mutant whether the named partial-ownership finding fired.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402

GUARD = "if ((i & 3u) == 0 && next - i >= 4u &&"
MUTANTS = {
    "none": None,
    "edge_cross_ge1": GUARD.replace(">= 4u", ">= 1u"),
    "edge_cross_ge2": GUARD.replace(">= 4u", ">= 2u"),
    "edge_cross_ge3": GUARD.replace(">= 4u", ">= 3u"),
    "no_edge_guard": "if ((i & 3u) == 0 &&",
    "byte_only_equivalent": "if (0 && (i & 3u) == 0 && next - i >= 4u &&",
    "ignore_ownership": None,
}
NAMED = "open record changed across unaligned"

text = nvm.FIRMWARE.read_text()
assert text.count(GUARD) == 1, "guard anchor not unique"
own = "copy = !((own[rec.id >> 5] >> (rec.id & 31u)) & 1u);"
assert text.count(own) == 1, "ownership anchor not unique"
cfgs = sorted((root / "configs").glob("endstation_*.yaml"))
rc = 0
for cfg in cfgs:
    for label, new in MUTANTS.items():
        if label == "none":
            src = text
        elif label == "ignore_ownership":
            src = text.replace(own, own[:-1] + " || 1;")
        else:
            src = text.replace(GUARD, new)
        sub = work / cfg.stem / label
        sub.mkdir(parents=True, exist_ok=True)
        bench = nvm.make_bench(cfg, sub, src)
        if label == "none":
            offs = bench.offsets()
            rids = sorted(bench.frames, key=offs.get)
            pairs = [(a, b) for a, b in zip(rids, rids[1:])
                     if offs[b] % 4 and offs[a] + len(bench.frames[a]) == offs[b]]
            print(f"{cfg.stem} unaligned_boundaries={len(pairs)} "
                  f"first_pair={pairs[0]} residue={offs[pairs[0][1]] % 4}")
        got = nvm.grade(bench)
        named = any(NAMED in g for g in got)
        print(f"  {cfg.stem:<28} {label:<22} findings={len(got)} named={int(named)}"
              + (f" first={got[0][:110]}" if got else ""))
        expect_clean = label in ("none", "byte_only_equivalent")
        if expect_clean and got:
            rc = 1
sys.exit(rc)

#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Reviewer probe: is the surviving `next - i >= 3u` mutant a real crossing?

Usage: edge_residue_probe.py <repo-root> <work-dir>
The committed grade_partial_ownership uses the first unaligned closed->open
boundary (pairs[0]). This probe re-runs the same committed grade body, with
only the pair choice changed to the first boundary of each residue 1, 2, 3,
against the unchanged firmware and the `>= 3u` and `>= 1u` mutants.
"""
from pathlib import Path
import inspect
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402

GUARD = "if ((i & 3u) == 0 && next - i >= 4u &&"
body = inspect.getsource(nvm.grade_partial_ownership)
assert body.count("closed, opened = pairs[0]") == 1
text = nvm.FIRMWARE.read_text()
cfgs = sorted((root / "configs").glob("endstation_*.yaml"))
for residue in (1, 2, 3):
    src = body.replace("def grade_partial_ownership(", f"def grade_r{residue}(").replace(
        "closed, opened = pairs[0]",
        f"pairs = [p for p in pairs if offsets[p[1]] % 4 == {residue}]\n"
        f"    if not pairs:\n        return ['no residue-{residue} boundary']\n"
        "    closed, opened = pairs[0]")
    exec(src, nvm.__dict__)
for cfg in cfgs:
    for label, new in (("none", GUARD), ("edge_cross_ge3", GUARD.replace(">= 4u", ">= 3u")),
                       ("edge_cross_ge1", GUARD.replace(">= 4u", ">= 1u"))):
        sub = work / cfg.stem / label
        sub.mkdir(parents=True, exist_ok=True)
        bench = nvm.make_bench(cfg, sub, text.replace(GUARD, new))
        row = []
        for residue in (1, 2, 3):
            got = getattr(nvm, f"grade_r{residue}")(bench)
            named = any("open record changed across unaligned" in g for g in got)
            row.append(f"r{residue}:findings={len(got)},named={int(named)}"
                       + (f"({got[0][:40]})" if got and not named else ""))
        print(f"{cfg.stem:<28} {label:<16} " + " ".join(row))

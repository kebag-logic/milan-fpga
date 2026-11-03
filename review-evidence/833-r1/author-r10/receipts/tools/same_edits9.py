#!/usr/bin/env python3
"""Each reviewer mutant published at round 8 has, byte for byte, the edits of its MUTANTS entry.

usage: python3 -I -B same_edits9.py <tree>
The published edits are read by candidates.py from the reviewers' own scripts (R763-8 r8_mutants.py by its
constants and MINE only; R764-8 r764_8_live_probes.py and r764_8_probes.py by their PROBES).
"""
import runpy
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as pts  # noqa: E402

c = runpy.run_path(str(Path(__file__).resolve().parent / "candidates.py"))
pairs = [("R763-8", "r8-resume-beside-new-live", "resume-beside-new-live"),
         ("R763-8", "r8-sigterm-trap-command-after-late-grace-resume", "sigterm-trap-command-after-resume-from-1.5s")]
pairs += [("R764-8", name, name) for name in c["R764_8_LIVE"]]
pairs += [("R764-8", name, name) for name in c["R764_8_EDGE"]]
published = {**c["R763_8"], **c["R764_8_LIVE"], **c["R764_8_EDGE"]}
bad = 0
for who, name, ours in pairs:
    same = ours in pts.MUTANTS and tuple(pts.MUTANTS[ours][2:]) == tuple(published[name])
    bad += not same
    entry = pts.MUTANTS.get(ours, (None, None))
    print(f"{who} {name} = {ours}: {'SAME' if same else 'DIFFERENT'}; control {entry[0]}; words {entry[1]!r}")
print(f"same edits: {len(pairs) - bad} of {len(pairs)}")
sys.exit(1 if bad else 0)

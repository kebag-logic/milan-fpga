#!/usr/bin/env python3
"""R524-3: grade one disjoint slice of ctrl_mutants.MUTANTS through the repository's campaign().

Usage (from the clone root): ctrl_campaign_slice.py <index> <count> <out-dir> <jobs>
Slice i takes MUTANTS[i::count], so count slices cover every mutant exactly once.
Prints the slice's mutant names first, then the repository campaign's own lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT / "sw/firmware/ctrl/test"), str(ROOT / "sw/firmware/gtest")]

import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import test_ctrl_firmware  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

index, count, out, jobs = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]).resolve(), int(sys.argv[4])
everything = ctrl_mutants.MUTANTS
ctrl_mutants.MUTANTS = everything[index::count]
print(f"slice {index}/{count}: {len(ctrl_mutants.MUTANTS)} of {len(everything)} mutants: "
      f"{', '.join(m.name for m in ctrl_mutants.MUTANTS)}", flush=True)
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
test_ctrl_firmware.cut_reuse(tree.reuse)
escaped = ctrl_mutants.campaign(out / "mutants", tree.reuse, jobs)
print(f"slice {index}: {'ESCAPED' if escaped else 'ALL CAUGHT'}")
sys.exit(1 if escaped else 0)

#!/usr/bin/env python3
"""Reviewer probe: judge ONE capture's compiles with the boundary's own compile judgement, skipping only the
capture-completeness check (ctrl_configs.held), which refuses an F5-only capture for the other builders it does
not hold. Uses ctrl_boundary.Places, targets, judged and counted from the checkout given, unchanged.
Usage: python3 -I judge_capture_only.py <checkout> <capture dir>"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_boundary as b  # noqa: E402
import ctrl_capture  # noqa: E402

cap = ctrl_capture.load(Path(sys.argv[2]))
assert b.ROOT.resolve() == root, (b.ROOT, root)
places = b.Places((root,), b.targets(cap, (root,)))
counts = b.counted(cap, places)
found = b.judged(cap, places)
print(f"invocations {len(cap.invocations)}; compiled sources by place {dict(counts)}")
for core, builders in found.items():
    print(f"FINDING: {core} [{', '.join(sorted(builders))}]")
print(f"findings {len(found)}")

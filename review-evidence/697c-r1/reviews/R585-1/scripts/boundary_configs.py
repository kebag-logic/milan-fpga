#!/usr/bin/env python3
"""Run ctrl_boundary.judge() on the checkout under each configuration the firmware arms build the stack
with (C_FLAGS; plus -DCTRL_REENTRY_ASSERT as the acmp arms; with -UNDEBUG as the debug arms), to show
whether the pinned tree is clean in every one. The checkout is only read.
usage: boundary_configs.py <repo> <work>"""
import sys
from pathlib import Path
repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_boundary as cb  # noqa: E402
base = tuple(cb.C_FLAGS)
for label, extra in (("C_FLAGS", ()), ("C_FLAGS -DCTRL_REENTRY_ASSERT", ("-DCTRL_REENTRY_ASSERT",)),
                     ("C_FLAGS -UNDEBUG", ("-UNDEBUG",)),
                     ("C_FLAGS -UNDEBUG -DCTRL_REENTRY_ASSERT", ("-UNDEBUG", "-DCTRL_REENTRY_ASSERT"))):
    cb.C_FLAGS = base + extra
    f = cb.judge(cb.Trees(cb.CTRL, cb.STACK), None, work / label.replace(" ", "_"))
    print(f"{label}: {len(f)} finding(s)" + "".join(f"\n  {x}" for x in f))

#!/usr/bin/env python3
"""Reviewer probe: re-run each escaped reviewer defect's arm once, planted, and print the arm's rc and verdict,
so an escape is shown to be a complete passing run (rc 0) and not a refused build (rc 2).

usage: r733_escape_check.py CHECKOUT WORKDIR NAME...
"""
import sys
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
names = sys.argv[3:]
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
sys.argv = [sys.argv[0], str(checkout), str(work), "0", "1", "--extras-only"]
import runpy  # noqa: E402

probe = runpy.run_path(str(Path(__file__).with_name("r733_plat_campaign.py")), run_name="r733_table")
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

cut_reuse(work / "reuse")

arms = {"plat": plat_arms.arm_plat, "platboot1": lambda t: plat_arms.arm_platboot(t, 1),
        "platboot2": lambda t: plat_arms.arm_platboot(t, 2)}
for m in probe["EXTRAS"]:
    if m.name not in names:
        continue
    root = work / m.name
    ctrl, stack = ctrl_mutants.plant(m, root)
    tree = Tree(ctrl, root / "work" / "build", work / "reuse", fw_gtest.Build(jobs=4), stack)
    out = arms[m.arm](tree)
    verdicts = [ln.strip() for ln in out.log.splitlines() if "verdict:" in ln or "RESULT" in ln]
    print(f"ESCAPE-CHECK {m.name}: arm {m.arm} rc {out.rc}; {verdicts}")

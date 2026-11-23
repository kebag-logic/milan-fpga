#!/usr/bin/env python3
"""Plant the srp_early_mutants.py defects (#969) of a milan-fpga tree at a chosen entity and interface count, through
the tree's own srp_mutants.campaign, each required caught on its own words.

Usage: python3 -I early_campaign.py <repo-root> <out-dir> <interfaces> <entity-stem|1x1>
Exit 0 when every defect was caught.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
interfaces = int(sys.argv[3])
entity = sys.argv[4]
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import srp_early_mutants  # noqa: E402
import srp_mutants  # noqa: E402
from ctrl_build import CTRL  # noqa: E402

assert CTRL.resolve().is_relative_to(root), (CTRL, root)
srp_mutants.DEFECTS = srp_early_mutants.defects(srp_mutants.Defect)
print("defects", len(srp_mutants.DEFECTS), "interfaces", interfaces, "entity", entity)
failed = srp_mutants.campaign(out, root / "third_party/lwSRP", int(sys.argv[5]) if len(sys.argv) > 5 else 4, interfaces, "" if entity == "1x1" else entity)  # entity stem or 1x1
print("EARLY-CAMPAIGN", "FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)

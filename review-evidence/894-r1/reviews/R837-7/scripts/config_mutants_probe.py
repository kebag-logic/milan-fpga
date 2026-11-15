#!/usr/bin/env python3
"""Reviewer probe: run the AECP app arm (1 and 2 interfaces) unmutated, then plant only the
SET_CONFIGURATION rows (aecp_configuration_mutants.ROWS) through aecp_mutants.campaign on a copy.

usage: python3 -B config_mutants_probe.py REPO OUT_DIR [JOBS]
The repository tree is never written: campaign() copies sw/firmware/ctrl under OUT_DIR.
"""
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
import aecp_configuration_mutants as rows  # noqa: E402
import aecp_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / "head/build", out / "head/reuse", fw_gtest.Build(jobs=jobs), aecp_mutants.STACK)
config = aecp_arms.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
bad = 0
for i in (1, 2):
    r = aecp_arms.core_arm(tree, config, i, mode="app")
    tail = [l for l in r.log.splitlines() if "PASSED" in l or "FAILED" in l][-3:]
    print(f"head app arm if{i}: rc {r.rc}; " + " | ".join(tail), flush=True)
    bad |= r.rc != 0
names = {row[0] for row in rows.ROWS}
aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
print(f"planting {len(aecp_mutants.DEFECTS)} of {len(names)} configuration rows", flush=True)
aecp_mutants.controls = lambda: None  # the whole-table drift guard refuses a subset; the author's gate runs it
escaped = aecp_mutants.campaign(out / "mutants", jobs)
print("RESULT:", "FAIL" if bad or escaped or len(aecp_mutants.DEFECTS) != len(names) else "PASS")
sys.exit(1 if bad or escaped else 0)

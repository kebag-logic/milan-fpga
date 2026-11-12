#!/usr/bin/env python3
"""Round 4 delta probes: plant the four defects the delta names, through the head's own plant and catch oracles,
and record what B20's AECP line does with the loop serviced after the DEPARTING, alone and with AECP's probe
silence lifted too.

usage: python3 -B r822_4_probes.py <head checkout> <output dir> <jobs>
The checkout is only read: every plant is written into copies under <output dir>/work.
"""
import dataclasses
import json
import sys
from pathlib import Path

head, out, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(head / "sw/firmware/ctrl/test"))

import aecp_mutants  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import Tree  # noqa: E402

PLAT = ("plat-reboot-transmits-after-the-departing", "plat-reboot-takes-aecp-frames-after-the-success")
AECP = ("reboot-serves-after-its-success", "reboot-probes-after-its-success")
B20 = "Boot.B20NoOtherChannelTransmitsAfterTheDeparting"
B20_AECP = "B20 no AECP transmission starts after ENTITY_DEPARTING"
out.mkdir(parents=True, exist_ok=True)
result = {}

# Controls: the full tables pass their own drift checks at this head before any subset is taken
result["plat_unnamed_tests_full_table"] = ctrl_mutants.unnamed_tests()
aecp_mutants.controls()
result["aecp_controls_full_table"] = "ok"
by_name = {m.name: m for m in ctrl_mutants.MUTANTS}
defects = {d.name: d for d in aecp_mutants.DEFECTS}
result["present"] = {n: (n in by_name) for n in PLAT} | {n: (n in defects) for n in AECP}

# 1. the two platform defects through ctrl_mutants.campaign, table narrowed after its full-table control
ctrl_mutants.MUTANTS = tuple(by_name[n] for n in PLAT)
ctrl_mutants.unnamed_tests = lambda: []
result["plat_campaign_escaped"] = ctrl_mutants.campaign(out / "plat", out / "plat-reuse", jobs)

# 2. the two AECP defects through aecp_mutants.campaign, table narrowed after its control ran above
aecp_mutants.DEFECTS = tuple(defects[n] for n in AECP)
aecp_mutants.controls = lambda: None
result["aecp_campaign_escaped"] = aecp_mutants.campaign(out / "aecp", jobs)
result["aecp_results"] = json.loads((out / "aecp/results.json").read_text())


def b20(label: str, extra: list) -> dict:
    """Plant the loop-on defect (and any extra aecp.c edit), run platboot1, report B20's AECP line."""
    root = out / label
    loop = by_name[PLAT[0]]
    ctrl, stack = ctrl_mutants.plant(loop, root)
    for d in extra:
        target = ctrl / d.path
        text = target.read_text()
        assert text.count(d.old) == 1, d.name
        target.write_text(text.replace(d.old, d.new))
    tree = Tree(ctrl, root / "work" / "build", root / "reuse", fw_gtest.Build(jobs=jobs), stack)
    o = plat_arms.arm_platboot(tree, 1)
    (root / "platboot1.log").write_text(o.log)
    fails = [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln and B20 in ln]
    return {"rc": o.rc, "b20_fail_lines": len(fails),
            "b20_aecp_caught": ctrl_mutants.caught(B20, B20_AECP, o),
            "b20_words_failed": sorted({ln.split(":", 1)[1].strip()[:80] for ln in fails if ":" in ln})}


result["b20_loop_on_alone"] = b20("b20-loop", [])
result["b20_loop_on_and_probes"] = b20("b20-loop-probes", [defects[AECP[1]]])
result["b20_loop_on_and_serves"] = b20("b20-loop-serves", [defects[AECP[0]]])
(out / "result.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
print(json.dumps(result, indent=2, default=str))

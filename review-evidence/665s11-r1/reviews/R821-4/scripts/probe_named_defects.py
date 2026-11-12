#!/usr/bin/env python3
"""Plant only the defects the round-4 comments name, from a read-only clone at the head, and
report each one's caught/escaped verdict with the repository's own campaign code.

usage: probe_named_defects.py <clone> <work-dir> <jobs> plat|aecp

plat: plat-reboot-transmits-after-the-departing, plat-reboot-takes-aecp-frames-after-the-success,
      and a reviewer-only combined defect (the loop-on defect plus AECP's
      reboot-probes-after-its-success) that must redden B20's AECP words, which shows that check is live.
aecp: reboot-serves-after-its-success and reboot-probes-after-its-success.
The campaign copies the clone's firmware tree into <work-dir>; the clone is never written.
"""
import sys
from dataclasses import replace
from pathlib import Path

clone, work, jobs, which = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))

if which == "plat":
    import ctrl_mutants  # noqa: E402

    by = {m.name: m for m in ctrl_mutants.MUTANTS}
    loop_on = by["plat-reboot-transmits-after-the-departing"]
    gate = by["plat-reboot-takes-aecp-frames-after-the-success"]
    combined = replace(loop_on, name="reviewer-loop-on-plus-aecp-probes",
                       needle="B20 no AECP transmission starts after ENTITY_DEPARTING", also=())
    for m in (loop_on, gate):
        print(f"defect {m.name} in {m.path}; kills: {m.kills()}")
    import aecp_mutants  # noqa: E402

    probes = {d.name: d for d in aecp_mutants.DEFECTS}["reboot-probes-after-its-success"]
    original_plant = ctrl_mutants.plant

    def plant(m, root):
        ctrl, stack = original_plant(m, root)
        if m.name == combined.name:
            target = ctrl / probes.path
            text = target.read_text(encoding="utf-8")
            assert text.count(probes.old) == 1, "AECP planting site not unique"
            target.write_text(text.replace(probes.old, probes.new), encoding="utf-8")
            print(f"combined: also planted {probes.name} in {probes.path}")
        return ctrl, stack

    ctrl_mutants.plant = plant
    # the head unplanted: a no-op edit, whose 0 failed checks show the tests pass at the head
    baseline = replace(loop_on, name="reviewer-baseline-unplanted", new=loop_on.old, also=())
    ctrl_mutants.MUTANTS = (baseline, loop_on, gate, combined)
    escaped = ctrl_mutants.campaign(work, work / "reuse", jobs)
    print(f"plat probe campaign escaped={escaped}")
else:
    import aecp_mutants  # noqa: E402

    keep = ("reboot-serves-after-its-success", "reboot-probes-after-its-success")
    aecp_mutants.controls()  # the full table's own drift and reader checks, before filtering
    aecp_mutants.controls = lambda: None
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in keep)
    for d in aecp_mutants.DEFECTS:
        print(f"defect {d.name} in {d.path}; checks: {d.checks}")
    escaped = aecp_mutants.campaign(work, jobs)
    print(f"aecp probe campaign escaped={escaped}")

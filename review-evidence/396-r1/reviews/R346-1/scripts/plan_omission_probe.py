#!/usr/bin/env python3
"""R346-1 probe: plant every single omission into the release plans and require
the head's own per-area audit to refuse each one.

Usage: python3 -B plan_omission_probe.py <repo-root>
Exit 0 only when every planted omission is refused and the clean plans pass.
Nothing is written to the repository; plans are deep-copied in memory.
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb" / "tools"))
import torture_campaign as tp  # noqa: E402

TOPOLOGIES = {
    "default": (tp.ARTY, tp.PEER),
    "sparse": (tp.parse_device_spec("talker_index_set=1|3,listener_index_set=2|5,"
                                    "crf_out=7,crf_in=8", tp.ARTY), tp.PEER),
    "wide": (tp.parse_device_spec("talkers=8,listeners=8,crf_out=8,crf_in=8",
                                  tp.ARTY), tp.PEER),
}
failures, planted = [], 0


def refused(plan, area, dut, peer):
    return not tp.area_covers_every_index(plan, area, dut, peer)[0]


for topo, (dut, peer) in TOPOLOGIES.items():
    base = tp.build_plan(["matrix", "soak", "power"], dut, peer)
    for area in ("soak", "power"):
        ok, detail = tp.area_covers_every_index(base, area, dut, peer)
        if not ok:
            failures.append(f"{topo}/{area}: clean plan refused {detail['missing']}")
        sids = [s.sid for s in base if s.area == area]
        for sid in sids:
            step0 = next(s for s in base if s.sid == sid)
            # 1. every single counter target removed, one at a time
            for k, target in enumerate(step0.args["counter_targets"]):
                plan = deepcopy(base)
                st = next(s for s in plan if s.sid == sid)
                del st.args["counter_targets"][k]
                planted += 1
                if not refused(plan, area, dut, peer):
                    failures.append(f"{topo}/{sid}: missing target {target} accepted")
            # 2. each whole direction removed
            for name, t_ent in (("outbound", dut.entity_id), ("return", peer.entity_id)):
                plan = deepcopy(base)
                st = next(s for s in plan if s.sid == sid)
                st.args["pairs"] = [p for p in st.args["pairs"] if p["talker"] != t_ent]
                planted += 1
                if not refused(plan, area, dut, peer):
                    failures.append(f"{topo}/{sid}: missing {name} direction accepted")
                # 3. AAF only removed from that direction (CRF kept)
                plan = deepcopy(base)
                st = next(s for s in plan if s.sid == sid)
                talker = dut if t_ent == dut.entity_id else peer
                st.args["pairs"] = [p for p in st.args["pairs"]
                                    if not (p["talker"] == t_ent
                                            and not talker.is_crf_talker(p["talker_index"]))]
                planted += 1
                if not refused(plan, area, dut, peer):
                    failures.append(f"{topo}/{sid}: {name} without AAF accepted")
                # 4. CRF pair only removed from that direction
                plan = deepcopy(base)
                st = next(s for s in plan if s.sid == sid)
                st.args["pairs"] = [p for p in st.args["pairs"]
                                    if not (p["talker"] == t_ent
                                            and talker.is_crf_talker(p["talker_index"]))]
                planted += 1
                if not refused(plan, area, dut, peer):
                    failures.append(f"{topo}/{sid}: {name} without CRF pair accepted")
            # 5. counter targets re-attributed to the wrong entity
            plan = deepcopy(base)
            st = next(s for s in plan if s.sid == sid)
            for t in st.args["counter_targets"]:
                if t["entity"] == peer.entity_id:
                    t["entity"] = dut.entity_id
            planted += 1
            if not refused(plan, area, dut, peer):
                failures.append(f"{topo}/{sid}: peer targets re-attributed accepted")
            # 6. the step removed entirely
            plan = [s for s in deepcopy(base) if s.sid != sid]
            planted += 1
            if not refused(plan, area, dut, peer):
                failures.append(f"{topo}/{sid}: step removed accepted")
    # 7. a power area with one phase twice and the other absent
    plan = deepcopy(base)
    for s in plan:
        if s.sid == "power.journal_commit":
            s.args["phase"] = "idle"
    planted += 1
    if not refused(plan, "power", dut, peer):
        failures.append(f"{topo}: power with two idle groups and no commit group accepted")

print(f"planted {planted} omissions over {len(TOPOLOGIES)} topologies; "
      f"{len(failures)} accepted")
for f in failures:
    print("ACCEPTED:", f)
sys.exit(1 if failures else 0)

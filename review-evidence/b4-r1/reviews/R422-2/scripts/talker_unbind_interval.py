#!/usr/bin/env python3
"""Talker end to unbind interval, per host clock, from the lane B4 run records.

usage: talker_unbind_interval.py <runs/timing-long dir>

events.jsonl is written by the orchestrating host (run_timing.py event(),
time.time() locally). controller-logs.txt and ctl-*.jsonl are written on the
controller host (run over ssh). The script shows the offset between the two
clocks from the same commands, and the interval on each single clock.
"""
import json, sys, os
d = sys.argv[1]
ev = [json.loads(l) for l in open(os.path.join(d, "events.jsonl"))]
evt = {e.get("tag", e["kind"]): e["t"] for e in ev}
ctl = {}
for tag in ("bind", "map-add", "map-remove", "unbind", "map-final"):
    first = json.loads(open(os.path.join(d, f"ctl-{tag}.jsonl")).readline())
    ctl[tag] = first["t"]
talker_end = None
for l in open(os.path.join(d, "controller-logs.txt")):
    if l.startswith("{"):
        r = json.loads(l)
        if r.get("kind") == "end":
            talker_end = r["t"]
out = dict(
    controller_talker_end_t=talker_end,
    controller_record_minus_orchestrator_event_s={k: round(ctl[k] - evt[k], 3) for k in ctl},
    note="each orchestrator event is logged AFTER its ssh command returned, so the controller clock leads by at least these amounts",
    interval_controller_clock_s=round(ctl["unbind"] - talker_end, 3),
    interval_mixed_clocks_s=round(evt["unbind"] - talker_end, 3),
)
print(json.dumps(out, indent=1))

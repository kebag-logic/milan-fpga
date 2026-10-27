"""Grade one explicit composition over the sweep's arms and print every channel's DUT events.

usage: python3 -I probe_case.py <torture_campaign.py> <frames> '<json list of synthesizer events>' | @<json file>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib  # noqa: E402

mod = probe_lib.load(sys.argv[1])
t = probe_lib.case(mod)
frames, arg = int(sys.argv[2]), sys.argv[3]
events = json.load(open(arg[1:])) if arg.startswith("@") else json.loads(arg)
verdict, detail, cols = t._sweep_grade(frames, events)
print("verdict", verdict, "|", detail.get("why"))
print("missed", [(a["class"], a["index"], a.get("channel")) for a in detail["planted_missed"]])
for e in sorted(detail["events"], key=lambda e: (e["channel"], e["capture_index"])):
    if e["attribution"] == "dut":
        print(" ", e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask"), e.get("located_within"))

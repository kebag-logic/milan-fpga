"""Reproduce one fuzz seed: print its units, verdict, DUT events and the check's outcome.

usage: python3 -I probe_seed.py <torture_campaign.py> <frames> <seed>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_lib  # noqa: E402

mod = probe_lib.load(sys.argv[1])
t = probe_lib.case(mod)
frames, seed = int(sys.argv[2]), int(sys.argv[3])
units = t._fuzz_units(frames, seed)
for kind, at, channels, span, events in units:
    print("unit", kind, at, channels, span, json.dumps(events[:2]), "... x%d" % len(events))
verdict, detail, cols = t._sweep_grade(frames, [e for u in units for e in u[4]])
print("verdict", verdict, "|", detail.get("why"))
print("missed", [(a["class"], a["index"], a.get("channel")) for a in detail["planted_missed"]])
for e in sorted(detail["events"], key=lambda e: (e["channel"], e["capture_index"])):
    print(" ", e["attribution"], e["channel"], e["capture_index"], e["class"], e.get("n"), e.get("mask"),
          e.get("located_within"), e.get("matches_channel"))
try:
    print("check", t._fuzz_check(frames, units))
except AssertionError as error:
    print("check VIOLATION", str(error)[:200])

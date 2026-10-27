"""Dump one fuzz composition's synthesizer events, verdict and every listed event.

Usage: python3 -I probe_dump.py <repo> <family arm|nested> <frames> <seed>
"""
import json
import sys
import unittest

REPO, FAMILY, FRAMES, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, REPO + "/tb/tools")
import torture_campaign as tc  # noqa: E402


class T(tc._ReleaseGateChecks, unittest.TestCase):
    def runTest(self):
        pass


t = T()
units = t._fuzz_units(FRAMES, SEED) if FAMILY == "arm" else t._fuzz_nested(FRAMES, SEED)
extra = [ev for u in units for ev in u[4]]
verdict, detail, _ = t._sweep_grade(FRAMES, extra)
print(json.dumps({"units": [(u[0], u[1], u[2], u[3]) for u in units],
                  "synth": [e for e in extra if e["kind"] != "flip"] + extra[:1],
                  "verdict": verdict, "why": detail.get("why"), "missed": detail.get("planted_missed")}))
for e in detail["events"]:
    print(json.dumps({k: e.get(k) for k in ("channel", "attribution", "class", "capture_index", "n", "mask",
                                             "located_within", "unresolved")}))
try:
    print("fuzz_check:", t._fuzz_check(FRAMES, units))
except AssertionError as error:
    print("fuzz_check FAILED:", str(error)[:300])

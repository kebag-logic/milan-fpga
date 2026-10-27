"""Probe: does the fuzz gate's "listed" test (overlap of a listing with the event's
words widened by 63) accept units whose only reaching DUT listing begins more than
63 samples before the unit's first word?  The documents state each listing "falls
no earlier than 63 samples before the event's first word".

Usage: python3 -I probe_reach.py <repo> <family arm|nested> <frames> <seed_lo> <seed_hi> <jobs>
Prints one JSON line per offending (seed, unit, channel) and a summary line.
"""
import json
import multiprocessing
import sys
import unittest

REPO, FAMILY, FRAMES, LO, HI, JOBS = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
sys.path.insert(0, REPO + "/tb/tools")
import torture_campaign as tc  # noqa: E402


class T(tc._ReleaseGateChecks, unittest.TestCase):
    def runTest(self):
        pass


def span(e):
    low, high = e.get("located_within", (e["capture_index"],) * 2)
    if e["class"] not in ("dropped", "repeated"):
        high = max(high, e["capture_index"] + e["n"] - 1)
    return low, high


def one(seed):
    t = T()
    units = t._fuzz_units(FRAMES, seed) if FAMILY == "arm" else t._fuzz_nested(FRAMES, seed)
    verdict, detail, _ = t._sweep_grade(FRAMES, [ev for u in units for ev in u[4]])
    out = []
    if verdict == "PASS":
        return verdict, out
    g = tc.AUDIO_GUARD_FRAMES
    for i, (kind, at, chans, n, _) in enumerate(units):
        first, last = at, at + n - 1
        for c in chans:
            reach = [e for e in detail["events"] if e["attribution"] == "dut" and e["channel"] == c
                     and t._fuzz_reach(e, first, last) <= g]
            if not reach:
                continue
            starts_in = [e for e in reach if first - g <= span(e)[0] <= last + g]
            if not starts_in:
                out.append({"seed": seed, "verdict": verdict, "unit": i, "kind": kind, "at": at, "n": n,
                            "channel": c,
                            "reaching": [(e["class"], e["capture_index"], e["n"], span(e)) for e in reach],
                            "on_channel": [(e["class"], e["capture_index"], e["n"], span(e)) for e in detail["events"]
                                           if e["attribution"] == "dut" and e["channel"] == c],
                            "units": [(u[0], u[1], u[2], u[3]) for u in units]})
    return verdict, out


if __name__ == "__main__":
    with multiprocessing.Pool(JOBS) as pool:
        bad, verdicts = 0, {}
        for verdict, out in pool.imap(one, range(LO, HI), chunksize=4):
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
            for o in out:
                bad += 1
                print(json.dumps(o))
    print(json.dumps({"summary": True, "family": FAMILY, "frames": FRAMES, "seeds": [LO, HI],
                      "verdicts": verdicts, "units_reached_only_by_a_listing_starting_before_first_minus_63": bad}))

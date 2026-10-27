"""Census of the round-8 coverage rule over seeded fuzz compositions, beside the gate's own check.

For each composition of one family (arm: _fuzz_units, nested: _fuzz_nested) it runs the gate's
_fuzz_check and, independently of the planner's _fuzz_reach, counts every (unit, channel it changes):

- covered: a DUT listing on that channel whose span (located_within or the listed sample, widened to its
  words for every class but dropped and repeated) overlaps [first word - 63, last word + 63];
- void: not covered, in a NOT RUN run with a missed arm within the unit's span +-2 on that channel
  (the stated exception);
- other: not covered otherwise, which the gate must excuse as cancelled (removing it leaves the bytes) or,
  in a PASS run, as clean (the bytes are a clean run's, each arm within its tolerance).

usage: python3 -I -B coverage_census.py <torture_campaign.py> <arm|nested> <frames> <lo> <hi> <jobs>
Prints one JSON line per composition the gate refuses or that has an "other" unit, then a summary.
"""
import importlib.util
import json
import multiprocessing
import sys
import unittest

T = FAMILY = FRAMES = None


def init(path, family, frames):
    global T, FAMILY, FRAMES
    spec = importlib.util.spec_from_file_location("torture_campaign_probe", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    class Case(mod._ReleaseGateChecks, unittest.TestCase):
        def runTest(self):
            pass
    T, FAMILY, FRAMES = Case(), family, frames


def span(e):
    low, high = e.get("located_within") or (e["capture_index"],) * 2
    if e["class"] not in ("dropped", "repeated"):
        high = max(high, e["capture_index"] + e["n"] - 1)
    return low, high


def one(seed):
    units = T._fuzz_units(FRAMES, seed) if FAMILY == "arm" else T._fuzz_nested(FRAMES, seed)
    try:
        verdict, allowed = T._fuzz_check(FRAMES, units)
        gate = None
    except AssertionError as error:
        verdict, allowed, gate = None, set(), str(error)[:300]
    graded, detail, _ = T._sweep_grade(FRAMES, [ev for u in units for ev in u[4]])
    counts = {"covered": 0, "void": 0, "other": 0}
    others = []
    for i, (kind, at, chans, n, _) in enumerate(units):
        low, high = at - 63, at + n - 1 + 63
        for c in chans:
            if any(e["attribution"] == "dut" and e["channel"] == c and span(e)[0] <= high and span(e)[1] >= low
                   for e in detail["events"]):
                counts["covered"] += 1
            elif graded == "NOT RUN" and any(at - 2 <= a["index"] <= at + n + 1 and a.get("channel") in (None, c)
                                             for a in detail["planted_missed"]):
                counts["void"] += 1
            else:
                counts["other"] += 1
                others.append((i, kind, at, n, c))
    return seed, graded, sorted(allowed), gate, counts, others


def main():
    path, family, frames, lo, hi, jobs = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), \
        int(sys.argv[5]), int(sys.argv[6])
    total = {"compositions": 0, "gate_refused": 0, "verdicts": {}, "allowances": {},
             "unit_channels": {"covered": 0, "void": 0, "other": 0}, "other_not_excused": 0}
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path, family, frames)) as pool:
        for seed, graded, allowed, gate, counts, others in pool.imap(one, range(lo, hi), chunksize=8):
            total["compositions"] += 1
            total["verdicts"][graded] = total["verdicts"].get(graded, 0) + 1
            for a in allowed:
                total["allowances"][a] = total["allowances"].get(a, 0) + 1
            for k, v in counts.items():
                total["unit_channels"][k] += v
            if others and not {"cancelled", "clean"} & set(allowed):
                total["other_not_excused"] += 1
            if gate is not None:
                total["gate_refused"] += 1
            if gate is not None or others:
                print(json.dumps({"seed": seed, "verdict": graded, "allowed": allowed, "gate": gate,
                                  "other": others}))
    print(json.dumps(dict(total, summary=True, family=family, frames=frames, seeds=[lo, hi]), sort_keys=True))


if __name__ == "__main__":
    main()

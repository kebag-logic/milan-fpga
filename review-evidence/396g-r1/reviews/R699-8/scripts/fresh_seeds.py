#!/usr/bin/env python3
"""Grade fresh fuzz seeds with the head planner's gate and an independent coverage count.

usage: fresh_seeds.py <planner.py> <family arm|nested> <frames> <seed_lo> <seed_hi>
For each composition: the gate's _fuzz_check outcome (verdict and allowances, or its assertion),
and, apart from _fuzz_reach, each unit-channel's coverage: some DUT listing on that channel whose
samples (its words; for a slip also located_within) overlap [first-63, last+63].
Prints one JSON line per composition with uncovered unit-channels, then a summary line.
"""
import importlib.util, json, sys, unittest
path, family, frames, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
spec = importlib.util.spec_from_file_location("planner_under_probe", path)
mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod)
T = type("T", (mod._ReleaseGateChecks, unittest.TestCase), {})
t = T("test_audio_compositions_never_pass_and_list_every_event")
G = 63
def samples(e):
    if e["class"] in ("dropped", "repeated"):
        lo_, hi_ = e.get("located_within", (e["capture_index"],) * 2)
        return min(lo_, e["capture_index"]), max(hi_, e["capture_index"])
    return e["capture_index"], e["capture_index"] + e["n"] - 1
summary = {"compositions": 0, "gate_refused": 0, "unit_channels": 0, "covered": 0, "uncovered": 0, "verdicts": {}}
for seed in range(lo, hi):
    units = t._fuzz_units(frames, seed) if family == "arm" else t._fuzz_nested(frames, seed)
    summary["compositions"] += 1
    try:
        verdict, allowed = t._fuzz_check(frames, units); refusal = None
    except AssertionError as error:
        verdict, allowed, refusal = "REFUSED", set(), str(error)[:400]
        summary["gate_refused"] += 1
    summary["verdicts"][verdict] = summary["verdicts"].get(verdict, 0) + 1
    _, detail, _ = t._sweep_grade(frames, [ev for u in units for ev in u[4]])
    dut = [e for e in detail.get("events", []) if e["attribution"] == "dut"]
    uncovered = []
    for kind, at, channels, span, _ in units:
        first, last = at, at + span - 1
        for c in channels:
            summary["unit_channels"] += 1
            if any(e["channel"] == c and samples(e)[0] <= last + G and samples(e)[1] >= first - G for e in dut):
                summary["covered"] += 1
            else:
                summary["uncovered"] += 1; uncovered.append((kind, at, c))
    if uncovered or refusal or verdict == "PASS":
        print(json.dumps({"seed": seed, "verdict": verdict, "allowed": sorted(allowed), "uncovered": uncovered,
                          "missed_arms": [a["index"] for a in detail.get("planted_missed", [])], "refusal": refusal}))
summary["verdicts"] = dict(sorted(summary["verdicts"].items()))
print("SUMMARY", family, frames, lo, hi, json.dumps(summary))

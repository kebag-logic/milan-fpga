#!/usr/bin/env python3
"""Triage r5_fuzz.py violations: drop those the stated neighbour-word limit explains.

Usage: python3 -I r5_triage.py <repo> <fuzz-log>

A one-word flip whose corrupted word equals a received neighbour is the stated
limit "a word equal to a neighbouring received word is a repeat" (TESTING 6d);
such a seed is re-graded without that flip and kept only if it still violates.
Each remaining seed is printed with its DUT events and the planted events.
"""
import json
import sys
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r5_fuzz as f  # noqa: E402


def main():
    f.REPO = sys.argv[1]
    m = f.tc()
    rows = [json.loads(line) for line in open(sys.argv[2]) if line.startswith("{")]
    kept = 0
    for row in rows:
        extra = row["extra"]
        source = [{"kind": "flip", "index": i, "channel": c, "mask": s} if k == "flip"
                  else {"kind": k, "index": i, "n": s} for k, i, s, c in f.ARMS]
        cap = array("I", m.synthesize_counter_capture(f.FRAMES, 4, byteorder=sys.byteorder, events=source + extra))
        flips = [e for e in extra if e["kind"] == "flip"]
        runs = {(e["channel"], e["mask"]) for e in flips}
        single = [e for e in flips if sum(1 for g in flips if g["channel"] == e["channel"]
                                          and abs(g["index"] - e["index"]) == 1 and g["mask"] == e["mask"]) == 0]
        neighbour = []
        for e in single:
            col = cap[e["channel"]::4]
            if col[e["index"]] in (col[e["index"] - 1], col[e["index"] + 1]):
                neighbour.append(e)
        rest = [e for e in extra if e not in neighbour]
        # Re-run the family's checks with the neighbour flips removed.
        verdict, detail = f.grade(m, rest)
        dut = sorted((e["channel"], e["capture_index"], e["class"], e["n"], e.get("mask", ""))
                     for e in detail["events"] if e["attribution"] == "dut")
        planted = [e for e in rest if e["kind"] != "flip"]
        flip_runs = {}
        for e in sorted((e for e in rest if e["kind"] == "flip"), key=lambda e: e["index"]):
            key = (e["channel"], e["mask"])
            r = flip_runs.setdefault(key, [])
            if r and r[-1][1] == e["index"]:
                r[-1][1] += 1
            else:
                r.append([e["index"], e["index"] + 1])
        want = []
        for e in planted:
            cls = {"drop": "dropped", "repeat": "repeated", "silence": "silence"}[e["kind"]]
            want += [(c, e["index"], cls, e["n"]) for c in range(4)]
        for (c, mask), spans in flip_runs.items():
            want += [(c, a, "bit-flip", b - a) for a, b in spans]
        got = sorted(d[:4] for d in dut)
        if got != sorted(want) or verdict != "FAIL":
            kept += 1
            print(json.dumps({"seed": row["seed"], "removed_neighbour_flips": neighbour, "verdict": verdict,
                              "why": detail.get("why"), "planted": planted,
                              "flip_runs": {f"{c}:{mask:#x}": s for (c, mask), s in flip_runs.items()},
                              "unexpected": sorted(set(got) - set(want)), "missing": sorted(set(want) - set(got)),
                              "dut": dut}, default=str))
    print(f"{len(rows)} violating seeds; {kept} not explained by the neighbour-word limit")


if __name__ == "__main__":
    main()

"""Recompute section 14's U, L and S columns from the raw results.

Usage: python3 -I estimate32.py <results-root>
U = 4 x worst(8x8/2if); L = line through (2, worst 1x1/1if) and (16, worst
8x8/2if) to 64 streams; S = worst 8x8/2if + 48 x slope(1x1/1if -> 8x8/1if) /
14. S is given twice: as the document builds it (1x1 worst of arms A and B,
8x8/1if arm A only) and with one arm on both ends of the slope (arm A).
"""
import json
import sys

root = sys.argv[1]
BACKLOG = ("backlog", "backlog-adp", "backlog-adp-refill", "backlog-owed")


def rows(label):
    d = json.load(open(f"{root}/{label}/results.json"))
    out = {}
    for r in d["results"]:
        if r["group"] not in BACKLOG:
            continue
        for p in r["probes"]:
            if p.get("status") != "measured":
                continue
            row = p["row"]
            if r["group"] == "backlog-owed" and row.startswith("AECP record") and row.endswith("last"):
                continue
            if r["group"] == "backlog-owed" and "composed load" not in row:
                continue
            out[row] = max(out.get(row, 0.0), p["ms"])
    out["longest work pass"] = max(r["passes"]["worst"]["ms"] for r in d["results"] if r["group"] in BACKLOG)
    return out


a1, b1, a8, b8, p81 = (rows(x) for x in ("N-A1", "N-B1", "N-A8", "N-B8", "P81-A8"))
print(f"{'row':72s} {'1x1w':>6s} {'81A':>6s} {'82w':>6s} {'U':>6s} {'L':>6s} {'S_doc':>6s} {'S_armA':>6s} {'S_armA_on_82w':>6s}")
for k in sorted(a8, key=str):
    w1 = max(a1[k], b1[k])
    w8 = max(a8[k], b8[k])
    U = 4 * w8
    L = w1 + (w8 - w1) * (64 - 2) / (16 - 2)
    S_doc = w8 + (p81[k] - w1) * 48 / 14
    S_a = a8[k] + (p81[k] - a1[k]) * 48 / 14
    S_a_w = w8 + (p81[k] - a1[k]) * 48 / 14
    print(f"{k:72s} {w1:6.2f} {p81[k]:6.2f} {w8:6.2f} {U:6.1f} {L:6.1f} {S_doc:6.1f} {S_a:6.1f} {S_a_w:6.1f}")

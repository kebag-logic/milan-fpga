#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare the findings page's step 3 per-cycle table with the reviewer's
independent re-derivation (both clock fits), column by column.

  r264_compare_step3.py <findings_page> <step3-cycles.jsonl> <step3-cycles-robust.jsonl>

Prints each page value beside the default-fit and robust-fit values and the
largest absolute difference per column, then the recovery range against the
5 s bound.
"""
import json
import sys

COLS = [("off_for", 2), ("dut_sync0", 3), ("dut_gm_self", 4), ("dut_asc0", 5), ("sw_first_frame", 6),
        ("sw_first_ann", 7), ("dut_asc1", 8), ("dut_gm_sw", 9), ("dut_allgood", 10), ("recovery", 11)]


def page_rows(path):
    rows = {}
    grab = False
    for line in open(path):
        if line.startswith("| Cycle | CRF binding | Off for |"):
            grab = True
            continue
        if grab:
            if not line.startswith("|"):
                break
            cells = [c.strip().strip("*") for c in line.strip().strip("|").split("|")]
            if cells[0].isdigit():
                rows[int(cells[0])] = cells
    return rows


def main(page, a, b):
    pr = page_rows(page)
    da = {json.loads(x)["cycle"]: json.loads(x) for x in open(a)}
    db = {json.loads(x)["cycle"]: json.loads(x) for x in open(b)}
    worst = {}
    for c in sorted(pr):
        print(f"cycle {c}")
        for name, idx in COLS:
            pv = float(pr[c][idx])
            va, vb = da[c][name], db[c][name]
            d = max(abs(pv - va), abs(pv - vb))
            worst[name] = max(worst.get(name, 0.0), min(abs(pv - va), abs(pv - vb)))
            print(f"   {name:15s} page {pv:7.2f}  default {va:8.3f}  robust {vb:8.3f}  max|diff| {d:.3f}")
    print("closest-fit |page - reviewer| per column, worst over cycles:")
    for k, v in worst.items():
        print(f"   {k:15s} {v:.3f} s")
    rec = [da[c]["recovery"] for c in da] + [db[c]["recovery"] for c in db]
    print(f"recovery over both fits: {min(rec):.2f} to {max(rec):.2f} s; 5 s bound {'met' if max(rec) < 5 else 'NOT met'}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    sys.exit(main(*sys.argv[1:]))

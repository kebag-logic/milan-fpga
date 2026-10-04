#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Rebuild the report's lockstep tables from the raw receipts.

usage: summarize.py RECEIPTS_DIR  (prints Markdown)
"""
import collections
import pathlib
import re
import sys

R = pathlib.Path(sys.argv[1])


def num(rx, t):
    m = re.search(rx, t)
    return int(m.group(1)) if m else None


def fifo(t):
    m = re.search(r"tk: max=(\d+) full_cycles=(\d+) full_blocked_pushes=(\d+) push_into_empty=(\d+) "
                  r"push_with_pop=(\d+) pops=(\d+) \| ls: max=(\d+) full_cycles=(\d+) "
                  r"full_blocked_pushes=(\d+) push_into_empty=(\d+) push_with_pop=(\d+) pops=(\d+)", t)
    return list(map(int, m.groups()))


def main():
    out = []
    # ---- random campaign
    agg = collections.OrderedDict()
    for f in sorted((R / "lockstep/random").glob("*/run-*.log")):
        t = f.read_text(); a = agg.setdefault(f.parent.name, collections.Counter())
        assert (f.with_suffix(".rc")).read_text().strip() == "0", f
        a["runs"] += 1
        a["cycles"] += num(r"LOCKSTEP SUMMARY .*? cycles=(\d+)", t)
        a["mismatching"] += num(r"mismatching=(\d+)", t)
        a["resets"] += num(r"reset_assertions=(\d+)", t)
        for k in ("pdus", "reqs", "frames", "arms", "registrations"):
            a[k] += num(rf"RAND SUMMARY .*\b{k}=(\d+)", t)
        for k in ("tk_wval", "ls_wval", "adm_slope_rd", "tf_head"):
            a[k] += num(rf"LOCKSTEP COVER \S+ .*\b{k}=(\d+)", t)
        q = fifo(t)
        a["tk_max"] = max(a["tk_max"], q[0]); a["ls_max"] = max(a["ls_max"], q[6])
        a["full_cycles"] += q[1] + q[7]; a["push_into_empty"] += q[3] + q[9]
        a["push_with_pop"] += q[4] + q[10]
    cols = ["runs", "cycles", "mismatching", "resets", "pdus", "reqs", "frames", "arms",
            "registrations", "tk_wval", "ls_wval", "adm_slope_rd", "tf_head", "tk_max", "ls_max",
            "full_cycles", "push_into_empty", "push_with_pop"]
    out.append("### Random lockstep campaign (shape-cadence)\n")
    out.append("| shape | " + " | ".join(cols) + " |")
    out.append("|---|" + "---:|" * len(cols))
    tot = collections.Counter()
    for k, a in agg.items():
        out.append(f"| {k} | " + " | ".join(f"{a[c]:,}" for c in cols) + " |")
        for c in cols:
            tot[c] = max(tot[c], a[c]) if c.endswith("_max") else tot[c] + a[c]
    out.append("| **total** | " + " | ".join(f"{tot[c]:,}" for c in cols) + " |\n")
    # ---- controls
    rows = [l.split("\t") for l in (R / "lockstep/controls/controls.tsv").read_text().splitlines() if l]
    shapes = ["1x1", "2x2", "3x5", "9x9"]
    out.append("### Planted controls (mismatching cycles, 3 runs x 500,000 cycles per cell)\n")
    out.append("| control | expect | " + " | ".join(shapes) + " |")
    out.append("|---|---|" + "---:|" * len(shapes))
    for name, exp, _ in rows:
        cells = []
        for sh in shapes:
            s = 0
            for f in sorted((R / "lockstep/controls" / name / f"b-{sh}").glob("run-*.log")):
                assert f.with_suffix(".rc").read_text().strip() == "0", f
                s += num(r"mismatching=(\d+)", f.read_text())
            cells.append(f"{s:,}")
        out.append(f"| `{name}` | {exp} | " + " | ".join(cells) + " |")
    out.append("")
    # ---- stall probe
    out.append("### Full-boundary probe (same TM_SEL stall in base and head; 4 runs x 2,000,000 cycles, compressed)\n")
    out.append("| variant | shape | mismatching per run | tk max / full cycles / blocked pushes | ls max / full cycles / blocked pushes |")
    out.append("|---|---|---|---|---|")
    for d in sorted((R / "lockstep/stall").glob("*/b-*")):
        mm, tk, ls = [], [], []
        for f in sorted(d.glob("run-*.log")):
            t = f.read_text(); q = fifo(t)
            mm.append(str(num(r"mismatching=(\d+)", t)))
            tk.append(f"{q[0]}/{q[1]}/{q[2]}"); ls.append(f"{q[6]}/{q[7]}/{q[8]}")
        out.append(f"| `{d.parent.name}` | {d.name[2:]} | {', '.join(mm)} | {', '.join(tk)} | {', '.join(ls)} |")
    out.append("")
    # ---- committed suites under lockstep
    out.append("### Committed suites with the lockstep bound in\n")
    for s in ("srp_top", "pp_top"):
        t = (R / "lockstep" / s / "ls_run.log").read_text()
        sums = re.findall(r"LOCKSTEP SUMMARY .*? cycles=(\d+) compared=\d+ mismatching=(\d+) reset_cycles=\d+ reset_assertions=(\d+)", t)
        tally = re.findall(r"^(\d+ checks: .*)$", t, re.M)
        out.append(f"- `tb/{s}`: rc {(R / 'lockstep' / s / 'ls_run.rc').read_text().strip()}, "
                   f"{tally[-1] if tally else 'no tally'}; {len(sums)} model instance(s), "
                   f"{sum(int(c) for c, _, _ in sums):,} compared cycles, "
                   f"{sum(int(m) for _, m, _ in sums)} mismatching, "
                   f"{sum(int(r) for _, _, r in sums)} reset assertions")
    print("\n".join(out))


if __name__ == "__main__":
    main()

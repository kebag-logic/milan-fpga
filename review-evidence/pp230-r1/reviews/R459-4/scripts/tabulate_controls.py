#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Tabulate failing checks per shape for the #230 controls from campaign receipts
and compare them with the control tables of tb/srp_top/README.md.

usage: tabulate_controls.py <campaign-output-dir> <README.md> <slope-receipts-dir>
The slope rows are read from per-shape runs (slope_shapes.sh): <label>-N<n>.log.
Exit 0 when every row of both tables equals the receipts.
"""
import re
import sys
from pathlib import Path

out, readme, slopes = Path(sys.argv[1]), Path(sys.argv[2]).read_text(), Path(sys.argv[3])

SHAPE = re.compile(r"^(?:walk records|timer-arm FIFOs): (\d+) sources, (\d+) sinks")
TALLY = re.compile(r"^(\d+) checks: (\d+) PASS, (\d+) FAIL")


def per_shape(log: str) -> dict[str, int]:
    res, cur = {}, None
    for ln in log.splitlines():
        m = SHAPE.match(ln)
        if m:
            cur = f"{m.group(1)}/{m.group(2)}"
            continue
        t = TALLY.match(ln)
        if t and cur:
            res[cur] = int(t.group(3))
            cur = None
    return res


def admission(log: str) -> list[tuple[int, int]]:
    return [(int(m.group(3)), int(m.group(1))) for m in map(TALLY.match, log.splitlines()) if m]


bad = 0
rows = re.findall(r"^\| `((?!slope-)[a-z0-9-]+)` \|[^|]*\|[^|]*\|[^|]*\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
                  readme, re.M)
for label, a, b, c, d, caught in rows:
    log = (out / f"{label}.log").read_text()
    got = per_shape(log)
    want = [a, b, c, d]
    shapes = ["1/1", "2/2", "3/5", "9/9"]
    cells = []
    ok = True
    for s, w in zip(shapes, want):
        g = got.get(s, 0)
        wn = int(w.strip().split()[0].replace(",", ""))
        cells.append(f"{s}={g}")
        ok &= g == wn
    n_caught = sum(1 for s in shapes if got.get(s, 0) > 0)
    ok &= caught.strip() == f"{n_caught} of 4"
    bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} {label}: {' '.join(cells)} caught {n_caught} of 4 | README {[x.strip() for x in want]} {caught.strip()}")

srows = re.findall(r"^\| `(slope-[a-z0-9-]+)` \|[^|]*\|[^|]*\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
                   readme, re.M)
for label, *cols in srows:
    want, caught = cols[:5], cols[5]
    got = []
    for n in (1, 2, 3, 5, 8):
        tallies = admission((slopes / f"{label}-N{n}.log").read_text())
        got.append(tallies[-1] if tallies else None)
    shown = []
    ok = True
    for i, w in enumerate(want):
        w = w.strip()
        if w.startswith("0"):
            g = got[i] if i < len(got) else None
            shown.append(f"{g[0]} of {g[1]}" if g else "n/r")
            ok &= g is not None and g[0] == 0
        else:
            m = re.match(r"([\d,]+) of ([\d,]+)", w)
            fw, tw = int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
            g = got[i] if i < len(got) else None
            shown.append(f"{g[0]} of {g[1]}" if g else "not run")
            ok &= g == (fw, tw)
    n_caught = sum(1 for g in got if g and g[0] > 0)
    ok &= caught.strip() == f"{n_caught} of 5"
    bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} {label}: {shown} caught {n_caught} of 5 | README {[w.strip() for w in want]} {caught.strip()}")
print(f"{len(rows)} control rows, {len(srows)} slope rows, {bad} differing")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Recount, from the committed srp_top campaign's own per-arm receipts, each
#230 control's failing checks per shape ([sources/sinks] suffix of every
FAIL: line) and its failing check names, and compare them row by row with
the PR body's control table.

usage: summarize_r2.py MUTANTS_OUT PR_BODY_MD
"""
import pathlib
import re
import sys

SHAPES = ["1/1", "2/2", "3/5", "9/9"]


def body_rows(path):
    rows = {}
    for line in pathlib.Path(path).read_text().splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 9 and c[0].startswith("`") and c[3] and c[3][0:2] in ("TF", "WK"):
            name = c[0].strip("`")
            cells = [int(re.match(r"(\d+)", x.replace(",", "")).group(1)) for x in c[4:8]]
            rows[name] = (sorted(t.strip() for t in c[3].split(",")), cells, c[8])
    return rows


def main():
    out, body = pathlib.Path(sys.argv[1]), sys.argv[2]
    rows = body_rows(body)
    bad = 0
    print("| control | named checks (receipt) | 1/1 | 2/2 | 3/5 | 9/9 | caught at | = PR body |")
    print("|---|---|---:|---:|---:|---:|---|---|")
    for name, (tags_b, cells_b, caught_b) in rows.items():
        log = out / f"{name}.log"
        text = log.read_text() if log.exists() else ""
        fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
        cells = []
        for sh in SHAPES:
            cells.append(sum(1 for l in fails if l.rstrip().endswith(f"[{sh}]")))
        tags = sorted({re.match(r"FAIL: (TF\d|WK\d)", l).group(1) for l in fails
                       if re.match(r"FAIL: (TF\d|WK\d)", l)})
        caught = f"{sum(1 for x in cells if x)} of 4"
        same = (cells == cells_b and tags == tags_b and caught == caught_b)
        bad += not same
        print(f"| `{name}` | {', '.join(tags)} | " + " | ".join(map(str, cells))
              + f" | {caught} | {'yes' if same else 'NO: body ' + str((tags_b, cells_b, caught_b))} |")
    print(f"\n{len(rows)} rows compared, {bad} differ")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

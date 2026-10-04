#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R458-2: the round-2 control table (29 storage/walk rows: per-shape failing
checks at 1/1, 2/2, 3/5, 9/9, the named failing checks and "Caught at"), in
each markdown file given, against this reviewer's own srp_top campaign receipts
(<campaign dir>/<label>.log, one per planted control).

usage: check_r2_table.py <campaign dir> <markdown file> [...]
"""
import collections
import pathlib
import re
import sys

SHAPES = ["1/1", "2/2", "3/5", "9/9"]


def measured(camp: pathlib.Path, label: str):
    txt = (camp / f"{label}.log").read_text()
    per = collections.Counter()
    tags = set()
    for ln in txt.splitlines():
        if not ln.startswith("FAIL:"):
            continue
        m = re.search(r"\[(\d+/\d+)\]\s*$", ln)
        if not m:
            continue
        per[m.group(1)] += 1
        tag = ln.split(":", 2)[1].strip()
        if re.fullmatch(r"(TF|WK)\d", tag):
            tags.add(tag)
    return per, tags


def main():
    camp = pathlib.Path(sys.argv[1])
    for md in sys.argv[2:]:
        rows = bad = 0
        for ln in open(md):
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(c) != 9 or not c[0].startswith("`") or not re.match(r"\d of 4", c[8]):
                continue
            label = c[0].strip("`")
            if not (camp / f"{label}.log").exists():
                print(f"{md}: {label}: no campaign receipt")
                bad += 1
                continue
            rows += 1
            per, tags = measured(camp, label)
            nz = 0
            for sh, v in zip(SHAPES, c[4:8]):
                n = int(re.match(r"(\d+)", v).group(1))
                nz += n != 0
                if n != per.get(sh, 0):
                    bad += 1
                    print(f"{md}: {label} {sh}: table {n}, campaign {per.get(sh, 0)}")
            named = {t.strip() for t in c[3].split(",")}
            if named != tags:
                bad += 1
                print(f"{md}: {label}: named {sorted(named)}, campaign {sorted(tags)}")
            if f"{nz} of 4" != c[8]:
                bad += 1
                print(f"{md}: {label}: caught-at {c[8]} but {nz} non-zero cells")
        print(f"{md}: {rows} rows, {bad} mismatches")


if __name__ == "__main__":
    main()

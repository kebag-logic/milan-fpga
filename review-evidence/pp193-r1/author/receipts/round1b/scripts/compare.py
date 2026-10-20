#!/usr/bin/env python3
"""Base vs head: normalized log diffs, and the campaigns' per-arm verdicts.

usage: compare.py gates <base dir> <head dir> <out dir>
       compare.py camps <base dir> <head dir> <out dir>
"""
import csv, difflib, re, sys
from pathlib import Path

NORM = [
    (re.compile(r"<scratch>/(base|head)-pp2?(-c)?"), "<tree>"),
    (re.compile(r"<scratch>"), "<scratch>"),
    (re.compile(r"<tmp>/[A-Za-z0-9_.-]+|<scratch><tmp>/[A-Za-z0-9_.-]+"), "<tmpdir>"),
    (re.compile(r"\b\d+(\.\d+)?\s*(s|ms|sec|seconds)\b"), "<t>"),
    (re.compile(r"Walltime [0-9.]+ s.*"), "Walltime <t>"),
    (re.compile(r"allocated [0-9.]+ MB"), "allocated <m>"),
    (re.compile(r"\b[0-9a-f]{40}\b"), "<sha>"),
    (re.compile(r"all\.v:\d+"), "all.v:N"),
]

def norm(text):
    out = []
    for line in text.splitlines():
        for rx, tok in NORM:
            line = rx.sub(tok, line)
        out.append(line)
    return out

def gates(base, head, out):
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for hl in sorted(head.glob("*.log")):
        bl = base / hl.name
        if not bl.exists():
            rows.append((hl.stem, "head only", ""))
            continue
        d = list(difflib.unified_diff(norm(bl.read_text(errors="replace")),
                                      norm(hl.read_text(errors="replace")),
                                      "base/" + hl.name, "head/" + hl.name, lineterm="", n=0))
        (out / (hl.stem + ".diff")).write_text("\n".join(d) + ("\n" if d else ""))
        rows.append((hl.stem, "identical" if not d else f"{sum(1 for x in d if x[:1] in '+-' and x[:3] not in ('+++','---'))} lines differ", ""))
    with (out / "SUMMARY.csv").open("w", newline="") as fh:
        csv.writer(fh).writerows([("log", "normalized base vs head", "")] + rows)

ARM = re.compile(r"^(?P<label>[A-Za-z0-9_.-]+): rc=(?P<rc>-?\d+) failures=(?P<n>\d+) (?P<v>KILLED|UNPROVEN)(?: tags=(?P<tags>.*))?$")

def arms(log):
    res = []
    for line in log.read_text(errors="replace").splitlines():
        m = ARM.match(line.strip())
        if m:
            res.append((m["label"], m["rc"], m["n"], m["v"], m["tags"] or ""))
    return res

def camps(base, head, out):
    out.mkdir(parents=True, exist_ok=True)
    summary = [("campaign", "base arms", "head arms", "common arms with the same verdict and tags", "changed", "head only")]
    for hl in sorted(head.glob("*.log")):
        bl = base / hl.name
        h = arms(hl); b = arms(bl) if bl.exists() else []
        with (out / f"{hl.stem}-arms.csv").open("w", newline="") as fh:
            w = csv.writer(fh); w.writerow(("side", "label", "rc", "failures", "verdict", "tags"))
            for side, rows in (("base", b), ("head", h)):
                for r in rows: w.writerow((side,) + r)
        bmap = {}
        for r in b: bmap.setdefault(r[0], []).append(r)
        same = changed = only = 0
        hseen = {}
        for r in h:
            k = hseen.get(r[0], 0); hseen[r[0]] = k + 1
            br = bmap.get(r[0], [])
            if k >= len(br): only += 1
            elif (br[k][3], br[k][4]) == (r[3], r[4]): same += 1
            else: changed += 1
        summary.append((hl.stem, len(b), len(h), same, changed, only))
    with (out / "SUMMARY.csv").open("w", newline="") as fh:
        csv.writer(fh).writerows(summary)

mode, base, head, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
(gates if mode == "gates" else camps)(base, head, out)
print("ok")

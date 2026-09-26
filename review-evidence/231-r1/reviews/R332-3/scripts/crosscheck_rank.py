#!/usr/bin/env python3
"""Reviewer check: every row present in a round-1 public (filtered) hierarchy
report must equal the committed ranking row at the same scope; rows absent
from the filtered report are listed with their committed LUT/FF.
usage: crosscheck_rank.py <ranking.tsv> <measurement> <report.rpt> <root>"""
import csv, sys
from pathlib import Path
rank, meas, rpt, root = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
rows, anc = {}, []
for line in rpt.read_text().splitlines():
    f = line.split("|")[1:-1]
    if len(f) != 10 or not f[2].strip().isdigit(): continue
    ind = len(f[0]) - len(f[0].lstrip()); d = (ind - 1) // 2; n = f[0].strip()
    if n.startswith("("): n = "@own"
    else: anc = anc[:d] + [n]
    rows["/".join(anc[:d] + [n])] = (int(f[2]), int(f[6]))
bad = missing = ok = 0
for r in csv.DictReader(open(rank), delimiter="\t"):
    if r["measurement"] != meas or r["instance"] == "@reconciliation": continue
    scope = root if r["scope"] == "wrapper" else root + "/u_pp"
    key = scope if r["instance"] == "@total" else scope + "/" + r["instance"]
    want = (int(r["LUT"]), int(r["FF"]))
    if key not in rows: missing += 1; print(f"absent-in-filtered\t{key}\t{want}")
    elif rows[key] != want: bad += 1; print(f"MISMATCH\t{key}\tcommitted={want}\treport={rows[key]}")
    else: ok += 1
print(f"{meas}: equal={ok} mismatch={bad} absent_in_filtered={missing}")

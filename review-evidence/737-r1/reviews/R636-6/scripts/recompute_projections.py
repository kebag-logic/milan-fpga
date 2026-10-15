#!/usr/bin/env python3
"""Recompute the round-6 docs/elaborate worker and workflow projections.

Hosted inputs are read from the saved job listings of the f6260253 runs; the
local inputs are the author's published measurements (round6-projections.json,
round6-docs-builder-legs.json). The formulas are the ones CI_WORKFLOWS.md states.
Usage: recompute_projections.py <docs_jobs.json> <elaborate_jobs.json>
"""
import datetime as dt
import json
import math
import sys


def seconds(a, b):
    t = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (t(b) - t(a)).total_seconds()


def job(path, name):
    j = next(j for j in json.load(open(path))["jobs"] if j["name"] == name)
    steps = {s["name"]: seconds(s["started_at"], s["completed_at"]) for s in j["steps"] if s["completed_at"]}
    return seconds(j["started_at"], j["completed_at"]), steps


docs_job, docs = job(sys.argv[1], "docs-check")
elab_job, elab = job(sys.argv[2], "elaborate")
print(f"hosted docs job {docs_job:.0f} builder {docs['End-station builder gates']:.0f} "
      f"contract {docs['CI event and SHA contract gate']:.0f} runner {docs['Local act runner contract gate']:.0f}")
print(f"hosted elaborate job {elab_job:.0f} gates {elab['Elaboration gates']:.0f} "
      f"litex {elab['Standalone LiteX simulation aggregate']:.0f} "
      f"verilator setup {elab.get('Put Verilator on PATH and prove the version', 0) + elab.get('Build Verilator from source on cache miss', 0) + elab.get('Cache the pinned Verilator build', 0):.0f}")

# Local inputs (author-published, round 5/6 measurements).
setup_and_gaps, worker0_larger, controls = 59.0, 1246.806, 28.331
lone, bank, leg0, leg1 = 1443.720, 1482.211, 1098.130, 506.263
events, runner = 316.686, 113.654
elab_lone, eleg0, eleg1 = 1433.969, 1081.009, 495.144

scale = max(docs["End-station builder gates"], bank, lone) / lone
escale = max(elab["Elaboration gates"], elab_lone) / elab_lone
verilator = 2.0
rows = {
    "docs-gates-0": setup_and_gaps + worker0_larger + controls + 60,
    "docs-gates-0 (hosted basis)": docs_job - docs["End-station builder gates"]
    - docs["CI event and SHA contract gate"] - docs["Local act runner contract gate"] + controls + 60,
    "docs-gates-1": 120 + leg0 * scale,
    "docs-gates-2": 120 + events + runner + 2 + leg1 * scale,
    "elaborate-gates-0": elab_job - elab["Standalone LiteX simulation aggregate"] - verilator
    - elab["Elaboration gates"] + eleg0 * escale + 60,
    "elaborate-gates-1": elab_job - elab["Elaboration gates"] + eleg1 * escale + 60,
}
limit = 45 * 60
for name, value in rows.items():
    up = math.ceil(value)
    print(f"{name:28s} exact {value:9.3f} rounded {up:5d} share {up / limit:.4f} "
          f"{'OK' if up <= 0.6 * limit else 'OVER'} (bound {0.6 * limit:.0f})")
for wf, keys in (("docs", ("docs-gates-0", "docs-gates-1", "docs-gates-2")),
                 ("elaborate", ("elaborate-gates-0", "elaborate-gates-1"))):
    slowest = max(math.ceil(rows[k]) for k in keys)
    total = slowest + 270
    print(f"workflow {wf}: {total} s = {total / 60:.2f} min, margin {1800 - total} s, "
          f"{'OK' if total <= 1800 else 'OVER'}")
# Sensitivity: the contended final-bank elaboration leg 0 (1193 s), which the
# author excludes as double-counted contention.
alt = elab_job - elab["Standalone LiteX simulation aggregate"] - verilator - elab["Elaboration gates"] + 1193 * escale + 60
print(f"sensitivity: elaborate-gates-0 with contended 1193 s leg -> {math.ceil(alt)} s, "
      f"workflow {math.ceil(alt) + 270} s")

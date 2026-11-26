#!/usr/bin/env python3
"""Recompute each divided job's slowest-leg projection from the published hosted job records.
Usage: projection.py <hosted-dir> <local-dir>
For a campaign job: leg projection = (largest leg share of the side-by-side local leg times) x (largest hosted
window of the campaign step) + (largest hosted job window outside that step). For firmware-unit: the sum of
its leg's steps' largest windows + the largest job window outside all four gate steps. Also reports the
alternative of (largest hosted window of the step) / legs + per-leg fixed overhead is NOT modelled here."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

hosted, local = Path(sys.argv[1]), Path(sys.argv[2])


def t(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def runs(workflow):
    data = json.loads((hosted / f"{workflow}-runs.json").read_text())
    return [r["id"] for r in data["workflow_runs"]]


def jobs(run_id):
    return json.loads((hosted / f"{run_id}-jobs.json").read_text())["jobs"]


def windows(workflow, job_name, steps):
    """Per run: job window, each named step's window, and the window outside them."""
    rows = []
    for rid in runs(workflow):
        for job in jobs(rid):
            if job["name"] != job_name or job["conclusion"] != "success":
                continue
            total = t(job["completed_at"]) - t(job["started_at"])
            got = {}
            for s in job["steps"]:
                if s["name"] in steps and s.get("started_at") and s.get("completed_at"):
                    got[s["name"]] = t(s["completed_at"]) - t(s["started_at"])
            if set(got) == set(steps):
                rows.append((rid, total, got, total - sum(got.values())))
    return rows


def local_times(path, pattern):
    out = {}
    for line in (local / path / "summary").read_text().splitlines():
        m = re.match(pattern, line)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


CAMPAIGNS = {
    "firmware-control-mutants": ("Run the control mutation campaign", ("control", r"leg (\d) rc=0 ([\d.]+) s")),
    "firmware-aecp-mutants": ("Run the AECP mutation campaign", ("aecp-srp", r"aecp leg (\d) rc=0 ([\d.]+) s")),
    "firmware-srp-mutants": ("Run both SRP mutation campaigns and pin controls",
                             ("aecp-srp", r"srp leg (\d) rc=0 ([\d.]+) s")),
    "publication-census": ("Run the publication census in every shape the builder builds",
                           ("census", r"leg (\d) rc=0 ([\d.]+) s")),
}
print(f"{'job':28} {'n':>3} {'job max':>8} {'step max':>8} {'outside max':>11} {'share%':>7} {'leg proj':>8} {'x1.41':>6}")
for job, (step, (where, pat)) in CAMPAIGNS.items():
    rows = windows("rtl-fast", job, [step])
    legs = local_times(where, pat)
    share = max(legs.values()) / sum(legs.values())
    step_max = max(r[2][step] for r in rows)
    outside = max(r[3] for r in rows)
    proj = share * step_max + outside
    print(f"{job:28} {len(rows):>3} {max(r[1] for r in rows):>8.0f} {step_max:>8.0f} {outside:>11.0f} "
          f"{100 * share:>7.1f} {proj:>8.0f} {1.41 * proj:>6.0f}   legs={sorted(legs.items())}")
UNIT = {0: ["Prove the tally reads a failing and a crashing test as failures",
            "Run the control-plane firmware suites and RV32 builds"],
        1: ["Run the saved-state store suites and its RV32 build"],
        2: ["Hold the firmware coverage ratchet"]}
names = [n for v in UNIT.values() for n in v]
rows = windows("rtl-fast", "firmware-unit", names)
outside = max(r[3] for r in rows)
for leg, steps in UNIT.items():
    proj = sum(max(r[2][s] for r in rows) for s in steps) + outside
    print(f"firmware-unit leg {leg:<18} {len(rows):>3} {max(r[1] for r in rows):>8.0f} "
          f"{sum(max(r[2][s] for r in rows) for s in steps):>8.0f} {outside:>11.0f} {'-':>7} {proj:>8.0f} {1.41 * proj:>6.0f}")

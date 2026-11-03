"""Recompute the elaborate component maxima from saved jobs-API JSON (reviewer probe, #737).

Usage: python3 -I figures_r767.py <dir-with-jobs-*.json> [file ...]
setup = job span - gate steps - Verilator source build, per elaborate worker.
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def dur(step):
    if not step.get("started_at") or not step.get("completed_at"):
        return 0
    return ts(step["completed_at"]) - ts(step["started_at"])


GATE = ("Elaboration gates", "Standalone LiteX simulation aggregate")
VERILATOR = "Build Verilator from source on cache miss"
base = Path(sys.argv[1])
files = sys.argv[2:] or sorted(p.name for p in base.glob("jobs-*.json"))
best = {}


def keep(key, value, where):
    if value > best.get(key, (-1, ""))[0]:
        best[key] = (value, where)


for name in files:
    data = json.loads((base / name).read_text())
    for job in data["jobs"]:
        if not job.get("started_at") or not job.get("completed_at"):
            continue
        span = ts(job["completed_at"]) - ts(job["started_at"])
        where = f"{name}:{job['name']}:{job['conclusion']}"
        if job["name"].startswith("elaborate-gates-"):
            gates = [(s["name"], dur(s)) for s in job["steps"] if s["name"].startswith(GATE)]
            verilator = sum(dur(s) for s in job["steps"] if s["name"] == VERILATOR)
            gate = sum(d for _, d in gates)
            setup = span - gate - verilator
            print(f"{where} span={span:.0f} gate={gate:.0f} verilator={verilator:.0f} setup={setup:.0f} "
                  + ";".join(f"{n}={d:.0f}" for n, d in gates))
            if job["conclusion"] == "success":
                keep("setup", setup, where)
                keep("span " + job["name"], span, where)
            keep("verilator", verilator, where)
            for gname, d in gates:
                if job["conclusion"] == "success":
                    keep(gname.split(",")[-1].strip() if "Elaboration" in gname else gname, d, where)
        elif job["name"] in ("elaborate", "Collect CI manifest", "Cancel late CI failures"):
            checkout = sum(dur(s) for s in job["steps"] if s["name"] == "Run actions/checkout@v4")
            first = min((ts(s["started_at"]) for s in job["steps"] if s.get("started_at")), default=None)
            lead = (first - ts(job["started_at"])) if first else 0
            print(f"{where} span={span:.0f} checkout={checkout:.0f} rest={span - checkout:.0f} lead={lead:.0f}")
            keep(job["name"] + " span", span, where)
            keep(job["name"] + " rest", span - checkout, where)

print("MAXIMA")
for key in sorted(best):
    print(f"{key}\t{best[key][0]:.0f}\t{best[key][1]}")

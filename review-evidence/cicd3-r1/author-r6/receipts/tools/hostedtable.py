"""hostedtable.py PRIOR.tsv WORKFLOW=JOBS.json...: every job of the given runs (the latest attempt's jobs API), its
minutes (completed_at - started_at; a job that never started counts 0), and its factor against the same job's
earlier successful windows (PRIOR.tsv: run, workflow, job, conclusion, seconds, runner; a matrix job's N/M is
kept, so a worker is compared with the same-numbered worker of older deals only where the name matches).
Factor = this window / the median earlier window; also / the slowest earlier window. Jobs over 1800 s are marked."""
import csv
import json
import statistics
import sys
from datetime import datetime


def secs(a: str, b: str) -> float:
    """b - a, both ISO times."""
    f = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (f(b) - f(a)).total_seconds()


prior: dict[tuple[str, str], list[float]] = {}
for row in csv.reader(open(sys.argv[1], encoding="utf-8"), delimiter="\t"):
    if len(row) >= 5 and row[3] == "success":
        prior.setdefault((row[1], row[2]), []).append(float(row[4]))
print("workflow\tjob\tconclusion\tstarted\tseconds\tminutes\tprior_n\tprior_median\tprior_max\tx_median\tx_max\tover_30")
total = {}
for arg in sys.argv[2:]:
    wf, path = arg.split("=", 1)
    jobs = json.load(open(path, encoding="utf-8"))["jobs"]
    for j in jobs:
        ran = j.get("steps") and any(s.get("started_at") for s in j["steps"][1:])
        s = secs(j["started_at"], j["completed_at"]) if j.get("completed_at") and ran else 0.0
        total[wf] = total.get(wf, 0.0) + s
        p = prior.get((wf, j["name"]), [])
        med = statistics.median(p) if p else None
        mx = max(p) if p else None
        print("\t".join([wf, j["name"], str(j.get("conclusion")), j["started_at"][11:19], f"{s:.0f}", f"{s / 60:.1f}",
                         str(len(p)), f"{med:.0f}" if med else "", f"{mx:.0f}" if mx else "",
                         f"{s / med:.2f}" if med and s else "", f"{s / mx:.2f}" if mx and s else "",
                         "OVER" if s > 1800 else ""]))
for wf, s in total.items():
    print(f"# {wf}: {s / 60:.1f} job-minutes (jobs that ran)")

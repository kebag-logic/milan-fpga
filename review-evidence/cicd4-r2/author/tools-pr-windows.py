"""Every job window of the PR head's hosted runs, against #998's 1276 s budget (1800 s at 1.41x)."""
import json, glob, datetime, sys
from pathlib import Path
d = Path(sys.argv[1]); t = lambda s: datetime.datetime.fromisoformat(s)
rows = []
for f in sorted(d.glob("jobs-*.json")):
    run = f.stem.split("-")[1]
    wf = json.loads((d / f"run-{run}.json").read_text())["name"]
    for j in json.loads(f.read_text())["jobs"]:
        if j["conclusion"] == "skipped":
            continue
        s = (t(j["completed_at"]) - t(j["started_at"])).total_seconds() if j.get("completed_at") and j.get("started_at") else None
        rows.append((wf, j["name"], j["status"], j["conclusion"], s))
print("workflow\tjob\tstatus\tconclusion\tseconds\tx1.41\tverdict")
for wf, n, st, c, s in sorted(rows, key=lambda r: (r[0], -(r[4] or 0))):
    v = "" if s is None else ("over" if s > 1276 else "within")
    if n.startswith(("Fail fast", "Physical gPTP")) and s is not None:
        v += " (documented exception)"
    print(f"{wf}\t{n}\t{st}\t{c}\t{'' if s is None else round(s)}\t{'' if s is None else round(s * 1.41)}\t{v}")

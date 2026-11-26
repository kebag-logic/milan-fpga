import json, subprocess, datetime, collections, statistics
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / "hosted"
def api(endpoint, file):
    data = subprocess.check_output(["gh", "api", endpoint], text=True)
    (OUT / file).write_text(data)
    return json.loads(data)
rows=[]
for name,wid in [("rtl-fast",339150340),("rtl-full",320750503),("elaborate",339283801),("docs",320168027)]:
    runs=api(f"repos/kebag-logic/milan-fpga/actions/workflows/{wid}/runs?status=success&per_page=20",f"{name}-runs.json")["workflow_runs"]
    assert len(runs)==20
    for run in runs:
        rid=run["id"]
        jobs=api(f"repos/kebag-logic/milan-fpga/actions/runs/{rid}/jobs?per_page=100", f"{rid}-jobs.json")
        assert jobs["total_count"]<=100
        for j in jobs["jobs"]:
            if j["conclusion"]=="skipped":continue
            if "self-hosted" in j["labels"]:continue
            duration=(datetime.datetime.fromisoformat(j["completed_at"])-datetime.datetime.fromisoformat(j["started_at"])).total_seconds()
            rows.append(dict(workflow=name,run=rid,sha=run["head_sha"],branch=run["head_branch"],name=j["name"],id=j["id"],seconds=duration,labels=j["labels"]))
    print(name,len(runs),"runs collected",flush=True)
(OUT/"durations.json").write_text(json.dumps(rows,indent=2)+"\n")
groups=collections.defaultdict(list)
for r in rows:groups[(r["workflow"],r["name"])].append(r["seconds"])
lines=["workflow\tjob\tn\tmin_s\tmean_s\tp95_s\tmax_s\tmean_x1.41_s\tmax_x1.41_s\tmax_run"]
for (w,n),v in groups.items():
    high=max(r["run"] for r in rows if r["workflow"]==w and r["name"]==n and r["seconds"]==max(v))
    lines.append(f"{w}\t{n}\t{len(v)}\t{min(v):.0f}\t{statistics.mean(v):.1f}\t{sorted(v)[int(.95*(len(v)-1))]:.0f}\t{max(v):.0f}\t{statistics.mean(v)*1.41:.1f}\t{max(v)*1.41:.1f}\t{high}")
(OUT/"durations.tsv").write_text("\n".join(lines)+"\n")
for name in ("rtl-fast","rtl-full","elaborate","docs"):
    totals=collections.defaultdict(float)
    for r in rows:
        if r["workflow"]==name:totals[r["run"]]+=r["seconds"]/60
    print(name,"mean runner minutes including watchers",round(statistics.mean(totals.values()),2))

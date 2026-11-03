"""Summarise hosted jobs at the exact head against ruling item 3 (job timeout, 2100 s elaborate worker span)."""
import json, subprocess, sys, datetime as d
HEAD = sys.argv[1]
t = lambda s: d.datetime.fromisoformat(s.replace('Z', '+00:00'))
runs = json.loads(subprocess.check_output(["gh", "api", f"repos/kebag-logic/milan-fpga/actions/runs?head_sha={HEAD}&per_page=50"]))
out = {}
for r in runs["workflow_runs"]:
    jobs = json.loads(subprocess.check_output(["gh", "api", "--paginate", f"repos/kebag-logic/milan-fpga/actions/runs/{r['id']}/attempts/{r['run_attempt']}/jobs?per_page=100"]))
    out[r["id"]] = {"name": r["name"], "attempt": r["run_attempt"], "status": r["status"], "conclusion": r["conclusion"], "jobs": jobs["jobs"]}
    counts = {}
    for j in jobs["jobs"]:
        counts[(j["status"], j["conclusion"])] = counts.get((j["status"], j["conclusion"]), 0) + 1
    print(r["id"], r["name"], "a%d" % r["run_attempt"], r["status"], r["conclusion"], dict((f"{k[0]}/{k[1]}", v) for k, v in counts.items()))
    for j in jobs["jobs"]:
        if j["conclusion"] not in (None, "success", "skipped") or r["name"] == "elaborate":
            span = (t(j["completed_at"]) - t(j["started_at"])).total_seconds() if j["completed_at"] and j["started_at"] else None
            print("   ", j["name"], j["status"], j["conclusion"], span)
json.dump(out, open(sys.argv[2], "w"), indent=1)

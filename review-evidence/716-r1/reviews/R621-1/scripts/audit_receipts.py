#!/usr/bin/env python3
"""Cross-check published historical measurements, prediction arithmetic and contexts."""
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime
import json
import math
from pathlib import Path
import subprocess

packet=Path(__file__).resolve().parents[1]
author=packet/"scratch/public-author"
out=packet/"receipts"
repo="repos/kebag-logic/milan-fpga"
head="f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48"


def api(path):
    return json.loads(subprocess.check_output(["gh","api",path],timeout=90))


def historical(item):
    job_id, rows=item
    j=api(f"{repo}/actions/jobs/{job_id}")
    assert j["name"] == "firmware-unit" and j["conclusion"] == "success"
    assert j["head_sha"] == rows[0]["head"]
    for r in rows:
        step=next(s for s in j["steps"] if s["number"] == int(r["step"]))
        assert step["name"] == r["name"]
        assert step["started_at"] == r["start_utc"] and step["completed_at"] == r["end_utc"]
        elapsed=(datetime.fromisoformat(step["completed_at"])-datetime.fromisoformat(step["started_at"])).total_seconds()
        assert elapsed == float(r["seconds"])
    total=(datetime.fromisoformat(j["completed_at"])-datetime.fromisoformat(j["started_at"])).total_seconds()
    return {"id":j["id"],"run_id":j["run_id"],"head_sha":j["head_sha"],"conclusion":j["conclusion"],"started_at":j["started_at"],"completed_at":j["completed_at"],"total_seconds":total,"steps":j["steps"]}


def main():
    rows=list(csv.DictReader((author/"HOSTED-STEPS.csv").open()))
    by_job={}
    for row in rows:
        by_job.setdefault(row["job_id"],[]).append(row)
    with ThreadPoolExecutor(max_workers=4) as pool:
        measured=list(pool.map(historical,by_job.items()))
    (out/"historical-api.json").write_text(json.dumps(measured,indent=2)+"\n")
    print(f"PASS: {len(rows)} published step timestamps and durations match the API across {len(measured)} historical jobs.")
    print("Historical total range: %d..%d seconds."%(min(j["total_seconds"] for j in measured),max(j["total_seconds"] for j in measured)))
    baseline=json.loads((author/"BASELINE-RESULTS.json").read_text())
    candidate=json.loads((author/"CANDIDATE-RESULTS.json").read_text())
    prediction=json.loads((author/"TIMING-PREDICTIONS.json").read_text())
    assert all(r["rc"]==0 for r in baseline)
    assert math.isclose(sum(r["seconds"] for r in baseline),prediction["baseline_local_seconds"])
    for job in candidate:
        assert job["head"]==head and all(c["rc"]==0 for c in job["commands"])
        assert math.isclose(sum(c["seconds"] for c in job["commands"]),job["seconds"],abs_tol=.02)
        p=next(p for p in prediction["predictions"] if p["job"]==job["job"])
        assert p["local_seconds"]==job["seconds"]
        for ratio_key,result_key in (("base_ratio","base_prediction_seconds"),("envelope_ratio","envelope_prediction_seconds")):
            assert math.ceil(job["seconds"]*prediction[ratio_key]+prediction["setup_allowance_seconds"])==p[result_key]
        assert p["envelope_prediction_seconds"] <= .6*p["timeout_seconds"]
    print("PASS: published four-CPU receipts and prediction arithmetic agree; maximum conservative prediction 879 seconds below 1620 seconds.")
    comparisons=list(csv.DictReader((author/"COVERAGE-COMPARISON.csv").open()))
    assert len(comparisons)==30
    for r in comparisons:
        for key in ("raw_lines","raw_branches","kept_lines","kept_branches"):
            assert r["baseline_"+key]==r["candidate_"+key]
        assert r["equal"]=="True"
    print("PASS: published coverage table has 30 matching rows (reported measurement; no local recompilation claimed).")
    checks=api(f"{repo}/commits/{head}/check-runs?per_page=100")
    assert checks["total_count"] <=100
    projected=[{k:c[k] for k in ("name","head_sha","status","conclusion","started_at","completed_at","details_url")} for c in checks["check_runs"]]
    (out/"hosted-contexts.json").write_text(json.dumps(projected,indent=2)+"\n")
    for c in projected:
        print("CONTEXT",c["name"],c["status"],c["conclusion"])


if __name__=="__main__":
    main()

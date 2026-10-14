#!/usr/bin/env python3
"""Read exact-head runs and derive first-start-to-last-end workflow windows."""
import datetime,json,pathlib,subprocess
packet=pathlib.Path(__file__).resolve().parent
repo="kebag-logic/milan-fpga";head="2658a64c408bf87ae36574f36a6deeb34b2f297f"
commands=[]
def run(cmd):
 commands.append(cmd)
 return json.loads(subprocess.check_output(cmd,text=True))
runs=run(["gh","api",f"repos/{repo}/actions/runs?head_sha={head}&per_page=100"])
(packet/"hosted-exact-head.json").write_text(json.dumps(runs,indent=2)+"\n")
windows=[]
for row in runs["workflow_runs"]:
 run_id=row["id"]
 d=run(["gh","run","view",str(run_id),"-R",repo,"--json","jobs,headSha,workflowName,status,conclusion,url"])
 (packet/f"hosted-run-{run_id}.json").write_text(json.dumps(d,indent=2)+"\n")
 executed=[job for job in d["jobs"] if job["conclusion"]!="skipped"]
 completed=executed and all(job["completedAt"] and job["completedAt"]!="0001-01-01T00:00:00Z" for job in executed)
 first=min((job["startedAt"] for job in executed),default=None)
 last=max((job["completedAt"] for job in executed),default=None) if completed else None
 seconds=(datetime.datetime.fromisoformat(last.replace("Z","+00:00"))-datetime.datetime.fromisoformat(first.replace("Z","+00:00"))).total_seconds() if last else None
 windows.append({"workflow":d["workflowName"],"run":row["id"],"head":d["headSha"],"first_start":first,"last_end":last,"seconds":seconds,"executed_jobs":len(executed),"skipped_jobs":len(d["jobs"])-len(executed),"conclusion":d["conclusion"]})
if not windows:
 windows=[{"workflow":name,"seconds":None,"reason":"No exact-head workflow run returned by GitHub"} for name in ("docs","elaborate","rtl-fast","rtl-full")]
state=run(["gh","pr","view","739","-R",repo,"--json","headRefOid,baseRefOid,mergeable,statusCheckRollup"])
(packet/"hosted-pr-state.json").write_text(json.dumps(state,indent=2)+"\n")
receipt={"queried_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":head,"total_count":runs["total_count"],"windows":windows,"commands":commands,"acceptance":"Manager decision; no duration inferred from skipped jobs or missing runs."}
(packet/"hosted-readback.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))

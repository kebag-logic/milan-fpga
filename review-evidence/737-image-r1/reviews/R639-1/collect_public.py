#!/usr/bin/env python3
"""Collect read-only public review and hosted state after independent assessment."""
import datetime,json,subprocess,sys
from pathlib import Path
packet=Path(sys.argv[1]);repo="repos/kebag-logic/milan-fpga";head="2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895"
def get(path):
 raw=subprocess.check_output(["gh","api",repo+path,"--paginate","--slurp"])
 pages=json.loads(raw)
 if isinstance(pages[0],list):return [row for page in pages for row in page]
 return pages
comments=get("/issues/738/comments");reviews=get("/pulls/738/reviews");inline=get("/pulls/738/comments")
out={"queried_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":head,"review_bodies": [{"id":r["id"],"body":r["body"],"commit_id":r["commit_id"],"state":r["state"]} for r in reviews],"inline_findings":[{"id":r["id"],"body":r["body"],"path":r["path"],"commit_id":r["commit_id"]} for r in inline],"issue_comment_ids":[r["id"] for r in comments],"reviewer_issue_comments":[{"id":r["id"],"body":r["body"],"url":r["html_url"]} for r in comments if r["body"].lstrip().startswith("[R")]}
(packet/"prior-review-state.json").write_text(json.dumps(out,indent=2)+"\n")
run_pages=get("/actions/runs?head_sha="+head+"&per_page=100")
runs=[r for page in run_pages for r in page["workflow_runs"] if r["head_sha"]==head]
collected=[]
for r in runs:
 jobs=[j for page in get(f"/actions/runs/{r['id']}/jobs?per_page=100") for j in page["jobs"]]
 collected.append({"id":r["id"],"name":r["name"],"head_sha":r["head_sha"],"url":r["html_url"],"status":r["status"],"conclusion":r["conclusion"],"jobs":[{"id":j["id"],"name":j["name"],"status":j["status"],"conclusion":j["conclusion"],"steps":[{"name":s["name"],"status":s["status"],"conclusion":s["conclusion"]} for s in j.get("steps",[])]} for j in jobs]})
(packet/"hosted-state.json").write_text(json.dumps({"queried_at":out["queried_at"],"head":head,"runs":collected,"limit":"One read-only snapshot; no hosted/act acceptance or source-bank claim."},indent=2)+"\n")
print(json.dumps({"prior_reviews":len(reviews),"inline_comments":len(inline),"reviewer_issue_comments":len(out["reviewer_issue_comments"]),"runs":[{"name":r["name"],"status":r["status"],"conclusion":r["conclusion"],"job_states":{k:sum(j["conclusion"]==k for j in r["jobs"]) for k in ("success","failure","skipped",None)}} for r in collected]},indent=2))

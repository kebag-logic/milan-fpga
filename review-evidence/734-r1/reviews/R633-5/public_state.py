#!/usr/bin/env python3
"""Read public scope, previous findings, and exact-head execution status."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

REPO = "repos/kebag-logic/milan-fpga"
HEAD = "7c862ad980dfe829ef4d85ff8f4fb4fab451984f"
DECISIONS = [6151273761, 6151933918, 6152693618, 6153494016, 6154792285, 6154957125, 6154996578]
PRIOR = [6151873947, 6151927790, 6152579254, 6152686595, 6153458432, 6153487534, 6154103252, 6154173153]


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", f"{REPO}/{path}"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("--comments-only", action="store_true")
    args = parser.parse_args()
    assert (args.packet / "independent-pass.md").exists(), "Write own verdict and ledger first"
    output = args.packet / "public-state"
    output.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    if args.comments_only:
        observation = {"observed_at": timestamp, "threads": {}}
        for number in (734, 735):
            comments = api(f"issues/{number}/comments?per_page=100")
            observation["threads"][str(number)] = {"comments": [{"id": c["id"], "url": c["html_url"], "lead": c["body"].splitlines()[0]} for c in comments], "manager_comments": [{"id": c["id"], "url": c["html_url"], "body": c["body"]} for c in comments if c["body"].startswith("[A10]")]}
        (output / "final-comment-observation.json").write_text(json.dumps(observation, indent=2) + "\n")
        print(json.dumps({"observed_at": timestamp, "counts": {n: len(t["comments"]) for n, t in observation["threads"].items()}}, indent=2))
        return
    def comment(number):
        data = api(f"issues/comments/{number}")
        return {k: data[k] for k in ("id", "html_url", "created_at", "updated_at", "body")}
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(comment, DECISIONS + PRIOR))
    for record in records:
        (output / f"comment-{record['id']}.json").write_text(json.dumps(record, indent=2) + "\n")
    issue = api("issues/734")
    (output / "issue.json").write_text(json.dumps({k: issue[k] for k in ("number", "html_url", "title", "body", "state")}, indent=2) + "\n")
    pr = api("pulls/735")
    assert pr["head"]["sha"] == HEAD
    (output / "pull.json").write_text(json.dumps({"observed_at": timestamp, "head": pr["head"]["sha"], "base": pr["base"]["sha"], "draft": pr["draft"], "html_url": pr["html_url"], "body": pr["body"]}, indent=2) + "\n")
    runs = api(f"actions/runs?head_sha={HEAD}&per_page=100")["workflow_runs"]
    def run(record):
        result = {k: record[k] for k in ("id", "name", "html_url", "head_sha", "event", "status", "conclusion")}
        result["jobs"] = [{k: job[k] for k in ("id", "name", "status", "conclusion", "html_url", "head_sha", "started_at", "completed_at")} for job in api(f"actions/runs/{record['id']}/jobs?per_page=100")["jobs"]]
        return result
    with ThreadPoolExecutor(max_workers=4) as pool:
        observed_runs = list(pool.map(run, runs))
    (output / "hosted.json").write_text(json.dumps({"observed_at": timestamp, "runs": observed_runs}, indent=2) + "\n")
    comments = api("issues/735/comments?per_page=100")
    # All public comment metadata, but do not read another current-round report.
    metadata = [{"id": c["id"], "url": c["html_url"], "lead": c["body"].splitlines()[0]} for c in comments]
    managers = [{"id": c["id"], "url": c["html_url"], "body": c["body"]} for c in comments if c["body"].startswith("[A10]")]
    issue_comments = api("issues/734/comments?per_page=100")
    issue_managers = [{"id": c["id"], "url": c["html_url"], "body": c["body"]} for c in issue_comments if c["body"].startswith("[A10]")]
    reviews = api("pulls/735/reviews?per_page=100")
    inline = api("pulls/735/comments?per_page=100")
    (output / "observation.json").write_text(json.dumps({"observed_at": timestamp, "comments": metadata, "manager_comments": managers, "issue_manager_comments": issue_managers, "submitted_review_count": len(reviews), "inline_comment_count": len(inline)}, indent=2) + "\n")
    print(json.dumps({"observed_at": timestamp, "runs": observed_runs, "public_comment_count": len(comments), "submitted_review_count": len(reviews), "inline_comment_count": len(inline)}, indent=2))


if __name__ == "__main__":
    main()

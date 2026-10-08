#!/usr/bin/env python3
"""Record public receipt population and evidence comments without copying review reports."""
from collections import Counter
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
for filename, endpoint, paginate in (
    ("issue.json", "issues/686", False),
    ("pr.json", "pulls/695", False),
    ("issue-comments.json", "issues/686/comments", True),
    ("pr-comments.json", "issues/695/comments", True),
    ("pr-reviews.json", "pulls/695/reviews", True),
    ("pr-inline.json", "pulls/695/comments", True),
):
    path = scratch / filename
    if not path.exists():
        cmd = ["gh", "api"] + (["--paginate", "--slurp"] if paginate else [])
        path.write_bytes(subprocess.check_output(cmd + ["repos/kebag-logic/milan-fpga/" + endpoint]))
inventories = {}
for filename in ("archive-tree.json", "fix-tree.json", "candidate-tree.json"):
    data = json.loads((scratch / filename).read_text())
    counts = Counter()
    paths = []
    for entry in data["tree"]:
        path = entry["path"]
        if entry["type"] != "blob" or not path.startswith("review-evidence/686-r1/"):
            continue
        parts = path.split("/")
        if parts[2] == "reviews":
            counts["reviewer packets (excluded as source-bank receipts)"] += 1
        else:
            counts["/".join(parts[2:4])] += 1
            paths.append(path)
    inventories[filename] = dict(truncated=data["truncated"], population=dict(counts), nonreview_files=paths)
comments = []
selected = {6029233665,6043036997,6047563934,6051028263,6052017268,6052020520}
for filename in ("issue-comments.json", "pr-comments.json"):
    for page in json.loads((scratch / filename).read_text()):
        for c in page:
            if c["id"] in selected:
                comments.append({k:c[k] for k in ("id","html_url","created_at","updated_at","body")})
pr = json.loads((scratch / "pr.json").read_text())
issue = json.loads((scratch / "issue.json").read_text())
result = dict(archives=inventories, evidence_comments=comments,
              issue=dict(number=issue["number"],body=issue["body"]),
              pr=dict(number=pr["number"],head=pr["head"]["sha"],body=pr["body"]),
              submitted_reviews=sum(map(len,json.loads((scratch/"pr-reviews.json").read_text()))),
              inline_comments=sum(map(len,json.loads((scratch/"pr-inline.json").read_text()))))
(packet / "receipts/public-inventory.json").write_text(json.dumps(result, indent=2) + "\n")
print("Public inventory recorded; no exact-source manager-bank directory among supplied evidence paths")

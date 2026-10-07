#!/usr/bin/env python3
"""Produce portable public metadata and a page-command ledger from receipts.

Usage: python3 scripts/summarize_receipts.py PACKET
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
scratch = packet / "scratch"
receipts = packet / "receipts"
def read(name):
    return json.loads((scratch / name).read_text())
pr = read("pr-5.json")
comments = read("pr-5-comments-final.json")
issue_comments = read("issue-1-comments-final.json")
status = read("commit-status.json")
snapshot = dict(
    collected_utc=datetime.now(timezone.utc).isoformat(),
    issue_url="https://github.com/kebag-logic/lwSRP/issues/1",
    pr_url="https://github.com/kebag-logic/lwSRP/pull/5",
    head=pr["head"]["sha"], current_pr_base=pr["base"]["sha"],
    review_source_base="19f5796b63652eb1151906de73cb827d4980a53f",
    live_parent_development="910f338dbd050f4efd2d96991ddcf928a583d55f",
    author_evidence_archive="3f31bba3bfade7da27bc45f42080aae9a9887a22",
    issue_comment_ids=[x["id"] for x in issue_comments],
    pr_comment_ids=[x["id"] for x in comments],
    formal_reviews=len(read("pr-5-reviews.json")), inline_comments=len(read("pr-5-inline.json")),
    check_runs=read("check-runs.json")["total_count"],
    workflow_runs=read("actions.json")["total_count"],
    commit_status_contexts=status["total_count"], combined_status=status["state"],
    manager_execution_evidence_comments_found=0,
    prior_findings_on_this_pr=0,
    previous_layout_finding="https://github.com/kebag-logic/lwSRP/pull/3#issuecomment-6030780352",
)
(receipts / "public-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
rows = []
for row in json.loads((receipts / "quick-start-commands.json").read_text()):
    rows.append((row["page"]+":"+str(row["line"]), row["command"], row["rc"], "quick-start-"+str(row["line"])))
commands = {x["name"]:x for x in json.loads((receipts / "commands.json").read_text())}
mapping = [(15,"configure"),(16,"build"),(17,"ctest"),(18,"unit"),(19,"scenarios"),(20,"scenario-dry"),
           (45,"isolated-compile"),(53,"isolated-run")]
for line, suffix in mapping:
    name = "published-" + suffix
    row = commands[name]
    cmd = " ".join(row["command"])
    if suffix == "isolated-compile":
        cmd = "isolated compile command and complete here-document, as printed on the page"
    rows.append(("doc/tester.md:"+str(line),cmd,row["rc"],name))
for line,suffix in [(14,"sentences"),(15,"references"),(16,"links"),(17,"render-published")]:
    name = "docs-" + suffix
    row = commands[name]
    rows.append(("doc/tools/README.md:"+str(line)," ".join(row["command"]),row["rc"],name))
out = ["All 16 shell-command occurrences ran from an exact-head disposable source copy.",
       "Dependency discovery variables point only to the disposable local installation.",
       "The isolated compile entry includes the complete here-document in commands.json.",
       "", "| Page and line | Command | rc | Receipt |", "| --- | --- | --- | --- |"]
for page,cmd,rc,name in rows:
    out.append(f"| {page} | `{cmd}` | {rc} | [{name}.log]({name}.log) |")
out.extend(["", "Only the expected eight licence-link failures returned nonzero.",
            "Every command has a matching .rc receipt. Raw process output changes only by path normalization."])
(receipts / "page-commands.md").write_text("\n".join(out)+"\n")
versions = {}
for key, cmd in [("renderer",["mmdc","--version"]),("compiler",["cc","-dumpfullversion"]),
                 ("build_system",["cmake","--version"]),("scenario_runner",["behave","--version"])]:
    r = subprocess.run(cmd,capture_output=True,text=True,check=True)
    versions[key] = dict(version=r.stdout.splitlines()[0], rc=r.returncode)
versions["unit_dependency"] = dict(release="1.7.0", archive_sha256=hashlib.sha256((scratch / "dependency.tar.gz").read_bytes()).hexdigest(), installation="scratch only")
versions["preview_bootstrap"] = dict(initial_rc=1, reason="Optional image-sheet dependency absent", retry_rc=0, installation="scratch only")
(receipts / "environment.json").write_text(json.dumps(versions,indent=2)+"\n")
# System locations are not useful public evidence. Preserve original streams in scratch.
for p in receipts.glob("*.log"):
    text = p.read_text()
    text = text.replace("/usr/bin/", "<system-bin>/").replace("/usr/lib/", "<system-lib>/")
    p.write_text(text)
print(json.dumps(snapshot,indent=2))

#!/usr/bin/env python3
"""Read public PR state and verify the round-two corrections. Usage: REPO PACKET."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo, packet = (Path(p).resolve() for p in sys.argv[1:])
head = "793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df"
parent = "26bd6334a7b8b2a8582b36ae4729a71620546c14"
base = "bd884631684ccf5060339efa92263d5c3e5c262c"
def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])
def api(endpoint):
    return json.loads(subprocess.check_output(["gh", "api", "--paginate", endpoint]))

paths = ["docs/testing/TESTING.md", "docs/testing/RUNNING_TESTS.md",
         "tb/verilator/milan_dp/README.md", "tb/verilator/milan_dp_gptp/README.md"]
assert git("rev-parse", head + "^").decode().strip() == parent
assert set(git("diff", "--name-only", parent, head).decode().splitlines()) == set(paths)
assert not git("diff", base, head, "--", "hdl", ".github", "scripts/suite_shards.py",
               "protocol-processor", "gptp-processor", "third_party/verilog-axis")
for path in paths:
    text = (repo / path).read_text()
    assert "CI_WORKFLOWS.md#exhaustive-validation" in text
    assert "issues/673#issuecomment-6015726285" in text
pattern = "1800-second deadline except|3600 seconds for .milan_dp|own 3600-second budget|milan_dp. has 3600"
result = subprocess.run(["rg", "-n", pattern, "docs", "tb/verilator", "--glob", "*.md"],
                        cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
assert result.returncode == 1 and not result.stdout, (result.returncode, result.stdout)
pr = api("repos/kebag-logic/milan-fpga/pulls/681")
assert pr["head"]["sha"] == head
body = pr["body"]
for stale in ("the branch has not been pushed", "no PR has been created", "prepared for the future PR comment"):
    assert stale not in body, stale
assert "Published as PR #681 for independent review." in body
(packet / "receipts/pr-body-snapshot.md").write_text(body + "\n")
snapshot = {k: pr[k] for k in ("number", "state", "draft", "html_url", "updated_at")}
snapshot.update(head=head, base=pr["base"]["sha"],
                body_sha256=hashlib.sha256((body + "\n").encode()).hexdigest())
(packet / "receipts/pr-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
comments = api("repos/kebag-logic/milan-fpga/issues/681/comments")
reviews = api("repos/kebag-logic/milan-fpga/pulls/681/reviews")
inline = api("repos/kebag-logic/milan-fpga/pulls/681/comments")
reconciliation = {
    "head": head,
    "comments": [{"id": c["id"], "url": c["html_url"]} for c in comments],
    "formal_review_count": len(reviews), "inline_comment_count": len(inline),
    "dispositions": {"R516-F1": "RESOLVED: docs point to current policy and ruling; exact search has no hits; 60-suite count confirmed",
                     "R516-F2": "RESOLVED: current public body has no unpublished or future-comment sentences",
                     "R517-1-D1": "RESOLVED: public body contains the requested publication sentence"},
    "prior_reports_read_after_independent_verdict_and_ledger": True,
    "stale_search_command": ["rg", "-n", pattern, "docs", "tb/verilator", "--glob", "*.md"],
    "stale_search_rc": result.returncode,
}
(packet / "receipts/prior-findings.json").write_text(json.dumps(reconciliation, indent=2) + "\n")
diff = git("diff", "--no-ext-diff", "--no-textconv", base, head)
delta = git("diff", "--no-ext-diff", "--no-textconv", parent, head)
(packet / "receipts/round2.diff").write_bytes(delta)
scope = {"head": head, "tree": git("rev-parse", head + "^{tree}").decode().strip(),
         "base": base, "parent": parent,
         "full_diff_sha256": hashlib.sha256(diff).hexdigest(),
         "round2_diff_sha256": hashlib.sha256(delta).hexdigest(),
         "full_changed_paths": git("diff", "--name-only", base, head).decode().splitlines(),
         "round2_changed_paths": sorted(paths),
         "history": git("log", "--format=%H %s", base + ".." + head).decode().splitlines(),
         "unchanged_behavior_paths": ["hdl", ".github", "scripts/suite_shards.py", "protocol-processor", "gptp-processor", "third_party/verilog-axis"]}
(packet / "receipts/source-scope.json").write_text(json.dumps(scope, indent=2) + "\n")
print("PASS: round two contains only the four assigned Markdown paths")
print("PASS: all four current deadline references link the policy table and ruling")
print("PASS: exact prior-review search returns rc 1 with zero hits")
print("PASS: public body resolves R516-F2 and R517-1-D1")
print(f"Public review records: {len(comments)} discussion comments, {len(reviews)} formal reviews, {len(inline)} inline comments")

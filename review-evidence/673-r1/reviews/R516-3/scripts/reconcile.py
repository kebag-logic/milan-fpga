#!/usr/bin/env python3
"""Read public findings metadata and verify the previously requested corrections."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
assert (packet / "receipts/independent-pass.md").read_text().startswith("[R516] POSITIVE")

def get(path):
    return json.loads(subprocess.check_output(["rtk", "proxy", "gh", "api", "--paginate",
                                              "repos/kebag-logic/milan-fpga/" + path]))

pr = get("pulls/681")
comments = get("issues/681/comments")
reviews = get("pulls/681/reviews")
inline = get("pulls/681/comments")
assert pr["head"]["sha"] == "793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df"
paths = ["docs/testing/TESTING.md", "docs/testing/RUNNING_TESTS.md",
         "tb/verilator/milan_dp/README.md", "tb/verilator/milan_dp_gptp/README.md"]
for name in paths:
    content = (repo / name).read_text()
    assert "CI_WORKFLOWS.md#exhaustive-validation" in content
    assert "issuecomment-6015726285" in content
    print("R516-F1 corrected policy and ruling links:", name)
pattern = "1800-second deadline except|3600 seconds for .milan_dp|own 3600-second budget|milan_dp. has 3600"
result = subprocess.run(["rtk", "proxy", "rg", "-n", pattern, "docs", "tb/verilator",
                         "--glob", "*.md"], cwd=repo, capture_output=True, text=True)
assert result.returncode == 1 and not result.stdout
print("R516-F1 original search: no matches, expected rc 1")
inventory = subprocess.check_output(["rtk", "proxy", "bash", "scripts/run_all_suites.sh", "--list"], cwd=repo, text=True).splitlines()
assert len(inventory) == len(set(inventory)) == 60
print("R516-F1 live default inventory: 60 distinct suites")
body = pr["body"]
for phrase in ["the branch has not been pushed", "no PR has been created",
               "self-test evidence is prepared for the future PR comment"]:
    assert phrase not in body
assert "Published as PR #681 for independent review." in body
print("R516-F2 / R517-1-D1: obsolete phrases absent, requested publication wording present")
metadata = {"pr_head": pr["head"]["sha"], "pr_body_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "discussion_comments": [{"id": c["id"], "url": c["html_url"],
                                      "opening": c["body"].splitlines()[0],
                                      "body_sha256": hashlib.sha256(c["body"].encode()).hexdigest()}
                                     for c in comments],
            "formal_reviews": len(reviews), "inline_comments": len(inline),
            "observed_dev": get("git/ref/heads/dev")["object"]["sha"],
            "resolved": ["R516-F1", "R516-F2", "R517-1-D1"]}
(packet / "receipts/public-context.json").write_text(json.dumps(metadata, indent=2) + "\n")
print("PUBLIC FINDING CENSUS", len(comments), "discussion comments;", len(reviews), "formal reviews;", len(inline), "inline comments")
print("PASS all three prior findings remain resolved")

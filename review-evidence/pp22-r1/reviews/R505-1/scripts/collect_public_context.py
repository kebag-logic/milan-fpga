#!/usr/bin/env python3
"""Capture read-only public authority and prior-finding endpoints."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
repo = "Mister-M-alt/protocol-processor-control-plane-avb-milan"
requests = [
    ("issue-22.json", f"repos/{repo}/issues/22", False),
    ("pr-162.json", f"repos/{repo}/pulls/162", False),
    ("issue-conversation.json", f"repos/{repo}/issues/22/comments", True),
    ("pr-conversation.json", f"repos/{repo}/issues/162/comments", True),
    ("pr-reviews.json", f"repos/{repo}/pulls/162/reviews", True),
    ("pr-inline-comments.json", f"repos/{repo}/pulls/162/comments", True),
]
responses = {}
for name, endpoint, pages in requests:
    argv = ["gh", "api", *( ["--paginate", "--slurp"] if pages else [] ), endpoint]
    data = subprocess.check_output(argv)
    (packet / "public" / name).write_bytes(data)
    parsed = json.loads(data)
    responses[name] = sum(parsed, []) if pages else parsed
comments = responses["pr-conversation.json"]
reviews = responses["pr-reviews.json"]
inline = responses["pr-inline-comments.json"]
potential = [r for r in comments if "FINDING" in r["body"].upper() or "REPORT.md" in r["body"]]
receipt = {
    "captured_utc": datetime.now(timezone.utc).isoformat(),
    "after_independent_diff_pass": True,
    "independent_verdict_and_ledger_already_written": (packet / "receipts/independent-verdict.json").is_file(),
    "conversation_count": len(comments),
    "conversation_ids": [r["id"] for r in comments],
    "submitted_review_count": len(reviews),
    "inline_comment_count": len(inline),
    "potential_finding_comment_ids": [r["id"] for r in potential],
    "disposition": "No prior public findings to retain or resolve" if not potential and not reviews and not inline else "Manual reconciliation required",
}
(packet / "receipts/prior-findings.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
for name in ["pr-conversation.json", "issue-conversation.json"]:
    print(name, [(r["id"], r["body"].splitlines()[0]) for r in responses[name]])

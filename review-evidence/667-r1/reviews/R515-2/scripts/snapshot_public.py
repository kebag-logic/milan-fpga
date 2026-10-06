#!/usr/bin/env python3
"""Retain the public disposition and PR wording without profile information."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess

REPO = "kebag-logic/milan-fpga"
HEAD = "41bc9dac031526c1fd637ff1e801d3c6dc1260b4"
COMMENTS = [6011846710, 6012843714, 6016181662, 6016186734]


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", f"repos/{REPO}/{path}"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    receipts = args.packet.resolve() / "receipts"
    retrieved = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records = []
    for number in COMMENTS:
        comment = api(f"issues/comments/{number}")
        record = {k: comment[k] for k in ["id", "html_url", "created_at", "updated_at", "body"]}
        record["retrieved_at"] = retrieved
        records.append(record)
    (receipts / "public-decisions.json").write_text(json.dumps(records, indent=2) + "\n")
    pr = api("pulls/680")
    assert pr["head"]["sha"] == HEAD
    note = pr["body"].split("**Manager note (A10), #657 equality at the published head.**")[1]
    for token in ["bd884631", "41bc9dac", "127 checks / 4 failures", "3746 bytes",
                  "3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b",
                  "423ac5d9", "5d6164a2", "predates the merge"]:
        assert token in note, token
    (receipts / "pr-body.md").write_text(pr["body"])
    metadata = {"url": pr["html_url"], "head": pr["head"]["sha"],
                "updated_at": pr["updated_at"], "retrieved_at": retrieved,
                "equality_note_checked": True}
    (receipts / "pr-snapshot.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print("PASS: public clarification and current PR body identify the accepted comparison")


if __name__ == "__main__":
    main()

"""Publish the authorized issue handoff once, then save its public URL."""
import json
import re
import subprocess
import sys
from pathlib import Path

output = Path(sys.argv[1])

def command(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()

body_file = output / "REVIEW-READY.md"
body = body_file.read_text()
assert body.startswith("[A592] REVIEW READY (round 4)\n")
assert "FINAL_HEAD" not in body and "CAPTURE_RESULT" not in body
head = command(["git", "rev-parse", "HEAD"])
assert f"Commit: {head} " in body
assert command(["git", "branch", "--show-current"]) == "671-read-fault"
assert command(["git", "remote", "get-url", "origin"]) == "https://github.com/kebag-logic/milan-fpga.git"
assert not command(["git", "status", "--porcelain"])
comments = command(["gh", "api", "repos/kebag-logic/milan-fpga/issues/671/comments", "--paginate", "--jq", ".[] | [.body, .html_url] | @json"])
matching = [url for line in comments.splitlines() for text, url in [json.loads(line)]
            if text.startswith("[A592] REVIEW READY") and head in text]
assert len(matching) <= 1
if matching:
    url = matching[0]
else:
    url = command(["gh", "issue", "comment", "671", "--repo", "kebag-logic/milan-fpga", "--body-file", str(body_file)])
assert url.startswith("https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-")
(output / "PUBLIC-COMMENT.txt").write_text(url + "\n")
handoff = output / "HANDOFF.md"
text = handoff.read_text()
if url not in text:
    handoff.write_text(text + f"\nPublic Round 4 handoff: [REVIEW READY]({url}).\n")
print(url)

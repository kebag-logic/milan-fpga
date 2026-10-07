#!/usr/bin/env python3
"""Capture read-only public source evidence, or reconcile reviews after an independent verdict."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

HEAD = "f800a2bb920c543934d6286a47fe20dde3efa2c5"
EVIDENCE = "f15a271b1211a566ff3b163b5a8195280e8bac9e"
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("phase", choices=("source", "reconcile"))
p.add_argument("packet", type=Path)
args = p.parse_args()
packet = args.packet.resolve()
receipts = packet / "receipts"
receipts.mkdir(parents=True, exist_ok=True)
records = []

def get(name, endpoint, paginate=False):
    command = ["gh", "api", "--method", "GET"]
    if paginate:
        command += ["--paginate", "--slurp"]
    command.append(endpoint)
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    (receipts / (name + ".json")).write_text(result.stdout)
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    records.append(dict(name=name, endpoint=endpoint, rc=result.returncode, utc=datetime.now(timezone.utc).isoformat()))
    result.check_returncode()
    return json.loads(result.stdout)

if args.phase == "source":
    for name, endpoint in [
        ("issue13", "issues/13"), ("pr14", "pulls/14"),
        ("head-license", "license?ref=" + HEAD), ("default-license", "license"),
        ("hosted-runs", "actions/runs?head_sha=" + HEAD + "&per_page=100"),
        ("check-runs", "commits/" + HEAD + "/check-runs"),
        ("commit-status", "commits/" + HEAD + "/status"),
    ]:
        get(name, "repos/kebag-logic/lwSRP/" + endpoint)
    get("repository", "repos/kebag-logic/lwSRP")
    with urllib.request.urlopen("https://www.apache.org/licenses/LICENSE-2.0.txt", timeout=60) as response:
        (receipts / "apache-response.txt").write_text(f"URL: {response.url}\nStatus: {response.status}\n" + str(response.headers))
        (receipts / "apache-LICENSE-2.0.txt").write_bytes(response.read())
    root = "repos/kebag-logic/milan-fpga/contents/review-evidence/lwsrplicfix-r1/"
    manifest = get("public-evidence-manifest", root + "MANIFEST.json?ref=" + EVIDENCE)
    data = base64.b64decode(manifest["content"])
    (receipts / "public-evidence-manifest-content.json").write_bytes(data)
    for entry in json.loads(data):
        # Only the two known public author artifacts; never import reviewer reports here.
        assert entry["file"] in ("author/PR-BODY.md", "author/links.log")
        content = get("public-" + Path(entry["file"]).name, root + entry["file"] + "?ref=" + EVIDENCE)
        raw = base64.b64decode(content["content"])
        assert hashlib.sha256(raw).hexdigest() == entry["published_sha256"]
        destination = receipts / "public-evidence" / entry["file"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
else:
    assert (receipts / "independent-verdict.md").is_file(), "Record your own verdict and ledger before reading reviews"
    for name, endpoint in [
        ("issue13-comments-final", "issues/13/comments?per_page=100"),
        ("pr14-comments-final", "issues/14/comments?per_page=100"),
        ("pr14-reviews-final", "pulls/14/reviews?per_page=100"),
        ("pr14-review-comments-final", "pulls/14/comments?per_page=100"),
    ]:
        get(name, "repos/kebag-logic/lwSRP/" + endpoint, paginate=True)
    for name, endpoint in [("pr14-final", "pulls/14"), ("issue13-final", "issues/13")]:
        get(name, "repos/kebag-logic/lwSRP/" + endpoint)
(receipts / (args.phase + "-capture.json")).write_text(json.dumps(records, indent=2) + "\n")
print(args.phase, "capture complete:", len(records), "GET requests")

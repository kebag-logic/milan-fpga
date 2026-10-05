#!/usr/bin/env python3
"""Audit the frozen public evidence and the captured public PR body."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
import docs_check
from sv_ports import declarations
def git(*args, cwd=root):
    return subprocess.check_output(["git", "-C", str(cwd), *args], env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))
ref = "0010a410b0150c2c7043142fb64036a7d2655799"
prefix = "review-evidence/661-r1/"
def read(name):
    return git("show", ref + ":" + prefix + name)
manifest = json.loads(read("MANIFEST.json"))
rows = []
for item in manifest:
    digest = hashlib.sha256(read(item["file"])).hexdigest()
    assert digest == item["published_sha256"], item["file"]
    rows.append(dict(file=item["file"], sha256=digest, matches_published=True))
sources = json.loads(read("author/source-receipts.json"))
count = 0
for item in sources["files"]:
    if "sha256" not in item:
        continue
    data = git("show", sources["head"] + ":" + item["path"])
    assert len(data) == item["bytes"]
    assert hashlib.sha256(data).hexdigest() == item["sha256"], item["path"]
    count += 1
body = (packet / "receipts/pr-body.md").read_text()
findings = docs_check.scrub_text("PR-BODY.md", body)
assert not findings, findings
assert "its 212 ports are unchanged" in body
assert "git fetch origin 661-pp-pin-ead80360 && git switch --detach FETCH_HEAD" in body
assert not any(s in body for s in ("/data/", "/home/", "sudo "))
ports = {}
for pin in ("631eeb342ca1e3fa80e734077a56a943aee76ff1", "ead8036035affd53ef4b29979190f2f4f67084c0"):
    source = git("show", pin + ":hdl/top/protocol_processor_top.sv", cwd=root / "protocol-processor").decode()
    ds = [d for d in declarations(source) if d[0] == "protocol_processor_top"]
    ports[pin] = dict(ports=sum(d[4] == "port" for d in ds), parameters=sum(d[4] == "param" for d in ds))
    assert ports[pin]["ports"] == 212
exact_fix = "At the measurement revision the builder accepted an 8x8 TDM8 configuration the saved-state backend refused (235 names against 128); since #652 the builder refuses that shape before generation."
assert exact_fix in (root / "docs/findings/README.md").read_text()
result = dict(evidence_commit=ref, manifest_files=rows, source_receipt_head=sources["head"], source_blobs_verified=count, body_sha256=hashlib.sha256(body.encode()).hexdigest(), body_privacy_findings=findings, public_body_fixes_retained=True, top_port_census=ports, R487_2_R1_exact_fix_present=True)
(packet / "receipts/public-evidence-audit.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS {len(rows)} published evidence hashes; {count} source blobs at recorded round-1 head")
print("PASS current body privacy, 212-port statement and published-branch setup")
print("PASS R487-2 R1 exact requested text")

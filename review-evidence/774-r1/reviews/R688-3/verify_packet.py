#!/usr/bin/env python3
"""Verify the public receipt archive and the documentary correction offline.
Usage: python3 verify_packet.py REPOSITORY PACKET
The evidence commit must already be fetched. No source files are changed.
"""
import ast, hashlib, json, subprocess, sys
from pathlib import Path
repo, out = map(Path, sys.argv[1:])
commit = "4484c29cd1224098b5b0d4576cc5d8e4897b4836"
prefix = "review-evidence/774-r1/"
def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])
def blob(path):
    return git("show", commit + ":" + prefix + path)
manifest = json.loads(blob("MANIFEST.json"))
receipts = [x for x in manifest if x["file"].startswith(("author/receipts/", "author-r2/receipts/"))]
for item in receipts:
    assert hashlib.sha256(blob(item["file"])).hexdigest() == item["published_sha256"], item["file"]
print(f"PASS: {len(receipts)} author receipt hashes match published_sha256")
selected = ["author-r2/scripts/round2/bdd_frame_mutants.py",
            "author-r2/receipts/round2/bdd/frame_mutants.log",
            "author-r2/receipts/round2/bdd/frame_mutants.rc"]
(out/"published-receipts").mkdir(exist_ok=True)
for name in selected:
    data = blob(name)
    item = next(x for x in manifest if x["file"] == name)
    assert hashlib.sha256(data).hexdigest() == item["published_sha256"]
    (out/"published-receipts"/Path(name).name).write_bytes(data)
    print("PASS published bytes:", name, item["published_sha256"])
script = ast.parse(blob(selected[0]))
cases = next(n.value for n in script.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CASES" for t in n.targets))
expected = [(ast.literal_eval(c.elts[0]), ast.literal_eval(c.elts[3])) for c in cases.elts]
assert len(expected) == 6 and sum(ok for _, ok in expected) == 1
lines = blob(selected[1]).decode().splitlines()
results = [line for line in lines if line.startswith("[PASS")]
assert len(results) == 6
for (name, clean), line in zip(expected, results):
    assert line.startswith(("[PASS clean] " if clean else "[PASS mutant caught] ") + name + ":"), line
    print("MATCH:", line)
assert lines[-1] == "6 checks: 6 PASS, 0 FAIL"
assert blob(selected[2]).strip() == b"0"
issue = json.loads((out/"issue.json").read_text())
correction = next(c for c in issue["comments"] if c["id"] == 6385747770)
assert "Five planted faults against the unchanged step are caught, and the clean control passes: six checks total." in correction["body"]
pr = json.loads((out/"pr.json").read_text())
assert "Internal cleared-context reviewer: [R687]" in pr["body"]
assert "External cleared-context reviewer: [R688]" in pr["body"]
assert "six planted faults" not in pr["body"]
assert pr["head_sha"] == "01fc54756f1ffb0a3aa836681215e8321ee7e86c"
assert git("rev-parse", "HEAD").decode().strip() == pr["head_sha"]
assert git("rev-parse", "HEAD^{tree}").decode().strip() == "7d8822f99d37284635fc34101123477e0c89846c"
print("PASS: correction, role lines, published head and local tree")
headers = git("cat-file", "commit", commit).split(b"\n\n", 1)[0]
print("Archive embedded signature:", "present" if b"gpgsig " in headers else "ABSENT; checksum verification does not authenticate a signer")

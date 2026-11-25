#!/usr/bin/env python3
"""Verify the pinned public author packet and focused receipt payloads."""
import hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent
SHA="73eaef87e14c2d299d0f63fda15c3251c0ca1512"
BASE="review-evidence/loopbram-r1/"
def blob(path):return subprocess.check_output(["git","show",SHA+":"+BASE+path])
manifest=json.loads(blob("MANIFEST.json"))
selected=[r for r in manifest if r["file"].startswith(("author-r6/","author-r6b/","author-r7/"))]
rows=[]
for r in selected:
    b=blob(r["file"]);h=hashlib.sha256(b).hexdigest()
    assert h==r["published_sha256"],r["file"]
    dest=OUT/"scratch/public-packet"/r["file"];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    rows.append(dict(file=r["file"],sha256=h,verified=True))
(OUT/"packet-integrity.json").write_text(json.dumps(dict(commit=SHA,entries=rows),indent=2)+"\n")
r7=OUT/"scratch/public-packet/author-r7/receipts"
cases=json.loads((r7/"suites--parent-mutants--results.json.txt").read_text())
assert len(cases)==17
for case in cases:
    assert case["built"] and case["passed"],case["name"]
    if case["name"].startswith("control"):assert case["exit"]==0
    else:assert case["exit"]!=0 and case["required"]
record=dict(source_commit=SHA,parent_campaign=cases,
            limitation="Published campaign results and driver assertions checked; individual parent runtime logs were not republished in author-r7.")
identity=json.loads((r7/"identity--identity--head.json.txt").read_text())
record["identity_payload_type"]=type(identity).__name__
(OUT/"receipt-audit.json").write_text(json.dumps(record,indent=2)+"\n")
# Preserve a small, verifiable set of cited raw public receipts.
names=["author-r6/receipts/repro--repro.log.txt","author-r6/receipts/source-binding.json.txt",
"author-r7/receipts/planner--logs--fit-at-merge-26-workers.txt.txt",
"author-r7/receipts/suites--logs--parent-mutants.log.txt",
"author-r7/receipts/suites--logs--leaf-mutants.log.txt",
"author-r7/receipts/boundary--logs--fwv-judge.log.txt",
"author-r7/receipts/boundary--logs--reasons-fixed.txt.txt",
"author-r7/receipts/boundary--logs--reasons-planted.txt.txt",
"author-r7/receipts/identity--logs--ident-head-vs-dev.txt.txt",
"author-r7/receipts/identity--logs--fwimages-compare.md.txt",
"author-r7/REVIEW-READY.md","author-r7/PR-BODY.md"]
for name in names:
    dest=OUT/"public-receipts"/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(blob(name))
print("PASS",len(rows),"published checksum entries;",len(cases),"parent campaign result records")


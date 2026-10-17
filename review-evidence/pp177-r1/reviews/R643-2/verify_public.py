#!/usr/bin/env python3
"""Fetch selected public immutable receipts and verify published hashes."""
import csv, hashlib, json, subprocess, sys
from pathlib import Path
packet=Path(sys.argv[1]).resolve()
out=packet/"public-evidence"; out.mkdir(exist_ok=True)
repo="kebag-logic/milan-fpga"
revision="8ef92c3bf2517c92f8ec674ae2edbfeac50ee79c"
base="review-evidence/pp177-r1/"
def fetch(path):
    return subprocess.check_output(["gh","api","-H","Accept: application/vnd.github.raw+json",f"repos/{repo}/contents/{base}{path}?ref={revision}"])
manifest=json.loads(fetch("MANIFEST.json"))
(out/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
paths=["author-r2/HANDOFF.md","author-r2/EXTERNAL-ARTIFACTS.csv",
"reviews/R642-1/receipts/results/dispatch-gavb-type-low-byte.FAIL-lines.txt",
"reviews/R642-1/receipts/results/dispatch-gavb-floor-14.FAIL-lines.txt",
"reviews/R642-1/receipts/results/dispatch-campaign.results.json",
"reviews/R642-1/receipts/results/decode-controls.results.json",
"reviews/R642-1/receipts/results/probe-decode-p-floor-15.summary.txt",
"reviews/R642-1/receipts/results/probe-decode-p-gate-ignores-bit12.summary.txt",
"reviews/R642-1/receipts/results/probe-dispatch-p-gate-ignores-bit12.summary.txt",
"reviews/R642-1/receipts/dispatch-campaign.rc",
"reviews/R642-1/receipts/decode-controls.rc"]
results=[]
for path in paths:
    content=fetch(path)
    expected=next(x for x in manifest if x["file"]==path)
    actual=hashlib.sha256(content).hexdigest()
    assert actual==expected["published_sha256"],path
    dest=out/path; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(content)
    results.append({"file":path,"sha256":actual,"bytes":len(content),"verified":True,"path_redacted":expected["path_redacted"]})
rows=list(csv.reader((out/"author-r2/EXTERNAL-ARTIFACTS.csv").open()))
rs={r[0]:r for r in rows[1:]}; comparisons=[]
for name,row in rs.items():
    if name.startswith("r2/") and "base-" in name:
        match=name.replace("base-","head-")
        if match in rs:
            comparisons.append({"base":name,"head":match,"same_size":row[1]==rs[match][1],"same_sha256":row[2]==rs[match][2]})
report={"revision":revision,"verified_files":results,"inventory_only_comparisons":comparisons,"raw_author_gate_logs_published_in_packet":False}
(packet/"public-evidence-verification.json").write_text(json.dumps(report,indent=2)+"\n")
print(f"Verified {len(results)} public files against published SHA-256 manifest; compared {len(comparisons)} inventory pairs.")

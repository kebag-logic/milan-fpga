#!/usr/bin/env python3
"""Verify the public receipt hashes and image section arithmetic, without rebuilding banks."""
import hashlib
import json
from pathlib import Path
import subprocess

PACKET=Path(__file__).resolve().parents[1]
REF="2f7ab26dadbd359c55eb248ef56fcbcbe4e6bd40"
BASE="review-evidence/665f4-r1/author-r11/"
def read(name): return subprocess.check_output(["git","show",REF+":"+BASE+name])

gates=json.loads(read("ROUND11-GATES.json"))
errors=[]
records=[]
for gate in gates["receipts"]:
    if gate["rc"]: errors.append(gate["label"]+": nonzero")
    log=gate.get("retained_log")
    if log:
        data=read(log["path"])
        digest=hashlib.sha256(data).hexdigest()
        okay=len(data)==log["size"] and digest==log["sha256"]
        if not okay: errors.append(gate["label"]+": hash mismatch")
        records.append({"label":gate["label"],"rc":gate["rc"],"retained_path":log["path"],
                        "sha256":digest,"hash_match":okay})
images=json.loads(read("ROUND11-SIZES.json"))
image_rows=[]
for im in images["srp_images"]:
    total=sum(im["sections"].get(k,0) for k in (".text",".rodata",".data",".bss",".stack"))
    # Each output section can have its own input-driven alignment, before
    # the final ALIGN(16). Section totals alone cannot reconstruct placement.
    valid=total==im["ram_sections"] and im["ram_span"]>=total and im["ram_span"]%16==0
    if not valid: errors.append(im["shape"]+": image arithmetic")
    image_rows.append({**{k:im[k] for k in ("shape","interfaces","sections","ram_sections","ram_span","artifacts")},
                       "recorded_padding_bytes":im["ram_span"]-total})
summary={"evidence_commit":REF,"source_head":gates["head"],"receipt_count":len(gates["receipts"]),
         "checked_retained_logs":len(records),"errors":errors,"receipts":records,
         "images":image_rows,"image_scope":"Published section figures and recorded hashes inspected; no fresh link in this review."}
(PACKET/"receipts/public-evidence-audit.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k not in ("receipts","images")},indent=2))
raise SystemExit(bool(errors))

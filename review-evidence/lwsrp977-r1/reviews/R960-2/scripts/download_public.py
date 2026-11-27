#!/usr/bin/env python3
"""Fetch only public author-r2 evidence; never fetch reviewer reports.
Usage: python3 scripts/download_public.py PACKET
Requires authenticated read access through gh. All downloads remain in scratch.
"""
import base64, concurrent.futures, json, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()/"scratch/public"
ref="16162ec2b6c26d1d2ba3e3f0e2d4568a4d462694"
prefix="review-evidence/lwsrp977-r1/"
def fetch(path):
    raw=subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/contents/"+prefix+path+"?ref="+ref])
    return base64.b64decode(json.loads(raw)["content"])
root.mkdir(parents=True,exist_ok=True)
manifest=fetch("MANIFEST.json")
(root/"MANIFEST.json").write_bytes(manifest)
entries=[r for r in json.loads(manifest) if r["file"].startswith("author-r2/") and "/superseded/" not in r["file"]]
def one(row):
    p=root/row["file"];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(fetch(row["file"]))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(one,entries))
print("Downloaded",len(entries),"files; run audit.py to verify published hashes.")

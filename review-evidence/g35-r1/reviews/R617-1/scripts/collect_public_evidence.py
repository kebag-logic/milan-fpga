#!/usr/bin/env python3
"""Download only public executable evidence at the frozen evidence commit.
Usage: collect_public_evidence.py OUT --jobs 8
Verifies the published SHA-256 of every downloaded file.
"""
import argparse, concurrent.futures, hashlib, json, urllib.request
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("out",type=Path); ap.add_argument("--jobs",type=int,default=8); a=ap.parse_args()
assert 1 <= a.jobs <= 16
root="https://raw.githubusercontent.com/kebag-logic/milan-fpga/2e3232522119b5ef06bc7d15ea1d46c0c81a07fb/review-evidence/g35-r1/"
a.out.mkdir(parents=True,exist_ok=True)
def fetch(path):
    with urllib.request.urlopen(root+path,timeout=90) as r: return r.read()
m=fetch("MANIFEST.json"); (a.out/"MANIFEST.json").write_bytes(m)
entries=[e for e in json.loads(m) if e["file"].startswith("author/evidence/")]
def collect(e):
    data=fetch(e["file"]); h=hashlib.sha256(data).hexdigest()
    assert h == e["published_sha256"], e["file"]
    dst=a.out/e["file"]; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(data)
    return f"{h}  {e['file']}"
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
    rows=list(pool.map(collect,entries))
print("Frozen public evidence commit: 2e3232522119b5ef06bc7d15ea1d46c0c81a07fb")
print("\n".join(rows)); print(f"VERIFIED {len(rows)} published evidence files")

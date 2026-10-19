#!/usr/bin/env python3
"""Fetch only public execution receipts, and audit their published digests."""
import concurrent.futures, hashlib, json, pathlib, subprocess, sys, urllib.request
p=pathlib.Path(sys.argv[1])
rev="afc1a1ac02210ae5868ec75b3102ff4778b29809"
prefix="review-evidence/761-r1/"
(p/"scratch").mkdir(parents=True,exist_ok=True)
manifest_url=f"https://raw.githubusercontent.com/kebag-logic/milan-fpga/{rev}/{prefix}MANIFEST.json"
manifest_data=urllib.request.urlopen(manifest_url,timeout=60).read()
(p/"scratch/public-manifest.json").write_bytes(manifest_data)
manifest=json.loads(manifest_data)
chosen=[]
for e in manifest:
 f=e["file"]
 if f.startswith("author-r3/receipts/r3-") or (f.startswith("author-r2/receipts/r2b-") and (f.endswith((".rc", ".summary", ".tsv", "commit.txt", "check.log", "all.list", "union.list")))):
  chosen.append(e)
def fetch(e):
 f=e["file"]
 url=f"https://raw.githubusercontent.com/kebag-logic/milan-fpga/{rev}/{prefix}{f}"
 data=urllib.request.urlopen(url,timeout=60).read()
 got=hashlib.sha256(data).hexdigest()
 assert got==e["published_sha256"],f
 out=p/"scratch/public"/f
 out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(data)
 return f"PASS {got} {f}"
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for line in pool.map(fetch,chosen): print(line)
print(f"Verified {len(chosen)} public receipts against published_sha256; original_sha256 is not asserted for redacted files.")

#!/usr/bin/env python3
"""Retrieve only public author executable receipts from an immutable evidence commit."""
import argparse, concurrent.futures, hashlib, json, subprocess, urllib.request
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("packet",type=Path);a=ap.parse_args();p=a.packet.resolve()
rev="bda25e67cb4df99a837ccb21383917c90b81a1ad";prefix="review-evidence/pp151-r1/"
manifest=json.loads((p/"public/upstream-MANIFEST.json").read_text())
files=[f for f in manifest if f["file"].startswith("author/evidence/")]
def fetch(f):
 name=f["file"];url="https://raw.githubusercontent.com/kebag-logic/milan-fpga/"+rev+"/"+prefix+name
 data=urllib.request.urlopen(url,timeout=60).read()
 got=hashlib.sha256(data).hexdigest();assert got==f["published_sha256"],name
 dest=p/"scratch/published-r1"/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 return {"path":name,"url":url,"sha256":got,"bytes":len(data)}
with concurrent.futures.ThreadPoolExecutor(8) as pool:results=list(pool.map(fetch,files))
(p/"receipts/public-evidence-fetch.json").write_text(json.dumps(results,indent=2)+"\n")
print(f"PASS: {len(results)} public executable receipts match the published manifest")

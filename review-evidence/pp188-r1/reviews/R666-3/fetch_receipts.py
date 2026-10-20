#!/usr/bin/env python3
"""Fetch selected public receipts at an immutable revision and verify published hashes."""
import concurrent.futures, hashlib, json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REV="61e4bb57da96c2c2e4d60987f390a435384ffe9f"
manifest=json.loads((ROOT/"evidence-manifest.json").read_text())
prefix="author-r2/receipts/round2/"
selected=[]
for item in manifest:
 f=item["file"]
 if f in ["author-r2/PR-BODY.md", "author-r2/receipts/round2/EXTERNAL-RECORDS.csv"] or (f.startswith(prefix) and re.match(r"(?:campaigns|gates|consumers)/(?:base|head|ooc-base|ooc-head)/[^/]+\.(?:log|rc|txt)$",f[len(prefix):])):
  selected.append(item)
def fetch(item):
 f=item["file"]; target=ROOT/"public"/f; target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists():
  data=subprocess.check_output(["gh","api",f"repos/kebag-logic/milan-fpga/contents/review-evidence/pp188-r1/{f}?ref={REV}","-H","Accept: application/vnd.github.raw+json"])
  target.write_bytes(data)
 digest=hashlib.sha256(target.read_bytes()).hexdigest()
 assert digest==item["published_sha256"], f
 return f"PASS {digest} {f}"
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 results=list(pool.map(fetch,selected))
(ROOT/"published-hashes.txt").write_text("\n".join(results)+"\n")
print(f"PASS {len(results)} published SHA-256 digests at {REV}")

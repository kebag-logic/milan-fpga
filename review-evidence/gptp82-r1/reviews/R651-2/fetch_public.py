#!/usr/bin/env python3
"""Fetch only the public round-two author packet and check its publication hashes."""
import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
REF="476262d73e7181b2d9eda360a774427bd07527a3"
ROOT="review-evidence/gptp82-r1/"
manifest=P/"public-manifest.json"
if not manifest.exists():
    manifest.write_bytes(subprocess.check_output(["rtk","proxy","gh","api",f"repos/kebag-logic/milan-fpga/contents/{ROOT}MANIFEST.json?ref={REF}","-H","Accept: application/vnd.github.raw+json"]))
m=json.loads(manifest.read_text())
rows=[r for r in m if r["file"].startswith("author-r2/")]
def fetch(r):
    f=r["file"]; dst=P/"scratch/public"/f; dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():
        b=subprocess.check_output(["rtk","proxy","gh","api",f"repos/kebag-logic/milan-fpga/contents/{ROOT}{f}?ref={REF}","-H","Accept: application/vnd.github.raw+json"])
        dst.write_bytes(b)
    b=dst.read_bytes(); h=hashlib.sha256(b).hexdigest()
    return {"file":f,"bytes":len(b),"sha256":h,"matches_publication_manifest":h==r["published_sha256"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: result=list(pool.map(fetch,rows))
(P/"public-packet-verification.json").write_text(json.dumps(result,indent=2)+"\n")
print(f"Verified {len(result)} files; mismatches:", [r["file"] for r in result if not r["matches_publication_manifest"]])

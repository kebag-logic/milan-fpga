#!/usr/bin/env python3
"""Fetch a bounded, immutable public evidence selection and check published hashes."""
import concurrent.futures, hashlib, json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parent
COMMIT="992033a936efe4add5139167612f2b268be01134"
BASE="review-evidence/pp185-r1/"
def api(path):
    return subprocess.check_output(["gh","api",path,"-H","Accept: application/vnd.github.raw+json"])
manifest=json.loads(api(f"repos/kebag-logic/milan-fpga/contents/{BASE}MANIFEST.json?ref={COMMIT}"))
selected=[]
for row in manifest:
    name=row["file"]
    if not name.startswith("author-r2/receipts/round2/"): continue
    rel=name.removeprefix("author-r2/receipts/round2/")
    parts=rel.split("/")
    keep=(rel.startswith(("base/gates/","head-final2/gates/","head-final2/campaigns/","head/campaigns/","base/campaigns/","compare/","newarms/","probes-head/"))
          or (parts[0] in ("parent-base","parent-head") and (rel.endswith((".rc","HEAD.txt","gitlink.txt","parent-log.txt","parent-patches.txt")) or "g11_lint_rtl.log" in rel)))
    if not keep or "/out/" in rel and not rel.endswith("results.json"): continue
    if rel.endswith((".secs","req-tags.txt","status-after.txt")): continue
    selected.append((row,rel))
def fetch(item):
    row,rel=item
    data=api(f"repos/kebag-logic/milan-fpga/contents/{BASE}{row['file']}?ref={COMMIT}")
    digest=hashlib.sha256(data).hexdigest()
    assert digest==row['published_sha256'], (rel,digest)
    dest=ROOT/"scratch/public"/rel
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    return {"path":row["file"],"published_sha256":digest,"verified":True,"path_redacted":row["path_redacted"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    receipts=list(pool.map(fetch,selected))
(ROOT/"public-hash-verification.json").write_text(json.dumps({"commit":COMMIT,"files":receipts},indent=2)+"\n")
print(f"Verified {len(receipts)} public receipts against the immutable published manifest")

#!/usr/bin/env python3
"""Read the pinned public receipts; never executes their scripts."""
import concurrent.futures, hashlib, json, pathlib, subprocess
P=pathlib.Path(__file__).resolve().parent
REV="948261dfc94d7da73dac5cdb80621b4cbaaaf4e2"
ROOT="review-evidence/gptp84-r1/"
(P/"scratch").mkdir(exist_ok=True)
tree_data=subprocess.check_output(["gh","api",f"repos/kebag-logic/milan-fpga/git/trees/{REV}?recursive=1"])
(P/"scratch/evidence-tree.json").write_bytes(tree_data)
tree=json.loads(tree_data)["tree"]
items=[x for x in tree if x["type"]=="blob" and x["path"].startswith(ROOT) and ("/receipts/" in x["path"] or x["path"].endswith(("MANIFEST.json","parent-adoption-gptp_shadow-85.patch")))]
def get(x):
 rel=x["path"][len(ROOT):]; target=P/"scratch/public-evidence"/rel
 target.parent.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(["gh","api",f"repos/kebag-logic/milan-fpga/contents/{x['path']}?ref={REV}","-H","Accept: application/vnd.github.raw+json"])
 target.write_bytes(data)
 blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert blob==x["sha"],rel
 return {"path":rel,"bytes":len(data),"git_blob":blob,"sha256":hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 rows=list(ex.map(get,items))
(P/"public-download-audit.json").write_text(json.dumps({"commit":REV,"files":rows},indent=2)+"\n")
print(f"Verified {len(rows)} public files against pinned Git blobs")

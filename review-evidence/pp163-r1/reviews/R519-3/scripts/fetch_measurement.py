#!/usr/bin/env python3
"""Fetch only the specified public measurement, never private material."""
import base64, concurrent.futures, json, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
REF="7e552ca502df6b0029ec9de4a1a7ec0d5576ab0f"
PREFIX="review-evidence/pp163-r1/author-r3/"
tree=json.loads((P/"receipts/evidence-tree.json").read_text())["tree"]
items=[x for x in tree if x["type"]=="blob" and (x["path"].startswith(PREFIX+"measurement-m3final/") or x["path"]==PREFIX+"evidence/measurement-m3final.json")]
def fetch(x):
    r=subprocess.run(["gh","api",f"repos/kebag-logic/milan-fpga/git/blobs/{x['sha']}"],capture_output=True,text=True,check=True)
    b=base64.b64decode(json.loads(r.stdout)["content"])
    import hashlib
    assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==x["sha"]
    out=P/"receipts/public-measurement"/x["path"][len(PREFIX):]
    out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(b)
    return {"path":x["path"],"blob":x["sha"],"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
with concurrent.futures.ThreadPoolExecutor(8) as pool: results=list(pool.map(fetch,items))
(P/"receipts/fetch-measurement.json").write_text(json.dumps({"archive":REF,"files":results},indent=2)+"\n")
print(f"Fetched and blob-verified {len(results)} public measurement files")

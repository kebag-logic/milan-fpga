#!/usr/bin/env python3
"""Fetch and hash-check only published executable receipts, not lane notes or other reviews."""
import base64,concurrent.futures,hashlib,json,subprocess,sys
from pathlib import Path
packet=Path(sys.argv[1]); out=packet/"receipts/public";out.mkdir(exist_ok=True)
ref="d445cbd4d2dadfa01fbefc36bec82d9ffde5695f"
manifest=json.loads((packet/"receipts/public-manifest.json").read_text())
selected=[r for r in manifest if r["file"].startswith("author/area_ooc_1x1/") or r["file"].startswith("author/stage2_")]
def fetch(r):
 endpoint="repos/kebag-logic/milan-fpga/contents/review-evidence/658-r1/"+r["file"]+"?ref="+ref
 data=json.loads(subprocess.check_output(["gh","api",endpoint]))
 blob=base64.b64decode(data["content"]);h=hashlib.sha256(blob).hexdigest();assert h==r["published_sha256"]
 target=out/Path(r["file"]).name;target.write_bytes(blob)
 return {"file":r["file"],"sha256":h,"bytes":len(blob)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,selected))
print(json.dumps(results,indent=2))

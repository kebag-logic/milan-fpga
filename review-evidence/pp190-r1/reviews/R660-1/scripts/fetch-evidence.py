#!/usr/bin/env python3
"""Fetch only the frozen public evidence subtree, verifying each Git blob ID."""
import concurrent.futures, hashlib, json, pathlib, sys, urllib.request
packet=pathlib.Path(sys.argv[1]).resolve()
commit="1dede13e4770f290ae04db3a3fec340195885437"
items=json.loads((packet/"receipts/public-evidence-tree.json").read_text())
root=packet/"scratch/public-evidence"; root.mkdir(parents=True,exist_ok=True)
def fetch(item):
 path=item["path"]; rel=path.removeprefix("review-evidence/pp190-r1/")
 data=urllib.request.urlopen(f"https://raw.githubusercontent.com/kebag-logic/milan-fpga/{commit}/{path}",timeout=60).read()
 sha=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 assert sha==item["sha"],path
 dst=root/rel; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(data)
 return {"path":rel,"bytes":len(data),"git_blob":sha,"sha256":hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 results=list(pool.map(fetch,[i for i in items if i["type"]=="blob"]))
(packet/"receipts/public-evidence-fetch.json").write_text(json.dumps(results,indent=2)+"\n")
print("Fetched and Git-blob-verified",len(results),"public files")

#!/usr/bin/env python3
import concurrent.futures, hashlib, json, pathlib, urllib.request
OUT=pathlib.Path(__file__).resolve().parents[1]
REV="178da610c7d6e41da1cc0466f6b246fcd363d798"
PREFIX="review-evidence/pp184-r1/"
rows=json.loads((OUT/"receipts/evidence-tree.json").read_text())
selected=[x for x in rows if x["type"]=="blob" and (x["path"].startswith(PREFIX+"author-r2/r2-receipts/") or x["path"]==PREFIX+"MANIFEST.json")]
def fetch(x):
 p=OUT/"receipts/public"/x["path"][len(PREFIX):]
 p.parent.mkdir(parents=True,exist_ok=True)
 url="https://raw.githubusercontent.com/kebag-logic/milan-fpga/"+REV+"/"+x["path"]
 data=urllib.request.urlopen(url,timeout=60).read()
 assert len(data)==x["size"]
 assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==x["sha"]
 p.write_bytes(data)
 return x["path"]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 got=list(pool.map(fetch,selected))
print("PASS downloaded and Git-blob-verified",len(got),"public files at",REV)

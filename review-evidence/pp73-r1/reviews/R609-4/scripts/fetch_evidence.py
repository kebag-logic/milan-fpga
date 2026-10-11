#!/usr/bin/env python3
"""Fetch only selected published author receipts; verify their published blob IDs."""
import base64,concurrent.futures,hashlib,json,pathlib,subprocess,sys
packet=pathlib.Path(sys.argv[1]); prefix="review-evidence/pp73-r1/author-r4/receipts/r4/"
tree=packet/"scratch/public-tree.json"
if not tree.exists():
 tree.parent.mkdir(parents=True,exist_ok=True)
 tree.write_bytes(subprocess.check_output(["rtk","proxy","gh","api","repos/kebag-logic/milan-fpga/git/trees/0cc8f8f5c9d3d6318f864d76c5a662f06b6eb689?recursive=1"]))
items=json.loads(tree.read_text())["tree"]
selected=[]
logs={"head-check","optimized-selftest","head-suites","head-lint","head-matrix","head-yosys","compare-suites","compare-campaigns","elaboration","new-controls","pr-reference-final","head-python"}
rootfiles={"final-identity.json","head.sha","head-export-final.json","elaboration-identity.tsv","export-artifacts.tsv","published-pr-head.sha","review-evidence-head.sha","rom-identity.tsv","production-identity.json","membership-positive.json","planted-drifts.tsv","membership-disabled.log","record-success-disabled.log","rom-success-disabled.log"}
for f in items:
 if f["type"]!="blob" or not f["path"].startswith(prefix): continue
 rel=f["path"][len(prefix):]; p=pathlib.PurePosixPath(rel)
 if rel in rootfiles or (p.parent.as_posix()=="logs" and p.stem in logs) or p.parent.as_posix() in {"shared-probe","review-probes"}: selected.append((f,rel))
def fetch(pair):
 f,rel=pair
 dest=packet/"receipts/public-author-r4"/rel
 if dest.exists(): content=dest.read_bytes()
 else:
  endpoint="repos/kebag-logic/milan-fpga/git/blobs/"+f["sha"]
  raw=subprocess.check_output(["rtk","proxy","gh","api",endpoint])
  content=base64.b64decode(json.loads(raw)["content"])
 actual=hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest(); assert actual==f["sha"]
 dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(content)
 return {"path":f["path"],"blob":f["sha"],"sha256":hashlib.sha256(content).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(fetch,selected))
(packet/"receipts/public-author-selected.json").write_text(json.dumps(results,indent=2)+"\n")
print(f"Fetched and verified {len(results)} published source receipts; no review reports or private material fetched.")

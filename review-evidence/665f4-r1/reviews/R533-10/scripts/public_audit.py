#!/usr/bin/env python3
"""Audit retained public evidence, not a rerun of the full source banks."""
import argparse,base64,concurrent.futures,hashlib,json,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("--source",type=Path,default=Path.cwd());ap.add_argument("--packet",type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument("--jobs",type=int,default=4);a=ap.parse_args();p=a.packet.resolve();r=a.source.resolve()
commit="8ba25cb06ac3f67c499a22179fc7960f67aeb3e3";repo="kebag-logic/milan-fpga";prefix="review-evidence/665f4-r1/author-r10/"
scratch=p/"scratch/public-audit";scratch.mkdir(exist_ok=True)
def api(path):return json.loads(subprocess.check_output(["gh","api",path]))
# The tree and metadata are independently fetched for portable reproduction.
tree=api(f"repos/{repo}/git/trees/{commit}?recursive=1");assert not tree["truncated"]
objects={x["path"]:x for x in tree["tree"]}
def get(path):
 oid=objects[path]["sha"];obj=api(f"repos/{repo}/git/blobs/{oid}");return base64.b64decode(obj["content"])
meta={}
for name in ["ROUND10-GATES.json","ROUND10-SOURCE.json","ROUND10-SIZES.json","ROUND10-CAMPAIGN.json","ROUND10-GATE-PARITY.json"]:
 data=get(prefix+name);(scratch/name).write_bytes(data);meta[name]=json.loads(data)
def audit(row):
 log=row.get("retained_log");out={"label":row["label"],"reported_rc":row["rc"]}
 if not log:return dict(out,retained=False,rerun=False)
 data=get(prefix+log["path"]);digest=hashlib.sha256(data).hexdigest();assert len(data)==log["size"] and digest==log["sha256"],row["label"]
 return dict(out,retained=True,bytes=len(data),sha256=digest,hash_verified=True,path=prefix+log["path"])
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:rows=list(pool.map(audit,meta["ROUND10-GATES.json"]["receipts"]))
source=[]
for f in meta["ROUND10-SOURCE.json"]["files"]:
 data=(r/f["path"]).read_bytes();assert len(data)==f["size"] and hashlib.sha256(data).hexdigest()==f["sha256"]
 source.append({"path":f["path"],"hash_verified":True})
result={"public_commit":commit,"metadata_sha256":{n:hashlib.sha256((scratch/n).read_bytes()).hexdigest() for n in meta},"source_files":source,"invocations":rows,"all_reported_rc_zero":all(x["reported_rc"]==0 for x in rows),"limits":"Retained-log hash audit and source-file binding only; does not rerun the reported banks or validate current-dev merge result."}
(p/"receipts/public-evidence-audit.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps({"invocations":len(rows),"retained_hashes_verified":sum(x["retained"] for x in rows),"source_files_verified":len(source)}))

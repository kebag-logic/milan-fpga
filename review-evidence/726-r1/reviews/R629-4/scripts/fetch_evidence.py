#!/usr/bin/env python3
"""Fetch only public author execution receipts, checking Git blob identities."""
import base64, concurrent.futures, hashlib, json, pathlib, subprocess, sys
packet=pathlib.Path(sys.argv[1]); entries=json.loads((packet/"scratch/evidence-tree.json").read_text())
def select(x):
 s=x["path"].removeprefix("review-evidence/726-r1/")
 if x["type"]!="blob": return False
 if s.startswith("author-r4/review-round4/"):
  return "build.log" not in s and (s.endswith((".json",".log")))
 return s in ["author-r4/ROUND4-GATES.tsv","author/IMAGE-ARTIFACTS.tsv"] or s.startswith("author/evidence/") and any(a in s for a in ("implementation-inputs.json","utilization_route.rpt","signoff_grade.txt","signoff_check_timing.rpt","timing_summary","alinx_ax7101.tcl"))
def fetch(x):
 b=json.loads(subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/git/blobs/"+x["sha"]])); data=base64.b64decode(b["content"])
 assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==x["sha"]
 relative=x["path"].removeprefix("review-evidence/726-r1/")
 dest=packet/"receipts/public"/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 return {"source":x["path"],"git_blob":x["sha"],"sha256":hashlib.sha256(data).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: records=list(pool.map(fetch,filter(select,entries)))
(packet/"receipts/public-evidence-provenance.json").write_text(json.dumps({"commit":"907f0116a8b7f548ce33dc2821a23f576ac0bab3","files":records},indent=2)+"\n")
print("Verified public author receipts:",len(records))

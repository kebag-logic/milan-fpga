#!/usr/bin/env python3
import base64,concurrent.futures,hashlib,json,pathlib,subprocess,sys
p=pathlib.Path(sys.argv[1]);index=p/"authority/evidence-tree-corrected.json"
if not index.exists():
 index.parent.mkdir(parents=True,exist_ok=True);index.write_bytes(subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/git/trees/a81c70d22a1ca128f86d3ae1e7b45b0bb97898c2?recursive=1"]))
tree=json.loads(index.read_text())["tree"]
prefix="review-evidence/tsn24-r1/"
scripts={"reviews/R630-1/scripts/escape_probe.py":"scripts/prior/escape_probe.py","reviews/R630-1/scripts/physical_removal.py":"scripts/prior/physical_removal.py","reviews/R630-2/scripts/gap_mutants.py":"scripts/prior/gap_mutants.py","reviews/R630-3/full_suite_probe.py":"scripts/prior/full_suite_probe.py","author-r4/round4/review-scripts/plants_gap.json":"scripts/prior/plants_gap.json"}
def select(q):
 if q in scripts:return scripts[q]
 base="author-r4/round4/"
 if not q.startswith(base):return None
 rel=q[len(base):]
 if rel in {"candidate-tree.txt","source-snapshot.json","target-source-equivalence.json","final-audit.json","sizes.json","contract-summary.json","contract-row-results.json","plants_contract.json","mutation-summary.json","reference-identities.json","rv32/results.json","review-ready.json"} or rel.startswith("validation/") and rel.count("/")==1:return "receipts/published/"+rel
items=[(x,select(x["path"][len(prefix):])) for x in tree if x["type"]=="blob" and x["path"].startswith(prefix)];items=[(x,t) for x,t in items if t]
def fetch(it):
 x,target=it
 data=json.loads(subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/git/blobs/"+x["sha"]]));b=base64.b64decode(data["content"])
 assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==x["sha"]
 dest=p/target;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 return {"source":x["path"],"blob":x["sha"],"sha256":hashlib.sha256(b).hexdigest(),"local":target}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(fetch,items))
(p/"receipts/public-fetch.json").write_text(json.dumps(results,indent=2)+"\n");print("verified public blobs",len(results))

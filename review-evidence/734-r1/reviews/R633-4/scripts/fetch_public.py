#!/usr/bin/env python3
"""Fetch selected public executable evidence, excluding review reports and author scratchpads."""
import base64,concurrent.futures,hashlib,json,pathlib,subprocess
p=pathlib.Path(__file__).resolve().parents[1]
root="review-evidence/734-r1/"
selected=["reviews/R632-1/scripts/probe_scope.py","reviews/R632-2/probe_r632_2.py","reviews/R632-2/rename_divergence_r632_2.sh","reviews/R632-3/apply_mutation.py","reviews/R633-2/scripts/scope_audit.py","reviews/R633-2/scripts/replay_prior_probe.py"]
selected += ["MANIFEST.json", "author-r4/r4-redactions.json", "author-r4/r4-image-controls.log"]
selected += ["author-r4/"+s for s in ["r4-head.json","r4-contract-final.json","r4-contract-final.log","r4-events-final.json","r4-events-final.log","r4-scope-final.json","r4-docs-final.json","r4-docs-no-git-accepted.json","r4-toc-final.json","r4-dash-head.json","r4-images.json","r4-images.log","r4-image-hashes.json","r4-image-controls.json","r4-mutation-table.json","r4-MANIFEST.sha256","r4-scope-table.json"]]
raw_tree=(p/"evidence-tree.json").read_text() if (p/"evidence-tree.json").exists() else subprocess.check_output(["gh","api","repos/kebag-logic/milan-fpga/git/trees/beeb9d6cbdd2d6abc75f2cb3cc21d9e6f33efa9c?recursive=1"],text=True)
tree={e["path"]:e for e in json.loads(raw_tree)["tree"]}
def fetch(rel):
 info=tree[root+rel];r=subprocess.run(["gh","api","repos/kebag-logic/milan-fpga/git/blobs/"+info["sha"]],capture_output=True,text=True,check=True)
 data=base64.b64decode(json.loads(r.stdout)["content"]);assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==info["sha"]
 f=p/"public"/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
 return {"path":rel,"git_blob":info["sha"],"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(fetch,selected))
(p/"receipts/public-provenance.json").write_text(json.dumps({"revision":"beeb9d6cbdd2d6abc75f2cb3cc21d9e6f33efa9c","files":rows},indent=2)+"\n")
print("Fetched and verified",len(rows),"selected public files")

#!/usr/bin/env python3
"""Read selected public receipts at the fixed evidence commit; verify published bytes."""
import concurrent.futures, hashlib, json, pathlib, subprocess
P=pathlib.Path(__file__).resolve().parents[1]
PREFIX="review-evidence/pp181-r1/"
tree=json.loads((P/"public/evidence-tree.json").read_text())["tree"]
manifest={x["file"]:x for x in json.loads((P/"public/evidence/MANIFEST.json").read_text())}
def selected(r):
 if not r.startswith("author-r2/receipts-r2/"):return False
 s=r.split("/",2)[2]
 if s.startswith(("logs/","ooc/","cone/","route-head760/","sums/","scripts/")):return not s.endswith(".hex")
 if s.startswith("proofs/"):return s.endswith((".sh",".py",".diff",".sv","rc.txt",".out",".log",".ys",".sby",".txt")) and "/mutants/" not in s or s.endswith(".diff")
 if s.startswith("pgates/"):return any(s.endswith(z) for z in ["summary.txt","gitlink.txt","parent-status-before.txt","parent-status-after.txt","check_submodule_docs.log","measure_test_evidence.log","measure_test_evidence_selftest.log"])
 if s.startswith("camp/"):return s.endswith((".out","rc.txt")) or s.count("/")==2 or "/notify/occupancy_" in s or "/notify/golden-aecp_notify-run.log" in s
 return s.endswith("RECIPE.txt")
chosen=[x for x in tree if x["type"]=="blob" and x["path"].startswith(PREFIX) and selected(x["path"][len(PREFIX):])]
def fetch(x):
 r=x["path"][len(PREFIX):]; dst=P/"public/evidence"/r;dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():dst.write_bytes(subprocess.check_output(["gh","api","-H","Accept: application/vnd.github.raw+json","repos/kebag-logic/milan-fpga/git/blobs/"+x["sha"]]))
 b=dst.read_bytes(); gitsha=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest();sha=hashlib.sha256(b).hexdigest()
 assert gitsha==x["sha"],r
 assert sha==manifest[r]["published_sha256"],r
 return {"file":r,"sha256":sha,"git_blob":gitsha,"verified":True}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(fetch,chosen))
(P/"receipts/evidence-integrity.json").write_text(json.dumps(rows,indent=2)+"\n")
print("Verified",len(rows),"selected published files against Git blobs and publication manifest")

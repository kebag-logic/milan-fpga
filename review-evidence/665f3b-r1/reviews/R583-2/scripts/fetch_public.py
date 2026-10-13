import concurrent.futures, hashlib, json, subprocess, sys
from pathlib import Path
packet=Path(sys.argv[1]).resolve()
commit="e3af796024d095e9f5cb9fa231e8efe34c501100"
base="review-evidence/665f3b-r1/author-r2/"
(packet/"scratch").mkdir(parents=True,exist_ok=True)
(packet/"receipts").mkdir(parents=True,exist_ok=True)
if not (packet/"scratch/evidence-tree.json").exists():
    tree=subprocess.check_output(["gh","api",f"repos/kebag-logic/milan-fpga/git/trees/{commit}?recursive=1"])
    (packet/"scratch/evidence-tree.json").write_bytes(tree)
paths=["pin-proof.json", "fabric-identity.json", "image-hashes.json", "gate-ledger.json"]
paths += ["round2/"+n for n in ("coverage-table.txt","final-state.json","gate-ledger.json","image-hashes.json","image-table.md","mutation-summary.json","fabric-identity.json","pin-integrity.json","mutations-control.csv","mutations-srp.csv","mutations-aecp.csv","reproduce/probe_owner.cpp","reproduce/run_probes_fixed.py","reproduce/run_focused.py")]
paths += ["round2/evidence/"+n+ext for n in ("control-campaign","aecp-campaign","srp-campaign","coverage","normal-suites","boundary-host-split","boundary-rtl","fabric","images","pins","owner-probe","predicate-controls","lifecycle-mutants","bounds","gate-list","doc-gates-summary") for ext in (".json",".log")]
known={x["path"]:x for x in json.loads((packet/"scratch/evidence-tree.json").read_text())["tree"]}
paths=[p for p in paths if base+p in known]
out=packet/"receipts/public-author"
def fetch(path):
    r=subprocess.run(["gh","api","-H","Accept: application/vnd.github.raw+json",f"repos/kebag-logic/milan-fpga/contents/{base+path}?ref={commit}"],capture_output=True,check=True)
    target=out/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(r.stdout)
    blob=hashlib.sha1(b"blob "+str(len(r.stdout)).encode()+b"\0"+r.stdout).hexdigest()
    assert blob==known[base+path]["sha"], path
    return {"path":str(target.relative_to(packet)),"public_path":base+path,"commit":commit,"git_blob":blob,"sha256":hashlib.sha256(r.stdout).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(fetch,paths))
(packet/"receipts/public-downloads.json").write_text(json.dumps(results,indent=2)+"\n")
print(f"Verified {len(results)} public evidence blobs")

#!/usr/bin/env python3
"""Fetch selected public executable receipts, verify published manifest hashes."""
import hashlib,json,pathlib,subprocess,sys
packet=pathlib.Path(sys.argv[1]).resolve()
rev="412c0f10e12755a47f79ec3f90e08ef5d2ecaa47"
base="review-evidence/677-r1"
out=packet/"scratch/public"
out.mkdir(parents=True,exist_ok=True)
def get(name):
    return subprocess.check_output(["gh","api","-H","Accept: application/vnd.github.raw+json",f"repos/kebag-logic/milan-fpga/contents/{base}/{name}?ref={rev}"])
manifest=json.loads(get("MANIFEST.json")); hashes={r["file"]:r["published_sha256"] for r in manifest}
names=["author/evidence.json","author/nvm-campaign.json", "author/logs/ctrl.log","author/logs/nvm-controls.log","author/logs/coverage-check.log","author/logs/coverage-selftest.log", "author/logs/erased-end-asan.log"]
names += ["author/logs/nvm-batch-"+b+".log" for b in ("1-20","21-40","41-60","61-80","81-95","96-109")]
rows=[]
for name in names:
    data=get(name); digest=hashlib.sha256(data).hexdigest()
    assert digest==hashes[name],name
    path=out/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    rows.append({"path":name,"sha256":digest,"manifest_match":True,"url":f"https://github.com/kebag-logic/milan-fpga/blob/{rev}/{base}/{name}"})
    if name.endswith(".log"):
        print(name)
        print("\n".join(data.decode().splitlines()[-6:]))
evidence=json.loads((out/"author/evidence.json").read_text())
assert evidence["head"]=="6c94e9f5f496ac25f8c4e31f9e3685c725de29f3"
summary={"head":evidence["head"],"evidence_commit":rev,"receipts":rows,"gates":[{k:r[k] for k in ("gate","rc","seconds","command")} for r in evidence["gates"]]}
text=json.dumps(summary,indent=2)+"\n"
# Public producer already normalizes roots; no private input is read.
(packet/"receipts/public-evidence-audit.json").write_text(text)
print("Published hashes verified:",len(rows),"Gate records:",len(evidence["gates"]))

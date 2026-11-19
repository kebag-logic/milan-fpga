#!/usr/bin/env python3
"""Package public receipts and verify the final publication manifest."""
import hashlib, json, os, pathlib, subprocess
p=pathlib.Path(__file__).resolve().parent
h=p/"hosted-snapshot.json"
d=json.loads(h.read_text())
if any("response" in r for r in d["runs"]):
    for r in d["runs"]:
        r["jobs"]=[{**{k:j.get(k) for k in ("id","name","status","conclusion")},
                    "steps":[{k:s.get(k) for k in ("name","status","conclusion")} for s in (j.get("steps") or [])]}
                   for j in r.pop("response")["jobs"]]
    d["scope"]="One snapshot; first job page per run; no polling for acceptance"
    h.write_text(json.dumps(d,indent=2)+"\n")
a="af70bbe3ceb299a0c65826df70c8bea492f28e0d"
prefix="review-evidence/951-r1/"
def show(path):
    return subprocess.check_output(["git","show",a+":"+prefix+path],
                                   env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"})
rows=json.loads(show("MANIFEST.json"))
selected=[]
for row in rows:
    path=row["file"]
    if path.startswith(("author-r1/receipts/images/pairs/","author-r1/receipts/cpu/legs/",
                        "author-r1/receipts/cpu/compare/","author-r2/receipts/images/",
                        "author-r2/receipts/gates/","author-r2/receipts/tests/")):
        data=show(path)
        assert hashlib.sha256(data).hexdigest()==row["published_sha256"]
        target=p/"public-receipts"/path
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
        selected.append(row)
(p/"public-receipts"/"ARCHIVE-MANIFEST.json").write_text(json.dumps({
    "archive":a,"prefix":prefix,"files":selected},indent=2)+"\n")
# Preliminary independent verdict remains a private work product; final REPORT governs publication.
pre=p/"independent-pass.md"
if pre.exists():
    (p/"scratch").mkdir(exist_ok=True)
    pre.rename(p/"scratch"/pre.name)
report=(p/"REPORT.md").read_text()
assert report.splitlines()[0]=="[R870] NEGATIVE - exact head f09d82e05270bdd77e07f7fc2e14d064c1123be8"
assert report.splitlines()[-1]=="R870-2 FINISHED"
assert "SKELETON" not in report
assert all((p/(name+".rc")).read_text().strip()=="0" for name in
           ("audit-delta","checkout-integrity","docs-check","diff-check"))
files=sorted(x for x in p.rglob("*") if x.is_file() and "scratch" not in x.relative_to(p).parts
             and x.name!="MANIFEST.sha256")
lines=[hashlib.sha256(x.read_bytes()).hexdigest()+"  "+str(x.relative_to(p)) for x in files]
(p/"MANIFEST.sha256").write_text("\n".join(lines)+"\n")
for x,line in zip(files,lines):
    assert hashlib.sha256(x.read_bytes()).hexdigest()==line[:64]
print("Publication files:",len(files),"including REPORT.md; public archive receipts:",len(selected))
print("Manifest hashes PASS; scratch excluded; final verdict NEGATIVE; report terminator verified")


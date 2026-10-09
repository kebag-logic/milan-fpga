#!/usr/bin/env python3
"""Publish selected text receipts with only local path prefixes replaced."""
import hashlib,json,pathlib,shutil,sys
root=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();out=p/"receipts";copied=[];mapping=[]
replacements=[(str(root),"<SOURCE>"),(str(p),"<PACKET>"),("<home-path>/work/tsn-c-stack/tsn-c-stack","<HOSTED_SOURCE>"),("<home-path>","<HOSTED_HOME>"),(str(pathlib.Path.home()),"<HOME>")]
def copy(source,target):
 if not source.is_file():return
 target.parent.mkdir(parents=True,exist_ok=True);text=source.read_text()
 for old,new in replacements:text=text.replace(old,new)
 target.write_text(text);copied.append(str(target.relative_to(p)));mapping.append({"file":str(target.relative_to(p)),"original_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"published_sha256":hashlib.sha256(target.read_bytes()).hexdigest()})
w=p/"scratch/local"
for source in w.iterdir():
 if source.suffix in (".json",".log",".rc"):copy(source,out/"local"/source.name)
gates=[]
for gate in ["static-analysis","graphs"]:gates.append({"gate":gate,"rc":int((w/(gate+".rc")).read_text())})
(out/"local/supplemental-gates.json").write_text(json.dumps(gates,indent=2)+"\n")
for directory in ["mutations","rv32","templates","conditionals","graphs","dependencies"]:
 for source in (w/directory).rglob("*"):
  if source.is_file() and (source.suffix in (".xml",".json",".map",".svg") or source.name in ("wrong-version.log","smoke.log","build.log","forms.log")):
   copy(source,out/"local"/source.relative_to(w))
for event in ["pr","push"]:
 for source in (p/"scratch/hosted"/event).rglob("*"):
  if source.is_file() and source.suffix in (".json",".log",".rc",".xml"):
   if event=="push" and source.suffix==".xml":continue
   copy(source,out/"hosted"/event/source.relative_to(p/"scratch/hosted"/event))
for name in ["hosted-checks.txt","hosted-pr-jobs.json","hosted-push-jobs.json","native-wrong-version.log","native-wrong-version.rc"]:copy(p/"scratch"/name,out/name)
for source in (p/"scratch/document-replay").glob("*"):
 if source.suffix in (".log",".rc"):copy(source,out/"prior"/source.name)
r=p/"scratch/replays"
for source in r.glob("*"):
 if source.suffix in (".log",".rc",".json"):copy(source,out/"prior"/source.name)
for source in (r/"r5566").glob("*"):
 if source.suffix in (".json",".log"):copy(source,out/"prior/r5566"/source.name)
for directory in ["r5574-comments","r5576-controls","legacy5/receipts","legacy6/receipts","early/receipts","early-driver/driver-probes/work"]:
 for source in (r/directory).glob("*.json"):copy(source,out/"prior"/directory/source.name)
for source in (r/"r5565-tree").glob("*.log"):copy(source,out/"prior/r5565-tree"/source.name)
for source in (r/"early-gates/probes").glob("*.log"):copy(source,out/"prior/early-gates"/source.name)
for source in (p/"scratch/explicit-package").glob("*"):
 if source.suffix in (".log",".rc",".json",".txt"):copy(source,out/"package-prefix"/source.name)
for source in (p/"scratch/package-prefix-probe").glob("*"):
 if source.suffix in (".log",".rc",".json",".txt"):copy(source,out/"package-prefix/control"/source.name)
for source in (p/"scratch/sdk/gtest/lib/pkgconfig").glob("*.pc"):copy(source,out/"package-prefix/metadata"/source.name)
# Review inputs are limited to public body/decision material and independent diff notes.
pr=json.loads((p/"scratch/pr.json").read_text());(out/"pr-body.md").write_text(pr["body"]+"\n")
copy(p/"scratch/closed-pr1-body.md",out/"closed-pr1-body.md")
copy(p/"scratch/independent-pass.txt",out/"independent-pass.txt")
(out/"receipt-format.json").write_text(json.dumps({"format":"Command outputs retained; only location prefixes replaced by placeholders. Raw originals and disposable builds remain in scratch, excluded from publication.","embedded_hashes":"Regrade hashes describe raw XML before location replacement; MANIFEST describes published bytes.","placeholders":[x[1] for x in replacements]},indent=2)+"\n")
(out/"export-map.json").write_text(json.dumps(mapping,indent=2)+"\n")
print(len(copied),"text receipts exported")

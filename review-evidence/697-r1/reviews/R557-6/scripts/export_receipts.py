#!/usr/bin/env python3
import hashlib,io,json,pathlib,shutil,subprocess,sys,tarfile
root=pathlib.Path(sys.argv[1]).resolve(); p=pathlib.Path(sys.argv[2]).resolve(); r=p/"receipts"; source=p/"scratch"
replacements=[(str(p),"$PACKET"),(str(root),"$SOURCE_ROOT"),("<home-path>/work/tsn-c-stack/tsn-c-stack","$HOSTED_SOURCE"),("<home-path>","$HOSTED_RUNNER")]
redactions=[]
def redact(data):
 try:text=data.decode()
 except UnicodeDecodeError:return data
 for old,new in replacements:text=text.replace(old,new)
 return text.encode()
def copy(src,dest):
 dest.parent.mkdir(parents=True,exist_ok=True); raw=src.read_bytes(); data=redact(raw); dest.write_bytes(data)
 if data!=raw:redactions.append({"file":str(dest.relative_to(p)),"original_sha256":hashlib.sha256(raw).hexdigest(),"published_sha256":hashlib.sha256(data).hexdigest()})
for label,work in (("local-linux",source/"suites/linux"),("hosted",source/"hosted/quality-evidence")):
 for file in work.iterdir():
  if file.is_file() and file.suffix in (".log",".rc",".json"):copy(file,r/label/file.name)
 for rel in ("conditionals/results.json","assertion-templates/forms.log","assertion-templates/forms.xml","assertion-templates/forms.cpp","mutations/results.json","mutations/message-markers.json"):
  if (work/rel).exists():copy(work/rel,r/label/rel)
 for file in (work/"graphs").glob("*.svg"):copy(file,r/label/"graphs"/file.name)
 archive=r/(label+"-mutation-xml.tar.gz")
 with tarfile.open(archive,"w:gz") as t:
  for file in sorted((work/"mutations").glob("*/*.xml")):
   data=redact(file.read_bytes()); info=tarfile.TarInfo(str(file.relative_to(work/"mutations")));info.size=len(data);info.mtime=0;t.addfile(info,io.BytesIO(data))
 if label=="local-linux":
  for kind in ("gcc","clang-sanitizers"):copy(work/kind/"Testing/Temporary/LastTest.log",r/label/(kind+"-instances.log"))
for label,work in (("local-rv32",source/"suites/rv32"),("hosted-rv32",source/"hosted/rv32-evidence")):
 for file in work.rglob("*"):
  if file.is_file() and (file.name=="results.json" or file.suffix in (".log",".map")):copy(file,r/label/file.relative_to(work))
for directory in ("independent-probes","full-assertion-probe"):
 for file in (source/directory).iterdir():
  if file.is_file() and file.suffix in (".log",".xml",".json",".cpp"):copy(file,r/directory/file.name)
for name in ("independent-probes.json","production-preservation.json","assembly-full-tree-probe.json","assembly-probe-comment-gate.log","assembly-probe-rv32.log"):
 copy(source/"prior/R557-5/receipts"/name,r/"prior/R557-5"/name)
for src,dest in ((source/"prior/r5565-hidden/results.json",r/"prior/R556-5-hidden.json"),(source/"prior/r5574-full.json",r/"prior/R557-4-full.json"),(source/"prior/r5574-comments/results.json",r/"prior/R557-4-comments.json"),(source/"prior/r5574-ownership.json",r/"prior/R557-4-ownership.json"),(source/"early-probes/legacy/receipts/comment-controls.json",r/"prior/early-comment-controls.json")):
 copy(src,dest)
for file in (source/"prior/r5565-tree").glob("*.log"):copy(file,r/"prior/R556-5-tree"/file.name)
for file in (source/"early-probes/probes").glob("*.log"):copy(file,r/"prior/early-gates"/file.name)
for rel in ("campaign.log","work/results.json"):
 copy(source/"early-probes/driver-probes"/rel,r/"prior/early-driver"/rel)
pr=json.loads((source/"pr.json").read_text()); (r/"pr-body.md").write_text(pr["body"]+"\n")
pr1=json.loads((source/"pr1.json").read_text()); (r/"closed-pr1-body.md").write_text(pr1["body"]+"\n")
a=json.loads((source/"issue-comments.json").read_text()); ready=next(x for x in a if x["id"]==6078586685); (r/"review-ready.md").write_text(ready["html_url"]+"\n\n"+ready["body"]+"\n")
run_data=json.loads((source/"runs.json").read_text()); selected=[{k:x[k] for k in ("id","head_sha","event","conclusion","html_url","created_at","updated_at")} for x in run_data["workflow_runs"]]; (r/"hosted-runs.json").write_text(json.dumps(selected,indent=2)+"\n")
for file in r.rglob("*"):
 if file.is_file() and file.suffix not in (".gz",):
  raw=file.read_bytes(); data=redact(raw)
  if raw!=data:
   redactions.append({"file":str(file.relative_to(p)),"original_sha256":hashlib.sha256(raw).hexdigest(),"published_sha256":hashlib.sha256(data).hexdigest()}); file.write_bytes(data)
(r/"path-redactions.json").write_text(json.dumps({"policy":"Only checkout, packet and hosted-runner path prefixes were replaced by symbolic placeholders. Scripts retained unchanged. XML archive members receive the same replacements. Original receipts remain in scratch.","files":redactions},indent=2)+"\n")
print("Exported review receipts; local and hosted mutation XML retained separately")

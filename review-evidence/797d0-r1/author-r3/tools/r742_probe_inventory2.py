#!/usr/bin/env python3
"""Reproduce focused inventory probes; all disposable files stay under packet/scratch."""
import argparse, io, json, os, subprocess, sys, tarfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("repo",type=Path);ap.add_argument("packet",type=Path);a=ap.parse_args()
r=a.repo.resolve();p=a.packet.resolve(); s=p/"scratch";s.mkdir(exist_ok=True)
os.environ["TMPDIR"]=str(s);os.environ["PYTHONDONTWRITEBYTECODE"]="1"
def run(root,*args,want=0):
 out=subprocess.run([sys.executable,"scripts/docs_inventory.py",*args],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=os.environ)
 print("COMMAND",list(args),"rc",out.returncode,"expected",want);print(out.stdout,end="")
 assert out.returncode==want
run(r,"--check");run(r,"--selftest")
t=s/"probe-tree";t.mkdir(exist_ok=True)
raw=subprocess.check_output(["git","archive","HEAD"],cwd=r)
with tarfile.open(fileobj=io.BytesIO(raw)) as tf: tf.extractall(t,filter="data")
subprocess.run(["git","init","-q",str(t)],check=True)
subprocess.run(["git","-C",str(t),"add","-A"],check=True)
data=t/"scripts/docs_inventory.json";d=json.loads(data.read_text());d["findings"].append({"id":"PROBE-001","page":"docs/README.md","quote":"The implementation remains Milan-oriented.","source":"Reviewer planted control, not a real contradiction","correction":"Remove planted control"});data.write_text(json.dumps(d))
print("PLANT finding on previously current docs/README.md")
run(t,"--check",want=1);run(t,"--write");run(t,"--check")
audit=t/"docs/DOCUMENTATION_AUDIT.md";text=audit.read_text();row=next(x for x in text.splitlines() if x.startswith("| [docs/README.md]"));assert "| stale |" in row;print("GENERATED",row)
audit.write_text(text.replace(row,row.replace("| stale |","| current |")))
print("PLANT current status against open finding");run(t,"--check",want=1)
run(t,"--write")
script=t/"scripts/docs_inventory.py";original=script.read_text()
mutants={
"gate-always-passes":("    expected = generate(root)\n", "    return 0\n    expected = generate(root)\n"),
"include-untracked":("[\"git\", \"-C\", str(root), \"ls-files\", \"-z\"]", "[\"git\", \"-C\", str(root), \"ls-files\", \"--cached\", \"--others\", \"--exclude-standard\", \"-z\"]"),
"remove-status-rule":("if page_findings and state == \"current\":", "if False:")}
for label,(old,new) in mutants.items():
 assert old in original,label
 script.write_text(original.replace(old,new,1));print("MUTANT",label);run(t,"--selftest",want=1)
script.write_text(original)
print("PASS all focused probes; candidate checkout untouched")

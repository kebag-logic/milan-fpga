#!/usr/bin/env python3
"""Independent parse/status, comment custody, and planting controls."""
import argparse, importlib.util, os, re, subprocess, sys, tempfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True);ap.add_argument("--work",type=Path,required=True);ap.add_argument("--make",type=Path,required=True);a=ap.parse_args()
root=a.repo.resolve();work=a.work.resolve();work.mkdir(parents=True,exist_ok=True)
make=a.make.resolve();os.environ["PATH"]=str(make.parent)+os.pathsep+os.environ["PATH"]
os.environ["MAKEFLAGS"]="-pqrR";os.environ["MFLAGS"]="-pqrR"
sys.path.insert(0,str(root/"scripts"));import shape_consumer_inventory as inv
print(subprocess.check_output([str(make),"--version"],text=True).splitlines()[0])
for label,prefix in (("early", ""),("after-rule", "fixture: missing-generated-input\n")):
 path=work/(label+".mk");path.write_text(prefix+"$(error planted stopped parse)\nfixture: ../../../hdl/common/gen/adp_shape_defaults.svh\n")
 raw=subprocess.run([str(make),"-pqrR","-f",str(path)],cwd=work,capture_output=True,text=True)
 assert raw.returncode==2 and "# Files" in raw.stdout
 assert inv.shape_prereqs_from_database(work,path.name)==(False,[])
 print(label,"raw_rc=2 partial_database=True inventory_unreadable=True")
path=work/"complete.mk";path.write_text("fixture: missing-generated-input ../../../hdl/common/gen/adp_shape_defaults.svh\n")
ok,items=inv.shape_prereqs_from_database(work,path.name);assert ok and items==["../../../hdl/common/gen/adp_shape_defaults.svh"]
print("missing generated input control: readable=True frozen_shape=True")
for name in ("milan_dp_render","pp_shadow"):
 suite=root/"tb/verilator"/name
 ok,items=inv.shape_prereqs_from_database(suite,"Makefile");assert ok and items,(name,ok,items)
 print(name,"readable=True frozen_prerequisites="+repr(items))
# Test the real consumer source with only the proposed assertion removed in a disposable file.
suite=root/"tb/verilator/pp_shadow";orig=(suite/"Makefile").read_text()
assertion="ifneq ($(.SHELLSTATUS),0)\n$(error ../milan_dp print-srcs failed; the datapath source list could not be derived)\nendif\n"
assert orig.count(assertion)==1
for label,text,fail_nested,expected in (("real-positive",orig,False,0),("real-refusal",orig,True,2),("assertion-deleted",orig.replace(assertion,""),True,0)):
 path=work/(label+".mk");path.write_text(text)
 command=[str(make),"-s","--no-print-directory","-C",str(suite),"-f",str(path),"--eval",".PHONY: review-probe","--eval","review-probe:;","review-probe"]
 if fail_nested:command.append("MAKE=false")
 r=subprocess.run(command,env=dict(os.environ,MAKEFLAGS="",MFLAGS=""),capture_output=True,text=True)
 assert r.returncode==expected,(label,r.returncode,r.stderr)
 if expected:assert "../milan_dp print-srcs failed" in r.stderr
 print(label,"rc="+str(r.returncode),"named_refusal="+str("../milan_dp print-srcs failed" in r.stderr))
# Compare executable RTL text, preserving strings; comment edits must remove all changes.
path="hdl/ieee8021q/filtering/rx_mac_filter.sv"
old=subprocess.check_output(["git","-C",str(root),"show","5603c353:"+path],text=True)
new=(root/path).read_text()
pattern=re.compile(r"(\"(?:\\.|[^\"\\])*\")|//[^\n]*|/\*[\s\S]*?\*/")
strip=lambda s:pattern.sub(lambda m:m.group(1) or "",s)
assert strip(old)==strip(new)
changed=subprocess.check_output(["git","-C",str(root),"diff","--name-only","5603c353..HEAD","--","hdl"],text=True).splitlines();assert changed==[path]
print("all changed RTL non-comment bytes identical: PASS")
spec=importlib.util.spec_from_file_location("binding",root/"tb/verilator/rx_filter/binding_mutant.py");mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for label,p,old,new,marker in mod.ARMS:
 assert p.read_text().count(old)==1,label
 print("plant_check:",label,"unique_anchor=1 replacement_changes_bytes=True")
print("focused probes PASS")

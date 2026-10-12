#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,re,shutil
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);p.add_argument("--path-map",type=pathlib.Path);a=p.parse_args();r=a.packet;s=r/"scratch"
# Copy execution output only: never source exports, objects, SDKs or executables.
for directory,target in [(s/"validation",r/"receipts/validation"),(s/"validation-initial",r/"receipts/initial-environment")]:
 for f in directory.iterdir():
  if f.is_file() and f.suffix in (".json",".log",".rc"):
   dest=target/f.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
for origin,target,patterns in [
 (s/"validation/mutations",r/"receipts/mutations",["results.json","message-markers.json","*/*.xml","*/run.log"]),
 (s/"contract",r/"receipts/contract-xml",["w*/build/*.xml"]),
 (s/"r630-3-full-suite",r/"receipts/r630-3-xml",["w*/build/*.xml"]),
 (s/"escape",r/"receipts/escape",["escape-probe.json","*/*.log"]),
 (s/"gap-mutants",r/"receipts/gap-mutants",["gap-mutants.json","*/run.log"]),
 (s/"rv32-head",r/"receipts/rv32-head",["results.json","*/*.log","*/*.map"]),
 (s/"rv32-base",r/"receipts/rv32-base",["results.json","*/*.log","*/*.map"]),
 (s/"graphs",r/"receipts/graphs",["*.svg"])]:
 for pattern in patterns:
  for f in origin.glob(pattern):
   dest=target/f.relative_to(origin);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
for directory in s.glob("physical-*"):
 for f in [directory/"physical-removal.json",*directory.glob("*/run.log")]:
  if f.is_file():
   dest=r/"receipts/physical"/directory.name/f.relative_to(directory);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
normalizations=[(str(s),"$SCRATCH"),(str(a.source),"$SOURCE"),(str(r),"$PACKET"),(str(pathlib.Path.home()),"$HOME")]
if a.path_map:normalizations.extend(json.loads(a.path_map.read_text()))
provenance=[]
for f in sorted((r/"receipts").rglob("*")):
 if not f.is_file() or f.name=="receipt-provenance.json":continue
 raw=f.read_bytes();data=raw
 try:
  text=raw.decode()
  for old,new in normalizations:text=text.replace(old,new)
  data=text.encode()
 except UnicodeError:pass
 if data!=raw:
  orig=s/"receipt-originals"/f.relative_to(r);orig.parent.mkdir(parents=True,exist_ok=True);orig.write_bytes(raw);f.write_bytes(data)
 provenance.append({"path":str(f.relative_to(r)),"original_sha256":hashlib.sha256(raw).hexdigest(),"published_sha256":hashlib.sha256(data).hexdigest(),"path_normalized":raw!=data})
(r/"receipts/receipt-provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
print("Collected",len(provenance),"execution receipts; normalized only machine-specific paths")

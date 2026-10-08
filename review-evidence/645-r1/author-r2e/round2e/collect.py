import hashlib,json,re,sys
from pathlib import Path
w=Path(__file__).resolve().parent
out=Path.home()/"milan-fpga-management/2026-09-23/645-a531/round2e"
out.mkdir(parents=True,exist_ok=True)
def scrub(t):
 for root,tag in [(str(w),"$WORK"),(str(Path.home()/"milan-fpga-management/2026-09-23/645-a531"),"$PACKET"),("$REPO","$REPO"),(str(Path.home()),"$HOME")]:t=t.replace(root,tag)
 return re.sub(r"^\| Host\s+:.*$","| Host : build host",t,flags=re.M)
def digest(p):
 with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
records=[]
def save(p,rel=None):
 if not p.is_file():return
 rel=rel or p.relative_to(w)
 row=dict(path=str(p.relative_to(w)),bytes=p.stat().st_size,sha256=digest(p))
 target=out/rel;target.parent.mkdir(parents=True,exist_ok=True)
 excluded=p.suffix in (".dcp",".bit",".bin",".init",".sv",".v",".svh",".hex",".mem")
 if not excluded and p.stat().st_size<=200000:
  data=scrub(p.read_text(errors="replace")).encode();assert len(data)<=200000
  target.write_bytes(data);row.update(retained=str(rel),retained_sha256=hashlib.sha256(data).hexdigest())
 elif p.suffix==".log":
  with p.open("rb") as f:f.seek(max(0,p.stat().st_size-40000));tail=f.read().decode(errors="replace").split("\n",1)[-1]
  data=scrub("EXCERPT: final portion only. Original bytes and SHA-256 are in the inventory.\n"+tail).encode()
  target=target.with_suffix(".tail.txt");target.write_bytes(data)
  row.update(excerpt=str(target.relative_to(out)),excerpt_sha256=hashlib.sha256(data).hexdigest())
 elif p.suffix==".rpt":
  with p.open("rb") as f:head=f.read(40000).decode(errors="replace").rsplit("\n",1)[0]
  data=scrub("EXCERPT: opening portion only. Original bytes and SHA-256 are in the inventory.\n"+head+"\n").encode()
  target=target.with_suffix(".head.txt");target.write_bytes(data)
  row.update(excerpt=str(target.relative_to(out)),excerpt_sha256=hashlib.sha256(data).hexdigest())
 records.append(row)
for root in [w/"logs",w/"jobs",w/"source-gates",w/"sweep-rerun",w/"physical",w/"litex-sims",w/"arrival",w/"follow-pullin",w/"timing/elaboration"]:
 if root.exists():
  for p in sorted(root.rglob("*")):
   if p.suffix in (".log",".rc",".json",".tsv",".txt",".md") and p.is_file():save(p)
for p in sorted(w.glob("*.json")):save(p)
for p in sorted(w.glob("*.py")):save(p)
save(w/"functional/run-simulator-limited")
for p in sorted((w/"timing").glob("*.json")):save(p)
for p in sorted((w/"functional").glob("exports-*.json")):save(p)
for name in ["functional.log","functional-continuation.log","firmware-shards.log","firmware-interleaved.log","sweeps.log","parallel-sweeps.log","extra.log","vendor.log","elaboration.log","elaboration8.log","quiet.json","campaign.py"]:save(w/name)
for root in [w/"area-ooc",w/"gmii-fixtures",w/"timing/ax7101/gateware",w/"timing/ax7101-AltSpreadLogic_high/gateware",w/"timing/ax7101-ExtraTimingOpt/gateware",w/"timing/ax8x8/gateware",w/"timing/ooc-1x1",w/"timing/ooc-8x8"]:
 if root.exists():
  for p in sorted(root.iterdir()):
   if p.is_file() and p.suffix in (".rpt",".json",".tcl",".tsv",".log",".rc",".bit",".dcp",".txt",".sv",".v",".svh",".xdc",".hex",".mem",".init",".bin"):save(p)
save(w/"area-ooc/prepare.py")
for build in (w/"timing").glob("ax7101*"):
 save(build/"flashboot_layout.json")
 save(build/"aem_desc.bin")
for name in ("render","dev-render","render-pullin","render-boundary"):
 root=w/"functional"/name/"tb/verilator/milan_dp_render"
 for p in sorted((root/"obj_pullin").glob("*.log")):save(p,Path(name+"-pullin")/p.name)
 for folder in root.glob("obj_*"):
  if "mut" in folder.name or "boundary" in folder.name:
   for p in folder.rglob("*"):
    if p.is_file() and p.suffix in (".json",".log",".rc") and not "build" in p.name:save(p,Path(name+"-campaign")/p.relative_to(root))
for p in sorted((w/"functional/builder/tb/verilator/milan_dp/obj_ax1x1gptp").glob("*.log")):
 save(p,Path("physical-controls")/p.name)
for i in range(0,len(records),100):
 data=json.dumps(records[i:i+100],indent=2)+"\n";assert len(data.encode())<=200000
 (out/("inventory-"+str(i//100).zfill(2)+".json")).write_text(data)
summary=[]
for p in sorted((w/"logs").glob("*.receipt.json")):
 row=json.loads(p.read_text());row["name"]=p.name.removesuffix(".receipt.json");summary.append(row)
command_data=(scrub(json.dumps(summary,indent=2))+"\n").encode()
assert len(command_data)<=200000, len(command_data)
(out/"commands.json").write_bytes(command_data)
print("retained receipts",len(records),"completed commands",len(summary))

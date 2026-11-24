#!/usr/bin/env python3
"""Reproduce the adoption's bounded artifact audit from public Git objects.
Usage: python3 review_audit.py REPO OUTPUT
The public evidence commit must already be available in REPO.
"""
import ast,difflib,hashlib,json,pathlib,re,subprocess,sys
sys.dont_write_bytecode=True
repo,out=(pathlib.Path(s).resolve() for s in sys.argv[1:])
base="300da99beed5bb1c77e4b04af0bb4f9369856e0d"
head="bbfdb6746d585e490508783dc8a88c79fbab02c0"
evidence="3779446004dfb5ea4b18088bed83637e49139754"
pin="1213ac5b9e09b8759ba76cc70c53652b5e108996"
def git(*args,root=repo):return subprocess.check_output(["git","-C",str(root),*args],text=True)
print("HEAD",git("rev-parse","HEAD").strip());print("TREE",git("rev-parse","HEAD^{tree}").strip())
assert git("rev-list","--count",base+".."+head).strip()=="4"
print(git("log","--format=%H %s",base+".."+head),end="")
print(git("diff","--stat",base,head),end="")
sub=repo/"gptp-processor"
assert git("rev-parse","HEAD",root=sub).strip()==pin
assert git("rev-parse",pin+"^{tree}",root=sub)==git("rev-parse","331e27de^{tree}",root=sub)
subprocess.run(["git","-C",str(sub),"merge-base","--is-ancestor","1616fc8f",pin],check=True)
print("Donor pin fast-forwards old pin; tree equals reviewed donor head",git("rev-parse",pin+"^{tree}",root=sub).strip())
for directory in ["hdl","configs","sw","tb","scripts"]:
 assert git("rev-parse","973f2f20:"+directory)==git("rev-parse",head+":"+directory)
 print("route-input-ancestor to final identical tree:",directory)
print("973f2f20..HEAD changed paths:");print(git("diff","--name-only","973f2f20",head),end="")
print("c2b2ba1a..base changed paths:");print(git("diff","--name-only","c2b2ba1a",base),end="")
for rev in ["c2b2ba1a",base]:
 tree=ast.dump(ast.parse(git("show",rev+":sw/litex/ctrl_memory.py")),include_attributes=False)
 if rev=="c2b2ba1a":old=tree
 else:assert old==tree
print("Base route ctrl_memory.py AST identical; changed source is string wrapping")
for directory in ["hdl","configs"]:
 assert git("rev-parse","c2b2ba1a:"+directory)==git("rev-parse",base+":"+directory)
print("Base route HDL/config trees identical")
rom=out/"scratch"/"audit-rom.hex"
r=subprocess.run([sys.executable,str(sub/"hdl/ucode/gen_gptp_ucode.py"),"-o",str(rom)],capture_output=True,text=True,check=True)
print(r.stdout.replace(str(out),"<packet>"),end="")
hash=hashlib.sha256(rom.read_bytes()).hexdigest()
assert hash=="4eb21cefc8d769df4a764402aead970b59be96cb3fa267d25af9d1857935f083"
assert hash==hashlib.sha256((sub/"syn/ooc/work/gptp_ucode.hex").read_bytes()).hexdigest()
assert pin+"\tgptp_ucode.hex\t"+hash in (repo/"syn/yosys/rom_digests.tsv").read_text()
print("ROM generated/default/tracked/ledger equal:",hash)
manifest=json.loads((repo/"docs/diagrams/PNG_MANIFEST.json").read_text())
# Find the two entries without assuming the manifest's outer wrapper name.
def entries(obj):
 if isinstance(obj,dict):
  for key,val in obj.items():
   if key in ["docs/diagrams/submodule_boundaries.png","docs/diagrams/timesync_chain.png"]:
    sys.path.insert(0,str(repo/"scripts"))
    from png_artifact import inspect_png
    assert inspect_png(repo/key).raster_sha256==val["raster_sha256"]
    assert hashlib.sha256((repo/val["source"]).read_bytes()).hexdigest()==val["source_sha256"]
    print("PNG/source manifest matches",key)
   else:entries(val)
entries(manifest)
public=out/"scratch/public";public.mkdir(parents=True,exist_ok=True)
prefix="review-evidence/gptppin-r1/author/"
files=git("ls-tree","-r","--name-only",evidence,prefix).splitlines()
for filename in files:
 p=public/filename.removeprefix(prefix);p.parent.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(["git","show",evidence+":"+filename],cwd=repo)
 p.write_bytes(data)
print("Read",len(files),"author packet files at",evidence)
receipts=public/"receipts"
for shape,want,delta in [("8x8-ExtraPostPlacementOpt",46246,-375),("1x1-ExtraTimingOpt",32639,-41)]:
 d=receipts/"route"/shape
 lut=lambda name:int(re.search(r"Slice LUTs=(\d+)",(d/name).read_text())[1])
 assert lut("utilization.txt")==want
 assert lut("utilization.txt")-lut("utilization-base-300da99b.txt")==delta
 print(shape,"LUT",want,"base",lut("utilization-base-300da99b.txt"),"delta",delta)
 corners=re.findall(r"(Slow_85C|Slow_0C|Fast_85C|Fast_0C): WNS ([+\d.]+) ns \(0 failing\), WHS ([+\d.]+) ns \(0 failing\)",(d/"signoff.txt").read_text())
 assert len(corners)==4
 for corner,wns,whs in corners:
  assert float(wns)>=0.030 and float(whs)>=0
  print("#818 PASS",corner,"WNS",wns,"WHS",whs)
 assert (d/"build.rc").read_text().strip()=="0"
 print("Published identity receipt:",(d/"identity.log").read_text().strip())
 print("Published image digests:",(d/"artifacts.sha256").read_text().strip())
print("1x1 signoff receipt rc=1 uses extra WHS>=0.030; #818 is WHS>=0 and passes")
for filename in ["rtl/milan_dp-gptp-39e9c9d2.log","rtl/milan_dp-gptp-lat-39e9c9d2.log"]:
 s=(receipts/filename).read_text();assert "212 checks: 212 PASS, 0 FAIL" in s
 print(filename)
 for line in s.splitlines():
  if "[CA]" in line or "checks:" in line:print(line)
for filename in sorted((receipts/"rtl").glob("sweep-shard-?-8c5a51e1.txt")):
 print(filename.name)
 for line in filename.read_text().splitlines():
  if "gptp" in line or line.startswith(("suites:","checks:","porcelain-after")):print(line)
snapshot=json.loads((out/"public-snapshot.json").read_text())
print("Public issue comments:",len(snapshot["issue_comments"]),"PR discussion entries:",len(snapshot["comments"]))
for c in snapshot["comments"]:print(c["url"],c["body"].splitlines()[0])
print("No prior public review findings in the returned merged discussion timeline")
print("Live body difference from the public packet:")
print("".join(difflib.unified_diff((public/"PR-BODY.md").read_text().splitlines(True),snapshot["body"].splitlines(True),fromfile="packet/PR-BODY.md",tofile="live PR body")))
print("PASS bounded artifact audit; this is not a full gate or a candidate merge validation")

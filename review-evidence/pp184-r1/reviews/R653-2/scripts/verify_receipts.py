#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys,subprocess
OUT=pathlib.Path(__file__).resolve().parents[1]
PUB=OUT/"receipts/public"; ROOT=PUB/"author-r2/r2-receipts"
manifest={x["file"]:x for x in json.loads((PUB/"MANIFEST.json").read_text())}
actual={str(p.relative_to(ROOT)):p for p in ROOT.rglob("*") if p.is_file() and p.name!="INDEX.md"}
rows=re.findall(r"^\| `([^`]+)` \| (\d+) \| `([a-f0-9]{64})` \| (.*) \|$",(ROOT/"INDEX.md").read_text(),re.M)
assert len(rows)==len(actual)==123
assert {x[0] for x in rows}==set(actual)
for name,size,digest,note in rows:
 data=actual[name].read_bytes()
 assert len(data)==int(size) and hashlib.sha256(data).hexdigest()==digest,name
for p in [ROOT/"INDEX.md",*actual.values()]:
 name=str(p.relative_to(PUB));assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest[name]["published_sha256"],name
print("PASS index: exact set of 123 files, all sizes/SHA256; all 124 public files match publication manifest")
heads={"head":"88cb206135c23eb86488ad110fe19cfca5f341cf","base":"5addf29759a22372ed6aa3e1d52a3aad29e3ecd7"}
for group in ["gates","campaigns"]:
 for p in sorted((ROOT/group).glob("*.rc")):
  rc=int(p.read_text()); assert rc==0,p
  log=p.with_suffix(".log").read_text()
  assert re.search(r"^## end .* rc 0$",log,re.M),p
  side=p.name.split("-")[0]
  if group=="gates" and not any(x in p.name for x in ["-area.","-guards."]):
   assert "## head "+heads[side] in log,p
  elif group=="gates" and "-area." in p.name:
   data=subprocess.check_output(["git","show",heads[side]+":hdl/srp/KL_srp_domain.sv"])
   assert hashlib.sha256(data).hexdigest() in log,p
 print("PASS",group,len(list((ROOT/group).glob("*.rc"))),"rc files agree with log footers (campaign exports have blank head fields)")
for side,n in [("base",1030013),("head",1030029)]:
 s=(ROOT/f"gates/{side}-suites.log").read_text()
 tallies=re.findall(r"^PASS (\S+) \((\d+) checks: (\d+) PASS, 0 FAIL\)$",s,re.M)
 assert len(tallies)==36 and sum(int(x[1]) for x in tallies)==n
 assert all(x[1]==x[2] for x in tallies)
 print("PASS",side,"36 suites; summed checks",n)
for p in sorted((ROOT/"probe").glob("*.rc")):
 rc=int(p.read_text());text=p.with_suffix(".log").read_text()
 assert (rc==1)==p.name.startswith("mut-"),p
 assert f"rc {rc}" in text,p
 print("PROBE",p.stem,"rc",rc,re.search(r"probe: .*",text).group())
print("PASS synthesis Domain stats present",(ROOT/"synthdom/base.stat").stat().st_size,(ROOT/"synthdom/head.stat").stat().st_size)

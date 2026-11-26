#!/usr/bin/env python3
"""Independently verify the published packet and serial/leg verdicts."""
import collections, hashlib, json, pathlib, re, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(sys.argv[2]).resolve()
a=packet/"author/receipts"
manifest=json.loads((packet/"MANIFEST.json").read_text())
checked=0
for entry in manifest:
 f=packet/entry["file"]
 if f.is_file():
  assert hashlib.sha256(f.read_bytes()).hexdigest()==entry["published_sha256"],entry["file"]
  checked+=1
print("Published manifest hashes verified:",checked)
def serial(path):
 lines=[]
 for line in path.read_text(encoding="utf-8-sig").splitlines():
  m=re.match(r"[\ufeff]?\d{4}-\d\d-\d\dT[\d:.]+Z (.*)$",line.split("\t",2)[-1])
  if m and not m[1].startswith("[endstation_builder] WARNING"): lines.append(m[1])
 return lines
def local(path):
 return [line.partition(" ")[2] for line in path.read_text().splitlines()]
def verdicts(lines):
 return collections.Counter(line+("\n"+lines[i+1] if i+1<len(lines) and lines[i+1].startswith("    first:") else "")
  for i,line in enumerate(lines) if re.match(r"\[(?:ok|ESCAPED|BAD)\] ",line))
for phase, pattern in (("control","control/leg?.log"),("aecp","aecp-srp/aecp-leg?.log"),("srp","aecp-srp/srp-leg?.log")):
 want=verdicts(serial(a/f"reference/45657606423-firmware-{phase}-mutants.log"))
 got=sum((verdicts(local(f)) for f in sorted((a/"local").glob(pattern))),collections.Counter())
 if phase=="srp":
  # The two dependency-pin controls run once in serial and in each of two legs.
  repeated=got-want
  assert sum(repeated.values())==2,(phase,repeated)
  assert all("pin" in x or "moved" in x or "edited" in x for x in repeated),repeated
  for x in repeated: assert got[x]==2 and want[x]==1
  got-=repeated
 assert want==got,(phase,want-got,got-want)
 assert not any(x.startswith(("[BAD]","[ESCAPED]")) for x in got)
 print(phase,"serial verdict multiset identical:",sum(want.values()))
s=serial(a/"reference/45657606423-publication-census.log")
start=next(i for i,x in enumerate(s) if x.startswith("publication census: elaborating"))
cut=next(i for i,x in enumerate(s) if x.startswith("publication census:") and "shape(s) elaborated" in x)
end=next(i for i,x in enumerate(s) if x.startswith("mutations:"))
l=local(a/"local/census/leg0.log")
l=l[next(i for i,x in enumerate(l) if x.startswith("publication census: elaborating")):]
mask=lambda x: re.sub(r"in \d+ s at --jobs \d+","in N s at --jobs J",x)
assert list(map(mask,s[start:cut+1]))==list(map(mask,l))
u=(a/"local/census/union.log").read_text().splitlines()
maskhex=lambda x: re.sub(r"\$0x[0-9a-f]+:","$0xADDR:",x)
w=[x for x in s[cut+1:end+1] if not x.startswith("selftest:")]
g=[x for x in u if not x.startswith("selftest:")]
assert list(map(maskhex,w))==list(map(maskhex,g))
print("Census check lines identical after duration normalization:",len(l))
print("Census arm/rule lines identical after heap-address normalization:",len(w))
print("Census typed leg JSON receipts in published packet:",len(list(a.rglob("census-leg-*.json"))))
for cmd in (["git","diff","--exit-code","09201d35","c34e7d8b","--","sw","hdl","configs","protocol-processor","gptp-processor","third_party"],
 ["git","diff","--exit-code","530149b5dd","HEAD","--","sw/mailbox","sw/firmware/ctrl"]):
 subprocess.run(cmd,cwd=root,check=True)
print("Serial input identity and later campaign/census source retention: PASS")

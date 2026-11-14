"""Verify the published evidence manifest and compare its image/step receipts. Argument: archive directory."""
import hashlib,json,re,sys
from pathlib import Path
root=Path(sys.argv[1])
items=json.loads((root/"MANIFEST.json").read_text())
bad=[]
for item in items:
 p=root/item["file"]
 if hashlib.sha256(p.read_bytes()).hexdigest()!=item["published_sha256"]:bad.append(item["file"])
print("Published manifest:",len(items),"files; mismatches:",bad)
images=root/"author-r3/receipts/images"
def records(name):
 out={}
 for line in (images/name).read_text().splitlines():
  m=re.fullmatch(r"([^:]+): rc (\d+) .*tiles ([\d.]+), .*ctrl_app.elf sha256 ([a-f0-9]{64}), loadable sha256 ([a-f0-9]{64})",line)
  if m:out[m[1]]=m.groups()[1:]
 return out
base=records("raw-base-184d47ca.txt")
keyed=records("raw-1-keying-only.txt")
measured=records("raw-2-8x8-1if-165-25.txt")
final=records("raw-4-fullpass-716a8ae7.txt")
assert len(base)==len(keyed)==len(measured)==len(final)==8
base902=records(root / "author-r2/receipts/images/raw-b-902-7398ec0a.txt")
assert len(base902)==8
for name in sorted(final):
 print(name,"keying identical:",base[name]==keyed[name],"final equals measured:",final[name]==measured[name],"final equals baseline:",final[name]==base[name],"tiles:",final[name][1])
 assert base[name]==keyed[name] and final[name]==measured[name]
 if not name.endswith("8x8-1if"):
  assert final[name]==base[name]==base902[name]
print("Six fixed images also equal base 7398ec0a recorded ELF/loadable hashes")
assert final["platform-8x8-1if"][1]=="56.0"
workflow=root/"author-r3/receipts/gates/workflows-verify-716a8ae7.md"
counts={}; missing_reason=[]
for line in workflow.read_text().splitlines():
 if line.startswith("| "):
  fields=[x.strip() for x in line.strip("|").split("|")]
  if len(fields)!=6 or fields[4] in ("rc",):continue
  counts[fields[4]]=counts.get(fields[4],0)+1
  if fields[4]=="NOT RUN" and not fields[5]:missing_reason.append(fields)
print("Local workflow-step receipt counts:",counts,"missing skip reasons:",missing_reason)
assert counts=={"0":139,"NOT RUN":226} and not missing_reason
assert not bad
print("RESULT PASS; image conclusions compare recorded hashes, not independently rebuilt images")

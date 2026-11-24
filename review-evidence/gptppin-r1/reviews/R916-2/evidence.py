#!/usr/bin/env python3
"""Verify the published packet and extract only the requested public receipts."""
import hashlib,json,pathlib,subprocess,sys,re
repo=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]).resolve()
rev="2fcbd46885448a4b4b80e6f39f8a8320667ae84a"; prefix="review-evidence/gptppin-r1/"
def git(*args): return subprocess.check_output(["git","--no-replace-objects","-C",str(repo),*args])
def blob(p): return git("show",rev+":"+prefix+p)
manifest=json.loads(blob("MANIFEST.json")); bad=[]
for row in manifest:
 actual=hashlib.sha256(blob(row["file"])).hexdigest()
 if actual!=row["published_sha256"]: bad.append(row["file"])
print("Published manifest:",len(manifest),"files; mismatches:",bad)
assert not bad
commit=git("cat-file","commit",rev)
print("Packet commit has embedded cryptographic signature:",b"\ngpgsig " in commit)
for row in manifest:
 name=row["file"]
 if name.startswith("author-r2/receipts/") and "/tools/" not in name:
  dest=out/"published"/name; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(blob(name))
 for wanted in ("author/receipts/ledger/", "author/receipts/route/"):
  if name.startswith(wanted):
   dest=out/"published"/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(blob(name))
rows=blob("author-r2/receipts/ledger/image-hashes-vs-round1.txt").decode().splitlines()
n=0
for row in rows:
 if "    ==    " in row:
  left,right=row.split("    ==    "); assert left==right;n+=1
assert n==24
print("Firmware image comparison: 24/24 SHA-256 and path pairs equal")
def digests(name):
 return {m[1]:m[0] for m in re.findall(r"^([0-9a-f]{64})  (\./[^\n]+)$",blob(name).decode(),re.M)}
old_images=digests("author/receipts/ledger/plat-ledger-39e9c9d2.txt")
new_images=digests("author-r2/receipts/ledger/plat-ledger-f97e49fe.txt")
assert len(old_images)==24 and old_images==new_images
print("Independent extraction from both raw ledger receipts: 24 identical image digests")
for p in ("docs/diagrams/submodule_boundaries.png","docs/diagrams/timesync_chain.png"):
 old=git("show","bbfdb674:"+p); new=git("show","HEAD:"+p)
 assert old==new
 print("Unchanged diagram",p,hashlib.sha256(new).hexdigest())
assert git("rev-parse","bbfdb674^{tree}")==git("rev-parse","3a8bdbf063^{tree}")
print("Train merge is tree-identical to prior reviewed head")
print("Changes from d616b1c6 to reviewed head:")
print(git("diff","--name-only","d616b1c6","HEAD").decode())
print("Consumer receipts (tail excerpts; interrupted windows are not passes):")
for p in sorted((out/"published/author-r2/receipts/rtl").iterdir()):
 if any(k in p.name for k in ("gptp_plane","gptp_tables","gptp_txts","gptp_shadow-mutants-slice","milan_dp-gptp","SUMMARY")):
  print("\n"+p.name)
  lines=p.read_text().splitlines()
  print("\n".join(lines[-8:]))

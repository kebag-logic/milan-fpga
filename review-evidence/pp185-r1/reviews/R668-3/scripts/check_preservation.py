#!/usr/bin/env python3
"""Compare historical public receipts, accounting explicitly for publication redaction."""
import concurrent.futures,difflib,hashlib,json,pathlib,urllib.request
P=pathlib.Path(__file__).resolve().parents[1];PUB=P/"scratch/public"
M={r["file"]:r for r in json.loads((P/"receipts/public-manifest.json").read_text())}
base="https://raw.githubusercontent.com/kebag-logic/milan-fpga/c6574c479b48fadc7c33f0fb12df36ee77c44423/review-evidence/pp185-r1/"
pairs=[(f,f.replace("author-r2/","author-r3/",1)) for f in M if f.startswith("author-r2/receipts/") and not f.endswith("/INDEX.md")]
def fetch(pair):
 a,b=pair
 if M[a]["published_sha256"]==M[b]["published_sha256"]:return
 dest=PUB/a
 if not dest.exists():
  with urllib.request.urlopen(base+a,timeout=60) as r:data=r.read()
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 assert hashlib.sha256(dest.read_bytes()).hexdigest()==M[a]["published_sha256"]
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:list(pool.map(fetch,pairs))
def norm(s):
 for a,b in [("<data>/lanes","$LANES"),("<data>/tmp","$VALIDATION_STORAGE"),("<home>/milan-fpga-management","$MANAGEMENT"),("<home>","$WORKSPACE_HOME")]:s=s.replace(a,b)
 return s
changed=[];unresolved=[]
for a,b in pairs:
 if M[a]["published_sha256"]==M[b]["published_sha256"]:continue
 old=(PUB/a).read_text();new=(PUB/b).read_text()
 item={"old":a,"new":b,"old_sha256":M[a]["published_sha256"],"new_sha256":M[b]["published_sha256"],"redaction_only":norm(old)==norm(new)}
 changed.append(item)
 if not item["redaction_only"]:
  unresolved.append(a)
  print(a)
  print("".join(difflib.unified_diff(norm(old).splitlines(True),norm(new).splitlines(True)))[:800])
(P/"receipts/publication-preservation.json").write_text(json.dumps({"total":len(pairs),"byte_identical":len(pairs)-len(changed),"redaction_changes":changed,"unresolved":unresolved},indent=2)+"\n")
print(f"{len(pairs)} prior files: {len(pairs)-len(changed)} byte-identical, {len(changed)-len(unresolved)} redaction-only, {len(unresolved)} unresolved")

assert not unresolved

#!/usr/bin/env python3
"""Fetch the immutable public evidence packet; verify published byte hashes."""
import concurrent.futures,hashlib,json,pathlib,urllib.request,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
COMMIT="c6574c479b48fadc7c33f0fb12df36ee77c44423"
BASE=f"https://raw.githubusercontent.com/kebag-logic/milan-fpga/{COMMIT}/review-evidence/pp185-r1/"
def get(path):
 for attempt in range(4):
  try:
   with urllib.request.urlopen(BASE+path,timeout=60) as r:return r.read()
  except Exception:
   if attempt==3:raise
   time.sleep(1)
manifest=get("MANIFEST.json")
(ROOT/"receipts/public-manifest.json").write_bytes(manifest)
rows=[x for x in json.loads(manifest) if x["file"].startswith("author-r3/") or x["file"] in ("reviews/R668-2/audit_evidence.py","reviews/R668-2/evidence-audit.json","reviews/R668-2/verify_checkout.py")]
def fetch(row):
 path=row["file"];dest=ROOT/"scratch/public"/path
 if dest.exists():data=dest.read_bytes()
 else:
  data=get(path);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 actual=hashlib.sha256(data).hexdigest()
 assert actual==row["published_sha256"],path
 return {"file":path,"sha256":actual,"bytes":len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
 result=list(pool.map(fetch,rows))
(ROOT/"receipts/fetched-hashes.json").write_text(json.dumps({"commit":COMMIT,"verified":len(result),"files":result},indent=2)+"\n")
print(f"PASS: {len(result)} public files verified against published_sha256 at {COMMIT}")

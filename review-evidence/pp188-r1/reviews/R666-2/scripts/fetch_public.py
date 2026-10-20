import concurrent.futures, hashlib, json, urllib.request
from pathlib import Path
P=Path(__file__).resolve().parents[1]
BASE="https://raw.githubusercontent.com/kebag-logic/milan-fpga/61e4bb57da96c2c2e4d60987f390a435384ffe9f/review-evidence/pp188-r1/"
manifest=json.loads((P/"receipts/public-MANIFEST.json").read_text())
def select(x):
 f=x["file"]
 return f.startswith("author-r2/receipts/round2/") and "/superseded/" not in f or f in ("author-r2/receipts/INDEX.md", "author-r2/receipts/EXTERNAL-RECORDS.csv")
def fetch(x):
 f=x["file"]; data=urllib.request.urlopen(BASE+f,timeout=120).read(); digest=hashlib.sha256(data).hexdigest()
 assert digest==x["published_sha256"],f
 out=P/"receipts/public"/f;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 return {"file":f,"sha256":digest,"verified":True,"path_redacted":x["path_redacted"]}
with concurrent.futures.ThreadPoolExecutor(12) as pool:
 results=list(pool.map(fetch,filter(select,manifest)))
(P/"receipts/public-verification.json").write_text(json.dumps(results,indent=2)+"\n")
print(f"Verified {len(results)} published receipts against the fixed-commit manifest.")

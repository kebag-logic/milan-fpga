import base64, concurrent.futures, hashlib, json, subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
repo="repos/kebag-logic/milan-fpga"
ref="e637950b796e5a01bdbd37c6e5bd663ccd867ec4"
prefix="review-evidence/423-r1/candidate1/"
def api(endpoint):
 r=subprocess.run(["rtk","proxy","gh","api",endpoint],capture_output=True,check=True); return json.loads(r.stdout)
tree=api(f"{repo}/git/trees/{ref}?recursive=1")
(root/"evidence-tree.json").write_text(json.dumps(tree))
selected=[x for x in tree["tree"] if x["type"]=="blob" and x["path"].startswith(prefix) and (x["path"].endswith(".json") or any(s in x["path"] for s in ("manager-builder/", "whitespace-correction/", "full-native/")))]
def fetch(x):
 raw=base64.b64decode(api(f"{repo}/git/blobs/{x['sha']}")["content"])
 oid=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest();assert oid==x["sha"]
 dest=root/"public-candidate1"/x["path"][len(prefix):];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 return dict(path=str(dest.relative_to(root)),git_blob=oid,sha256=hashlib.sha256(raw).hexdigest(),size=len(raw))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: receipts=list(pool.map(fetch,selected))
(root/"downloaded-evidence.json").write_text(json.dumps(receipts,indent=2)+"\n")
print(f"Downloaded {len(receipts)} public manager files, Git blob hashes verified")

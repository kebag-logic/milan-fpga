import base64,concurrent.futures,hashlib,json,subprocess,sys
from pathlib import Path
out=Path(sys.argv[1]);rev="3811227ee1af4ed96493528f1af17e852e2b7176";prefix="review-evidence/478-r1/"
def api(path): return json.loads(subprocess.check_output(["rtk","proxy","gh","api","repos/kebag-logic/milan-fpga/"+path]))
tree=api("git/trees/"+rev+"?recursive=1");assert not tree.get("truncated")
selected=[]
for e in tree["tree"]:
 path=e["path"]
 if e["type"]!="blob": continue
 manager=path.startswith(prefix+"round2/manager/")
 if manager and ("/full-suite-logs/" in path or "/yosys-results/" in path):
  manager=path.endswith("/pp_shadow.log")
 if manager or path in [prefix+"MANIFEST.json",prefix+"author/after-rates.json",prefix+"author/baseline-rates.json"]: selected.append(e)
def get(e):
 obj=api("git/blobs/"+e["sha"]);data=base64.b64decode(obj["content"])
 assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==e["sha"]
 dst=out/e["path"][len(prefix):];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
 return dict(path=e["path"],blob=e["sha"],size=len(data),sha256=hashlib.sha256(data).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: receipts=list(pool.map(get,selected))
(out/"download-verification.json").write_text(json.dumps(dict(revision=rev,files=receipts),indent=2))
print("Verified Git blobs:",len(receipts));print((out/"MANIFEST.json").read_text()[:2400])

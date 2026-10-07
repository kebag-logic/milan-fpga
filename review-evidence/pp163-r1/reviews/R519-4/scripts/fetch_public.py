#!/usr/bin/env python3
"""Fetch only allowlisted public evidence blobs; verify each Git blob identity."""
import argparse, base64, concurrent.futures, hashlib, json, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("packet",type=Path);args=ap.parse_args()
ref="90f80ddaad5c7dda290d01f3b7153b1de7879b5f"
repo="kebag-logic/milan-fpga"
def api(path):
    return json.loads(subprocess.check_output(["gh","api",f"repos/{repo}/{path}"],text=True))
tree=api(f"git/trees/{ref}?recursive=1")
assert not tree.get("truncated")
prefix="review-evidence/pp163-r1/"
files=[x for x in tree["tree"] if x["type"]=="blob" and
       (x["path"].startswith(prefix+"author-r3/evidence/") or
        x["path"].startswith(prefix+"author-r3/measurement-m3final/") or
        x["path"]==prefix+"MANIFEST.json")]
def fetch(x):
    data=base64.b64decode(api("git/blobs/"+x["sha"])["content"])
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==x["sha"]
    dest=args.packet/"receipts"/"public"/x["path"][len(prefix):]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    return dict(path=x["path"],blob=x["sha"],bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    receipts=list(ex.map(fetch,files))
(args.packet/"receipts"/"public-fetch.json").write_text(json.dumps(dict(repository=repo,revision=ref,files=receipts),indent=2)+"\n")
print(f"Verified {len(receipts)} public evidence blobs at {ref}")

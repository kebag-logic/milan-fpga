#!/usr/bin/env python3
"""Download only immutable public source/native evidence; verify Git blob IDs."""
import argparse, concurrent.futures, hashlib, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("packet",type=Path); a=p.parse_args()
tree=json.loads((a.packet/"raw/evidence-tree.stdout").read_bytes())
prefix="review-evidence/423-r1/"
selected=[]
for e in tree["tree"]:
    name=e["path"].removeprefix(prefix)
    if not e["path"].startswith(prefix) or e["type"]!="blob": continue
    take=name.startswith("corrected-source3/manager/") or name.startswith("reviews/R251-2/scripts/") or name in ("reviews/R251-2/REPORT.md","reviews/R251-2/REPRODUCE.md")
    take=take or name.startswith("reviews/R251-2/raw/") and not name.endswith(("evidence-tree.json","pr519.json","issue423.json"))
    take=take or name=="locale-manager/receipts/locale_transport_probe.txt"
    if name=="reviews/R251-1/receipts/locale_transport_probe.sh":
        name="original-locale-probe.sh"; take=True
    if take: selected.append((name,e))
def one(pair):
    name,e=pair
    dst=a.packet/"public"/name; dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): data=dst.read_bytes()
    else:
        r=subprocess.run(["gh","api","-H","Accept: application/vnd.github.raw+json","repos/kebag-logic/milan-fpga/git/blobs/"+e["sha"]],capture_output=True,check=True)
        data=r.stdout
        if data.startswith(b'{'):
            try:
                import base64
                j=json.loads(data)
                if j.get("encoding")=="base64": data=base64.b64decode(j["content"])
            except (ValueError,KeyError): pass
        dst.write_bytes(data)
    actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    assert actual==e["sha"], (name,actual,e["sha"])
    return {"path":name,"source_path":e["path"],"git_blob":actual,"sha256":hashlib.sha256(data).hexdigest(),"size":len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(one,selected))
(a.packet/"raw/evidence-verification.json").write_text(json.dumps({"commit":"2738c16fa8f75bbd9193105f1cb633729d2d736d","files":results},indent=2)+"\n")
print("Verified",len(results),"immutable public blobs")

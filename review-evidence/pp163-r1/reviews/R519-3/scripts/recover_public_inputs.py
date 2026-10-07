#!/usr/bin/env python3
"""Recover immutable public source inputs only; all disposable files stay in scratch."""
import argparse,base64,concurrent.futures,hashlib,json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
BASE="28f9666feab2b2ba287643c63ed3a16b1e0bb863"
PUBLIC="kebag-logic/milan-fpga"
cache=P/"scratch/public-inputs"
def api(route):
    r=subprocess.run(["gh","api",route],capture_output=True,text=True,check=True)
    return json.loads(r.stdout)
def blob(repo,item):
    b=base64.b64decode(api(f"repos/{repo}/git/blobs/{item['sha']}")["content"])
    assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==item["sha"]
    return b
def main():
    tree=api(f"repos/{PUBLIC}/git/trees/{BASE}?recursive=1")
    assert not tree.get("truncated")
    index={x["path"]:x for x in tree["tree"]}
    modules=blob(PUBLIC,index[".gitmodules"]).decode()
    repos={}
    for section in modules.split("[submodule ")[1:]:
        path=re.search(r"path = (.+)",section).group(1)
        url=re.search(r"url = (.+)",section).group(1)
        repos[path]=url.removeprefix("https://github.com/").removesuffix(".git")
    subindexes={}
    pins={}
    for sub in ("gptp-processor","third_party/verilog-axis","protocol-processor"):
        pins[sub]=index[sub]["sha"]
        if sub!="protocol-processor":
            t=api(f"repos/{repos[sub]}/git/trees/{pins[sub]}?recursive=1")
            assert not t.get("truncated")
            subindexes[sub]={x["path"]:x for x in t["tree"]}
    script=(P/"receipts/public-measurement/measurement-m3final/ooc-m3final/baseline_ooc.tcl").read_text()
    prefix="$VALIDATION_STORAGE/pp163-a553/parent/"
    reads=re.findall(r"^(?:read_verilog(?: -v)?|read_xdc|source) \{?([^{}\s]+)\}?[ \t]*$",script,re.M)
    requested=[x[len(prefix):] for x in reads if x.startswith(prefix) and not x.startswith(prefix+"protocol-processor/")]
    dirs=re.search(r" -include_dirs \{([^}]*)\}",script).group(1).split()
    for directory in dirs:
        rel=directory.removeprefix(prefix)
        requested.extend(x for x in index if str(Path(x).parent)==rel and Path(x).suffix in (".vh",".svh"))
    requested += ["docs/integration/BUILDING.md","AGENTS.md","CONTRIBUTING.md","scripts/ci_rv32_sdk.py","syn/ooc/pp_resource_gate.py"]
    def fetch(rel):
        repo=PUBLIC; idx=index; key=rel
        for sub in subindexes:
            if rel.startswith(sub+"/"):
                repo=repos[sub];idx=subindexes[sub];key=rel[len(sub)+1:];break
        item=idx.get(key)
        if not item or item["type"]!="blob":return {"path":rel,"status":"absent from public pinned tree"}
        data=blob(repo,item); out=cache/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
        return {"path":rel,"status":"fetched","repository":repo,"blob":item["sha"],"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
    with concurrent.futures.ThreadPoolExecutor(8) as pool: results=list(pool.map(fetch,sorted(set(requested))))
    result={"parent":BASE,"submodule_gitlinks":pins,"gitmodules":modules,"files":results}
    (P/"receipts/public-input-recovery.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"fetched":sum(x["status"]=="fetched" for x in results),"unavailable":[x for x in results if x["status"]!="fetched"],"submodule_gitlinks":pins},indent=2))
if __name__=="__main__":main()

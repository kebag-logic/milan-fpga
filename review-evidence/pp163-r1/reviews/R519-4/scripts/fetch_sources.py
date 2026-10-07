#!/usr/bin/env python3
"""Fetch only measurement sources from their recorded public revisions."""
import argparse,base64,concurrent.futures,hashlib,json,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("packet",type=Path);args=ap.parse_args()
p=args.packet; parent="28f9666feab2b2ba287643c63ed3a16b1e0bb863"
repos={"parent":("kebag-logic/milan-fpga",parent),"gptp-processor":("Mister-M-alt/FPGA-gPTP","5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d"),"third_party/verilog-axis":("alexforencich/verilog-axis","48ff7a7e2ef782cf778d47910cf85835c64b1bce")}
def api(repo,path):return json.loads(subprocess.check_output(["gh","api",f"repos/{repo}/{path}"],text=True))
trees={}
for key,(repo,ref) in repos.items():
    t=api(repo,f"git/trees/{ref}?recursive=1");assert not t.get("truncated");trees[key]={x["path"]:x for x in t["tree"]}
for key in ["gptp-processor","third_party/verilog-axis"]:assert trees["parent"][key]["sha"]==repos[key][1]
rows=json.loads((p/"receipts/public/author-r3/measurement-m3final/inputs-digest/inputs-components.json").read_text())["files"]
paths=[r["path"].removeprefix("$ROOT1/") for r in rows if r["path"].startswith("$ROOT1/") and not r["path"].startswith("$ROOT1/protocol-processor/")]
paths += ["syn/ooc/pp_resource_gate.py","syn/ooc/pp_baseline_rank.py","syn/ooc/pp_baseline.py",".gitmodules"]
def fetch(path):
    key=next((x for x in repos if x!="parent" and path.startswith(x+"/")),"parent")
    rel=path if key=="parent" else path[len(key)+1:];x=trees[key][rel];repo,ref=repos[key]
    data=base64.b64decode(api(repo,"git/blobs/"+x["sha"])["content"])
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==x["sha"]
    dest=p/"scratch"/"parent-sources"/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    return dict(path=path,repository=repo,revision=ref,git_blob=x["sha"],sha256=hashlib.sha256(data).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: receipts=list(ex.map(fetch,paths))
# Independently enumerate all include headers, not only components advertised in the manifest.
include_dirs=["configs/generated/endstation_ax7101_1x1_tdm8","configs/generated/endstation_ax7101_1x1_tdm8/gen","hdl/common","hdl/ieee8021q/ts","hdl/ieee8021as/ptp_timestamp","hdl/ieee17221/adp","hdl/common/csr","hdl/common/eth_event_counter","hdl/ieee1722/avtp"]
headers=[]
for directory in include_dirs:
    (p/"scratch/parent-sources"/directory).mkdir(parents=True,exist_ok=True)
    headers.extend(sorted(x for x in trees["parent"] if str(Path(x).parent)==directory and Path(x).suffix in (".svh",".vh")))
expected=[r["path"].removeprefix("$ROOT1/") for r in rows if r["order"]>=122]
assert headers==expected,(headers,expected)
result=dict(repositories=repos,verified_gitlinks={key:trees["parent"][key]["sha"] for key in ["protocol-processor","gptp-processor","third_party/verilog-axis"]},measurement_processor_override="c4539ff107a6a4c7d2e4a4844182b00a2bf33c82",include_headers=headers,files=receipts)
(p/"receipts/source-fetch.json").write_text(json.dumps(result,indent=2)+"\n")
print(f"Verified {len(receipts)} source/authority blobs, required dependency gitlinks, and exact include header inventory")

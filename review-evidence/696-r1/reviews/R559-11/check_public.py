#!/usr/bin/env python3
import hashlib,json,subprocess,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True);a=p.parse_args()
packet=Path(__file__).resolve().parent;public=packet/"scratch/public"
manifest={}
for line in (public/"MANIFEST-01.sha256").read_text().splitlines():
    sha,path=line.split("  ",1);manifest[path]=sha
verified=[]
for row in json.loads((packet/"public-receipts.json").read_text()):
    name=row["file"]
    if name=="MANIFEST-01.sha256":continue
    assert hashlib.sha256((public/name).read_bytes()).hexdigest()==manifest[name],name
    verified.append(name)
inputs=[];not_local=[]
for shape in json.loads((public/"source-inputs.json").read_text()):
    for f in shape["files"]:
        prefix="$WORK/candidate/"
        if f["path"].startswith(prefix):
            path=a.root/f["path"][len(prefix):]
            if path.is_file():
                data=path.read_bytes()
                assert len(data)==f["bytes"] and hashlib.sha256(data).hexdigest()==f["sha256"],f
                inputs.append(f["path"])
            else:not_local.append(f["path"])
        else:not_local.append(f["path"])
measure=json.loads((public/"measurement-records.json").read_text())
baseline=json.loads((a.root/"syn/ooc/pp_resource_baseline.json").read_text())
print(json.dumps({"manifest_verified_files":verified,"input_checks":len(inputs),"unique_source_inputs":len(set(inputs)),"unverified_generated_inputs":not_local,"resource_figures":{k:v["figures"]for k,v in measure.items()}},indent=2))

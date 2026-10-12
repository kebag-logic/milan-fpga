#!/usr/bin/env python3
import concurrent.futures,json,os,pathlib,subprocess,sys
out=pathlib.Path(sys.argv[1]).resolve();py=sys.argv[2]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",PYTHONHASHSEED="0",TMPDIR=str(out/"scratch"),PYTHONPATH=str(out/"scratch/cpu"),MAKEFLAGS="-j16")
items=[(tag,rev,shape) for tag,rev in [("base","c6bd08c6f52632c6d33d834ce842ac3cf63f29cc"),("head","8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d")] for shape in ["1x1_tdm8","8x8"]]
def run(item):
 tag,rev,shape=item;name=f"export-{tag}-{shape}"
 argv=[py,str(out/"export_probe.py"),rev,f"configs/endstation_ax7101_{shape}.yaml",str(out/"scratch"/name)]
 with (out/"scratch"/(name+".raw.log")).open("w") as log:rc=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (out/(name+".rc")).write_text(str(rc)+"\n")
 print(name,rc,flush=True);return {"name":name,"rc":rc,"argv":argv}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,items))
(out/"exports.json").write_text(json.dumps(rows,indent=2)+"\n")
sys.exit(int(any(r["rc"] for r in rows)))

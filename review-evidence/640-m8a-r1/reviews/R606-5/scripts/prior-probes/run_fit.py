#!/usr/bin/env python3
"""Relink the four current fixture shapes concurrently and preserve plan receipts."""
import concurrent.futures,json,os,pathlib,subprocess,sys
out=pathlib.Path(sys.argv[1]).resolve();py=sys.argv[2];prefix=sys.argv[3] if len(sys.argv)>3 else ""
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(out/"scratch"),MAKEFLAGS="-j16")
def run(item):
 shape,interfaces=item;tag=f"{prefix}fit-{shape}-if{interfaces}";dest=out/"scratch"/tag
 argv=[py,"sw/firmware/ctrl/test/ctrl_srp_image.py","--config",f"configs/endstation_ax7101_{shape}.yaml","--interfaces",str(interfaces),"--with-aecp","--layout","split","--output",str(dest),"--libc",str(out/"scratch/runtime/libc.a"),"--compiler-runtime",str(out/"scratch/runtime/libcompiler_rt.a")]
 with (out/"scratch"/(tag+".raw.log")).open("w") as log:rc=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,env=env).returncode
 (out/(tag+".rc")).write_text(str(rc)+"\n")
 if (dest/"size.json").exists():(out/(tag+".json")).write_bytes((dest/"size.json").read_bytes())
 print(tag,rc,flush=True);return {"name":tag,"rc":rc,"argv":argv}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,[(s,i) for s in ["1x1_tdm8","8x8"] for i in [1,2]]))
(out/(prefix+"fit-runs.json")).write_text(json.dumps(rows,indent=2)+"\n")
sys.exit(int(any(r["rc"] for r in rows)))

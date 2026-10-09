import concurrent.futures, json, os, subprocess, time
from pathlib import Path
root=Path.cwd()
out=Path(os.environ["F5_SCRATCH"])
def run_case(case):
 shape, interfaces=case
 name=f"base-final-{shape}-if{interfaces}"
 dest=out/name
 argv=["python3","sw/firmware/ctrl/test/ctrl_srp_image.py","--config",f"configs/endstation_ax7101_{shape}.yaml","--interfaces",str(interfaces),"--output",str(dest),"--libc",str(out/"runtime-freestanding/libc.a"),"--compiler-runtime",str(out/"runtime-freestanding/libcompiler_rt.a")]
 start=time.monotonic()
 with (out/f"{name}.log").open("w") as log:
  result=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,timeout=580)
 receipt={"argv":argv,"rc":result.returncode,"seconds":round(time.monotonic()-start,2)}
 (out/f"{name}-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(name,receipt["rc"],receipt["seconds"],flush=True)
 if result.returncode==0:
  data=json.loads((dest/"size.json").read_text())
  print(json.dumps({k:data[k] for k in ("shape","interfaces","sections","static_storage","ram_span")}),flush=True)
 return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 codes=list(pool.map(run_case,[(s,i) for s in ("1x1_tdm8","8x8") for i in (1,2)]))
raise SystemExit(max(codes))

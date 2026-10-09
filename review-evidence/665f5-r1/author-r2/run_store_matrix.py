import concurrent.futures, json, os, subprocess, time
from pathlib import Path
out=Path(os.environ["F5_SCRATCH"])
def run_case(case):
 shape, interfaces=case
 name=f"store-{shape}-if{interfaces}"
 argv=["python3",str(out/"measure_store.py"),"--root",".","--output",str(out/name),"--runtime",str(out/"runtime-freestanding"),"--shape",f"endstation_ax7101_{shape}","--interfaces",str(interfaces)]
 start=time.monotonic()
 with (out/f"{name}.log").open("w") as log:
  result=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,timeout=580)
 receipt={"argv":argv,"rc":result.returncode,"seconds":round(time.monotonic()-start,2)}
 (out/f"{name}-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(name,receipt["rc"],receipt["seconds"],flush=True)
 if result.returncode==0:
  data=json.loads((out/name/"size.json").read_text())
  print(json.dumps({k:data[k] for k in ("shape","interfaces","sections","static_storage","ram_span")}),flush=True)
 return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 codes=list(pool.map(run_case,[(s,i) for s in ("1x1_tdm8","8x8") for i in (1,2)]))
raise SystemExit(max(codes))

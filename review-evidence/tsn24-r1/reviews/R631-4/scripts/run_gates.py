#!/usr/bin/env python3
import argparse, concurrent.futures, json, os, pathlib, subprocess, time
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,required=True);p.add_argument("--packet",type=pathlib.Path,required=True);a=p.parse_args()
r=a.packet; s=r/"scratch"; env=dict(os.environ);env["TMPDIR"]=str(s/"temp");(s/"temp").mkdir(exist_ok=True)
commands=[("validate",["python3",str(a.source/"scripts/validate.py"),"--work",str(s/"validation"),"--jobs","3"],a.source),
("rv32-head",["python3",str(a.source/"scripts/baremetal.py"),"--work",str(s/"rv32-head"),"--jobs","2"],a.source),
("rv32-base",["python3",str(s/"base/scripts/baremetal.py"),"--work",str(s/"rv32-base"),"--jobs","2"],s/"base")]
def run(item):
 n,c,d=item;t=time.monotonic()
 with (r/"receipts"/(n+".log")).open("w") as f:
  result=subprocess.run(c,cwd=d,env=env,stdout=f,stderr=subprocess.STDOUT)
 (r/"receipts"/(n+".rc")).write_text(str(result.returncode)+"\n")
 out={"name":n,"argv":c,"rc":result.returncode,"seconds":round(time.monotonic()-t,2)}
 print(json.dumps(out),flush=True);return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: results=list(ex.map(run,commands))
(r/"receipts/gate-runs.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(x["rc"] for x in results))

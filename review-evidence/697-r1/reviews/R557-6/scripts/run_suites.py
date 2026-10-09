#!/usr/bin/env python3
import concurrent.futures,json,pathlib,subprocess,sys,time
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
work=packet/"scratch/suites"; work.mkdir(parents=True,exist_ok=True)
commands={"linux":[sys.executable,"scripts/validate.py","--work",str(work/"linux"),"--jobs","16"],"rv32":[sys.executable,"scripts/baremetal.py","--work",str(work/"rv32"),"--jobs","16"]}
def run(item):
 name,argv=item; start=time.monotonic()
 with (work/(name+".log")).open("w") as log: result=subprocess.run(argv,cwd=root,stdout=log,stderr=subprocess.STDOUT)
 (work/(name+".rc")).write_text(str(result.returncode)+"\n")
 row={"suite":name,"rc":result.returncode,"seconds":round(time.monotonic()-start,2)}; print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(run,commands.items()))
(packet/"receipts/suites.json").write_text(json.dumps(rows,indent=2)+"\n")

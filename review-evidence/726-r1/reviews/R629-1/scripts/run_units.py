#!/usr/bin/env python3
"""Replay only focused unit recipes, with all objects outside the checkout."""
import argparse,concurrent.futures,json,os,shlex,subprocess,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);ap.add_argument("packet",type=Path);ap.add_argument("--verilator",required=True);a=ap.parse_args()
root=a.root.resolve();packet=a.packet.resolve();env=dict(os.environ,TMPDIR=str(packet/"scratch"),PYTHONDONTWRITEBYTECODE="1")
jobs=[("tkdiag","build",None),("crf_rx","unit",None),("avtp_rxmon","run","nx"),("avtp_rxmon","lockstep-build","lockstep")]
def job(item):
    suite,target,filter_=item;name=suite+("-"+filter_ if filter_ else "");cwd=root/"tb/verilator"/suite
    dry=subprocess.check_output(["make","-j16","-n",target,"VERILATOR="+a.verilator],cwd=cwd,text=True,env=env)
    lines=dry.replace("\\\n"," ").splitlines();commands=[]
    for line in lines:
        if not line.startswith(a.verilator+" "):continue
        if filter_=="nx" and "sim_main_nx.cpp" not in line:continue
        if filter_=="lockstep" and "sim_lockstep.cpp" not in line:continue
        argv=shlex.split(line);md=packet/"scratch"/name/str(len(commands));md.mkdir(parents=True,exist_ok=True)
        if "--Mdir" in argv:
            i=argv.index("--Mdir");del argv[i:i+2]
        argv[argv.index("-j")+1]="2"
        argv += ["--Mdir",str(md)]
        argv=[str((cwd/x).resolve()) if x.endswith((".cpp",".sv",".v")) else x for x in argv]
        commands.append((argv,md/argv[argv.index("-o")+1]))
    rc=0
    with (packet/"receipts"/(name+".log")).open("w") as log:
        for cmd,exe in commands:
            r=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
            if r.returncode:rc=r.returncode;break
            r=subprocess.run([str(exe)],cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
            if r.returncode:rc=r.returncode;break
    (packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
    print(name,"rc",rc,flush=True);return {"suite":name,"rc":rc,"recipes":len(commands)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(job,jobs))
(packet/"receipts/units-results.json").write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(r["rc"] for r in results))

#!/usr/bin/env python3
"""Run selected review tasks in the foreground with bounded concurrency."""
import argparse, concurrent.futures, json, os, pathlib, subprocess, time
ap=argparse.ArgumentParser(); ap.add_argument("root",type=pathlib.Path); ap.add_argument("packet",type=pathlib.Path); ap.add_argument("plan",type=pathlib.Path); ap.add_argument("--jobs",type=int,default=2); args=ap.parse_args()
env=dict(os.environ, TMPDIR=str(args.packet/"scratch"), PYTHONDONTWRITEBYTECODE="1")
def run(task):
    name=task["name"]; start=time.monotonic(); use=dict(env,**task.get("env",{}))
    command=[s.replace("{root}",str(args.root)).replace("{packet}",str(args.packet)) for s in task["cmd"]]
    with (args.packet/"receipts"/(name+".log")).open("w") as out:
        out.write("COMMAND: "+json.dumps(task["cmd"])+"\n"); out.flush()
        rc=subprocess.run(command,cwd=args.root/task.get("cwd",""),env=use,stdout=out,stderr=subprocess.STDOUT).returncode
    record={"name":name,"rc":rc,"seconds":round(time.monotonic()-start,3)}
    (args.packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
    print(json.dumps(record),flush=True)
    return record
with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    results=list(pool.map(run,json.loads(args.plan.read_text())))
(args.packet/"receipts"/(args.plan.stem+"-results.json")).write_text(json.dumps(results,indent=2)+"\n")
raise SystemExit(any(x["rc"] for x in results))

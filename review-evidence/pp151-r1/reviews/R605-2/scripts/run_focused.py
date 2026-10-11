#!/usr/bin/env python3
"""Run independent focused campaigns concurrently, with foreground children and receipts."""
import argparse, concurrent.futures, json, os, subprocess, time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);ap.add_argument("packet",type=Path);ap.add_argument("--verilator",required=True);a=ap.parse_args()
r=a.root.resolve();p=a.packet.resolve();env=dict(os.environ,TMPDIR=str(p/"scratch"),PYTHONDONTWRITEBYTECODE="1",VERILATOR=a.verilator)
units=[("guards-lint",["python3","-B","tb/elab_guards/guards.py","--frontend","verilator","--verilator",a.verilator,"--jobs","4"]),
("mutants-lint",["python3","-B","tb/elab_guards/mutants.py","--frontend","verilator","--verilator",a.verilator,"--jobs","8","--output",str(p/"receipts/mutants-lint")]),
("guards-yosys013",["python3","-B","tb/elab_guards/guards.py","--frontend","yosys","--jobs","4"])]
def run(unit):
 name,cmd=unit;start=time.monotonic();print("START "+name,flush=True)
 (p/f"receipts/{name}.command.json").write_text(json.dumps({"argv":cmd,"cwd":str(r),"TMPDIR":env["TMPDIR"]},indent=2)+"\n")
 with (p/f"receipts/{name}.log").open("w") as log:
  result=subprocess.run(cmd,cwd=r,env=env,stdout=log,stderr=subprocess.STDOUT)
 (p/f"receipts/{name}.rc").write_text(str(result.returncode)+"\n")
 (p/f"receipts/{name}.seconds").write_text(f"{time.monotonic()-start:.3f}\n")
 print("DONE "+name+" rc="+str(result.returncode),flush=True);return result.returncode
with concurrent.futures.ThreadPoolExecutor(3) as pool:rcs=list(pool.map(run,units))
raise SystemExit(any(rcs))

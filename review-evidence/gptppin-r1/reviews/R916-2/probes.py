#!/usr/bin/env python3
"""Replay the previous round’s two exact faults in verified disposable inputs."""
import argparse, concurrent.futures, os, pathlib, subprocess, sys
p=argparse.ArgumentParser(); p.add_argument("repo",type=pathlib.Path); p.add_argument("packet",type=pathlib.Path); p.add_argument("--compiler",required=True); a=p.parse_args()
a.repo=a.repo.resolve(); a.packet=a.packet.resolve()
sys.path[:0]=[str(a.repo/"tb/verilator/gptp_shadow"),str(a.repo/"scripts")]
from private_inputs import copy_inputs
from owned_process import OwnedProcesses
os.environ["TMPDIR"]=str(a.packet/"scratch")
env=dict(os.environ, VERILATOR=a.compiler, VERILATOR_JOBS="5", MAKEFLAGS="", CCACHE_DISABLE="1", PYTHONDONTWRITEBYTECODE="1")
print(subprocess.check_output([a.compiler,"--version"],text=True).strip(),flush=True)
def prepare(label):
 root=a.packet/"scratch"/label; root.mkdir(exist_ok=True)
 with OwnedProcesses() as owner:
  copy_inputs(a.repo,a.repo/"tb/verilator/gptp_shadow",root,owner,set())
 if label!="control":
  patch=a.packet/(label+".patch")
  subprocess.run(["git","apply",str(patch)],cwd=root/"gptp-processor",check=True)
def run(label):
 root=a.packet/"scratch"/label
 with (a.packet/(label+".log")).open("w") as f:
  rc=subprocess.run(["make","-j16","run"],cwd=root/"tb/verilator/gptp_shadow",env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (a.packet/(label+".rc")).write_text(str(rc)+"\n")
 lines=(a.packet/(label+".log")).read_text().splitlines()
 relevant=[s for s in lines if s.startswith("FAIL ") or "checks:" in s or s.startswith("INFO #10")]
 print(label,"rc",rc,"\n"+"\n".join(relevant),flush=True)
 if label=="control": assert rc==0 and any("408 checks: 408 PASS, 0 FAIL" in s for s in lines)
 elif label=="delayed-announce": assert rc!=0 and any(s.startswith("FAIL #106 race: one master Announce") for s in lines)
 else:
  assert rc!=0
  for sign in ("+100","-100"):
   assert any(s.startswith("FAIL #107 settled "+sign+" ppm: the mastership") for s in lines)
   assert any(s.startswith("FAIL #107 settled "+sign+" ppm: the real counter") for s in lines)
for label in ["control","delayed-announce","retained-slave-rate"]: prepare(label)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 list(pool.map(run,["control","delayed-announce","retained-slave-rate"]))
print("PASS: pristine control and both restored faults produced the required verdicts",flush=True)

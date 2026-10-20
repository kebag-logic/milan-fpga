#!/usr/bin/env python3
"""Run the exact-head phase mutation campaign with bounded concurrency."""
import argparse,os,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument("repo",type=pathlib.Path);p.add_argument("--compiler",required=True);a=p.parse_args()
r=pathlib.Path(__file__).resolve().parent;env=os.environ.copy();env.update(VERILATOR=a.compiler,VERILATOR_JOBS="2",TMPDIR=str(r/"scratch"),MAKEFLAGS="-j16")
with (r/"receipts/mutants.log").open("w") as f: rc=subprocess.call(["python3",str(a.repo/"tb/verilator/media_phase/phase_mutants.py"),"--jobs","8"],cwd=a.repo,env=env,stdout=f,stderr=subprocess.STDOUT)
(r/"receipts/mutants.rc").write_text(str(rc)+"\n");print("campaign rc",rc);raise SystemExit(rc)

#!/usr/bin/env python3
"""Run the focused capture crossbar main test without its broader synthesis bank."""
import argparse,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument("repo",type=pathlib.Path);p.add_argument("--compiler",required=True);a=p.parse_args()
r=pathlib.Path(__file__).resolve().parent;l=r/"receipts";b=r/"scratch/chmap-build";l.mkdir(exist_ok=True)
cmd=["make","-j16","-C",str(a.repo/"tb/verilator/chmap_capture"),"build","VERILATOR="+a.compiler,"VERILATOR_JOBS=2","MDIR="+str(b)]
with (l/"chmap-build.log").open("w") as f:rc=subprocess.call(cmd,stdout=f,stderr=subprocess.STDOUT)
(l/"chmap-build.rc").write_text(str(rc)+"\n")
if rc:raise SystemExit(rc)
with (l/"chmap-main.log").open("w") as f:rc=subprocess.call([str(b/"Vchmap_wrap")],stdout=f,stderr=subprocess.STDOUT)
(l/"chmap-main.rc").write_text(str(rc)+"\n");raise SystemExit(rc)

#!/usr/bin/env python3
"""Run the focused mailbox integration suites in a disposable exact-head export."""
import argparse, hashlib, os, subprocess, tarfile, time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("repo",type=Path);ap.add_argument("compiler",type=Path);a=ap.parse_args()
p=Path(__file__).resolve().parent;work=p/"scratch/mailbox";work.mkdir(parents=True,exist_ok=True)
identity=subprocess.check_output([str(a.compiler),"--version"],text=True)
assert identity.startswith("Verilator 5.050 "),identity
(p/"compiler-identity.log").write_text(identity+"launcher sha256 "+hashlib.sha256(a.compiler.read_bytes()).hexdigest()+"\n")
archive=p/"scratch/mailbox.tar"
with archive.open("wb") as f:
 subprocess.run(["git","-C",str(a.repo.resolve()),"archive","HEAD","hdl/milan/mailbox","sw/mailbox","sw/firmware/ctrl","sw/firmware/ctrl_nvm","tb/verilator/mbx","tb/common"],stdout=f,check=True)
with tarfile.open(archive) as t:t.extractall(work,filter="data")
argv=["make","-C",str(work/"tb/verilator/mbx"),"-j16","VBUILD_JOBS=2","VERILATOR="+str(a.compiler),"run-wb","run-axil","run-cosim","run-if2"]
start=time.monotonic()
with (p/"mailbox.log").open("w") as f:
 r=subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,"TMPDIR":str(p/"scratch")})
(p/"mailbox.rc").write_text(str(r.returncode)+"\n")
print("mailbox",r.returncode,"seconds",round(time.monotonic()-start,2),flush=True)
raise SystemExit(r.returncode)

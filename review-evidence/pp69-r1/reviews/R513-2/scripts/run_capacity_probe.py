#!/usr/bin/env python3
"""Exercise the per-interface registry at its 16-controller product depth.
Only a disposable testbench is changed; the implementation bytes are copied unchanged.
"""
import os, pathlib, shutil, subprocess, sys
repo, packet = map(lambda x:pathlib.Path(x).resolve(), sys.argv[1:])
tree=packet/"scratch/capacity-tree"
if tree.exists(): shutil.rmtree(tree)
for rel in ["hdl","tb/common","tb/aecp_notify"]:
    shutil.copytree(repo/rel,tree/rel,ignore=shutil.ignore_patterns("obj*","*.hex","__pycache__"))
suite=tree/"tb/aecp_notify"
f=suite/"sim_main.cpp"; t=f.read_text().replace("N_CTRL = 2;","N_CTRL = 16;").replace("REGISTRY_ACCEPT_CYCLES = 24;","REGISTRY_ACCEPT_CYCLES = 96;"); f.write_text(t)
f=suite/"port_tuple.hpp"; t=f.read_text(); t=t[:t.index("int PortHarness::run() {")]+(packet/"scripts/capacity_probe.cpp.inc").read_text(); f.write_text(t)
f=suite/"Makefile";f.write_text(f.read_text().replace("-GN_CTRL_P=2 ","-GN_CTRL_P=16 "))
env=os.environ.copy();env["TMPDIR"]=str(packet/"scratch")
cmd=["make","-j16","interfaces","VERILATOR="+str(packet/"scripts/verilator_bounded.py")]
with (packet/"receipts/capacity-probe.log").open("w") as f:
    rc=subprocess.run(cmd,cwd=suite,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
(packet/"receipts/capacity-probe.rc").write_text(str(rc)+"\n")
print("capacity-probe rc",rc);sys.exit(rc)

#!/usr/bin/env python3
"""Run the optional port-integration arm and its two pin refusal controls."""
import pathlib,subprocess,sys
root=pathlib.Path.cwd();packet=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import ctrl_arms,ctrl_build,ctrl_mutants,ctrl_reuse,fw_gtest
repo=packet/"scratch/lwsrp"
subprocess.run(["git","-C",str(repo),"checkout","--quiet","--detach",ctrl_arms.LWSRP_REV],check=True)
ctrl_arms.lwsrp_pin(repo)
print("lwSRP pin verified",ctrl_arms.LWSRP_REV,flush=True)
work=packet/"scratch/lwsrp-arm"
tree=ctrl_build.Tree(ctrl_build.CTRL,work/"build",work/"reuse",fw_gtest.Build(jobs=4))
ctrl_reuse.cut_reuse(tree.reuse)
out=ctrl_arms.arm_lwsrp(tree,repo)
print(out.log,flush=True)
assert out.rc==0
assert ctrl_mutants.lwsrp_pin_arms(work/"pin-probes",repo)==0
print("PASS lwSRP integration and pin controls")

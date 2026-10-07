# SPDX-License-Identifier: Apache-2.0
"""Build both profiles under one job budget and run independent suites concurrently."""
import argparse, concurrent.futures, pathlib, subprocess, sys
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,required=True);p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--prefix",type=pathlib.Path,required=True);p.add_argument("--jobs",type=int,default=16)
a=p.parse_args();source=a.source.resolve();packet=a.packet.resolve();prefix=a.prefix.resolve()
if not 1<=a.jobs<=16:p.error("jobs must be between 1 and 16")
scratch=packet/"scratch";scratch.mkdir(exist_ok=True)
runner=[sys.executable,str(packet/"scripts/run.py"),"--source",str(source),"--packet",str(packet)]
def run(pair):
 label,cmd=pair;return subprocess.run([*runner,"--label",label,"--",*cmd]).returncode
profiles=[("default","OFF"),("milan","ON")]
configure=[("configure-"+name,["cmake","-S",str(source),"-B",str(scratch/("build-"+name)),"-DCMAKE_BUILD_TYPE=Debug","-DCMAKE_PREFIX_PATH="+str(prefix),"-DLWSRP_MILAN="+flag]) for name,flag in profiles]
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as pool:codes=list(pool.map(run,configure))
if any(codes):sys.exit(1)
makefile=scratch/"profiles.mk"
# Paths are recipe arguments; quote them for the shell. No source file is mutated.
import shlex
makefile.write_text(".PHONY: all default milan\nall: default milan\n"+"".join(name+":\n\t+$(MAKE) -C "+shlex.quote(str(scratch/("build-"+name)))+"\n" for name,_ in profiles))
if run(("builds",["make","-f",str(makefile),"-j"+str(a.jobs)])):sys.exit(1)
tests=[]
for name,_ in profiles:
 build=scratch/("build-"+name)
 tests += [("ctest-"+name,["ctest","--test-dir",str(build),"-V"]),("behave-"+name,["env","SHLAN_LIBRARY="+str(build/"libshlan.so"),"behave"])]
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,4)) as pool:codes=list(pool.map(run,tests))
sys.exit(int(any(codes)))

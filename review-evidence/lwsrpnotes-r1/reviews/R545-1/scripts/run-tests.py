#!/usr/bin/env python3
"""Run both profiles and both unmodified reversal campaigns in the foreground."""
import concurrent.futures, os, subprocess, sys
from pathlib import Path
packet=Path(__file__).resolve().parents[1]
repo=Path(sys.argv[1]).resolve()
scratch=packet/"scratch"
prefix=scratch/"cgreen-prefix"
(scratch/"tmp").mkdir(exist_ok=True)
os.environ.update(PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch/"tmp"),
                  LD_LIBRARY_PATH=str(prefix/"lib")+os.pathsep+os.environ.get("LD_LIBRARY_PATH",""))
def record(name,cmd,cwd=repo):
    return subprocess.run([sys.executable,str(packet/"scripts"/"record.py"),"--name",name,"--cwd",str(cwd),"--",*cmd]).returncode
def configure(profile):
    return record("configure-"+profile,["cmake","-S",str(repo),"-B",str(scratch/("build-"+profile)),"-DCMAKE_BUILD_TYPE=Debug", "-DCMAKE_PREFIX_PATH="+str(prefix),"-DLWSRP_MILAN="+profile])
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    if any(pool.map(configure,["OFF","ON"])): raise SystemExit(1)
# Recursive make shares one jobserver: at most 16 build jobs across both profiles.
makefile=scratch/"profiles.mk"
makefile.write_text(".PHONY: all OFF ON\nall: OFF ON\n"+"".join(p+":\n\t+$(MAKE) -C '"+str(scratch/("build-"+p))+"'\n" for p in ["OFF","ON"]))
if record("build-both",["make","-j16","-f",str(makefile)],scratch):raise SystemExit(1)
checks=[]
for profile in ["OFF","ON"]:
    build=scratch/("build-"+profile)
    checks.extend([(profile+"-ctest",["ctest","--test-dir",str(build),"--output-on-failure","-V"]),
                   (profile+"-behave",["env","SHLAN_LIBRARY="+str(build/"libshlan.so"),"behave"]),
                   (profile+"-reversals",[sys.executable,"tests/check_reversals.py","--work-dir",str(scratch/("reversals-"+profile)),"--prefix",str(prefix),"--milan",profile])])
# The upstream reversal driver has no --jobs option and uses two build workers.
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results=list(pool.map(lambda c:record(*c),checks))
raise SystemExit(int(any(results)))

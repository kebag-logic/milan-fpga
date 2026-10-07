# SPDX-License-Identifier: Apache-2.0
import argparse,concurrent.futures,shutil
from common import *
p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=2);args=p.parse_args()
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=SOURCE,text=True).strip()=="14c8b364863be49bc222f4913830b79d23dcf173"
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=SCRATCH/"cgreen",text=True).strip()=="feeb85ed48d163f6b7b0011a6d8e6043951541e4"
run("dependency-configure",["cmake","-S",SCRATCH/"cgreen","-B",SCRATCH/"cgreen-build",f"-DCMAKE_INSTALL_PREFIX={PREFIX}","-DCGREEN_WITH_UNIT_TESTS=OFF","-DCGREEN_WITH_LIBXML2=OFF","-DCMAKE_POLICY_VERSION_MINIMUM=3.5"])
build("dependency-build",SCRATCH/"cgreen-build")
run("dependency-install",["cmake","--install",SCRATCH/"cgreen-build"])
def profile(mode):
 b=SCRATCH/("baseline-"+mode)
 run(mode+"-configure",["cmake","-S",SOURCE,"-B",b,"-DCMAKE_BUILD_TYPE=Debug",f"-DCMAKE_PREFIX_PATH={PREFIX}","-DLWSRP_MILAN="+mode])
 build(mode+"-build",b)
 run(mode+"-ctest",["ctest","--test-dir",b,"--output-on-failure"])
 run(mode+"-units",[b/"unit_tests"])
 env=ENV.copy();env["SHLAN_LIBRARY"]=str(b/"libshlan.so")
 run(mode+"-scenarios",["behave"],env=env)
 exe=b/"prior-probe"
 run(mode+"-probe-build",["cc","-std=c11","-O1","-g","-Isrc/include","-Isrc","-Itests/unit",PACKET/"scripts/prior_cross_port_probe.c","tests/unit/fault_alloc.c","-L"+str(b),"-Wl,-rpath,"+str(b),"-lshlan","-o",exe])
 run(mode+"-cross-port",[exe,"cross-port"])
 run(mode+"-broad-probe",[exe])
 run(mode+"-freestanding",["python3","tests/check_freestanding.py"],env=dict(ENV,CC="cc -DLWSRP_MILAN="+("1" if mode=="ON" else "0")))
 return mode
with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.jobs,2)) as ex:
 for result in ex.map(profile,["OFF","ON"]): print("Completed "+result,flush=True)
run("scenario-dry-run",["behave","--dry-run"])

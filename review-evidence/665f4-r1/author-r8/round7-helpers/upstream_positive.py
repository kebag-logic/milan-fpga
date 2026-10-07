import os,subprocess
from pathlib import Path
source=Path.cwd()/"third_party/lwSRP"
root=Path(os.environ["SCRATCH"])
prefix=Path(os.environ["CGREEN"])
env=os.environ.copy()
env["LD_LIBRARY_PATH"]=str(prefix/"lib")
for profile in ("OFF","ON"):
 build=root/("upstream-"+profile.lower())
 commands=[
 ["cmake","-S",str(source),"-B",str(build),"-DCMAKE_BUILD_TYPE=Debug",f"-DCMAKE_PREFIX_PATH={prefix}",f"-DLWSRP_MILAN={profile}"],
 ["cmake","--build",str(build),"--parallel","2"],
 ["ctest","--test-dir",str(build),"--output-on-failure"],
 [str(build/"unit_tests")],
 ["behave","--no-capture","-f","plain"]]
 env["SHLAN_LIBRARY"]=str(build/"libshlan.so")
 for command in commands:
  print("COMMAND",command,flush=True)
  subprocess.run(command,env=env,cwd=source,check=True,timeout=120)

#!/usr/bin/env python3
"""Reproduce the non-default-prefix package build; change no reviewed source."""
import argparse,json,os,pathlib,shlex,shutil,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument("root",type=pathlib.Path);ap.add_argument("packet",type=pathlib.Path);ap.add_argument("--control-only",action="store_true");a=ap.parse_args();root=a.root.resolve();p=a.packet.resolve();w=p/"scratch/package-prefix-probe";w.mkdir(parents=True,exist_ok=True)
env=dict(os.environ);env.update(json.loads((p/"scratch/environment.json").read_text()))
for key in ["CPLUS_INCLUDE_PATH","C_INCLUDE_PATH","CPATH","LIBRARY_PATH","PKG_CONFIG_ALLOW_SYSTEM_CFLAGS","PKG_CONFIG_ALLOW_SYSTEM_LIBS"]:env.pop(key,None)
flags=subprocess.check_output(["pkg-config","--cflags","--libs","gtest","gmock"],env=env,text=True)
(w/"flags.txt").write_text(flags);rows=[]
def run(name,args,environment=env):
 with (w/(name+".log")).open("w") as f:rc=subprocess.run(args,cwd=root,env=environment,stdout=f,stderr=subprocess.STDOUT).returncode
 (w/(name+".rc")).write_text(str(rc)+"\n");rows.append({"step":name,"rc":rc});print(name,rc,flush=True);return rc
if not a.control_only:
 run("configure",["cmake","-S",str(root),"-B",str(w/"cmake"),"-DCMAKE_BUILD_TYPE=Debug"])
 run("build",["cmake","--build",str(w/"cmake"),"-j2"])
 run("test",["ctest","--test-dir",str(w/"cmake"),"--output-on-failure","-j2"])
 run("mutation",[sys.executable,"scripts/mutation.py","--work",str(w/"mutation"),"--select","acmp-header-no-resp-2s","--jobs","4"])
 run("dependency-control",[sys.executable,"scripts/dependency_selftest.py","--work",str(w/"dependency"),"--jobs","2"])
# Diagnostic control: preserve package metadata, changing only third-party -I to -isystem.
bindir=w/"bin";bindir.mkdir(exist_ok=True);proxy=bindir/"pkg-config";real=shutil.which("pkg-config",path=env["PATH"])
proxy.write_text("#!"+sys.executable+"\nimport subprocess,sys,shlex\nr=subprocess.run(["+repr(real)+",*sys.argv[1:]],capture_output=True,text=True)\ns=r.stdout\nif any(x.startswith(\"--cflags\") for x in sys.argv):\n a=shlex.split(s); b=[]\n for x in a:\n  b.extend([\"-isystem\",x[2:]] if x.startswith(\"-I\") else [x])\n s=shlex.join(b)+\"\\n\"\nprint(s,end=\"\");print(r.stderr,end=\"\",file=sys.stderr);sys.exit(r.returncode)\n");proxy.chmod(0o755)
control=dict(env,PATH=str(bindir)+os.pathsep+env["PATH"])
run("system-header-control",[sys.executable,"scripts/mutation.py","--work",str(w/"system-header-control"),"--select","acmp-header-no-resp-2s","--jobs","4"],control)
(w/"results.json").write_text(json.dumps({"package_flags":flags,"ambient_paths_removed":True,"control":"Only pkg-config -I classification changes to -isystem; source and library unchanged.","results":rows},indent=2)+"\n")

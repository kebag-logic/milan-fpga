#!/usr/bin/env python3
"""Run one foreground gate in a disposable unprivileged job; retain raw receipts."""
import argparse, json, os, pathlib, resource, subprocess, time
p=argparse.ArgumentParser(); p.add_argument("source",type=pathlib.Path); p.add_argument("packet",type=pathlib.Path); p.add_argument("name"); p.add_argument("--deps",action="store_true"); p.add_argument("--sdk",action="store_true"); p.add_argument("--generated",action="store_true"); p.add_argument("command",nargs=argparse.REMAINDER); a=p.parse_args()
a.source=a.source.resolve(); a.packet=a.packet.resolve(); cmd=a.command
if cmd[0]=="--": cmd=cmd[1:]
work=a.packet/"scratch"/a.name; work.mkdir(parents=True,exist_ok=True)
(work/"passwd").write_text(f"reviewer:x:{os.getuid()}:{os.getgid()}:Reviewer:/work:/bin/bash\n")
b=["bwrap","--unshare-all","--die-with-parent","--new-session","--clearenv","--cap-drop","ALL","--ro-bind","/usr","/usr","--symlink","usr/bin","/bin","--symlink","usr/lib","/lib","--symlink","usr/lib64","/lib64","--dir","/etc","--ro-bind",str(work/"passwd"),"/etc/passwd","--proc","/proc","--dev","/dev","--tmpfs","/run","--ro-bind",str(a.source),"/src","--ro-bind",str(a.packet/"scripts"),"/review","--ro-bind",str(a.packet/"public"),"/public","--bind",str(work),"/work","--bind",str(work),"/tmp","--chdir","/src","--setenv","PATH","/usr/bin:/bin","--setenv","TMPDIR","/tmp","--setenv","PYTHONDONTWRITEBYTECODE","1","--setenv","LC_ALL","C.UTF-8","--setenv","GIT_CONFIG_NOSYSTEM","1","--setenv","GIT_CONFIG_GLOBAL","/dev/null","--setenv","GIT_CONFIG_COUNT","1","--setenv","GIT_CONFIG_KEY_0","safe.directory","--setenv","GIT_CONFIG_VALUE_0","*"]
if a.deps: b += ["--ro-bind",str(a.packet/"scratch/python-deps"),"/deps","--setenv","PYTHONPATH","/deps"]
if a.sdk: b += ["--ro-bind",str(a.packet/"scratch/sdk"),"/sdk","--setenv","MILAN_RV32_CC","/sdk/bin/riscv32-buildroot-linux-gnu-gcc"]
if a.generated:
 import shutil
 for rel in ("configs/generated","hdl/common/csr/gen"):
  target=work/rel; target.parent.mkdir(parents=True,exist_ok=True)
  shutil.copytree(a.source/rel,target,dirs_exist_ok=True)
  b += ["--bind",str(target),"/src/"+rel]
b += ["--",*cmd]
start=time.monotonic(); out=a.packet/"receipts"; out.mkdir(exist_ok=True)
with (out/(a.name+".log")).open("wb") as log:
 r=subprocess.run(b,stdout=log,stderr=subprocess.STDOUT,timeout=570)
info={"command":cmd,"isolation":"unprivileged disposable filesystem, PID, IPC, UTS and network namespaces; no capabilities; read-only source; no host credential or service mounts", "rc":r.returncode,"seconds":round(time.monotonic()-start,3)}
(out/(a.name+".json")).write_text(json.dumps(info,indent=2)+"\n"); (out/(a.name+".rc")).write_text(str(r.returncode)+"\n")
print(a.name+": "+json.dumps(info)); print((out/(a.name+".log")).read_text(errors="replace")[-1800:]); raise SystemExit(r.returncode)

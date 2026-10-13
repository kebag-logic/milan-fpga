#!/usr/bin/env python3
"""Run a focused gate in a disposable unprivileged filesystem/process/network job."""
import argparse, datetime, json, os, pathlib, subprocess, time, shutil
p=argparse.ArgumentParser(); p.add_argument("--generated",action="store_true"); p.add_argument("--deps",type=pathlib.Path); p.add_argument("--sdk",type=pathlib.Path); p.add_argument("source",type=pathlib.Path); p.add_argument("packet",type=pathlib.Path); p.add_argument("name"); p.add_argument("command",nargs=argparse.REMAINDER); a=p.parse_args()
source=a.source.resolve(); packet=a.packet.resolve(); work=packet/"scratch"/a.name
work.mkdir(parents=True,exist_ok=True); (work/"tmp").mkdir(exist_ok=True); (work/"home").mkdir(exist_ok=True)
command=a.command[1:] if a.command[:1]==["--"] else a.command
argv=["bwrap","--unshare-all","--die-with-parent","--new-session","--cap-drop","ALL","--clearenv"]
for directory in ("/usr","/bin","/lib","/lib64"):
 if pathlib.Path(directory).exists(): argv += ["--ro-bind",directory,directory]
argv += ["--proc","/proc","--dev","/dev","--ro-bind",str(source),"/source","--bind",str(work),"/work","--dir","/etc","--ro-bind","/etc/passwd","/etc/passwd","--ro-bind","/etc/group","/etc/group","--symlink","/work/tmp","/tmp","--chdir","/source"]
for key,value in {"PATH":"/usr/bin:/bin","HOME":"/work/home","TMPDIR":"/work/tmp","LANG":"C.UTF-8","LC_ALL":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1","GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null","GIT_NO_REPLACE_OBJECTS":"1"}.items(): argv += ["--setenv",key,value]
if a.generated:
 for rel in ("configs/generated","hdl/common/csr/gen"):
  target=work/"overlays"/rel
  shutil.copytree(source/rel,target,dirs_exist_ok=True)
  argv += ["--bind",str(target),"/source/"+rel]
if a.deps:
 argv += ["--ro-bind",str(a.deps.resolve()),"/deps","--setenv","PYTHONPATH","/deps"]
if a.sdk:
 argv += ["--ro-bind",str(a.sdk.resolve()),"/sdk","--setenv","MILAN_RV32_CC","/sdk/bin/riscv32-linux-gcc"]
argv += command
start=time.monotonic(); receipt={"command":command,"source_head":subprocess.check_output(["git","-C",str(source),"rev-parse","HEAD"],text=True).strip(),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"isolation":"unprivileged disposable mount, PID, user and network namespaces; read-only candidate; no host credentials or service sockets; no delegated capabilities"}
with (packet/"receipts"/(a.name+".log")).open("w") as log:
 try: result=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,timeout=540); rc=result.returncode
 except subprocess.TimeoutExpired: rc=124
receipt.update(generated_scratch_overlays=bool(a.generated), documentation_dependencies=bool(a.deps), sdk_read_only=bool(a.sdk), returncode=rc,elapsed_seconds=round(time.monotonic()-start,3))
(packet/"receipts"/(a.name+".json")).write_text(json.dumps(receipt,indent=2)+"\n"); (packet/"receipts"/(a.name+".rc")).write_text(str(rc)+"\n")
print(json.dumps(receipt)); raise SystemExit(rc)

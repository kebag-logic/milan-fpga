#!/usr/bin/env python3
"""Run a focused command in a disposable, credential-free, networkless boundary."""
import argparse,json,os,pathlib,shutil,subprocess,time
p=argparse.ArgumentParser()
p.add_argument("label");p.add_argument("--source",default=os.getcwd());p.add_argument("command",nargs=argparse.REMAINDER)
a=p.parse_args(); packet=pathlib.Path(__file__).resolve().parents[1]
root=packet/"scratch"/a.label;root.mkdir(parents=True,exist_ok=True)
cmd=a.command
if cmd and cmd[0]=="--":cmd=cmd[1:]
bound=["bwrap","--unshare-all","--die-with-parent","--new-session","--cap-drop","ALL","--ro-bind","/usr","/usr","--symlink","usr/bin","/bin","--symlink","usr/lib","/lib","--symlink","usr/lib64","/lib64","--proc","/proc","--dev","/dev","--dir","/etc","--ro-bind","/etc/ld.so.cache","/etc/ld.so.cache","--bind",str(root),"/tmp","--ro-bind",str(pathlib.Path(a.source).resolve()),"/work","--ro-bind",str(packet/"scripts"),"/review","--chdir","/work","--clearenv","--setenv","PATH","/usr/bin:/bin","--setenv","HOME","/tmp/home","--setenv","TMPDIR","/tmp","--setenv","LANG","C.UTF-8","--setenv","GITHUB_WORKSPACE","/work","--setenv","PYTHONDONTWRITEBYTECODE","1","--setenv","GIT_CONFIG_GLOBAL","/dev/null","--setenv","GIT_CONFIG_SYSTEM","/dev/null","--setenv","GIT_CONFIG_NOSYSTEM","1","--setenv","GIT_CONFIG_COUNT","2","--setenv","GIT_CONFIG_KEY_0","safe.directory","--setenv","GIT_CONFIG_VALUE_0","*","--setenv","GIT_CONFIG_KEY_1","core.hooksPath","--setenv","GIT_CONFIG_VALUE_1","/dev/null","--",*cmd]
if (packet/'scratch/deps').exists():
 bound[1:1]=['--ro-bind',str(packet/'scratch/deps'),'/deps']
if (packet/'scratch/sdk').exists():
 bound[1:1]=['--ro-bind',str(packet/'scratch/sdk'),'/sdk']
if a.label.startswith(('linked-images','image-controls')):
 generated=root/'generated';generated.mkdir(exist_ok=True)
 initial=pathlib.Path(a.source)/'configs/generated'
 if initial.exists():shutil.copytree(initial,generated,dirs_exist_ok=True)
 i=bound.index('--chdir');bound[i:i]=['--bind',str(generated),'/work/configs/generated']
 csr=root/'csr-generated';shutil.copytree(pathlib.Path(a.source)/'hdl/common/csr/gen',csr,dirs_exist_ok=True)
 i=bound.index('--chdir');bound[i:i]=['--bind',str(csr),'/work/hdl/common/csr/gen']
started=time.time()
with (packet/"receipts"/(a.label+".log")).open("w") as log:
 log.write("command: "+json.dumps(cmd)+"\n");log.flush()
 result=subprocess.run(bound,stdout=log,stderr=subprocess.STDOUT,timeout=570)
meta={"command":cmd,"returncode":result.returncode,"elapsed_seconds":round(time.time()-started,3),"source_head":subprocess.check_output(["git","-C",a.source,"rev-parse","HEAD"],text=True).strip(),"boundary":"unprivileged mount, user, PID and network namespaces; source read-only; no credentials; writes confined to scratch; image commands overlay generated configuration outputs"}
(packet/"receipts"/(a.label+".json")).write_text(json.dumps(meta,indent=2)+"\n")
(packet/"receipts"/(a.label+".rc")).write_text(str(result.returncode)+"\n")
print(json.dumps(meta));raise SystemExit(result.returncode)

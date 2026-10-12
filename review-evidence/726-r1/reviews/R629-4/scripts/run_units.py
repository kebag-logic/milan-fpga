#!/usr/bin/env python3
"""Execute the tracked unit recipes with object directories confined to scratch."""
import os,pathlib,shlex,subprocess,sys
root=pathlib.Path(sys.argv[1]);packet=pathlib.Path(sys.argv[2]);compiler=os.environ["VERILATOR"]
for suite,target,chosen in [("tkdiag","build",None),("crf_rx","unit",None),("avtp_rxmon","run","avtp_rxmon_nx_wrap"),("avtp_rxmon","lockstep-build",None)]:
 cwd=root/"tb/verilator"/suite
 recipe=subprocess.check_output(["make","--no-print-directory","-j16","-n",target,"VERILATOR="+compiler],cwd=cwd,text=True)
 for n,line in enumerate(recipe.replace("\\\n"," ").splitlines()):
  if not line.startswith(compiler+" "):continue
  cmd=shlex.split(line)
  if chosen and chosen not in cmd:continue
  label=suite+"-"+target+"-"+str(n);mdir=packet/"scratch"/label
  for flag in ["--Mdir","-Mdir"]:
   if flag in cmd:
    i=cmd.index(flag);del cmd[i:i+2]
  cmd[cmd.index("-j")+1]="2"
  for i,s in enumerate(cmd):
   if s.startswith("+incdir+"):cmd[i]="+incdir+"+str((cwd/s[8:]).resolve())
   elif s.endswith((".sv",".v",".cpp")):cmd[i]=str((cwd/s).resolve())
  exe=cmd[cmd.index("-o")+1]; cmd += ["--Mdir",str(mdir)]
  with (packet/"receipts"/(label+".build.log")).open("w") as f: rc=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT).returncode
  if rc:raise SystemExit(label+" build failed")
  with (packet/"receipts"/(label+".run.log")).open("w") as f:rc=subprocess.run([str(mdir/exe)],cwd=cwd,stdout=f,stderr=subprocess.STDOUT).returncode
  (packet/"receipts"/(label+".rc")).write_text(str(rc)+"\n");print(label,"rc",rc,flush=True)
  if rc:raise SystemExit(rc)

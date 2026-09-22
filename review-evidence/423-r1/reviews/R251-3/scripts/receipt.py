#!/usr/bin/env python3
"""Record portable commands, raw output and expected exit without shell interpolation."""
import argparse,json,os,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);p.add_argument("--cwd",type=Path,required=True);p.add_argument("--expected",type=int,default=0);p.add_argument("command",nargs=argparse.REMAINDER);a=p.parse_args()
cmd=a.command.removeprefix(["--"]) if hasattr(a.command,"removeprefix") else (a.command[1:] if a.command and a.command[0]=="--" else a.command)
start=time.time();r=subprocess.run(cmd,cwd=a.cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"),capture_output=True)
a.output.parent.mkdir(parents=True,exist_ok=True)
Path(str(a.output)+".stdout").write_bytes(r.stdout);Path(str(a.output)+".stderr").write_bytes(r.stderr)
row={"argv":cmd,"cwd":str(a.cwd),"exit":r.returncode,"expected":a.expected,"started_unix":start,"seconds":time.time()-start}
Path(str(a.output)+".json").write_text(json.dumps(row,indent=2)+"\n")
print(json.dumps(row));print(r.stdout.decode("utf-8","backslashreplace")[-1600:]);print(r.stderr.decode("utf-8","backslashreplace")[-1000:])
raise SystemExit(0 if r.returncode==a.expected else 1)

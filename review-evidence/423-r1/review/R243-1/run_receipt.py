import argparse, datetime, hashlib, json, os, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("name"); p.add_argument("--cwd",default="$VALIDATION_STORAGE/reviews/r243-423-r1"); p.add_argument("command",nargs=argparse.REMAINDER);a=p.parse_args()
root=Path(__file__).resolve().parent
command=a.command[1:] if a.command[:1]==["--"] else a.command
if command[:1]!=["rtk"]: raise SystemExit("Every recorded shell invocation must start with rtk")
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",MAX_JOBS="8",JOBS="8",MAKEFLAGS="-j8")
start=time.monotonic(); stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(command,cwd=a.cwd,env=env,capture_output=True)
(root/(a.name+".stdout")).write_bytes(r.stdout);(root/(a.name+".stderr")).write_bytes(r.stderr)
d=dict(command=command,cwd=a.cwd,started=stamp,seconds=time.monotonic()-start,exit=r.returncode,stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest())
(root/(a.name+".json")).write_text(json.dumps(d,indent=2)+"\n");print(json.dumps(d));print(r.stdout.decode("utf-8","backslashreplace")[-4000:]);print(r.stderr.decode("utf-8","backslashreplace")[-2000:]);raise SystemExit(r.returncode)

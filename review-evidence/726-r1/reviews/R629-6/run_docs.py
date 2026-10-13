#!/usr/bin/env python3
"""Run allowed documentation workflow checks; excluded banks remain explicit."""
import argparse,json,os,shlex,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import yaml
p=argparse.ArgumentParser();p.add_argument("root",type=Path);p.add_argument("--jobs",type=int,default=2);a=p.parse_args()
root=a.root.resolve();packet=Path(__file__).resolve().parent
scratch=packet/"scratch";receipts=packet/"docs";receipts.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE="1",PATH=str(Path(sys.executable).parent)+os.pathsep+os.environ["PATH"])
wf=yaml.safe_load((root/".github/workflows/docs.yml").read_text())
commands=[]
for jobid,job in wf["jobs"].items():
    if jobid=="docs-check-no-git":continue
    for step in job["steps"]:
        for line in step.get("run","").splitlines():
            line=line.strip()
            if not line.startswith("python3 ") or line.endswith("\\"):continue
            if any(s in line for s in ("pip install","test_builder.py","ci_rv32_sdk","act_ci.py","test_firmware_compiler.py","$")):continue
            if line.startswith("python3 scripts/gen_hdl_reference.py") and "--selftest" not in line:continue
            command=shlex.split(line);command[0]=sys.executable
            if command not in commands:commands.append(command)
commands += [[sys.executable,"scripts/check_em_dash.py","--base","c6bd08c6"],[sys.executable,"tb/tools/torture_campaign.py","--self-test"],[sys.executable,"-m","behave","--no-capture","-f","plain"],["make","-j16","-C","gptp-processor","docs"]]
(receipts/"commands.json").write_text(json.dumps(commands,indent=2)+"\n")
def run(item):
    i,cmd=item;name=f"{i:02d}-"+Path(cmd[1] if cmd[0]==sys.executable else "gptp-docs").stem
    cwd=root/"tests" if "behave" in cmd else root
    with (receipts/(name+".log")).open("w") as log:
        r=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
    (receipts/(name+".rc")).write_text(str(r.returncode)+"\n")
    print(name,r.returncode,flush=True);return r.returncode
with ThreadPoolExecutor(max_workers=a.jobs) as pool:results=list(pool.map(run,enumerate(commands)))
sys.exit(bool(any(results)))

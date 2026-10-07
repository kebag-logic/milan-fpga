#!/usr/bin/env python3
"""Reproduce this focused review packet; all subprocesses are joined in the foreground."""
import argparse, concurrent.futures, os, subprocess
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--packet", type=Path, required=True)
parser.add_argument("--verilator", type=Path, required=True)
a=parser.parse_args()
root=a.source.resolve(); packet=a.packet.resolve()
env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(packet/"scratch/tmp"), VERILATOR=str(a.verilator.resolve()))
(packet/"scratch/tmp").mkdir(parents=True,exist_ok=True)
(packet/"receipts").mkdir(exist_ok=True)
identity=subprocess.check_output([str(a.verilator.resolve()),"--version"],text=True)
assert "Verilator 5.050 " in identity
assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()=="938497af1dffd8a87edebf3ab93663914bf85e5e"
def run(name,cmd):
 with (packet/"receipts"/(name+".log")).open("w") as log:
  result=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=570)
 (packet/"receipts"/(name+".rc")).write_text(str(result.returncode)+"\n")
 return result.returncode
# Two independent foreground child campaigns, at most 8+4 compiler jobs.
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(run,name+"-campaign",["bash",str(packet/"scripts/run_campaign.sh"),str(root),str(packet),name]) for name in ("focused","differential")]
 codes=[f.result() for f in fs]
# Scoped RTL uses two four-job builds; coverage uses four jobs.
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(run,"coverage",["python3","sw/firmware/gtest/fw_coverage.py","--check","--jobs","4","--keep",str(packet/"scratch/coverage")]),pool.submit(run,"mailbox",["bash",str(packet/"scripts/run_mailbox.sh"),str(root),str(packet)])]
 codes.extend(f.result() for f in fs)
for name,args in (("generator",["--check","--crosscheck"]),("generator-selftest",["--selftest"])):
 codes.append(run(name,["python3","sw/mailbox/gen_mailbox.py",*args]))
codes.append(run("integrity-reproduced",["python3",str(packet/"scripts/integrity.py"),str(root)]))
raise SystemExit(any(codes))

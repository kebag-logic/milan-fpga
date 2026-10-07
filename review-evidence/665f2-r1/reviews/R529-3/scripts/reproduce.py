#!/usr/bin/env python3
"""Reproduce the bounded foreground review runs in a NEW packet directory.
Requires exact-head source, installed host test dependencies, a pinned SDK
archive, and the pinned simulator executable. Does not write source files.
"""
import argparse,concurrent.futures,os,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--packet",type=Path,required=True);p.add_argument("--sdk-archive",type=Path,required=True);p.add_argument("--verilator",type=Path,required=True);a=p.parse_args()
root=a.repo.resolve();out=a.packet.resolve();here=Path(__file__).resolve().parent
for d in ("scratch","receipts"): (out/d).mkdir(parents=True,exist_ok=True)
env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","TMPDIR":str(out/"scratch"),"MILAN_RV32_CC":str(out/"scratch/sdk/bin/riscv32-linux-gcc"),"VERILATOR":str(a.verilator.resolve())}
def run(name,cmd):
 subprocess.run([sys.executable,str(here/"run_logged.py"),str(out/"receipts"/(name+".log")),*map(str,cmd)],cwd=root,env=env,check=True)
run("integrity-before",[sys.executable,here/"integrity.py",root])
run("simulator-identity",[a.verilator.resolve(),"--version"])
run("sdk-install",[sys.executable,root/"scripts/ci_rv32_sdk.py","--destination",out/"scratch/sdk","--archive",a.sdk_archive.resolve()])
run("retention",[sys.executable,here/"retention.py",root])
# Each batch is joined in the foreground. Peak compiler parallelism <=13.
batches=[[
 ("maap-focused",[sys.executable,here/"focused.py","maap","--repo",root,"--out",out/"scratch/maap-focused","--jobs","4"]),
 ("rv32-focused",[sys.executable,here/"focused.py","rv32","--repo",root,"--out",out/"scratch/rv32-focused","--jobs","1"]),
 ("differential",[sys.executable,root/"sw/firmware/ctrl/test/maap_differential.py","--keep",out/"scratch/differential"])], [
 ("rv32-selftest",[sys.executable,root/"sw/firmware/gtest/fw_rv32_selftest.py","--require-rv32"]),
 ("coverage",[sys.executable,root/"sw/firmware/gtest/fw_coverage.py","--check","--jobs","4"])]]
for batch in batches:
 with concurrent.futures.ThreadPoolExecutor(max_workers=len(batch)) as pool:
  futures=[pool.submit(run,name,cmd) for name,cmd in batch]
  for future in futures: future.result()
run("selector-probe",[sys.executable,here/"selector_probe.py","--repo",root,"--out",out/"scratch/selector"])
run("integrity-final",[sys.executable,here/"integrity.py",root])

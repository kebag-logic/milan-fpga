#!/usr/bin/env python3
"""Replay unchanged public round-10 probes and focused ACMP controls."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

PACKET = Path(__file__).resolve().parents[1]
ROOT = Path.cwd()
REF = "2f7ab26dadbd359c55eb248ef56fcbcbe4e6bd40"
BASE = "review-evidence/665f4-r1/author-r11/round11-helpers/review11/"
HEADERS = ("independent_feedback.hpp", "r532_10_probe_kind.hpp", "r532_10_probe_guard.hpp")

def worker(n, jobs):
    sys.path.insert(0,str(ROOT/"sw/firmware/ctrl/test"))
    import ctrl_arms, ctrl_mutants, srp_arms, fw_gtest
    from ctrl_build import CTRL, Tree
    from ctrl_reuse import cut_reuse
    out = PACKET / "scratch" / f"replay-{n}"
    out.mkdir(parents=True,exist_ok=True)
    if n:
        tests = out / "tests"
        shutil.copytree(CTRL/"test",tests,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__"))
        for h in HEADERS: shutil.copyfile(PACKET/"scripts/prior-probes"/h,tests/h)
        main = tests/"test_acmp_mbx.cpp"
        main.write_text(main.read_text()+"\n"+"\n".join('#include "'+h+'"' for h in HEADERS)+"\n")
        srp_arms.HERE=tests
        selection="R533Feedback.*:SrpBinding.R10KindChange*:SrpBinding.R10FailedToAdvertise*:SrpBinding.R10DiscoveredWithdrawal*:SrpBinding.R10Replacement*:SrpBinding.R10Earlier*"
        result=srp_arms.arm_srp(Tree(CTRL,out/"build",out/"reuse",fw_gtest.Build(jobs=jobs)),
            ROOT/"third_party/lwSRP",n,test=("test_acmp_mbx.cpp",selection))
        print(result.log,flush=True)
        return result.rc
    reuse=out/"reuse"
    cut_reuse(reuse)
    build=fw_gtest.Build(jobs=jobs,address_sanitizer=True)
    control=ctrl_arms.arm_acmp(Tree(CTRL,out/"clean",reuse,build))
    print("SANITIZED CLEAN CORE",control.log,flush=True)
    failed=bool(control.rc)
    selected=("acmp-kind-lost","acmp-kind-any-state","acmp-open-unguarded","acmp-init-too-many-sources")
    for name in selected:
        mutation=next(m for m in ctrl_mutants.MUTANTS if m.name==name)
        src=ctrl_mutants.plant(mutation,out)
        result=ctrl_arms.arm_acmp(Tree(src,out/"plant-build",reuse,build))
        ok=all(ctrl_mutants.caught(test,needle,result) for arm,test,needle in mutation.kills() if arm=="acmp")
        ok=ok and "ERROR: AddressSanitizer" not in result.log
        (PACKET/"receipts"/(name+"-asan.log")).write_text(result.log)
        print(name,"caught",ok,flush=True)
        failed |= not ok
    return int(failed)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",type=int)
    ap.add_argument("--jobs",type=int,default=4)
    args=ap.parse_args()
    os.environ["TMPDIR"]=str(PACKET/"scratch")
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    if args.worker is not None: return worker(args.worker,args.jobs)
    dest=PACKET/"scripts/prior-probes"
    dest.mkdir(exist_ok=True)
    inputs=[]
    for h in HEADERS:
        raw=subprocess.check_output(["git","show",REF+":"+BASE+h])
        (dest/h).write_bytes(raw)
        inputs.append({"evidence_commit":REF,"path":BASE+h,"sha256":hashlib.sha256(raw).hexdigest()})
    (PACKET/"receipts/probe-inputs.json").write_text(json.dumps(inputs,indent=2)+"\n")
    def run(n):
        command=[sys.executable,"-B",str(Path(__file__).resolve()),"--worker",str(n),"--jobs",str(args.jobs)]
        start=time.monotonic()
        with (PACKET/"receipts"/f"replay-{n}.log").open("w") as log:
            rc=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT).returncode
        (PACKET/"receipts"/f"replay-{n}.rc").write_text(str(rc)+"\n")
        return {"worker":n,"argv":command,"rc":rc,"seconds":round(time.monotonic()-start,3)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(run,(0,1,2)))
    (PACKET/"receipts/replay.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))
    return int(any(r["rc"] for r in results))

if __name__=="__main__": raise SystemExit(main())

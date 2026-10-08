#!/usr/bin/env python3
"""Replay scoped SRP review checks from any exact-head checkout."""
import argparse
from pathlib import Path
import shutil
import sys

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--packet", type=Path, required=True)
p.add_argument("--interfaces", type=int, choices=(1, 2), required=True)
p.add_argument("--mode", choices=("baseline", "mutants", "asan"), required=True)
p.add_argument("--jobs", type=int, default=3)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
from ctrl_build import CTRL, Tree
import fw_gtest
import srp_arms
import srp_mutants

tag = f"{a.mode}-if{a.interfaces}"
work = packet / "scratch" / tag
receipts = packet / "receipts" / tag
receipts.mkdir(parents=True, exist_ok=True)
lw = repo / "third_party/lwSRP"
print(f"Scoped SRP campaign: {tag}; jobs={a.jobs}", flush=True)
if a.mode == "mutants":
    names = {
        "feedback-intrapdu-lost", "feedback-advertise-copy-lost",
        "feedback-failed-copy-lost", "feedback-identity-copy-stale",
        "p11-supersession-kind-stale", "p11-reset-withdrawal-lost",
        "p11-postwithdrawal-kind-overwrite",
    }
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
    assert len(srp_mutants.DEFECTS) == len(names)
    failed = srp_mutants.campaign(work, lw, a.jobs, a.interfaces)
    for log in work.glob("*.log"):
        shutil.copyfile(log, receipts / log.name)
else:
    build = fw_gtest.Build(jobs=a.jobs, address_sanitizer=a.mode == "asan")
    tree = Tree(CTRL, work / "build", work / "reuse", build)
    failed = False
    suites = ("test_acmp_mbx.cpp", "srp_mbx.cpp", "srp_rx_retry.cpp", "srp_app.cpp", "srp_latency.cpp", "srp_walk.cpp")
    for suite in suites:
        outcome = srp_arms.arm_srp(tree, lw, a.interfaces, test=suite)
        (receipts / f"{suite}.log").write_text(outcome.log)
        print(f"{suite}: rc={outcome.rc}", flush=True)
        for line in outcome.log.splitlines():
            if "checks:" in line or "RESULT:" in line or "[FAIL]" in line:
                print(line, flush=True)
        failed |= bool(outcome.rc)
print(f"RESULT: {'FAIL' if failed else 'PASS'}", flush=True)
raise SystemExit(int(failed))

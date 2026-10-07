#!/usr/bin/env python3
"""Run the mailbox controls and the six round-4 fault probes in disposable builds."""
import argparse
import concurrent.futures
import importlib.util
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("root", type=Path)
ap.add_argument("packet", type=Path)
ap.add_argument("--jobs", type=int, default=2)
args = ap.parse_args()
root, packet = args.root.resolve(), args.packet.resolve()
spec = importlib.util.spec_from_file_location("mailbox_mutants", root / "tb/verilator/mbx/mutants.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
work = packet / "scratch/rtl-focus"
receipts = packet / "receipts"
bad = 0
for ifs in (1, 2):
    rtl = m.RTL
    if ifs == 2:
        import shutil
        rtl = work / "variant"
        shutil.copytree(m.RTL, rtl)
        m.variant(rtl, ifs)
    for host in (0, 1):
        name = f"control-if{ifs}-host{host}"
        rc, log = m.build_and_run(rtl, work / name, host, ifs)
        (receipts / f"rtl-{name}.log").write_text(log)
        print(name, "rc", rc, *[ln for ln in log.splitlines() if "checks:" in ln], flush=True)
        bad += rc != 0

def probe(arm):
    rtl = m.plant(arm, work)
    rc, log = m.build_and_run(rtl, work / arm.name, arm.host, arm.ifs)
    (receipts / f"rtl-{arm.name}.log").write_text(log)
    failures = [ln for ln in log.splitlines() if "[FAIL]" in ln and arm.needle in ln]
    caught = rc == 1 and bool(failures)
    return arm.name, rc, caught, failures

arms = [a for a in m.ARMS if "verdict-of-the-presented-interface" in a.name or "live-reads-interface-0-owed" in a.name]
assert len(arms) == 6
with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
    for name, rc, caught, failures in pool.map(probe, arms):
        print(name, "rc", rc, "CAUGHT" if caught else "ESCAPED", *failures, sep="\n", flush=True)
        bad += not caught
print("round-4 RTL probes:", len(arms), "faults; failures:", bad)
sys.exit(bool(bad))

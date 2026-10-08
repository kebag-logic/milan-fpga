#!/usr/bin/env python3
"""Foreground bounded review run; supply checkout and pinned compiler paths."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--verilator", type=Path, required=True)
a = p.parse_args()
repo = a.repo.resolve()
packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch" / "focused"
receipts = packet / "receipts" / "focused"
scratch.mkdir(parents=True, exist_ok=True)
receipts.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
version = subprocess.check_output([str(a.verilator), "--version"], text=True)
assert version.startswith("Verilator 5.050 "), version
(receipts / "compiler.txt").write_text(version)
spec = importlib.util.spec_from_file_location("campaign", repo / "tb/verilator/maap/mutants.py")
campaign = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(campaign)
source = (repo / "hdl/ieee1722/maap/KL_maap.sv").read_text()
assert {x[1] for x in campaign.MUTANTS} - {0} == {1, 2, 3, 4}

def case(row):
    name, item, anchor, replacement, failure = row
    work = scratch / name
    work.mkdir(exist_ok=True)
    rtl = work / "KL_maap.sv"
    if anchor:
        assert source.count(anchor) == 1, name
        rtl.write_text(source.replace(anchor, replacement))
    else:
        rtl.write_text(source)
    obj = work / "obj"
    if name == "seed_probe":
        cmd = [str(a.verilator), "--cc", "--exe", "--build", "-j", "4",
               "--public-flat-rw", "--top-module", "KL_maap", "-GCLK_FREQ_HZ_P=10000",
               "-Wno-fatal", "--Mdir", str(obj), str(rtl),
               str(packet / "scripts/seed_probe.cpp"), "-o", "probe"]
        binary = obj / "probe"
    else:
        cmd = ["make", "-j16", "-s", "-C", str(repo / "tb/verilator/maap"), "build",
               f"MAAP_RTL={rtl}", f"MDIR={obj}", f"VERILATOR={a.verilator}", "VERILATOR_JOBS=4"]
        binary = obj / "VKL_maap_sim"
    with (work / "build.log").open("w") as log:
        build = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=300)
    (receipts / f"{name}.build.rc").write_text(f"{build.returncode}\n")
    if build.returncode:
        return dict(name=name, item=item, build_rc=build.returncode, passed=False)
    with (receipts / f"{name}.log").open("w") as log:
        run = subprocess.run([str(binary)], cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)
    (receipts / f"{name}.rc").write_text(f"{run.returncode}\n")
    output = (receipts / f"{name}.log").read_text()
    passed = (run.returncode == 1 and f"[FAIL] {failure}" in output) if failure else (run.returncode == 0 and "0 failures" in output)
    result = dict(name=name, item=item, build_rc=0, run_rc=run.returncode, required_failure=failure, passed=passed)
    print(json.dumps(result), flush=True)
    return result

clean = case(("clean", 0, None, None, None))
assert clean["passed"], "clean control failed"
rows = list(campaign.MUTANTS) + [("seed_probe", 0, None, None, None)]
# Four concurrent builds, each capped at four workers. All are joined here.
with ThreadPoolExecutor(max_workers=4) as pool:
    results = [clean, *pool.map(case, rows)]
(receipts / "results.json").write_text(json.dumps(results, indent=2) + "\n")
passed = all(r["passed"] for r in results)
(receipts / "campaign.rc").write_text(f"{0 if passed else 1}\n")
print(f"focused campaign: {sum(r['passed'] for r in results)}/{len(results)} rows passed")
raise SystemExit(0 if passed else 1)

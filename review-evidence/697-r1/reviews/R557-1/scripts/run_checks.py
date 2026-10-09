#!/usr/bin/env python3
"""Run portable-core checks with bounded concurrency and separate receipts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("work", type=Path)
p.add_argument("receipts", type=Path)
a = p.parse_args()
root, work, receipts = a.repository.resolve(), a.work.resolve(), a.receipts.resolve()
work.mkdir(parents=True, exist_ok=True)
receipts.mkdir(parents=True, exist_ok=True)
(work / "temp").mkdir(exist_ok=True)
env = {k: v for k, v in os.environ.items() if not k.startswith("GTEST_")}
env.update(TMPDIR=str(work / "temp"), ASAN_OPTIONS="detect_leaks=1:halt_on_error=1", UBSAN_OPTIONS="halt_on_error=1", PYTHONDONTWRITEBYTECODE="1")
def run(name, command):
    start = time.monotonic()
    with (receipts / (name + ".log")).open("w") as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=590)
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    record = {"check": name, "rc": result.returncode, "seconds": round(time.monotonic()-start, 2), "command": command}
    print(json.dumps(record), flush=True)
    return record
results = []
# Each native build uses -j16. Build phases do not overlap, preserving the cap.
for name, cc, cxx, flags in [("gcc", "gcc", "g++", ["-DTSN_COVERAGE=ON"]), ("sanitizers", "clang", "clang++", ["-DTSN_SANITIZERS=ON"])]:
    directory = work / name
    record = run(name+"-configure", ["cmake", "-S", str(root), "-B", str(directory), "-DCMAKE_BUILD_TYPE=Debug", "-DCMAKE_C_COMPILER="+cc, "-DCMAKE_CXX_COMPILER="+cxx, *flags])
    results.append(record)
    if record["rc"] == 0:
        results.append(run(name+"-build", ["make", "-C", str(directory), "-j16"]))

def gcc_tests():
    for path in (work/"gcc").rglob("*.gcda"):
        path.unlink()
    group = [run("gcc-test", ["ctest", "--test-dir", str(work/"gcc"), "--output-on-failure", "-V", "-j1"])]
    if group[0]["rc"] == 0:
        group.append(run("coverage", ["python3", "scripts/coverage.py", str(work/"gcc")]))
    return group
def metadata():
    group = []
    for name, flags in [("check_boundary", ["--selftest"]), ("check_license", ["--selftest"]), ("traceability", ["--selftest"]), ("test_inventory", []), ("coverage_selftest", []), ("check_privacy", []), ("render_graphs", ["--output", str(work/"graphs")])]:
        group.append(run(name, ["python3", "scripts/"+name+".py", *flags]))
    return group
# Eight mutation workers plus four analysis files fit within sixteen active jobs.
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(lambda: [run("mutation", ["python3", "scripts/mutation.py", "--work", str(work/"mutations"), "--jobs", "8"])]), pool.submit(lambda: [run("static-analysis", ["python3", "scripts/static_analysis.py"])]), pool.submit(metadata)]
    for f in futures:
        results.extend(f.result())
with ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(gcc_tests), pool.submit(lambda: [run("sanitizers-test", ["ctest", "--test-dir", str(work/"sanitizers"), "--output-on-failure", "-V", "-j1"])])]
    for f in futures:
        results.extend(f.result())
(receipts/"checks.json").write_text(json.dumps(results, indent=2)+"\n")
raise SystemExit(any(r["rc"] for r in results))

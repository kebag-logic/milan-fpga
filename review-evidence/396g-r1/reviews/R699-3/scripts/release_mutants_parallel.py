#!/usr/bin/env python3
"""Run tb/tools/torture_release_mutants.py's MUTANTS table in parallel.

Usage: python3 -I release_mutants_parallel.py <export root> [jobs]

Same criteria as the driver's main(): a pristine self-test passes with OK;
each mutation (one exact single-occurrence replacement) must make the
self-test exit 1 with "FAIL: <named test> " in its stderr. Each mutant runs
on its own copy in its own temporary directory; the export is never written.
"""
import importlib.util
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
spec = importlib.util.spec_from_file_location("drv", root / "tb/tools/torture_release_mutants.py")
drv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drv)
source = root / "tb/tools/torture_campaign.py"
original = source.read_bytes()
text = original.decode("utf-8")


def selftest(body: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="r699-mut-") as d:
        candidate = Path(d) / source.name
        candidate.write_text(body, encoding="utf-8")
        return subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                              capture_output=True, text=True, timeout=900)


clean = selftest(text)
if clean.returncode != 0 or "\nOK\n" not in clean.stderr:
    print("FAIL: pristine planner self-test")
    sys.exit(1)
print("PASS: pristine planner self-test", flush=True)


def one(mutant):
    name, old, new, test = mutant
    if text.count(old) != 1:
        return f"INVALID: {name}: expected one source anchor"
    result = selftest(text.replace(old, new))
    if result.returncode == 1 and f"FAIL: {test} " in result.stderr:
        return f"KILLED: {name}: {test}"
    return f"SURVIVED: {name}: {test} rc={result.returncode}"


with ThreadPoolExecutor(jobs) as pool:
    lines = list(pool.map(one, drv.MUTANTS))
for line in lines:
    print(line)
counts = {k: sum(line.startswith(k) for line in lines) for k in ("KILLED", "SURVIVED", "INVALID")}
print(f"SUMMARY: {len(drv.MUTANTS)} mutants {counts}; export source unchanged: {source.read_bytes() == original}")
sys.exit(0 if counts["KILLED"] == len(drv.MUTANTS) else 1)

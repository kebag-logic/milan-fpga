#!/usr/bin/env python3
"""Run the release controls in parallel with the driver's criteria, recording each self-test's wall time.

Usage: python3 -I release_mutants_timed.py <export root> [jobs]

Same criteria as tb/tools/torture_release_mutants.py: a pristine self-test
passes with OK; each control (one exact single-occurrence replacement) must
make the self-test exit 1 with "FAIL: <named test> " in its stderr. Each
control runs on its own temporary copy; the export is never written. Prints
one line per control with its seconds, then the slowest ten and a summary;
the driver's own limit is 600 seconds per self-test. Exit 0 when every
control is killed.
"""
import importlib.util
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 6
sys.path.insert(0, str(root / "tb/tools"))
spec = importlib.util.spec_from_file_location("driver", root / "tb/tools/torture_release_mutants.py")
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
source = root / "tb/tools/torture_campaign.py"
original = source.read_bytes()
text = original.decode("utf-8")


def selftest(body: str) -> tuple:
    with tempfile.TemporaryDirectory(prefix="r5-timed-") as directory:
        candidate = Path(directory) / source.name
        candidate.write_text(body, encoding="utf-8")
        start = time.monotonic()
        result = subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                                capture_output=True, text=True, timeout=1800)
        return result, time.monotonic() - start


clean, seconds = selftest(text)
print(f"pristine rc={clean.returncode} {seconds:.0f}s {'OK' if clean.returncode == 0 and chr(10) + 'OK' + chr(10) in clean.stderr else 'FAIL'}",
      flush=True)


def one(mutant: tuple) -> tuple:
    name, old, new, test = mutant
    if text.count(old) != 1:
        return "INVALID", name, test, 0.0
    result, seconds = selftest(text.replace(old, new))
    killed = result.returncode == 1 and f"FAIL: {test} " in result.stderr
    return ("KILLED" if killed else "SURVIVED"), name, test, seconds


with ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(one, driver.MUTANTS))
for status, name, test, seconds in rows:
    print(f"{status}: {name}: {test} {seconds:.0f}s", flush=True)
print("SLOWEST:")
for status, name, test, seconds in sorted(rows, key=lambda row: -row[3])[:10]:
    print(f"    {seconds:.0f}s {status}: {name}")
counts = {k: sum(row[0] == k for row in rows) for k in ("KILLED", "SURVIVED", "INVALID")}
print(f"SUMMARY: {len(rows)} controls {counts}; slowest {max(row[3] for row in rows):.0f}s; "
      f"export source unchanged: {source.read_bytes() == original}")
sys.exit(0 if counts["KILLED"] == len(rows) else 1)

#!/usr/bin/env python3
"""Weaken the download-path digest check six ways; the self-test must fail.

Usage: mutate_download_auth.py <checkout> <scratch-dir>
Copies scripts/ci_rv32_sdk.py and its self-test into one scratch directory
per mutant (never edits the checkout), applies one textual weakening of the
extract() check, runs the complete self-test, and records KILLED (non-zero
exit) or SURVIVED, with the failing test names.
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

checkout, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
source = (checkout / "scripts/ci_rv32_sdk.py").read_text()
selftest = (checkout / "scripts/ci_rv32_sdk_selftest.py").read_text()
CHECK = ('    if actual != ARCHIVE_SHA256:\n'
         '        raise ValueError(f"SDK archive digest mismatch: {actual}")\n')
EXTRACTED = ('    subprocess.run(["tar", "-xJf", str(archive), "--strip-components=1",\n'
             '                    "-C", str(destination)], check=True)\n')
assert source.count(CHECK) == 1 and source.count(EXTRACTED) == 1
MUTANTS = {
    "delete the extract() digest check": source.replace(CHECK, ""),
    "compare only the first 8 hex digits": source.replace(
        CHECK, CHECK.replace("actual != ARCHIVE_SHA256",
                             "actual[:8] != ARCHIVE_SHA256[:8]")),
    "warn instead of refusing": source.replace(
        CHECK, '    if actual != ARCHIVE_SHA256:\n'
               '        print(f"SDK archive digest mismatch: {actual}")\n'),
    "compare the download with itself": source.replace(
        CHECK, CHECK.replace("actual != ARCHIVE_SHA256",
                             "actual != digest(archive)")),
    "check only after tar extraction": source.replace(CHECK, "").replace(
        EXTRACTED, EXTRACTED + CHECK),
    "skip the check for the download file name only": source.replace(
        CHECK, CHECK.replace("if actual != ARCHIVE_SHA256",
                             'if archive.name != f"{RELEASE}.tar.xz" and '
                             'actual != ARCHIVE_SHA256')),
}


def run(label, mutated):
    assert mutated != source, label
    work = scratch / label.replace(" ", "_").replace("(", "").replace(")", "")
    work.mkdir(parents=True)
    (work / "ci_rv32_sdk.py").write_text(mutated)
    (work / "ci_rv32_sdk_selftest.py").write_text(selftest)
    done = subprocess.run([sys.executable, "ci_rv32_sdk_selftest.py"], cwd=work,
                          capture_output=True, text=True, timeout=600)
    failed = sorted({line.split(" ")[1] for line in done.stderr.splitlines()
                     if line.startswith(("FAIL:", "ERROR:"))})
    return {"mutant": label, "selftest_exit": done.returncode,
            "verdict": "KILLED" if done.returncode else "SURVIVED",
            "failing_tests": failed}


baseline = subprocess.run([sys.executable, "scripts/ci_rv32_sdk_selftest.py"],
                          cwd=checkout, capture_output=True, text=True)
print(json.dumps({"baseline_exit": baseline.returncode,
                  "baseline": baseline.stderr.strip().splitlines()[-3:]}))
with ThreadPoolExecutor(max_workers=6) as pool:
    for result in pool.map(lambda item: run(*item), MUTANTS.items()):
        print(json.dumps(result))

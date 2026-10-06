"""Foreground coordinator; independent checks run concurrently and are all awaited.

Usage: python3 run-checks.py CHECKOUT PACKET
Uses the separately verified SDK at PACKET/scratch/sdk. No detached jobs.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:])
env = {**os.environ, "TMPDIR": str(packet / "scratch"),
       "MILAN_RV32_CC": str(packet / "scratch/sdk/bin/riscv32-linux-gcc"),
       "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1",
       "PYTHON_CPU_COUNT": "3", "MAKEFLAGS": "-j16"}
groups = [
    [("ctrl-campaign", ["sw/firmware/ctrl/test/test_ctrl_firmware.py", "--require-rv32", "--self-test"])],
    [("nvm-campaign", [str(packet / "scripts/nvm-campaign.py")])],
    [("coverage", ["sw/firmware/gtest/fw_coverage.py", "--check", "--jobs", "3"])],
    [("rv32-controls", ["sw/firmware/gtest/fw_rv32_selftest.py", "--require-rv32"]),
     ("ctrl-unit", ["sw/firmware/ctrl/test/test_ctrl_firmware.py", "--require-rv32"]),
     ("nvm-unit", ["sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py", "--require-rv32", "--jobs", "2"]),
     ("sdk-controls", ["scripts/ci_rv32_sdk_selftest.py"]),
     ("tally-controls", ["sw/firmware/gtest/tally_selftest.py", "--mutants"]),
     ("coverage-controls", ["sw/firmware/gtest/fw_coverage.py", "--selftest"]),
     ("ci-events-check", ["scripts/ci_events.py", "--check"]),
     ("ci-events-controls", ["scripts/ci_events.py", "--selftest"]),
     ("ci-scope-controls", ["scripts/ci_scope.py", "--selftest"]),
     ("docs-check", ["scripts/docs_check.py"]),
     ("doc-style", ["scripts/check_doc_style.py"]),
     ("em-dash", ["scripts/check_em_dash.py", "--base", "6714181d0c8a16e2983f85b724f4d688f5111835"]),
     ("toc-check", ["scripts/gen_toc.py", "--check"])]
]


def group_run(group):
    receipts = []
    for name, args in group:
        start = time.monotonic()
        argv = [sys.executable, *args]
        print(f"START {name}", flush=True)
        with (packet / f"scratch/{name}.log").open("w") as log:
            log.write("argv: " + json.dumps(argv) + "\n")
            log.flush()
            result = subprocess.run(argv, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                                    timeout=2400, check=False)
        record = {"name": name, "argv": argv, "rc": result.returncode,
                  "seconds": round(time.monotonic() - start, 3)}
        (packet / f"receipts/{name}.rc").write_text(str(result.returncode) + "\n")
        receipts.append(record)
        print(json.dumps(record), flush=True)
    return receipts


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(group_run, groups))
flat = [record for group in results for record in group]
(packet / "scratch/check-results.json").write_text(json.dumps(flat, indent=2) + "\n")
raise SystemExit(int(any(record["rc"] for record in flat)))

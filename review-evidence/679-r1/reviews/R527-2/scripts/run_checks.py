#!/usr/bin/env python3
"""Run independent focused checks concurrently, waiting for every child.

Usage: python3 scripts/run_checks.py CHECKOUT PACKET
The pinned SDK must already be installed at PACKET/scratch/sdk.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
base = dict(os.environ, TMPDIR=str(packet / "scratch"),
            PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1",
            MILAN_RV32_CC=str(packet / "scratch/sdk/bin/riscv32-linux-gcc"),
            MAKEFLAGS="-j16", VERILATOR_JOBS="2")

def run(name, argv, cpus=2):
    env = dict(base, PYTHON_CPU_COUNT=str(cpus))
    start = time.monotonic()
    print(f"START {name}", flush=True)
    raw = packet / "scratch" / (name + ".raw")
    with raw.open("w") as stream:
        stream.write("argv: " + json.dumps(argv) + "\n")
        stream.flush()
        result = subprocess.run(argv, cwd=root, env=env, stdout=stream,
                                stderr=subprocess.STDOUT, check=False)
    content = raw.read_text(errors="replace")
    for path, replacement in ((str(packet), "<packet>"), (str(root), "<checkout>"),
                              (str(Path.home()), "<home>")):
        content = content.replace(path, replacement)
    elapsed = time.monotonic() - start
    content += f"\nexit_code={result.returncode}\nelapsed_seconds={elapsed:.3f}\n"
    (packet / "receipts" / (name + ".log")).write_text(content)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(f"END {name} rc={result.returncode} seconds={elapsed:.1f}", flush=True)
    return result.returncode

def controls():
    tasks = [
        ("rv32-controls", ["python3", "sw/firmware/gtest/fw_rv32_selftest.py", "--require-rv32"]),
        ("sdk-controls", ["python3", "scripts/ci_rv32_sdk_selftest.py"]),
        ("tally-controls", ["python3", "sw/firmware/gtest/tally_selftest.py", "--mutants"]),
        ("coverage-controls", ["python3", "sw/firmware/gtest/fw_coverage.py", "--selftest"]),
        ("ci-events-check", ["python3", "scripts/ci_events.py", "--check"]),
        ("ci-scope-controls", ["python3", "scripts/ci_scope.py", "--selftest"]),
    ]
    return sum(run(name, args, 1) != 0 for name, args in tasks)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    futures = [
        pool.submit(run, "ctrl-campaign", ["python3", "sw/firmware/ctrl/test/test_ctrl_firmware.py",
                    "--require-rv32", "--self-test"], 4),
        pool.submit(run, "nvm-campaign", ["python3", str(packet / "scripts/nvm_campaign.py"),
                    str(root), "--require-rv32", "--self-test", "--jobs", "4"], 4),
        pool.submit(run, "coverage", ["python3", "sw/firmware/gtest/fw_coverage.py",
                    "--check", "--jobs", "2"], 2),
        pool.submit(controls),
    ]
    results = [future.result() for future in futures]
print("COMPLETE " + json.dumps(results), flush=True)
sys.exit(any(results))

#!/usr/bin/env python3
"""Run bounded, foreground composition checks; each command has its own receipt."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
group = sys.argv[2]
scratch = packet / "scratch"
(scratch / "tmp").mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch / "tmp"), PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
python = sys.executable
jobs = {
    "docs": [
        ("docs-check", ["scripts/docs_check.py"]),
        ("toc-check", ["scripts/gen_toc.py", "--check"]),
        ("toc-anchors", ["scripts/gen_toc.py", "--verify-anchors"]),
        ("toc-selftest", ["scripts/gen_toc.py", "--selftest"]),
        ("em-dash", ["scripts/check_em_dash.py", "--base", "af5be4710c3516cc247c353213d6939fa8d23f57"]),
        ("em-dash-selftest", ["scripts/check_em_dash.py", "--selftest"]),
        ("doc-paths", ["scripts/check_doc_paths.py"]),
        ("feature-status", ["scripts/check_feature_status.py"]),
        ("ci-events", ["scripts/ci_events.py", "--check"]),
        ("ci-events-selftest", ["scripts/ci_events.py", "--selftest"]),
        ("test-evidence", ["scripts/measure_test_evidence.py", "--check"]),
        ("mailbox-contract", ["sw/mailbox/gen_mailbox.py", "--check", "--crosscheck"]),
        ("mailbox-selftest", ["sw/mailbox/gen_mailbox.py", "--selftest"]),
    ],
    "firmware": [
        ("ctrl-firmware", ["sw/firmware/ctrl/test/test_ctrl_firmware.py", "--require-rv32", "--build-dir", str(scratch / "ctrl")]),
        ("firmware-coverage", ["sw/firmware/gtest/fw_coverage.py", "--check", "--jobs", "4", "--keep", str(scratch / "coverage")]),
        ("rv32-selftest", ["sw/firmware/gtest/fw_rv32_selftest.py", "--require-rv32"]),
        ("coverage-selftest", ["sw/firmware/gtest/fw_coverage.py", "--selftest", "--jobs", "1"]),
    ],
}
if group == "firmware":
    sys.path.insert(0, str(root / "sw/firmware/gtest"))
    import fw_rv32
    cc = fw_rv32.compiler()
    assert cc, "required RV32 compiler unavailable"
    env["MILAN_RV32_CC"] = cc

def one(item):
    name, args = item
    started = time.monotonic()
    with (packet / "receipts" / f"{name}.log").open("w") as output:
        result = subprocess.run([python, "-B", *args], cwd=root, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=580)
    (packet / "receipts" / f"{name}.rc").write_text(str(result.returncode) + "\n")
    portable_args = [arg.replace(str(scratch), "${PACKET}/scratch") for arg in args]
    row = {"name": name, "argv": ["python3", "-B", *portable_args], "rc": result.returncode, "seconds": round(time.monotonic() - started, 2)}
    print(json.dumps(row), flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(one, jobs[group]))
(packet / "receipts" / f"{group}-commands.json").write_text(json.dumps(rows, indent=2) + "\n")
sys.exit(any(row["rc"] for row in rows))

#!/usr/bin/env python3
"""Run permitted lightweight checks concurrently, retaining every return code."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = (Path(x).resolve() for x in sys.argv[1:3])
python = sys.argv[3] if len(sys.argv) > 3 else sys.executable
commands = [
 "ci_gate_workflows.py --check", "ci_events.py --check", "ci_events.py --selftest",
 "ci_gate_workflows_selftest.py", "ci_case_receipts_selftest.py", "ci_make_cases_selftest.py",
 "ci_maap_cases_selftest.py", "ci_capture_cases_selftest.py", "ci_suite_pieces_selftest.py",
 "ci_suite_collect_selftest.py", "ci_fail_fast_selftest.py", "ci_runtime_evidence_selftest.py",
 "ci_install_cache_selftest.py", "generate_ci_evidence_pins.py --check", "ci_workflow_plan_selftest.py",
 "ci_manifest_selftest.py", "check_wire_accountability.py --self-test", "docs_check.py",
 "check_doc_paths.py", "check_doc_style.py", "check_doc_style.py --selftest",
 "check_em_dash.py --base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6", "check_hygiene.py --check",
 "check_todo_ownership.py", "check_sh_idiom.py", "check_py_idiom.py", "check_py_idiom.py --selftest",
 "docs_inventory.py --check",
]
logs = packet / "gates"
logs.mkdir(exist_ok=True)
scratch = packet / "scratch" / "gates"
scratch.mkdir(parents=True, exist_ok=True)
env = {**os.environ, "TMPDIR": str(scratch), "PYTHONDONTWRITEBYTECODE": "1", "MAKEFLAGS": "-j16"}
def run(item):
    index, command = item
    argv = [python, "scripts/" + command.split()[0], *command.split()[1:]]
    stem = f"{index:02d}-" + command.replace(" ", "_").replace("/", "_")
    start = time.monotonic()
    with (logs / (stem + ".log")).open("w") as output:
        try:
            result = subprocess.run(argv, cwd=root, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=540)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            rc = 124
            output.write("\nREVIEW TIME LIMIT: 540 seconds\n")
    (logs / (stem + ".rc")).write_text(str(rc) + "\n")
    row = {"command": "python3 scripts/" + command, "rc": rc, "seconds": round(time.monotonic() - start, 2), "log": "gates/" + stem + ".log"}
    print(json.dumps(row), flush=True)
    return row
with ThreadPoolExecutor(max_workers=4) as pool:
    results = [future.result() for future in as_completed([pool.submit(run, item) for item in enumerate(commands, 1)])]
(packet / "gates.json").write_text(json.dumps(sorted(results, key=lambda row: row["log"]), indent=2) + "\n")
raise SystemExit(int(any(row["rc"] for row in results)))

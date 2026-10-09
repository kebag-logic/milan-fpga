#!/usr/bin/env python3
"""Run independent focused checks concurrently; join all foreground child processes."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
python = sys.argv[3] if len(sys.argv) > 3 else sys.executable
env = dict(os.environ, TMPDIR=str(packet / "scratch"), PYTHONDONTWRITEBYTECODE="1",
           PYTHON_CPU_COUNT="4", MAKEFLAGS="-j16", VERILATOR_JOBS="2")
checks = {
    "ooc": [python, "syn/ooc/ooc_tcl_selftest.py"],
    "recipe": [python, "syn/ooc/pp_baseline.py", "--selftest"],
    "recipe-mutants": [python, "syn/ooc/pp_baseline_mutants.py"],
    "resource": [python, "syn/ooc/pp_resource_gate.py", "--selftest"],
    "resource-mutants": [python, "-X", "cpu_count=4", "syn/ooc/pp_resource_gate_mutants.py"],
    "baseline": [python, "syn/ooc/pp_resource_gate.py", "check-baseline"],
    "reports": [python, "syn/ooc/pp_baseline_reports_selftest.py"],
    "builder-focused": [python, str(packet / "scripts/focused_builder.py"), str(root), str(packet / "scratch")],
}
for name, script, args in (
    ("docs", "scripts/docs_check.py", []),
    ("docs-selftest", "scripts/docs_check.py", ["--selftest"]),
    ("style", "scripts/check_doc_style.py", []),
    ("paths", "scripts/check_doc_paths.py", []),
    ("solution", "scripts/check_solution_docs.py", []),
    ("archive", "scripts/check_archive.py", []),
    ("toc", "scripts/gen_toc.py", ["--check"]),
    ("anchors", "scripts/gen_toc.py", ["--verify-anchors"]),
    ("status", "scripts/check_feature_status.py", ["--self-test"]),
    ("matrix", "docs/traceability/gen_module_matrix.py", ["--check"]),
    ("py-idiom", "scripts/check_py_idiom.py", []),
    ("hygiene", "scripts/check_hygiene.py", ["--check"]),
    ("sources", "scripts/pp_srcs.py", ["--check", "--selftest"]),
    ("em-dash", "scripts/check_em_dash.py", ["--base", "7c1b52bee26b497080ee22b1c1986109f80a5ee7"]),
):
    checks[name] = [python, script, *args]

def run(item):
    name, command = item
    begin = time.monotonic()
    with (packet / "receipts" / (name + ".log")).open("wb") as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=590)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    row = {"name": name, "argv": command, "rc": result.returncode, "seconds": round(time.monotonic()-begin, 2)}
    print(json.dumps(row), flush=True)
    return row

# Four resource-mutation workers plus at most five other children: below 16.
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    rows = list(pool.map(run, checks.items()))
(packet / "receipts/checks.json").write_text(json.dumps(rows, indent=2) + "\n")
sys.exit(int(any(row["rc"] for row in rows)))

#!/usr/bin/env python3
"""Run independent light checks concurrently while remaining in the foreground."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
python = sys.argv[2]
packet = Path(__file__).resolve().parents[1]
env = dict(os.environ, TMPDIR=str(packet / "scratch"), PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0",
           MILAN_LITEX_PYTHON=python)
commands = {
    "refusals": [python, "sw/builder/test_soc_options.py"],
    "byte-count-underflow": [python, str(packet / "scripts/byte_count_underflow.py"), str(root)],
    "independent-options": [python, str(packet / "scripts/independent_options.py"), str(root)],
    "builder-registration": [python, "-c", "import sys;sys.path.insert(0,'sw/builder');import test_builder as t;assert t._litex_python();t.test_soc_option_refusals()"],
    "doc-style": [sys.executable, "scripts/check_doc_style.py"],
    "python-idiom": [sys.executable, "scripts/check_py_idiom.py"],
    "solution-docs": [sys.executable, "scripts/check_solution_docs.py"],
    "docs-check": [sys.executable, "scripts/docs_check.py"],
}
def run(item):
    name, command = item
    with (packet / "receipts" / (name + ".log")).open("w") as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=300)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(name, result.returncode, flush=True)
    return {"name": name, "command": command, "rc": result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, commands.items()))
(packet / "scratch/focused-commands.json").write_text(json.dumps(results, indent=2))
assert all(row["rc"] == 0 for row in results), results

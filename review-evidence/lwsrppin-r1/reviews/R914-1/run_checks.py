#!/usr/bin/env python3
"""Run independent lightweight checks concurrently; keep a log and exit status per check."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
commands = {
    "twin-selftest": [sys.executable, "-B", "tb/verilator/milan_dp/twin_mrp.py", "--selftest"],
    "load": [sys.executable, "-B", "tb/verilator/ctrl_service_budget/load_grade.py", "--check"],
    "flip-1x1": [sys.executable, "-B", "tb/verilator/ctrl_service_budget/flip_grade.py", "--check", "--point", "1x1/1if"],
    "flip-8x8": [sys.executable, "-B", "tb/verilator/ctrl_service_budget/flip_grade.py", "--check", "--point", "8x8/1if"],
    "diagram": [sys.executable, "-B", "docs/diagrams/submodule_boundaries.gen.py", "--check"],
    "diagram-selftest": [sys.executable, "-B", "docs/diagrams/submodule_boundaries.gen.py", "--selftest"],
    "png": [sys.executable, "-B", "scripts/check_diagram_pngs.py"],
    "pins": [sys.executable, "-B", "scripts/check_submodule_docs.py"],
}
def run(item):
    name, command = item
    with (packet / (name + ".log")).open("w") as log:
        result = subprocess.run(command, cwd=root, stdout=log, stderr=subprocess.STDOUT,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    (packet / (name + ".rc")).write_text(str(result.returncode) + "\n")
    return name, result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for result in pool.map(run, commands.items()):
        print(*result, flush=True)

#!/usr/bin/env python3
"""Run mutant trees against every owner control and the whole test.

Usage: python3 -I matrix.py HEAD_SCRIPTS TREES_DIR JOBS NAME [NAME ...]

Uses the head's own run_mutant (scripts/process_test_support.py) and its
OWNER_CONTROLS, so each run is exactly what --matrix runs: a new session, a
file for output, 150 s per control and 400 s for the whole test. TREES_DIR/NAME
is a tree made by mktree.py. One line per run: name / control: green|red|cut.
"""
import ast
import concurrent.futures
import sys
from pathlib import Path

head = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(head))
from process_test_support import run_mutant  # noqa: E402

source = (head / "test_suite_cancellation.py").read_text()
controls = next(ast.literal_eval(node.value) for node in ast.parse(source).body
                if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "OWNER_CONTROLS")
trees, jobs, names = Path(sys.argv[2]).resolve(), int(sys.argv[3]), sys.argv[4:]
runs = [(name, control) for name in names for control in (*controls, None)]
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(lambda run: run_mutant(trees / run[0], run[1]), runs))
for (name, control), (status, seconds, output) in zip(runs, results):
    lines = [line for line in output.splitlines() if line.strip()]
    verdict = "cut" if status is None else "red" if status else "green"
    print(f"{name} / {control or 'whole'}: {verdict} rc {status} {seconds:.1f} s: "
          f"{lines[-1][:300] if lines else ''}", flush=True)
for name in names:
    reds = [control or "whole" for (n, control), (status, _s, _o) in zip(runs, results) if n == name and status != 0]
    print(f"SUMMARY {name}: red on {len(reds)} of {len(controls) + 1}: {', '.join(reds) or 'none'}", flush=True)

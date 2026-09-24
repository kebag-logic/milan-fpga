#!/usr/bin/env python3
"""Run the assigned read-only gates in the foreground, preserving every exit."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
BASE = "573f0052a0e4412e81f0845438fcec2086ce5d55"
GATES = [
    ("docs-check", ["python3", "scripts/docs_check.py"]),
    ("docs-check-no-git", ["env", "GIT_DIR=/dev/null", "python3", "scripts/docs_check.py"]),
    ("doc-style", ["python3", "scripts/check_doc_style.py"]),
    ("toc", ["python3", "scripts/gen_toc.py", "--check"]),
    ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
    ("module-matrix", ["python3", "docs/traceability/gen_module_matrix.py", "--check"]),
    ("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
    ("rtl-source-lists", ["python3", "scripts/check_rtl_source_lists.py"]),
    ("cpp-idiom", ["python3", "scripts/check_cpp_idiom.py"]),
    ("py-idiom", ["python3", "scripts/check_py_idiom.py"]),
    ("diff-check", ["git", "diff", "--check"]),
]
if "--committed" in sys.argv:
    GATES = [("em-dash", ["python3", "scripts/check_em_dash.py", "--base", BASE]),
             ("diff-check-committed", ["git", "diff", "--check", BASE, "HEAD"])]
results = []
for name, command in GATES:
    started = time.monotonic()
    with (OUT / f"{name}.log").open("w") as log:
        completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                   check=False, env=os.environ.copy())
    result = dict(name=name, command=shlex.join(command), rc=completed.returncode,
                  seconds=round(time.monotonic() - started, 3))
    results.append(result)
    suffix = "-committed" if "--committed" in sys.argv else ""
    (OUT / f"gates{suffix}.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{name}: rc={completed.returncode}, seconds={result['seconds']}", flush=True)
    if completed.returncode:
        print((OUT / f"{name}.log").read_text()[-5000:], flush=True)
raise SystemExit(1 if any(r["rc"] for r in results) else 0)

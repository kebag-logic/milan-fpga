"""Run the authorized focused gates, retaining exact commands and raw output."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
commands = [
    ("ci-events-check", ["python3", "-B", "scripts/ci_events.py", "--check"]),
    ("ci-events-selftest", ["python3", "-B", "scripts/ci_events.py", "--selftest"]),
    ("docs-check", ["python3", "-B", "scripts/docs_check.py"]),
    ("toc-check", ["python3", "-B", "scripts/gen_toc.py", "--check"]),
    ("doc-paths", ["python3", "-B", "scripts/check_doc_paths.py"]),
    ("em-dash", ["python3", "-B", "scripts/check_em_dash.py", "--base",
                 "b17580b91deb11f3441dfc5d7f9fafe539d929b8"]),
    ("doc-style", ["python3", "-B", "scripts/check_doc_style.py"]),
    ("python-idiom", ["python3", "-B", "scripts/check_py_idiom.py"]),
    ("python-idiom-selftest", ["python3", "-B", "scripts/check_py_idiom.py", "--selftest"]),
    ("hygiene", ["python3", "-B", "scripts/check_hygiene.py", "--check"]),
    ("todo-ownership", ["python3", "-B", "scripts/check_todo_ownership.py"]),
    ("fail-fast", ["python3", "-B", "scripts/measure_fail_fast.py", "--check"]),
    ("feature-status", ["python3", "-B", "scripts/check_feature_status.py"]),
    ("lint", ["python3", "-B", "scripts/lint_rtl.py", "--check"]),
    ("diff-check", ["git", "diff", "--check"]),
]
env = dict(os.environ, MAKEFLAGS="-j8", CMAKE_BUILD_PARALLEL_LEVEL="8")
results = []
for name, command in commands:
    start = time.monotonic()
    with (out / f"{name}.log").open("w") as log:
        proc = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
    result = {"name": name, "command": command, "cwd": str(root), "exit": proc.returncode,
              "elapsed_seconds": round(time.monotonic() - start, 3)}
    results.append(result)
    (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(name, proc.returncode, result["elapsed_seconds"], flush=True)
raise SystemExit(int(any(result["exit"] for result in results)))

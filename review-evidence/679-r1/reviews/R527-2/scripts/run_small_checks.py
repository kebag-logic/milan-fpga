#!/usr/bin/env python3
"""Run focused validation contracts and documentation gates; no source edits."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
doc_python = sys.argv[3] if len(sys.argv) > 3 else sys.executable
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHON_CPU_COUNT="1",
           TMPDIR=str(packet / "scratch"))
tasks = [
    ("control-sensitivity", [sys.executable, str(packet / "scripts/control_sensitivity.py"), str(root), str(packet)]),
    ("ci-events-controls", [sys.executable, "scripts/ci_events.py", "--selftest"]),
    ("docs-check", [doc_python, "scripts/docs_check.py"]),
    ("doc-style", [doc_python, "scripts/check_doc_style.py"]),
    ("em-dash", [doc_python, "scripts/check_em_dash.py", "--base", "6714181d0c8a16e2983f85b724f4d688f5111835"]),
    ("toc", [doc_python, "scripts/gen_toc.py", "--check"]),
    ("diff-check", ["git", "diff", "--check", "6714181d0c8a16e2983f85b724f4d688f5111835..HEAD"]),
]
codes = []
for name, args in tasks:
    start = time.monotonic()
    result = subprocess.run(args, cwd=root, env=env, capture_output=True, text=True, check=False)
    content = "argv: " + json.dumps(args) + "\n" + result.stdout + result.stderr
    content += f"\nexit_code={result.returncode}\nelapsed_seconds={time.monotonic()-start:.3f}\n"
    for prefix, value in ((str(packet), "<packet>"), (str(root), "<checkout>"),
                          (str(Path.home()), "<home>"), (doc_python, "<docs-python>")):
        content = content.replace(prefix, value)
    (packet / "receipts" / (name + ".log")).write_text(content)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    print(f"{name}: rc={result.returncode}", flush=True)
    codes.append(result.returncode)
sys.exit(any(codes))

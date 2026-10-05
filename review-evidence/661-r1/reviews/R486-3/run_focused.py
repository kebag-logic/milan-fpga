#!/usr/bin/env python3
"""Foreground coordinator: independent focused checks, at most four at once."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
packet = Path(__file__).resolve().parent
(packet / "receipts").mkdir(exist_ok=True)
(packet / "scratch" / "tmp").mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0",
           TMPDIR=str(packet / "scratch" / "tmp"), GIT_NO_REPLACE_OBJECTS="1")
if (packet / "scratch" / "markdown").is_dir():
    env["PYTHONPATH"] = str(packet / "scratch" / "markdown")
checks = [
    ("docs-check", ["python3", "scripts/docs_check.py"]),
    ("doc-style", ["python3", "scripts/check_doc_style.py"]),
    ("doc-style-controls", ["python3", "scripts/check_doc_style.py", "--selftest"]),
    ("toc", ["python3", "scripts/gen_toc.py", "--check"]),
    ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", "fa450d301805881ad713b67521477bf042ddadfd"]),
    ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
    ("wire-accountability", ["python3", "scripts/check_wire_accountability.py", "--self-test"]),
    ("feature-status", ["python3", "scripts/check_feature_status.py", "--self-test"]),
    ("wire-truth", ["python3", "tb/tools/avtp_wire_truth.py", "--self-test"]),
    ("diff-check", ["git", "diff", "--check", "506d91dbeeba585d72d2e80d92fca799c719f8ee..HEAD"]),
]


def run(check):
    name, command = check
    start = time.monotonic()
    with (packet / "receipts" / (name + ".log")).open("wb") as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    row = {"name": name, "command": command, "rc": result.returncode,
           "seconds": round(time.monotonic() - start, 3)}
    print(json.dumps(row), flush=True)
    return row


selected = set(sys.argv[2:])
if selected:
    assert selected <= {name for name, _ in checks}
    checks = [row for row in checks if row[0] in selected]
with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks))
(packet / "receipts" / ("renderer-results.json" if selected else "focused-results.json")).write_text(json.dumps(results, indent=2) + "\n")
raise SystemExit(1 if any(r["rc"] for r in results) else 0)

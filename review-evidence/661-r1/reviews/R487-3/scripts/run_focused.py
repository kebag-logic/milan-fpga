#!/usr/bin/env python3
"""Run bounded, concurrent documentation checks; join every child before exit."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time
root = Path(sys.argv[1]).resolve()
packet = Path(sys.argv[2]).resolve()
python = sys.argv[3] if len(sys.argv) > 3 else sys.executable
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
receipts = packet / "receipts"
receipts.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch), GIT_NO_REPLACE_OBJECTS="1")
cases = {
    "docs-check": [python, "scripts/docs_check.py"],
    "docs-scrub-controls": [python, "scripts/docs_check.py", "--selftest"],
    "doc-style": [python, "scripts/check_doc_style.py"],
    "doc-style-controls": [python, "scripts/check_doc_style.py", "--selftest"],
    "contents": [python, "scripts/gen_toc.py", "--check"],
    "em-dash-source": [python, "scripts/check_em_dash.py", "--base", "506d91dbeeba585d72d2e80d92fca799c719f8ee"],
    "em-dash-dev": [python, "scripts/check_em_dash.py", "--base", "fa450d301805881ad713b67521477bf042ddadfd"],
    "doc-paths": [python, "scripts/check_doc_paths.py"],
    "wire-accountability": [python, "scripts/check_wire_accountability.py", "--self-test"],
    "feature-status": [python, "scripts/check_feature_status.py", "--self-test"],
    "diff-whitespace": ["git", "diff", "--check", "506d91dbeeba585d72d2e80d92fca799c719f8ee..HEAD"],
}
def run(item):
    name, command = item
    started = time.monotonic()
    with (receipts / (name + ".log")).open("wb") as log:
        try:
            rc = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540).returncode
        except subprocess.TimeoutExpired:
            log.write(b"TIMEOUT after 540 seconds\n")
            rc = 124
    seconds = round(time.monotonic() - started, 3)
    (receipts / (name + ".rc")).write_text(str(rc) + "\n")
    portable = ["python3", *command[1:]] if command[0] == python else command
    result = dict(name=name, command=portable, rc=rc, seconds=seconds)
    print(json.dumps(result), flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, cases.items()))
(receipts / "focused-results.json").write_text(json.dumps(results, indent=2) + "\n")
sys.exit(int(any(row["rc"] for row in results)))

#!/usr/bin/env python3
"""Run the requested documentation checks concurrently; retain separate receipts."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()
a.out.mkdir(parents=True, exist_ok=True)
jobs = {
    "docs-check": ["scripts/docs_check.py"],
    "em-dash": ["scripts/check_em_dash.py", "--base", "6bfeeb132fa0b1ad8a5b957446c66a498e633af7"],
    "toc-check": ["scripts/gen_toc.py", "--check"],
    "toc-anchors": ["scripts/gen_toc.py", "--verify-anchors"],
    "doc-style": ["scripts/check_doc_style.py"],
    "doc-paths": ["scripts/check_doc_paths.py"],
}
def run(item):
    name, args = item
    command = [sys.executable, *args]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    with (a.out / (name + ".log")).open("w") as log:
        log.write("command: python3 " + " ".join(args) + "\n")
        log.flush()
        try:
            result = subprocess.run(command, cwd=a.repo, env=env, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=540, check=False)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            log.write("TIMEOUT after 540 seconds\n")
            rc = 124
    (a.out / (name + ".rc")).write_text(str(rc) + "\n")
    return {"name": name, "command": ["python3", *args], "rc": rc}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run, jobs.items()))
(a.out / "docs-summary.json").write_text(json.dumps(results, indent=2) + "\n")
for row in results:
    print(row["name"], "rc", row["rc"])
sys.exit(any(row["rc"] != 0 for row in results))

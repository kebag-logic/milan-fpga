#!/usr/bin/env python3
"""Run only the documentation and interface checks used by R509-1."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("output", type=Path)
p.add_argument("--only", nargs="+", help="Run only named checks, for a dependency recheck")
a = p.parse_args()
repo, out = a.repository.resolve(), a.output.resolve()
out.mkdir(parents=True, exist_ok=True)
tmp = out.parent / "scratch" / "check-tmp"
tmp.mkdir(parents=True, exist_ok=True)
commands = [
    ("matrix", ["docs/traceability/gen_module_matrix.py", "--check"]),
    ("wire", ["scripts/check_wire_accountability.py", "--self-test"]),
    ("status", ["scripts/check_feature_status.py"]),
    ("docs", ["scripts/docs_check.py"]),
    ("style", ["scripts/check_doc_style.py"]),
    ("paths", ["scripts/check_doc_paths.py"]),
    ("solution", ["scripts/check_solution_docs.py"]),
    ("toc", ["scripts/gen_toc.py", "--check"]),
    ("anchors", ["scripts/gen_toc.py", "--verify-anchors"]),
    ("em-dash", ["scripts/check_em_dash.py", "--base", "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"]),
    ("mailbox-drift", ["sw/mailbox/gen_mailbox.py", "--check", "--crosscheck"]),
]
if a.only:
    unknown = set(a.only) - {name for name, _ in commands}
    if unknown:
        p.error("unknown check names: " + ", ".join(sorted(unknown)))
    commands = [item for item in commands if item[0] in a.only]

def run(item):
    name, tail = item
    command = [sys.executable, *tail]
    start = time.monotonic()
    env = dict(os.environ, TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
    with (out / (name + ".log")).open("w") as log:
        log.write("Command: python3 " + " ".join(tail) + "\n")
        log.flush()
        result = subprocess.run(command, cwd=repo, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=300)
    (out / (name + ".rc")).write_text(str(result.returncode) + "\n")
    return dict(name=name, command=["python3", *tail], rc=result.returncode,
                elapsed_seconds=round(time.monotonic() - start, 3))

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands))
(out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
for result in results:
    print(result["name"], "rc", result["rc"])
sys.exit(int(any(r["rc"] for r in results)))

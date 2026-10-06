#!/usr/bin/env python3
"""Run independent, documentation-focused checks; no exhaustive banks or host runner."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
python = str(packet / "scratch/venv/bin/python")
jobs = [
    ["scripts/docs_check.py"],
    ["scripts/check_doc_style.py"],
    ["scripts/check_doc_paths.py"],
    ["scripts/check_solution_docs.py"],
    ["scripts/check_feature_status.py"],
    ["docs/traceability/gen_module_matrix.py", "--check"],
    ["scripts/check_wire_accountability.py", "--self-test"],
    ["scripts/gen_toc.py", "--check"],
    ["scripts/gen_toc.py", "--verify-anchors"],
    ["scripts/check_em_dash.py", "--base", "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"],
    ["sw/mailbox/gen_mailbox.py", "--check"],
]


def one(item):
    i, args = item
    name = f"focused-{i:02}"
    tmp = packet / "scratch" / name
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
    start = time.monotonic()
    with (packet / "receipts" / (name + ".log")).open("w") as out:
        out.write("COMMAND: python3 " + " ".join(args) + "\n")
        out.flush()
        try:
            result = subprocess.run([python, *args], cwd=root, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=540)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            out.write("TIMEOUT after 540 seconds\n")
            rc = 124
    (packet / "receipts" / (name + ".rc")).write_text(str(rc) + "\n")
    return {"id": name, "command": ["python3", *args], "rc": rc, "elapsed_seconds": round(time.monotonic()-start, 3)}


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(one, enumerate(jobs, 1)))
(packet / "receipts/focused-results.json").write_text(json.dumps(results, indent=2) + "\n")
for result in results:
    print(result["id"], result["rc"], " ".join(result["command"]))
sys.exit(any(r["rc"] for r in results))

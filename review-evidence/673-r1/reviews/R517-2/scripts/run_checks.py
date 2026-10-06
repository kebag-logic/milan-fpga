#!/usr/bin/env python3
"""Join bounded independent read-only checks in the foreground. Usage: REPO PACKET."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo, packet = (Path(p).resolve() for p in sys.argv[1:])
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(packet / "scratch"))
base = "bd884631684ccf5060339efa92263d5c3e5c262c"
checks = {
    "focused-probe": [sys.executable, str(packet / "scripts/focused_probe.py"), str(repo)],
    "evidence-check": [sys.executable, "scripts/measure_test_evidence.py", "--check"],
    "evidence-selftest": [sys.executable, "scripts/measure_test_evidence.py", "--selftest"],
    "shell-syntax": ["bash", "-n", "scripts/run_all_suites.sh"],
    "shards-selftest": [sys.executable, "scripts/suite_shards.py", "--selftest"],
    "ci-policy": [sys.executable, "scripts/ci_events.py", "--check"],
    "docs-check": [sys.executable, "scripts/docs_check.py"],
    "doc-paths": [sys.executable, "scripts/check_doc_paths.py"],
    "doc-style": [sys.executable, "scripts/check_doc_style.py"],
    "toc-check": [sys.executable, "scripts/gen_toc.py", "--check"],
    "em-dash": [sys.executable, "scripts/check_em_dash.py", "--base", base],
    "diff-check": ["git", "diff", "--check", base, "HEAD"],
}

def run(item):
    name, command = item
    started = time.monotonic()
    with (packet / "receipts" / (name + ".log")).open("wb") as output:
        try:
            result = subprocess.run(command, cwd=repo, env=env, stdout=output,
                                    stderr=subprocess.STDOUT, timeout=300)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            rc = 124
    (packet / "receipts" / (name + ".rc")).write_text(str(rc) + "\n")
    portable = [a.replace(str(repo), "$REPO").replace(str(packet), "$PACKET") for a in command]
    portable[0] = "python3" if command[0] == sys.executable else portable[0]
    return {"name": name, "command": portable, "rc": rc,
            "seconds": round(time.monotonic() - started, 3)}

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, checks.items()))
(packet / "receipts/checks.json").write_text(json.dumps(results, indent=2) + "\n")
for result in results:
    print(f"{result['name']}: rc={result['rc']}; seconds={result['seconds']}")
sys.exit(int(any(result["rc"] for result in results)))

#!/usr/bin/env python3
"""Foreground runner, maximum four concurrent lightweight checks.

Usage: python3 run_review_checks.py CHECKOUT EVIDENCE_ROOT MARKDOWN_PYTHON
Writes each raw stdout/stderr receipt and exit code beside this script.
All disposable probe outputs go under scratch/; never runs hardware commands.
"""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    repo, evidence, md_python = map(Path, sys.argv[1:])
    packet = Path(__file__).resolve().parent
    repo, evidence = repo.resolve(), evidence.resolve()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_OPTIONAL_LOCKS="0")
    jobs = {
        "receipt-audit": [sys.executable, str(packet / "audit_receipts.py"), str(evidence), str(repo)],
        "offline-probes": [sys.executable, str(packet / "offline_probes.py"), str(evidence), str(packet / "scratch/probes")],
        "integrity-initial": [sys.executable, str(packet / "verify_checkout.py"), str(repo)],
        "documentation": [str(md_python), "scripts/docs_check.py"],
        "style": [str(md_python), "scripts/check_doc_style.py"],
        "contents": [str(md_python), "scripts/gen_toc.py", "--check"],
        "punctuation": [str(md_python), "scripts/check_em_dash.py", "--base", "fa450d301805881ad713b67521477bf042ddadfd"],
        "paths": [str(md_python), "scripts/check_doc_paths.py"],
        "product-policy": [sys.executable, "scripts/check_baremetal_only.py", "--check"],
        "whitespace": ["git", "diff", "--check", "fa450d301805881ad713b67521477bf042ddadfd", "bef8dd7036f711bf286929fa4cba6bf724c7118d"],
    }
    def run(item):
        name, command = item
        with (packet / (name + ".log")).open("wb") as log:
            try:
                r = subprocess.run(command, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=480)
                rc = r.returncode
            except subprocess.TimeoutExpired:
                log.write(b"TIMEOUT\n")
                rc = 124
        (packet / (name + ".rc")).write_text(str(rc) + "\n")
        return {"check": name, "exit": rc}
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, jobs.items()))
    for result in results:
        print(json.dumps(result))
    return int(any(x["exit"] for x in results))


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run independent offline checks concurrently; no hardware or remote writes.

Usage: run_checks.py <candidate> <published-author-evidence> <docs-python>
All generated fixtures and dependencies belong under scratch/.
"""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, evidence = (Path(s).resolve() for s in sys.argv[1:3])
# Preserve the environment launcher path: resolving its symlink bypasses it.
docpy = Path(sys.argv[3]).absolute()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch" / "checks"
scratch.mkdir(parents=True, exist_ok=True)
receipts = packet / "receipts"
receipts.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1",
           OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", GIT_NO_REPLACE_OBJECTS="1",
           GIT_OPTIONAL_LOCKS="0")
jobs = []
for name, args in [
    ("docs-check", ["scripts/docs_check.py"]),
    ("doc-style", ["scripts/check_doc_style.py"]),
    ("doc-paths", ["scripts/check_doc_paths.py"]),
    ("toc-check", ["scripts/gen_toc.py", "--check"]),
    ("toc-anchors", ["scripts/gen_toc.py", "--verify-anchors"]),
    ("em-dash", ["scripts/check_em_dash.py", "--base", "c20c85bd"]),
]:
    jobs.append((name, [str(docpy), "-B", *args], root, None))
jobs.append(("diff-check", ["git", "diff", "--check", "c20c85bd", "HEAD"], root, None))
for name, script, mode, args in [
    ("tone-presence", "tone_points_b16.py", "control", []),
    ("alignment", "align_b16.py", "control", ["synth", "-", "-"]),
    ("loop-decoder", "dloop_b16.py", "control", []),
    ("b6-controls", "b6_thdn.py", "controls", []),
    ("b9-controls", "b9_thdn.py", "controls", []),
]:
    out = scratch / (name + ".json")
    jobs.append((name, [sys.executable, "-B", str(evidence / "tools" / script), mode, *args, str(out)], scratch, out))


def run(job):
    name, cmd, cwd, out = job
    start = time.monotonic()
    with (receipts / (name + ".log")).open("wb") as log:
        try:
            rc = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=570).returncode
        except subprocess.TimeoutExpired:
            log.write(b"\nTIMEOUT after 570 seconds\n")
            rc = 124
    (receipts / (name + ".rc")).write_text(str(rc) + "\n")
    if out and out.exists():
        (receipts / out.name).write_bytes(out.read_bytes())
    # Command paths are supplied as arguments, never published as host paths.
    return {"check": name, "rc": rc, "seconds": round(time.monotonic() - start, 3)}


if "--failed-only" in sys.argv[4:]:
    jobs = [j for j in jobs if (receipts / (j[0] + ".rc")).exists()
            and (receipts / (j[0] + ".rc")).read_text().strip() != "0"]
    for name, *_ in jobs:
        for suffix in (".rc", ".log"):
            old = receipts / (name + suffix)
            old.rename(receipts / (name + "-initial" + suffix))
with ThreadPoolExecutor(max_workers=6) as pool:
    result = list(pool.map(run, jobs))
(receipts / ("checks-retry.json" if "--failed-only" in sys.argv[4:] else "checks.json")).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
sys.exit(int(any(r["rc"] != 0 for r in result)))

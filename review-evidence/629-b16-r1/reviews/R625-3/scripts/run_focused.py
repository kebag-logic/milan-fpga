#!/usr/bin/env python3
"""Foreground focused checks, with up to eight concurrent child processes.

Usage: python3 run_focused.py REPO EVIDENCE_PACKET OUTPUT_PACKET MARKDOWN_PYTHON
All disposable files stay in OUTPUT_PACKET/scratch. No network or hardware calls.
"""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo, evidence, out = [Path(x).resolve() for x in sys.argv[1:4]]
# Resolving the interpreter symlink bypasses its virtual environment.
md = Path(sys.argv[4]).absolute()
receipts = out / "receipts"
scratch = out / "scratch"
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
scripts = evidence / "tools"
py = sys.executable
jobs = {
    "figures-controls": [py, "-I", scripts / "r3_check_controls.py", scripts / "check_b16_figures.py", page, evidence,
                         scratch / "figures-controls", receipts / "figures-controls.json"],
    "b0-reproduction": [py, "-I", scripts / "r2_b0_receipt.py", evidence, receipts / "b0-recomputed.json"],
    "alignment-controls": [py, "-I", scripts / "align_b16.py", "control", "synth", "-", "-", receipts / "alignment-controls.json"],
    "presence-controls": [py, "-I", scripts / "tone_points_b16.py", "control", receipts / "presence-controls.json"],
    "grade-controls": [py, "-I", scripts / "b9_thdn.py", "controls", receipts / "grade-controls.json"],
    "loop-controls": [py, "-I", scripts / "dloop_b16.py", "control", receipts / "loop-controls.json"],
    "docs-check": [md, "scripts/docs_check.py"],
    "doc-style": [md, "scripts/check_doc_style.py"],
    "doc-paths": [md, "scripts/check_doc_paths.py"],
    "toc-check": [md, "scripts/gen_toc.py", "--check"],
    "toc-anchors": [md, "scripts/gen_toc.py", "--verify-anchors"],
    "em-dash": [md, "scripts/check_em_dash.py", "--base", "c20c85bd"],
    "diff-check": ["git", "diff", "--check", "c20c85bd", "HEAD"],
}
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1",
           PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch))


def public(text):
    for value, token in [(str(evidence), "<evidence>"), (str(out), "<review-packet>"),
                         (str(repo), "<repo>"), (str(md), "<markdown-python>"), (py, "python3")]:
        text = text.replace(value, token)
    return text


def run(item):
    name, cmd = item
    start = time.monotonic()
    proc = subprocess.run([str(x) for x in cmd], cwd=repo, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=540)
    (receipts / (name + ".log")).write_text(public(proc.stdout.decode(errors="replace")))
    (receipts / (name + ".rc")).write_text(str(proc.returncode) + "\n")
    result = {"check": name, "command": [public(str(x)) for x in cmd], "rc": proc.returncode,
              "seconds": round(time.monotonic() - start, 3)}
    print(json.dumps(result), flush=True)
    return result


if len(sys.argv) > 5:
    selected = set(sys.argv[5].split(","))
    jobs = {name: command for name, command in jobs.items() if name in selected}
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, jobs.items()))
(receipts / ("focused-retry.json" if len(sys.argv) > 5 else "focused-results.json")).write_text(json.dumps(results, indent=2) + "\n")
sys.exit(0 if all(x["rc"] == 0 for x in results) else 1)

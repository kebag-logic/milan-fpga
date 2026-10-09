#!/usr/bin/env python3
"""Replay published review probes without changing their bytes."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
work = packet / "scratch/prior-replay"
tree = work / "tree"
tree.mkdir(parents=True, exist_ok=True)
for name in subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).decode().split("\0"):
    if name:
        target = tree / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
           TSN_CLANG=str(packet / "scratch/clang18/usr/lib/llvm-18/bin/clang"),
           LD_LIBRARY_PATH=str(packet / "scratch/clang18/usr/lib/x86_64-linux-gnu"))
out = packet / "receipts/prior-replay"
out.mkdir(exist_ok=True)
cases = [
    ("r556-3-comments", "R556-3/scripts/comment_probes.py", [str(tree)]),
    ("r556-3-needles", "R556-3/scripts/needle_probes.py", [str(tree)]),
    ("r556-4-comments", "R556-4/scripts/comment_bypass_probe.py", [str(tree), str(work / "bypass")]),
    ("r556-4-needles", "R556-4/scripts/needle_default_fragments.py", [str(tree)]),
    ("r557-4-comments", "R557-4/scripts/full_comment_bypass.py", ["--repo", str(tree), "--work", str(work / "r557"), "--output", str(out / "r557-4-comments.json")]),
]

def run(item):
    name, relative, args = item
    script = packet / "scripts/prior" / relative
    result = subprocess.run([sys.executable, str(script), *args], env=env, capture_output=True, text=True, cwd=work)
    (out / (name + ".log")).write_text(result.stdout + result.stderr)
    (out / (name + ".rc")).write_text(str(result.returncode) + "\n")
    row = {"name": name, "script": relative, "sha256": hashlib.sha256(script.read_bytes()).hexdigest(), "rc": result.returncode}
    print(row, flush=True)
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, cases))
(out / "results.json").write_text(json.dumps(results, indent=2) + "\n")

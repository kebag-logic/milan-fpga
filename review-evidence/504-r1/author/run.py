#!/usr/bin/env python3
"""Record exact local argv, exit, head and tree beside unfiltered output."""
import datetime
import fcntl
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
repo = Path("$CANDIDATE")
def git(*args):
    return subprocess.check_output(["git", "--no-optional-locks", *args], cwd=repo, text=True).strip()
def index_tree():
    with (root / "receipt.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return git("write-tree")
record = {"argv": argv, "cwd": str(repo), "start": datetime.datetime.now(datetime.timezone.utc).isoformat(), "head": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}"), "index_tree": index_tree(), "status_before": git("status", "--porcelain=v1"), "diff_sha256": __import__("hashlib").sha256(subprocess.check_output(["git", "--no-optional-locks", "diff", "HEAD"], cwd=repo)).hexdigest()}
with (root / (label + ".log")).open("w") as log:
    result = subprocess.run(argv, cwd=repo, stdout=log, stderr=subprocess.STDOUT)
record.update(exit=result.returncode, end=datetime.datetime.now(datetime.timezone.utc).isoformat(), status_after=git("status", "--porcelain=v1"))
(root / (label + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
print((root / (label + ".log")).read_text()[-6000:])
sys.exit(result.returncode)

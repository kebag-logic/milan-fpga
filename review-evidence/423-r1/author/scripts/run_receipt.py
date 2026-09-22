"""Run one authorized command under an eight-CPU cap, retaining raw output."""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parent.parent
name, *cmd = sys.argv[1:]
os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:8])
started = time.time()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="8", MAKEFLAGS="-j8")
result = subprocess.run(cmd, capture_output=True, env=env)
(root / "receipts" / (name + ".stdout")).write_bytes(result.stdout)
(root / "receipts" / (name + ".stderr")).write_bytes(result.stderr)
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
index_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True, check=True).stdout.strip()
paths = ["CONTRIBUTING.md", *[str(p) for p in Path("scripts").glob("*containment*.py")]]
digests = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in paths}
record = dict(command=cmd, cwd=str(Path.cwd()), head=head, index_tree=index_tree, source_sha256=digests, exit=result.returncode,
              seconds=round(time.time() - started, 3), cpu_affinity=sorted(os.sched_getaffinity(0)))
(root / "receipts" / (name + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k: v for k, v in record.items() if k != "source_sha256"}))
sys.exit(result.returncode)

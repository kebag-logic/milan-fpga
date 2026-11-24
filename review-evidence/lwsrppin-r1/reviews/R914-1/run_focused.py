#!/usr/bin/env python3
"""Run four independent reproduction arms, at most sixteen compiler jobs."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
old = scratch / "old-lwsrp"
base = "08ee86e812a0eb5e1dc6cd61b494d8baf3491348"
head = "d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b"
if not old.exists():
    subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(root / "third_party/lwSRP"), str(old)], check=True)
    subprocess.run(["git", "-C", str(old), "checkout", "--quiet", "--detach", base], check=True)

def run(spec):
    label, dependency, revision, shape = spec
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    cmd = [sys.executable, "-B", str(packet / "run_own_la.py"), str(root), str(scratch / label),
           str(dependency), revision, shape]
    with (packet / (label + ".log")).open("w") as log:
        result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)
    (packet / (label + ".rc")).write_text(str(result.returncode) + "\n")
    return label, result.returncode

specs = [(f"own-{version}-{shape}", old if version == "base" else root / "third_party/lwSRP",
          base if version == "base" else head, shape) for version in ("base", "head") for shape in ("1x1", "8x8")]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(run, specs):
        print(*result, flush=True)

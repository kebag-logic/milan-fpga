#!/usr/bin/env python3
"""Retry renderer-dependent checks in the packet's isolated locked environment."""
from concurrent.futures import ThreadPoolExecutor
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo, packet = (Path(p).resolve() for p in sys.argv[1:])
env = dict(os.environ, TMPDIR=str(packet / "scratch"), PYTHONDONTWRITEBYTECODE="1")
python = packet / "scratch/markdown-env/bin/python"
checks = {
    "toc-check-pinned": ["scripts/gen_toc.py", "--check"],
    "toc-anchors-pinned": ["scripts/gen_toc.py", "--verify-anchors"],
    "em-dash-pinned": ["scripts/check_em_dash.py", "--base", "bd884631684ccf5060339efa92263d5c3e5c262c"],
}
def run(item):
    name, args = item
    start = time.monotonic()
    with (packet / "receipts" / (name + ".log")).open("wb") as output:
        rc = subprocess.run([str(python), *args], cwd=repo, env=env, stdout=output,
                            stderr=subprocess.STDOUT, timeout=300).returncode
    (packet / "receipts" / (name + ".rc")).write_text(str(rc) + "\n")
    return {"name": name, "command": ["$PACKET/scratch/markdown-env/bin/python", *args],
            "rc": rc, "seconds": round(time.monotonic() - start, 3)}
with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, checks.items()))
(packet / "receipts/docs-retry.json").write_text(json.dumps(results, indent=2) + "\n")
for result in results:
    print(f"{result['name']}: rc={result['rc']}; seconds={result['seconds']}")
sys.exit(int(any(result["rc"] for result in results)))

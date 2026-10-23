#!/usr/bin/env python3
"""Run only documentation gates, concurrently, preserving each result."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

repo, out = (Path(a).resolve() for a in sys.argv[1:3])
python = sys.argv[3] if len(sys.argv) > 3 else sys.executable
gates = [
    ["scripts/docs_check.py"],
    ["scripts/check_doc_style.py"],
    ["scripts/check_gptp_docs.py"],
    ["scripts/check_doc_paths.py"],
    ["scripts/check_em_dash.py", "--base", "24a292a0"],
    ["scripts/gen_toc.py", "--check"],
    ["scripts/gen_toc.py", "--verify-anchors"],
]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(out / "scratch"))
def run(args):
    name = Path(args[0]).stem + ("-anchors" if "--verify-anchors" in args else "")
    result = subprocess.run([python, *args], cwd=repo, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out / (name + ".final.log")).write_bytes(result.stdout)
    (out / (name + ".final.rc")).write_text(str(result.returncode) + "\n")
    return {"command": ["python", *args], "rc": result.returncode,
            "log": name + ".final.log"}
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
    results = list(pool.map(run, gates))
(out / "local-doc-gates-final.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
sys.exit(any(r["rc"] for r in results))

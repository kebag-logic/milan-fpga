import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
renderer_python = "$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3"
base = "ffcbd33de70278ae34b533dcbadde0b36c8cba13"
steps = [
    ("docs-git", ["python3", "-B", "scripts/docs_check.py"], {}),
    ("docs-no-git", ["python3", "-B", "scripts/docs_check.py"], {"GIT_DIR": "/tmp/544-no-git-metadata"}),
    ("baremetal", ["python3", "scripts/check_baremetal_only.py", "--check"], {}),
    ("em-dash", [renderer_python, "scripts/check_em_dash.py", "--base", base], {}),
    ("doc-style", ["python3", "scripts/check_doc_style.py"], {}),
    ("toc", [renderer_python, "scripts/gen_toc.py", "--check"], {}),
    ("doc-paths", ["python3", "scripts/check_doc_paths.py"], {}),
    ("py-idiom", ["python3", "scripts/check_py_idiom.py"], {}),
    ("diff-check", ["git", "diff", "--check"], {}),
    ("committed-diff-check", ["git", "diff", "--check", base, "HEAD"], {}),
    ("retained-rows", ["python3", str(out / "compare-retained.py")], {}),
]
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
results = []
for label, command, environment in steps:
    started = time.monotonic()
    with (out / (label + ".log")).open("w") as log:
        result = subprocess.run(command, env={**os.environ, **environment}, stdout=log, stderr=subprocess.STDOUT, timeout=3600)
    row = dict(label=label, command=command, environment=environment, returncode=result.returncode, seconds=round(time.monotonic()-started, 2), head=head)
    results.append(row)
    (out / "static-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{label}: rc {result.returncode}", flush=True)
assert all(row["returncode"] == 0 for row in results), results

"""Run assigned gates in the foreground; retain bounded evidence files."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path("$LANES/595-yaml-int-refusal")
OUT = Path(__file__).parent
SCRATCH = Path((OUT / "artifact-scratch.txt").read_text().strip())
MD = "$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python"
BASE = "1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
gates = [
    ("declarations", ["python3", "sw/builder/test_declarations.py"], {}),
    ("builder-full", ["python3", "sw/builder/test_builder.py", "--require-rv32", "--require-elaboration"], {}),
    ("compiler-controls", ["python3", "sw/builder/test_firmware_compiler.py", "--selftest"], {}),
    ("compiler-absent", ["python3", "sw/builder/test_firmware_compiler.py", "--absent", "--audit",
                          str(SCRATCH / "compiler-absent-audit.jsonl")], {}),
    ("focused-mutants", ["python3", str(OUT / "focused_evidence.py")], {}),
    ("artifact-identity", ["python3", str(OUT / "artifact_inventory.py"), "after", str(SCRATCH)], {}),
    ("docs-check", [MD, "scripts/docs_check.py"], {}),
    ("docs-check-no-git", [MD, "scripts/docs_check.py"], {"GIT_DIR": "/dev/null"}),
    ("em-dash", [MD, "scripts/check_em_dash.py", "--base", BASE], {}),
    ("doc-style", [MD, "scripts/check_doc_style.py"], {}),
    ("doc-style-selftest", [MD, "scripts/check_doc_style.py", "--selftest"], {}),
    ("toc-selftest", [MD, "scripts/gen_toc.py", "--selftest"], {}),
    ("anchors", [MD, "scripts/gen_toc.py", "--verify-anchors"], {}),
    ("toc", [MD, "scripts/gen_toc.py", "--check"], {}),
    ("doc-paths", [MD, "scripts/check_doc_paths.py"], {}),
    ("python-idiom", ["python3", "scripts/check_py_idiom.py"], {}),
    ("naming", ["python3", "scripts/measure_naming.py", "--check"], {}),
    ("diff-worktree", ["git", "diff", "--check"], {}),
    ("diff-branch", ["git", "diff", "--check", BASE, "HEAD"], {}),
]
selected = set(sys.argv[1:])
for name, argv, overrides in gates:
    if selected and name not in selected:
        continue
    print(f"START {name} at {head}", flush=True)
    path = SCRATCH / (name + ".log")
    started = time.monotonic()
    with path.open("w") as stream:
        result = subprocess.run(argv, cwd=ROOT, env={**os.environ, "PYTHONUNBUFFERED": "1", **overrides},
                                stdout=stream, stderr=subprocess.STDOUT, timeout=7200)
    data = path.read_bytes()
    record = dict(name=name, head=head, cwd=str(ROOT), argv=argv, env=overrides,
                  rc=result.returncode, seconds=round(time.monotonic()-started, 2),
                  size=len(data), sha256=hashlib.sha256(data).hexdigest())
    if len(data) <= 200000:
        shutil.copyfile(path, OUT / path.name)
        record["log"] = path.name
    else:
        record["log"] = str(path)
    with (OUT / "gates.jsonl").open("a") as stream:
        stream.write(json.dumps(record) + "\n")
    print(f"END {name}: rc={result.returncode}, {record['seconds']}s, {len(data)} bytes", flush=True)
    if result.returncode:
        print(data.decode(errors="replace")[-6000:], flush=True)
        raise SystemExit(result.returncode)

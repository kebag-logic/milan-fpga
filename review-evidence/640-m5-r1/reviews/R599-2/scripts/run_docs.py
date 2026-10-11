#!/usr/bin/env python3
"""Usage: run_docs.py REPO PINNED_RENDERER_PYTHON. All commands run foreground."""
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
# Preserve the virtual environment path; resolving its interpreter symlink
# would select the global environment instead.
python = str(Path(sys.argv[2]).absolute())
commands = [
    ["scripts/docs_check.py"],
    ["scripts/docs_check.py", "NO_GIT"],
    ["scripts/check_em_dash.py", "--base", "e8454e2751d05b02ee8e5a571857589ab358ab86"],
    ["scripts/check_em_dash.py", "--selftest"],
    ["scripts/check_doc_style.py"], ["scripts/check_doc_style.py", "--selftest"],
    ["scripts/check_gptp_docs.py"], ["scripts/check_gptp_docs.py", "--selftest"],
    ["scripts/gen_toc.py", "--selftest"],
    ["scripts/gen_toc.py", "--verify-anchors"], ["scripts/gen_toc.py", "--check"],
    ["scripts/check_doc_paths.py"],
    ["docs/traceability/gen_module_matrix.py", "--check"],
    ["scripts/check_sv_idiom.py"], ["scripts/check_hygiene.py", "--check"],
    ["scripts/measure_naming.py", "--check"],
    ["scripts/measure_fail_fast.py", "--check"],
    ["scripts/check_todo_ownership.py"],
    ["scripts/measure_test_evidence.py", "--check"],
    ["scripts/check_port_contracts.py"], ["scripts/check_rtl_source_lists.py"],
]
failures = 0
for args in commands:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["TMPDIR"] = str(Path(__file__).resolve().parents[1] / "scratch/tmp")
    print("COMMAND python " + " ".join(args), flush=True)
    if args[-1] == "NO_GIT":
        env["GIT_DIR"] = "/dev/null"
        args = args[:-1]
    result = subprocess.run([python, *args], cwd=repo, env=env)
    print(f"RC {result.returncode}", flush=True)
    failures += result.returncode != 0
result = subprocess.run(["git", "diff", "--check", "e8454e27", "HEAD"], cwd=repo)
print(f"git diff --check e8454e27 HEAD: RC {result.returncode}", flush=True)
failures += result.returncode != 0
print(f"RESULT: {failures} failed commands of {len(commands) + 1}", flush=True)
sys.exit(bool(failures))

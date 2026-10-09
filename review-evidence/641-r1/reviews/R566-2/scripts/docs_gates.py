#!/usr/bin/env python3
"""Run the docs-workflow checks that touch this PR's changed files, one by one.

Usage: MD_PYTHON=<markdown-env python3> docs_gates.py <base-rev> <out.json>
(run from the reviewed tree)
Each command's rc and output tail are recorded; heavy banks (builder, SDK,
submodule docs build, HDL reference build) are deliberately not run.
"""
import json
import os
import subprocess
import sys

BASE, OUT = sys.argv[1], sys.argv[2]
MD_PY = os.environ["MD_PYTHON"]  # interpreter of the pinned Markdown-renderer environment
PY = sys.executable
CMDS = [
    [MD_PY, "scripts/docs_check.py"],
    [MD_PY, "scripts/check_em_dash.py", "--base", BASE],
    [MD_PY, "scripts/check_em_dash.py", "--selftest"],
    [PY, "scripts/check_doc_style.py"],
    [PY, "scripts/check_doc_style.py", "--selftest"],
    [PY, "docs/DOC_MAP.gen.py", "--check"],
    [PY, "scripts/check_solution_docs.py"],
    [PY, "scripts/check_submodule_docs.py"],
    [MD_PY, "scripts/gen_toc.py", "--verify-anchors"],
    [MD_PY, "scripts/gen_toc.py", "--check"],
    [PY, "scripts/check_feature_status.py"],
    [PY, "scripts/check_archive.py"],
    [PY, "scripts/check_hygiene.py", "--check"],
    [PY, "scripts/check_sv_idiom.py"],
    [PY, "scripts/check_py_idiom.py"],
    [PY, "scripts/check_sh_idiom.py"],
    [PY, "scripts/measure_naming.py", "--check"],
    [PY, "scripts/measure_fail_fast.py", "--check"],
    [PY, "scripts/measure_test_evidence.py", "--check"],
    [PY, "scripts/check_todo_ownership.py"],
    [PY, "scripts/check_rtl_source_lists.py"],
    [PY, "scripts/check_port_contracts.py"],
    [PY, "scripts/ci_scope.py", "--selftest"],
    [PY, "scripts/ci_events.py", "--check"],
    [PY, "scripts/ci_events.py", "--selftest"],
]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
results = []
for cmd in CMDS:
    shown = " ".join(["python3" if c in (MD_PY, PY) else c for c in cmd])
    if cmd[0] == MD_PY:
        shown = "<markdown-venv> " + shown
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
    tail = (p.stdout + p.stderr).strip().splitlines()[-4:]
    results.append({"cmd": shown, "rc": p.returncode, "tail": tail})
    print(f"rc={p.returncode:<3} {shown}")
    for line in tail:
        print(f"      {line[:200]}")
with open(OUT, "w", encoding="utf-8") as handle:
    json.dump(results, handle, indent=1)
failed = [r["cmd"] for r in results if r["rc"] != 0]
print(f"{len(results) - len(failed)}/{len(results)} rc 0; failed: {failed}")
sys.exit(1 if failed else 0)

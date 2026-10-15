#!/usr/bin/env python3
"""Execute exact generated census shell over disposable cgroup fixtures, unprivileged."""
import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("repository", type=Path)
parser.add_argument("--scratch", required=True, type=Path)
args = parser.parse_args()
source = (args.repository / "scripts/ci_runtime_workflows.py").read_text()
tree = ast.parse(source)
nodes = [node for node in tree.body if
         isinstance(node, ast.FunctionDef) and node.name == "census_budget_step" or
         isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CENSUS_WORKER_BYTES" for t in node.targets)]
namespace = {}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "ci_runtime_workflows.py:budget-only", "exec"), namespace)
shell = namespace["census_budget_step"]()["run"]
workflow = (args.repository / ".github/workflows/rtl-fast.yml").read_text()
assert all("          " + line in workflow for line in shell.splitlines())
args.scratch.mkdir(parents=True, exist_ok=True)
assert os.geteuid() != 0, "permission-denial control must run without root"
results = []
for case in ("readable-8GiB", "unreadable-8GiB", "unreadable-ancestor-4GiB", "garbage-limit", "missing-controller"):
    with tempfile.TemporaryDirectory(prefix="census-", dir=args.scratch) as temporary:
        root = Path(temporary)
        (root / "bin").mkdir()
        (root / "bin/nproc").write_text("#!/bin/sh\necho 16\n")
        (root / "bin/nproc").chmod(0o755)
        (root / "meminfo").write_text("MemTotal: 63963136 kB\n")
        nested = case == "unreadable-ancestor-4GiB"
        (root / "cgroup").write_text("0::" + ("/a/b" if nested else "/") + "\n")
        cg = root / "sys"
        cg.mkdir()
        limit = cg / "memory.max"
        if nested:
            (cg / "a/b").mkdir(parents=True)
            limit.write_text("max\n")
            (cg / "a/b/memory.max").write_text("max\n")
            limit = cg / "a/memory.max"
        if case != "missing-controller":
            limit.write_text("garbage\n" if case == "garbage-limit" else str((4 if nested else 8) * 2**30) + "\n")
        if case.startswith("unreadable"):
            limit.chmod(0)
            assert not os.access(limit, os.R_OK)
        script = shell.replace("/proc/meminfo", str(root / "meminfo")).replace("/proc/self/cgroup", str(root / "cgroup")).replace("/sys/fs/cgroup", str(cg))
        output = root / "env"
        ran = subprocess.run(["bash", "-c", script], env={**os.environ, "PATH": str(root / "bin") + ":" + os.environ["PATH"], "GITHUB_ENV": str(output)}, capture_output=True, text=True, timeout=10)
        result = {"case": case, "rc": ran.returncode, "stdout": ran.stdout.strip(), "export": output.read_text().strip() if output.exists() else None,
                  "stderr": ran.stderr.replace(str(root), "<fixture>").strip()}
        results.append(result)
        print(json.dumps(result, sort_keys=True))
        if limit.exists():
            limit.chmod(0o600)
assert results[0]["rc"] == 0 and results[0]["export"] == "CI_CENSUS_JOBS=4"
assert results[3]["rc"] != 0 and results[3]["export"] is None
assert results[4]["rc"] == 0 and results[4]["export"] == "CI_CENSUS_JOBS=16"
assert all(r["rc"] == 0 and r["export"] == "CI_CENSUS_JOBS=16" for r in results[1:3])
print("REPRODUCED: unreadable existing leaf and ancestor limits are silently skipped; successful exports use host memory.")

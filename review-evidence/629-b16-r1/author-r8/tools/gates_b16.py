#!/usr/bin/env python3
"""Lane B16 (lane B15's gates_r2.py pattern, new list): run the lane's gates, each to its own log, never piped.

usage: gates_b16.py <lane_worktree> <md_python> <out_dir>
Every gate runs from the lane worktree (its physical path) with its output to <out_dir>/<name>.log; the
return codes go to <out_dir>/results.json. The Markdown gates run under <md_python>, the others under
this interpreter's python3 on PATH.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

lane, md, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
G = [
    ("tool-md", [md, "--version"]),
    ("tool-python3", ["python3", "--version"]),
    ("docs-check", [md, "scripts/docs_check.py"]),
    ("doc-style", [md, "scripts/check_doc_style.py"]),
    ("toc-check", [md, "scripts/gen_toc.py", "--check"]),
    ("toc-verify-anchors", [md, "scripts/gen_toc.py", "--verify-anchors"]),
    ("em-dash", [md, "scripts/check_em_dash.py", "--base", "e8454e27"]),
    ("doc-paths", [md, "scripts/check_doc_paths.py"]),
    ("ci-scope-selftest", ["python3", "scripts/ci_scope.py", "--selftest"]),
    ("baremetal-only-check", ["python3", "scripts/check_baremetal_only.py", "--check"]),
    ("baremetal-only-selftest", ["python3", "scripts/check_baremetal_only.py", "--selftest"]),
    ("feature-status-selftest", ["python3", "scripts/check_feature_status.py", "--self-test"]),
    ("git-diff-check-worktree", ["git", "diff", "--check"]),
    ("git-diff-check-range", ["git", "diff", "--check", "c20c85bd", "HEAD"]),
]
res = []
for name, cmd in G:
    t0 = time.time()
    with open(out / f"{name}.log", "w") as f:
        f.write("$ " + " ".join(cmd) + "\n")
        f.flush()
        r = subprocess.run(cmd, cwd=lane, stdout=f, stderr=subprocess.STDOUT, timeout=900)
    res.append(dict(gate=name, cmd=cmd, rc=r.returncode, seconds=round(time.time() - t0, 1)))
    print(f"{name}: rc={r.returncode}", flush=True)
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=lane, capture_output=True, text=True).stdout.strip()
json.dump(dict(head=head, lane=str(lane), gates=res, all_rc0=all(g["rc"] == 0 for g in res)), open(out / "results.json", "w"), indent=1)
print("ALL_RC0" if all(g["rc"] == 0 for g in res) else "SOME_FAILED", head)
sys.exit(0 if all(g["rc"] == 0 for g in res) else 1)

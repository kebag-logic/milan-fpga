#!/usr/bin/env python3
"""Run bounded reviewer checks; repository and output directory are arguments."""
import concurrent.futures, json, os, pathlib, subprocess, sys
repo, out = map(pathlib.Path, sys.argv[1:3])
scratch = out / "scratch" / "tmp"
scratch.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch))
checks = [
 ("egress-selftest", ["egress_ledger.py", "--selftest"]),
 ("load", ["load_grade.py", "--check", "--selftest"]),
 ("record-classes", ["record_classes.py", "--selftest"]),
 ("shape", ["shape_costs.py", "--check", "--selftest"]),
 ("flip-1x1", ["flip_grade.py", "--check", "--point", "1x1/1if"]),
 ("flip-8x8", ["flip_grade.py", "--check", "--point", "8x8/1if"]),
]
def run(task):
 name, args = task
 command = [sys.executable, "-B", str(repo / "tb/verilator/ctrl_service_budget" / args[0]), *args[1:]]
 with (out / (name + ".log")).open("w") as f:
  f.write("Command: python3 -B tb/verilator/ctrl_service_budget/" + " ".join(args) + "\n"); f.flush()
  rc = subprocess.run(command, cwd=repo, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=550).returncode
 (out / (name + ".rc")).write_text(str(rc) + "\n")
 return {"check": name, "rc": rc}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 results = list(pool.map(run, checks))
(out / "focused-checks.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results))
sys.exit(any(r["rc"] for r in results))


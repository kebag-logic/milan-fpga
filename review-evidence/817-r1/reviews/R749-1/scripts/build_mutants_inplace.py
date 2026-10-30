#!/usr/bin/env python3
"""Run the #817 build mutants of mutants.py in place, one at a time, restoring each file.

Usage: build_mutants_inplace.py <clone> <scratch-dir> <out-dir> <python-with-litex>
The elaboration lists submodule files through git, so it cannot run in a plain copy.
Each mutated file is restored with `git checkout --` before the next mutant.
"""
import json, os, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutants as m

clone, scratch, out, python = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
out.mkdir(parents=True, exist_ok=True)
results = []
for name, kind, rel, old, new, expect in m.MUTANTS:
    if kind != "ship":
        continue
    path = clone / rel if rel else None
    if path:
        text = path.read_text()
        if text.count(old) != 1:
            results.append(dict(mutant=name, verdict="NOT-APPLIED")); continue
        path.write_text(text.replace(old, new))
    try:
        argv = [python, m.SHIP[0], str(clone / m.SHIP[1]), *m.SHIP[2:],
                "--output-dir", str(scratch / f"elab-{name}")]
        env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
        t0 = time.time()
        p = subprocess.run(argv, cwd=clone / "sw/litex", env=env, text=True,
                           capture_output=True, timeout=1200)
    finally:
        if path:
            subprocess.run(["git", "checkout", "--", rel], cwd=clone, check=True)
    log = p.stdout + p.stderr
    (out / f"{name}.log").write_text(log)
    if rel is None:
        verdict = "PASS" if p.returncode == 0 and " PASS" in log else "CONTROL-FAILED"
    else:
        verdict = "KILLED" if p.returncode != 0 and expect in log else (
            "SURVIVED" if p.returncode == 0 else "FAILED-UNEXPECTEDLY")
    results.append(dict(mutant=name, file=rel, rc=p.returncode,
                        seconds=round(time.time() - t0), expected=expect, verdict=verdict))
    print(f"{name:40s} {verdict} rc={p.returncode}", flush=True)
(out / "build-mutants.json").write_text(json.dumps(results, indent=1) + "\n")
ok = all(r["verdict"] == ("PASS" if r["mutant"].startswith("C") else "KILLED") for r in results)
print("BUILD-CAMPAIGN", "ALL-KILLED-CONTROL-PASS" if ok else "NOT-CLEAN")
sys.exit(0 if ok else 1)

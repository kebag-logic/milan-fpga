#!/usr/bin/env python3
"""Fault probes for tb/mutation_order_test.py.

usage: order_probe.py <head-tree> <scratch-dir> <out-dir>

Runs the order test against the head's own mutants.py (expected rc 0), then
against copies of the arm with one planted ordering defect each (expected
rc 1). Each copy is a full copy of the head tree under <scratch-dir>; the
head tree itself is never edited. Writes one log per case and a summary.
"""
import shutil
import subprocess
import sys
from pathlib import Path

head, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)
ARM = "tb/verilator/engine/mutants.py"

# (case, expected rc, [(old, new), ...] applied to the copy's mutants.py)
CASES = [
    ("head-unmodified", 0, []),
    ("completion-order-yield", 1, [(
        "        futures = [pool.submit(task) for task in tasks]\n"
        "        for future in futures:\n"
        "            yield future.result()\n",
        "        from concurrent.futures import as_completed\n"
        "        futures = [pool.submit(task) for task in tasks]\n"
        "        for future in as_completed(futures):\n"
        "            yield future.result()\n")]),
    ("lines-printed-on-completion", 1, [(
        "                return run_mutant(work, clean_exe, mutation, lines.append), lines\n",
        "                return run_mutant(work, clean_exe, mutation, print), lines\n")]),
    ("one-mutant-dropped", 1, [(
        "args.jobs, [control, *map(planted, MUTATIONS)])) as results:",
        "args.jobs, [control, *map(planted, MUTATIONS[:-1])])) as results:")]),
    ("shared-run-directory", 1, [(
        "    rundir = own / f\"run_{tag}\"\n",
        "    rundir = work / \"run_shared\"\n")]),
]

summary = []
for case, want, edits in CASES:
    tree = head if not edits else scratch / f"order-{case}"
    if edits:
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(head, tree)
        arm = tree / ARM
        text = arm.read_text(encoding="utf-8")
        for old, new in edits:
            assert text.count(old) == 1, (case, old)
            text = text.replace(old, new)
        arm.write_text(text, encoding="utf-8")
    res = subprocess.run(
        [sys.executable, str(tree / "tb/mutation_order_test.py"), str(tree / ARM)],
        cwd=str(tree / "tb/verilator/engine"), capture_output=True, text=True)
    log = res.stdout + res.stderr
    (out / f"{case}.log").write_text(log, encoding="utf-8")
    fails = [line for line in log.splitlines() if line.startswith("FAIL ")]
    ok = res.returncode == want
    summary.append(f"{'OK  ' if ok else 'BAD '} {case}: rc {res.returncode} (want {want}); "
                   f"{len(fails)} FAIL lines; last: {log.strip().splitlines()[-1] if log.strip() else ''}")
    for line in fails:
        summary.append(f"       {line}")
(out / "SUMMARY.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
print("\n".join(summary))
sys.exit(0 if all(s.startswith("OK") for s in summary if not s.startswith("       ")) else 1)

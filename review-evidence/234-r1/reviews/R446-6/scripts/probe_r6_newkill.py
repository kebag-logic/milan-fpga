#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 6): the shipped mutants round 6 adds, against the round-5 and the round-6 self-test.

The new mutants are the keys of MUTANTS in <after>'s pp_resource_gate_mutants.py absent from <before>'s. Each is
applied to the gate (byte-identical at both commits), beside the parser and either commit's self-test, and the
whole --selftest runs; rc != 0 = KILLED. The first failing line names what killed it at <after>: an arm's
AssertionError, a generated case ("fuzz FAILURE"), or a refusal before any arm.

Usage: probe_r6_newkill.py <checkout> <before> <after> <scratch-dir> [--jobs N]
"""

import ast
import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys

REPO, BEFORE, AFTER, SCRATCH = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve()
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8


def show(commit: str, name: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:syn/ooc/{name}"], check=True,
                          capture_output=True, text=True).stdout


def mutants(commit: str) -> dict:
    """MUTANTS of a commit's campaign, evaluated from its literal (module-level names it uses resolved first)."""
    tree = ast.parse(show(commit, "pp_resource_gate_mutants.py"))
    scope: dict = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) for t in node.targets):
            try:
                value = eval(compile(ast.Expression(node.value), "m", "eval"), {}, scope)  # noqa: S307
            except Exception:  # noqa: BLE001
                continue
            for target in node.targets:
                scope[target.id] = value
    return scope["MUTANTS"]


GATE, RANK, SELF = "pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py"
SOURCES = {commit: {name: show(commit, name) for name in (GATE, RANK, SELF)} for commit in (BEFORE, AFTER)}
OLD, NEW = mutants(BEFORE), mutants(AFTER)
ADDED = [name for name in NEW if name not in OLD]


def run(job: tuple[str, str]) -> tuple[str, str, int, str]:
    name, commit = job
    folder = SCRATCH / commit[:8] / "".join(char if char.isalnum() else "_" for char in name)
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for file, text in SOURCES[commit].items():
        (folder / file).write_text(text)
    entry = NEW[name]
    file, old, new = (GATE, *entry) if len(entry) == 2 else entry
    source = (folder / file).read_text()
    if source.count(old) != 1:
        return name, commit, -1, f"span found {source.count(old)} times in {file}"
    (folder / file).write_text(source.replace(old, new))
    done = subprocess.run([sys.executable, "-B", GATE, "--selftest"], cwd=folder, capture_output=True, text=True,
                          timeout=1800)
    lines = (done.stdout + done.stderr).splitlines()
    first = next((line.strip() for line in lines if "AssertionError" in line or "FAILURE" in line), "")
    return name, commit, done.returncode, first[:160]


def main() -> None:
    print(f"new shipped mutants: {len(ADDED)} (campaign {len(OLD)} -> {len(NEW)})")
    jobs = [(name, commit) for name in ADDED for commit in (BEFORE, AFTER)]
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = {(name, commit): (rc, first) for name, commit, rc, first in pool.map(run, jobs)}
    missed = killed = 0
    for name in ADDED:
        (rc5, _), (rc6, first) = results[(name, BEFORE)], results[(name, AFTER)]
        missed += rc5 == 0
        killed += rc6 != 0
        print(f"{name}: round-5 self-test {'KILLED' if rc5 else 'missed'} (rc {rc5}); "
              f"round-6 self-test {'KILLED' if rc6 else 'SURVIVED'} (rc {rc6}) | {first}")
    print(f"probe_r6_newkill: {len(ADDED)} new; the round-5 self-test misses {missed}; the round-6 one kills {killed}")
    raise SystemExit(0 if killed == len(ADDED) else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reviewer sweep over row 3's parent cells: per-cell mutants of scripts/owned_process.py.

Usage: python3 -I row3_sweep.py <clone root> <scratch dir> <jobs>
Each mutant is confined to one cell (parent kind x shell placement) and must turn
`--control owner_stated_seconds` red. Prints one line per mutant and a summary.
"""
import concurrent.futures
import os
import shutil
import subprocess
import sys
from pathlib import Path

root, scratch, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])

ANY = "if any(parent == pid and child in live for child, (parent, _start) in owned.items()):"
ELIF = "                elif clock < kill_all:\n"
ROOT = "if pid == root_pid and self.root_notified and (resumed is None or clock < kill_all):"


def kid(who: str, kind: str) -> str:
    test = "in initial" if kind == "first" else "not in initial"
    return (f"any(_p == {who} and _c in live and (_c, _s) {test} "
            f"for _c, (_p, _s) in owned.items())")


def place(who: str, where: str) -> str:
    return {"none": "not self.root_notified",
            "under": f"(self.root_notified and resumed is None and owned[{who}][0] == root_pid)",
            "beside": f"(self.root_notified and resumed is None and {who} != root_pid "
                      f"and owned[{who}][0] != root_pid)"}[where]


def cell(who: str, kind: str, where: str) -> str:
    return f"({kid(who, kind)} and {place(who, where)})"


mutants = {"identity": []}  # The unmutated copy: must be green, or the sweep proves nothing.
for kind in ("first", "new"):
    for where in ("none", "under", "beside"):
        c = cell("pid", kind, where)
        mutants[f"unspare-{kind}-{where}"] = [(ANY, ANY[:-1] + f" and not {c}:")]
        mutants[f"tick-early-{kind}-{where}"] = [(ELIF, f"                elif clock < kill_all - (2 ** -19 if {c} else 0):\n")]
        mutants[f"pass-late-{kind}-{where}"] = [(ELIF, f"                elif clock < kill_all or (clock == kill_all and {c}):\n")]
        if where != "none":
            q = cell("_q", kind, where)
            mutants[f"shell-killed-at-kill-all-{kind}-{where}"] = [(
                ROOT, "if pid == root_pid and self.root_notified and ((resumed is None and not (clock >= kill_all "
                      f"and any({q} for _q in owned if _q != root_pid))) or clock < kill_all):")]


def run(name: str) -> tuple[str, str, str]:
    tree = scratch / name
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(root / "scripts", tree / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = tree / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in mutants[name]:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    product.write_text(text)
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    try:
        proc = subprocess.run([sys.executable, "-B", str(tree / "scripts/test_suite_cancellation.py"),
                               "--control", "owner_stated_seconds"], cwd=tree, env=env, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=150, start_new_session=True)
        verdict = "red" if proc.returncode else "green"
        out = (proc.stdout + proc.stderr).strip().splitlines()
    except subprocess.TimeoutExpired:
        verdict, out = "cut", []
    return name, verdict, (out[-1][:260] if out else "")


with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(run, mutants))
for name, verdict, last in results:
    print(f"{name}: {verdict}: {last}")
identity = [v for n, v, _ in results if n == "identity"] == ["green"]
results = [r for r in results if r[0] != "identity"]
survivors = [n for n, v, _ in results if v != "red"] + ([] if identity else ["identity-not-green"])
print(f"row3-sweep: {len(results)} mutants, {len(results) - len(survivors)} red, survivors={survivors}")
sys.exit(1 if survivors else 0)

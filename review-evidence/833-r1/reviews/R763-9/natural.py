"""Reviewer natural mutants for #833: each on probe_cells.py, every owner control and the whole test.

Usage: python3 -I natural.py <clean-tree> <scratch-dir> <jobs>
"""
import concurrent.futures
import os
import shutil
import subprocess
import sys
from pathlib import Path

CLEAN, SCRATCH, JOBS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
PROBE = Path(__file__).resolve().parent / "probe_cells.py"
CONTROLS = ("owner_stated_seconds", "owner_report", "owner_reparented", "owner_late_exit", "owner_stall",
            "owner_shell_window", "owner_survivor", "owner_vanishing", "owner_late_cancel", "owner_reused_identity")
TERM = "                    if (pid, start) not in initial:\n                        continue\n"
PARENT = "if any(parent == pid and child in live for child, (parent, _start) in owned.items()):"
LIMIT = "            limit = kill_all + REAP_SECONDS\n"
MUTANTS = {
    # A descendant first seen in the first quarter or half second is taken for one the first census missed.
    "early-new-sigtermed-0.25": [(TERM, "                    if (pid, start) not in initial and clock >= 0.25:\n"
                                        "                        continue\n")],
    "early-new-sigtermed-0.5": [(TERM, "                    if (pid, start) not in initial and clock >= 0.5:\n"
                                       "                        continue\n")],
    "early-trap-command-sigtermed": [(TERM, "                    if (pid, start) not in initial and not (resumed is not"
                                            " None and clock < 0.5):\n                        continue\n")],
    "early-live-new-sigtermed": [(TERM, "                    if (pid, start) not in initial and not (pid in live and"
                                        " clock < 0.5):\n                        continue\n")],
    # A trap's command listed in the pass right after the resume is taken for the shell's own work: SIGTERM.
    "trap-command-next-pass-sigtermed": [
        ("        passes = 0\n", "        passes = 0\n        resume_pass = None\n"),
        ("                resumed = clock\n", "                resumed = clock\n                resume_pass = passes\n"),
        (TERM, "                    if (pid, start) not in initial and not (resume_pass is not None and passes =="
               " resume_pass + 1):\n                        continue\n")],
    # Beside a cancelled shell, a parent of a live new descendant is not spared.
    "parent-of-live-new-unspared-beside-shell": [
        (PARENT, "if any(parent == pid and child in live and not (self.root_notified and (child, _start) not in"
                 " initial) for child, (parent, _start) in owned.items()):")],
    # A live new descendant beside a never-resumed shell brings the verdict a pass early.
    "verdict-early-live-new-beside-stopped-shell": [
        (LIMIT, "            limit = kill_all + REAP_SECONDS - (0.25 if self.root_notified and resumed is None and"
                " any((p, e[1]) not in initial and _live(p) for p, e in owned.items()) else 0)\n")],
}


def apply(name, edits):
    root = SCRATCH / name
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(CLEAN / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = root / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    product.write_text(text)
    return root


def run(argv, cwd, timeout):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    try:
        p = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=timeout, start_new_session=True)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return None, "timeout"


def task(item):
    name, target = item
    root = SCRATCH / name
    if target == "probe":
        rc, out = run([sys.executable, "-I", str(PROBE), str(root)], root, 120)
    else:
        argv = [sys.executable, "-B", str(root / "scripts/test_suite_cancellation.py")]
        rc, out = run(argv + (["--control", target] if target != "whole" else []), root, 150 if target != "whole" else 600)
    lines = [l for l in out.splitlines() if l.strip()]
    cells = [l.split(":")[0] for l in lines if l.startswith("CELL ")]
    return name, target, rc, (cells if target == "probe" else (lines[-1][:200] if lines else ""))


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for name, edits in MUTANTS.items():
        apply(name, edits)
    items = [(n, t) for n in MUTANTS for t in ("probe", *CONTROLS, "whole")]
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(task, items))
    for name in MUTANTS:
        rows = [r for r in results if r[0] == name]
        probe = next(r for r in rows if r[1] == "probe")
        reds = [r[1] for r in rows if r[1] != "probe" and r[2] != 0]
        verdict = "SURVIVOR" if probe[2] and not reds else "equivalent" if not probe[2] else "killed"
        print(f"{name}: {verdict}; probe rc {probe[2]} cells {probe[3]}; red controls {reds}")
        for r in rows:
            if r[1] != "probe":
                print(f"    {r[1]}: rc {r[2]} {r[3]}")


main()

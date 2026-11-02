#!/usr/bin/env python3
"""Reviewer edge mutants for round 7 against the cleanup table's rows (review probe).

Usage: python3 r7_mutants.py <repo> <jobs> [NAME ...]
Each mutant is applied to a copy of <repo>/scripts (the repository's own mutant_tree) and run
against every owner control (the repository's own run_mutant). Green on all ten is a survivor.
"""
import concurrent.futures
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
import process_test_support as pts  # noqa: E402
import test_suite_cancellation as tsc  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

OPEN = ("        try:\n            fd = os.pidfd_open(pid)\n        except ProcessLookupError:\n            return False\n"
        "        try:\n            identity = _identity(pid)\n")
RESUME = "and root_pid in owned and not (live - {root_pid}):"
NEW_TERM = "                    if (pid, start) not in initial:\n                        continue\n                elif"
NEW_KILL = "if (pid, start) not in initial and resumed is not None:"
MINE = {
    # Row 1: the SIGKILL's recheck read before its handle is opened.
    "r7-check-before-open-sigkill": (OPEN, "        early = _identity(pid) if signum == signal.SIGKILL else None\n"
                                           "        try:\n            fd = os.pidfd_open(pid)\n"
                                           "        except ProcessLookupError:\n            return False\n"
                                           "        try:\n            identity = early or _identity(pid)\n"),
    # Row 5: no resume inside grace after the first pass.
    "r7-no-resume-in-grace-after-pass-1": (RESUME, RESUME[:-1] + " and not (passes > 1 and clock < deadline):"),
    # Rows 2 and 6: SIGTERM to the trap's command after a resume inside grace in a later pass.
    "r7-sigterm-trap-command-later-grace-resume": (NEW_TERM, "                    if (pid, start) not in initial"
                                                             " and (resumed is None or resumed == 0.0):\n"
                                                             "                        continue\n                elif"),
    # Rows 3 and 8: the trap's command loses its window after a resume inside grace in a later pass.
    "r7-trap-window-not-later-grace": (NEW_KILL, NEW_KILL[:-1] + " and (resumed == 0.0 or resumed >= deadline):"),
    # Row 2: a new descendant gets SIGTERM while a notified shell waits, stopped, for its resume.
    "r7-sigterm-new-while-shell-stopped": (NEW_TERM, "                    if (pid, start) not in initial"
                                                     " and (resumed is not None or not self.root_notified):\n"
                                                     "                        continue\n                elif"),
}
names = sys.argv[3:] or list(MINE)
for name in names:
    old, new = MINE[name]
    pts.MUTANTS[name] = (None, "reviewer probe", (old, new))
runs = [(name, control) for name in names for control in tsc.OWNER_CONTROLS]
with OwnedProcesses():
    with tempfile.TemporaryDirectory(prefix="r7-mutants-",
                                     dir=str(Path(__file__).resolve().parent.parent / "scratch")) as scratch:
        trees = {name: pts.mutant_tree(Path(scratch), name) for name in names}
        with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
            results = dict(zip(runs, pool.map(lambda run: pts.run_mutant(trees[run[0]], run[1]), runs)))
survivors = []
for name in names:
    red = []
    for control in tsc.OWNER_CONTROLS:
        status, seconds, output = results[(name, control)]
        lines = [line for line in output.splitlines() if line.strip()]
        verdict = "cut" if status is None else "red" if status else "green"
        print(f"{name} / {control}: {verdict} rc {status} {seconds:.1f} s: {lines[-1][:240] if lines else ''}",
              flush=True)
        if verdict != "green":
            red.append(control)
    print(f"== {name}: {'SURVIVES (green on all ten)' if not red else 'red on ' + ', '.join(red)}", flush=True)
    if not red:
        survivors.append(name)
print(f"r7 mutants: {len(names)} run, survivors {survivors}")

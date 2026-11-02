#!/usr/bin/env python3
"""Reviewer mutants for a cancelled shell resumed inside grace after the first pass (review probe).

Usage: python3 rv7_mutants.py <repo> <jobs> [NAME ...]   (RV7_WHOLE=1: run the whole test instead)
Each mutant is applied to a copy of <repo>/scripts (the repository's own mutant_tree) and run
against every owner control (the repository's own run_mutant). Green on every control: survives.
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

NEW = "                    if (pid, start) not in initial:\n                        continue\n                elif"
MINE = {
    # Rows 2 and 6: a trap's command gets SIGTERM after a resume inside grace that is not in the first pass.
    "rv7-sigterm-trap-command-later-grace-resume": (NEW,
        "                    if (pid, start) not in initial and not (resumed is not None and resumed > 0):\n"
        "                        continue\n                elif"),
    # Row 2: any descendant new since the first census gets SIGTERM after a later in-grace pass of the clock.
    "rv7-sigterm-to-new-after-1s": (NEW,
        "                    if (pid, start) not in initial and clock < 1.0:\n"
        "                        continue\n                elif"),
    # Row 5: no resume inside grace after the first pass; the shell waits for grace to end.
    "rv7-no-resume-later-in-grace": ("and root_pid in owned and not (live - {root_pid}):",
        "and root_pid in owned and not (live - {root_pid}) and not (passes > 1 and clock < deadline):"),
    # Rows 6, 7, 8: a resume inside grace after the first pass opens no window of its own.
    "rv7-no-window-later-in-grace": ("kill_all = max(kill_all, clock + TRAP_SECONDS)",
        "kill_all = max(kill_all, clock + TRAP_SECONDS) if clock >= deadline or passes == 1 else kill_all"),
}
names = sys.argv[3:] or list(MINE)
for name in names:
    pts.MUTANTS[name] = (None, "reviewer probe", MINE[name])
import os
targets = (None,) if os.environ.get("RV7_WHOLE") else tsc.OWNER_CONTROLS
runs = [(name, control) for name in names for control in targets]
with OwnedProcesses():
    with tempfile.TemporaryDirectory(prefix="rv7-mutants-",
                                     dir=str(Path(__file__).resolve().parent.parent / "scratch")) as scratch:
        trees = {name: pts.mutant_tree(Path(scratch), name) for name in names}
        with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
            results = dict(zip(runs, pool.map(lambda run: pts.run_mutant(trees[run[0]], run[1]), runs)))
survivors = []
for name in names:
    red = []
    for control in targets:
        status, seconds, output = results[(name, control)]
        lines = [line for line in output.splitlines() if line.strip()]
        verdict = "cut" if status is None else "red" if status else "green"
        print(f"{name} / {control or 'whole'}: {verdict} rc {status} {seconds:.1f} s: {lines[-1][:240] if lines else ''}",
              flush=True)
        if verdict != "green":
            red.append(control)
    print(f"== {name}: {'SURVIVES (green on all ' + str(len(targets)) + ')' if not red else 'red on ' + ', '.join(red)}",
          flush=True)
    if not red:
        survivors.append(name)
print(f"rv7 mutants: {len(names)} run, survivors {survivors}")

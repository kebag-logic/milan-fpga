#!/usr/bin/env python3
"""Reviewer mutants against rows of the TESTING.md cleanup table (review probe).

Usage: python3 row_mutants.py <repo> <jobs> [NAME ...]   (RV6_WHOLE=1: run the whole test instead)
Each mutant is applied to a copy of <repo>/scripts (the repository's own mutant_tree) and run
against every owner control (the repository's own run_mutant). A mutant whose row is stated
must turn at least one control red; one green on all ten survives.
"""
import concurrent.futures
import sys
from pathlib import Path
import tempfile

repo = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
import process_test_support as pts  # noqa: E402
import test_suite_cancellation as tsc  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

SEND = "            self._signal(fd, signum)\n            self._signal(fd, signal.SIGCONT)\n"
MINE = {
    # Row 1: "Every signal goes through a handle ..."
    "rv6-sigkill-by-number": (SEND, "            if signum == signal.SIGKILL:\n                os.kill(pid, signum)\n"
                                    "            else:\n                self._signal(fd, signum)\n"
                                    "            self._signal(fd, signal.SIGCONT)\n"),
    "rv6-sigcont-by-number": (SEND, "            self._signal(fd, signum)\n            os.kill(pid, signal.SIGCONT)\n"),
    "rv6-sigterm-by-number": (SEND, "            if signum == signal.SIGTERM:\n                os.kill(pid, signum)\n"
                                    "            else:\n                self._signal(fd, signum)\n"
                                    "            self._signal(fd, signal.SIGCONT)\n"),
    # Row 2: the cancelled shell is not sent SIGTERM in the first pass.
    "rv6-shell-sigtermed": ("if pid == root_pid and self.root_notified and (resumed is None or clock < kill_all):",
                            "if pid == root_pid and self.root_notified and signum == signal.SIGKILL"
                            " and (resumed is None or clock < kill_all):"),
    # Row 2: every listed descendant, parents included, gets SIGTERM in the first pass.
    "rv6-sigterm-leaves-only": ("                    if (pid, start) not in initial:\n                        continue\n"
                                "                elif",
                                "                    if (pid, start) not in initial or pid in initial.values():\n"
                                "                        continue\n                elif"),
    # Row 3: two seconds after grace.
    "rv6-kill-all-1.5s": ("KILL_ALL_SECONDS = 2.0", "KILL_ALL_SECONDS = 1.5"),
    # Row 5: resumed in the first pass in which no other descendant lives.
    "rv6-resume-not-before-grace": ("and root_pid in owned and not (live - {root_pid}):",
                                    "and root_pid in owned and not (live - {root_pid}) and clock >= deadline:"),
    "rv6-resume-not-first-pass": ("and root_pid in owned and not (live - {root_pid}):",
                                  "and root_pid in owned and not (live - {root_pid}) and passes > 1:"),
    # Row 6: ten seconds of its own.
    "rv6-trap-9s": ("TRAP_SECONDS = 10.0", "TRAP_SECONDS = 9.0"),
    # Row 11: 10 s after that deadline and no later (here: earlier).
    "rv6-vanishing-5s": ("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= limit + REAP_SECONDS / 2)"),
}
names = sys.argv[3:] or list(MINE)
for name in names:
    old, new = MINE[name]
    pts.MUTANTS[name] = (None, "reviewer probe", (old, new))
import os
targets = (None,) if os.environ.get("RV6_WHOLE") else tsc.OWNER_CONTROLS
runs = [(name, control) for name in names for control in targets]
with OwnedProcesses():
    with tempfile.TemporaryDirectory(prefix="rv6-mutants-",
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
    print(f"== {name}: {'SURVIVES (green on all ' + str(len(targets)) + ')' if not red else 'red on ' + ', '.join(red)}", flush=True)
    if not red:
        survivors.append(name)
print(f"row mutants: {len(names)} run, survivors {survivors}")

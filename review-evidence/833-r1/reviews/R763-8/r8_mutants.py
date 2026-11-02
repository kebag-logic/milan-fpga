"""Reviewer mutants for round 8: each applied by the repository's own mutant_tree and run by its run_mutant.

Usage: python3 -B r8_mutants.py <clone> <jobs> [NAME ...]
Prints each mutant / control as red or green, and its last line. A mutant green on every owner control
is a survivor.
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

RESUME = "and root_pid in owned and not (live - {root_pid}):"
NEW_TERM = "                    if (pid, start) not in initial:\n                        continue\n                elif"
MINE = {
    # Row 5: the shell is resumed while a descendant new since the first census still lives.
    "r8-resume-beside-new-live": (RESUME, "and root_pid in owned and not ({p for p in live if (p, owned[p][1])"
                                          " in initial} - {root_pid}):"),
    # Rows 2 and 6: a trap's command gets SIGTERM inside grace after a resume at or past 1.5 s.
    "r8-sigterm-trap-command-after-late-grace-resume": (NEW_TERM, "                    if (pid, start) not in initial"
                                                                  " and not (resumed is not None and resumed >= 1.5):\n"
                                                                  "                        continue\n                elif"),
}
names = sys.argv[3:] or list(MINE)
for name in names:
    pts.MUTANTS[name] = (None, "reviewer probe", MINE[name])
runs = [(name, control) for name in names for control in tsc.OWNER_CONTROLS]
with OwnedProcesses():
    with tempfile.TemporaryDirectory(prefix="r8-mutants-") as scratch:
        trees = {name: pts.mutant_tree(Path(scratch), name) for name in names}
        with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
            results = dict(zip(runs, pool.map(lambda run: pts.run_mutant(trees[run[0]], run[1]), runs)))
for name in names:
    reds = []
    for control in tsc.OWNER_CONTROLS:
        status, seconds, output = results[(name, control)]
        lines = [line for line in output.splitlines() if line.strip()]
        verdict = "cut" if status is None else "red" if status else "green"
        reds += [control] if status else []
        print(f"{name} / {control}: {verdict} rc {status} {seconds:.1f} s: {lines[-1][:200] if lines else ''}")
    print(f"{name}: {'SURVIVOR' if not reds else 'red on ' + ', '.join(reds)}")

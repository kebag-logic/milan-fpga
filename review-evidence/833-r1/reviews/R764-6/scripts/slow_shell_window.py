#!/usr/bin/env python3
"""Run owner_shell_window with every census pass of its owner slowed (review probe).

Usage:
  python3 slow_shell_window.py one <scripts_dir> <seconds>     # one run, from that scripts dir
  python3 slow_shell_window.py campaign <repo> <jobs> <reps> <seconds,...> [MUTANT ...]
The campaign runs `none` <reps> times at each pass time, and each named mutant (default: every
MUTANTS entry whose control is owner_shell_window) once at each pass time, each in a fresh
process from a mutant tree made by the repository's own mutant_tree. Only the control's own
owner is slowed: a sleep inside its census, so the pass, not the pause after it, is long.
"""
import concurrent.futures
import subprocess
import sys
import tempfile
import time
from pathlib import Path

if sys.argv[1] == "one":
    scripts, seconds = Path(sys.argv[2]), float(sys.argv[3])
    sys.path.insert(0, str(scripts))
    import test_suite_cancellation as tsc
    from owned_process import OwnedProcesses

    passes = []

    class Slow(OwnedProcesses):
        def _descendants(self):
            passes.append(time.monotonic())
            time.sleep(seconds)
            return super()._descendants()

    with tempfile.TemporaryDirectory(prefix="slow-sw-") as scratch, OwnedProcesses():
        tsc.OwnedProcesses = Slow
        began = time.monotonic()
        tsc.owner_shell_window(Path(scratch))
    print(f"slow-shell-window {seconds}: PASS passes={len(passes)} wall={time.monotonic() - began:.1f}s")
    sys.exit(0)

repo, jobs, reps = Path(sys.argv[2]).resolve(), int(sys.argv[3]), int(sys.argv[4])
times = [float(x) for x in sys.argv[5].split(",")]
sys.path.insert(0, str(repo / "scripts"))
import process_test_support as pts  # noqa: E402

names = sys.argv[6:] or [n for n, e in pts.MUTANTS.items() if e[0] == "owner_shell_window"]
runs = [("none", t, r) for t in times for r in range(reps)] + [(n, t, 0) for n in names for t in times]


def one(run):
    name, t, _r = run
    root = trees[name]
    began = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-B", __file__, "one", str(root / "scripts"), str(t)], cwd=root,
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=240,
                           start_new_session=True)
        status, out = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        status, out = None, "TIMEOUT"
    return status, time.monotonic() - began, out


scratch_root = Path(__file__).resolve().parent.parent / "scratch"
with tempfile.TemporaryDirectory(prefix="slow-sw-trees-", dir=str(scratch_root)) as scratch:
    trees = {"none": repo}
    trees.update({n: pts.mutant_tree(Path(scratch), n) for n in names})
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = list(zip(runs, pool.map(one, runs)))
bad = []
for (name, t, r), (status, secs, out) in results:
    lines = [l for l in out.splitlines() if l.strip()]
    verdict = "cut" if status is None else "red" if status else "green"
    words = pts.MUTANTS[name][1] if name != "none" else ""
    hit = (words in out) if name != "none" else None
    print(f"{name} @ {t}s #{r}: {verdict} rc {status} {secs:.1f}s words={hit}: {lines[-1][:220] if lines else ''}")
    if (name == "none" and status != 0) or (name != "none" and (not status or not hit)):
        bad.append((name, t, r, verdict))
print(f"slow shell-window campaign: {'FAIL' if bad else 'PASS'} runs={len(results)} bad={bad}")

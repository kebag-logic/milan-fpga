#!/usr/bin/env python3
"""Build one mutant copy of the cleanup owner and its sweep test.

Usage: mutate.py REPO OUTDIR NAME
Copies REPO/scripts/{owned_process,test_suite_cancellation,process_test_support}.py
to OUTDIR/scripts and applies the named mutation, refusing unless each anchor
occurs exactly once. NAME 'none' copies unchanged.
"""
import shutil, sys
from pathlib import Path

MUTANTS = {
    "none": [],
    # The parent becomes part of a descendant's identity again.
    "identity-includes-parent": [(
        "return None if fields is None else (int(fields[1]), fields[19])",
        "return None if fields is None else (int(fields[1]), fields[1] + ':' + fields[19])")],
    # Judge the census with no collection after it.
    "no-reap-after-census": [("reaped = self._reap()", "reaped = set()")],
    # Deadlines on the wall clock: a stalled pass advances them in full.
    "deadline-wall-clock": [("clock += min(now - last, MAX_PASS_SECONDS)", "clock += now - last")],
    # The cap exists but is larger than every deadline in the stall control.
    "pass-cap-5s": [("MAX_PASS_SECONDS = 0.5", "MAX_PASS_SECONDS = 5.0")],
    # A resumed shell gets no window of its own.
    "no-shell-window": [("kill_all = max(kill_all, clock + TRAP_SECONDS)", "kill_all = kill_all")],
    # Trap-started commands get the pre-change 1 s instead of the shell's window.
    "trap-commands-1s": [(
        "if (pid, start) not in initial and resumed is not None:",
        "if (pid, start) not in initial and resumed is not None and clock < resumed + 1.0:")],
    # Raise without first sending SIGKILL to what remains.
    "no-kill-before-raise": [(
        "                for pid, (_parent, start) in owned.items():\n"
        "                    self._send(pid, start, signal.SIGKILL)\n", "")],
    # An empty owned set never reaches a verdict.
    "endless-unbounded": [("(owned or clock >= limit + REAP_SECONDS)", "owned")],
    # A survivor never fails the run: the verdict is removed.
    "survivor-never-fails": [(
        "if clock >= limit and (owned or clock >= limit + REAP_SECONDS):", "if False:")],
    # A SIGKILLed process is treated as gone.
    "killed-counts-as-gone": [(
        "owned = {pid: entry for pid, entry in census.items() if pid not in reaped}",
        "owned = {pid: entry for pid, entry in census.items() if pid not in reaped and pid not in killed}")],
    # The failure message omits the scheduler state.
    "report-without-state": [("state {fields[0]} wchan", "wchan")],
    # The failure message omits the wait channel.
    "report-without-wchan": [("wchan {wchan} parent", "parent")],
    # Cleanup does nothing at all.
    "cleanup-does-nothing": [(
        "        started = last = time.monotonic()\n", "        return\n        started = last = time.monotonic()\n")],
}

repo, out, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
(out / "scripts").mkdir(parents=True, exist_ok=True)
for f in ("owned_process.py", "test_suite_cancellation.py", "process_test_support.py"):
    shutil.copyfile(repo / "scripts" / f, out / "scripts" / f)
target = out / "scripts/owned_process.py"
text = target.read_text()
for old, new in MUTANTS[name]:
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique ({text.count(old)}): {old!r}")
    text = text.replace(old, new)
target.write_text(text)
print(name, "applied", len(MUTANTS[name]))

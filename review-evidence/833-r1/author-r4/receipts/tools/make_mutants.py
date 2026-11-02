#!/usr/bin/env python3
"""usage: make_mutants.py <head_scripts_dir> <out_dir>

Write one copy of scripts/ per mutant under <out_dir>/<name>/, each with one
fix of scripts/owned_process.py reverted. Every edit must match exactly once."""
import shutil, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
MUTANTS = {
    "none": [],
    "identity-includes-parent": [
        ("initial = {(pid, start): parent for pid, (parent, start) in owned.items()}",
         "initial = {(pid, start, parent): parent for pid, (parent, start) in owned.items()}"),
        ("first = {pid: parent for (pid, _start), parent in initial.items()}",
         "first = {pid: parent for (pid, _start, _p), parent in initial.items()}"),
        ("if (pid, start) not in initial:\n                        continue",
         "if (pid, start, _parent) not in initial:\n                        continue"),
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start, _parent) not in initial and resumed is not None:"),
        # The send's identity recheck also compares the parent, as before #833.
        ("if key not in notified and self._send(pid, start, signum):",
         "if key not in notified and _identity(pid) == (_parent, start) and self._send(pid, start, signum):"),
    ],
    "no-reap-after-census": [("reaped = self._reap()", "reaped = set()")],
    "deadline-wall-clock": [("clock += min(now - last, MAX_PASS_SECONDS)", "clock += now - last")],
    "pass-cap-5s": [("MAX_PASS_SECONDS = 0.5", "MAX_PASS_SECONDS = 5.0")],
    "pass-cap-1.5s": [("MAX_PASS_SECONDS = 0.5", "MAX_PASS_SECONDS = 1.5")],
    "no-shell-window": [("kill_all = max(kill_all, clock + TRAP_SECONDS)", "pass")],
    "trap-commands-1s": [("if (pid, start) not in initial and resumed is not None:",
                          "if (pid, start) not in initial and resumed is not None and clock < resumed + 1.0:")],
    "trap-commands-no-window": [("if (pid, start) not in initial and resumed is not None:", "if False:")],
    "no-kill-before-raise": [("for pid, (_parent, start) in owned.items():\n                    self._send(pid, start, signal.SIGKILL)",
                              "for pid, (_parent, start) in ():\n                    self._send(pid, start, signal.SIGKILL)")],
    "endless-unbounded": [("(owned or clock >= limit + REAP_SECONDS)", "owned")],
    "survivor-never-fails": [("if clock >= limit and (owned", "if False and (owned")],
    "report-without-state": [("state {fields[0]} wchan {wchan} ", "")],
    "reap-window-2s": [("REAP_SECONDS = 10.0", "REAP_SECONDS = 2.0")],
}
for name, edits in MUTANTS.items():
    dest = out / name
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))
    path = dest / "owned_process.py"
    text = path.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old, text.count(old))
        text = text.replace(old, new)
    path.write_text(text)
    print(name, len(edits), "edits")

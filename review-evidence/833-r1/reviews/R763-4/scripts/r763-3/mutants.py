#!/usr/bin/env python3
"""Reviewer mutants of scripts/owned_process.py: one product edit each, applied to a copy.

usage: mutants.py HEAD_SCRIPTS_DIR OUT_DIR
Each mutant names the cleanup property it removes; every edit must match exactly once.
"""
import shutil, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
FIX = "resumed is None and root_pid in owned and not (live - {root_pid}):"
MUT = {
    "none": [],
    "new-fix-reverted": [(FIX, "resumed is None and not (live - {root_pid}):")],
    "new-fix-census-not-owned": [(FIX, "resumed is None and root_pid in census and not (live - {root_pid}):")],
    "pass-unclamped": [("clock += min(now - last, MAX_PASS_SECONDS)", "clock += now - last")],
    "no-reap-after-census": [("reaped = self._reap()\n", "reaped = set()\n")],
    "no-trap-window": [("kill_all = max(kill_all, clock + TRAP_SECONDS)", "kill_all = max(kill_all, clock)")],
    "listing-unbounded": [("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
                           "if clock >= limit and owned:")],
    "no-kill-before-raise": [("                for pid, (_parent, start) in owned.items():\n"
                              "                    self._send(pid, start, signal.SIGKILL)\n", "")],
    "identity-has-parent": [("initial = {(pid, start): parent for pid, (parent, start) in owned.items()}",
                             "initial = {(pid, start, parent): parent for pid, (parent, start) in owned.items()}")],
    "report-without-state": [("return (f\"pid {pid} ({name.split('(', 1)[1]}) state {fields[0]} wchan {wchan} parent {fields[1]} \"",
                              "return (f\"pid {pid} ({name.split('(', 1)[1]}) parent {fields[1]} \"")],
    "shell-killed-when-resumed": [("(resumed is None or clock < kill_all):", "resumed is None:")],
    "trap-commands-no-window": [("                    if (pid, start) not in initial and resumed is not None:\n"
                                 "                        continue\n", "")],
    "survivor-never-fails": [("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):", "if False:")],
}
for name, edits in MUT.items():
    d = out / name
    shutil.copytree(src, d, dirs_exist_ok=True)
    p = d / "owned_process.py"
    text = p.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    p.write_text(text)
    print(name)

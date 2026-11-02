#!/usr/bin/env python3
"""One product edit per mutant of scripts/owned_process.py, each applied to a copy of the head's scripts/.

usage: mutants.py HEAD_SCRIPTS_DIR OUT_DIR
Every edit must match exactly once. Names follow the earlier public tables where the edit is the same.
"""
import shutil, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
GUARD = "(resumed is None or clock < kill_all):"
TRAP_CHILD = ("                    if (pid, start) not in initial and resumed is not None:\n"
              "                        continue\n")
MUT = {
    "none": [],
    # The round 3 finding's mutant: the in-window term removed from the guard.
    "shell-killed-when-resumed": [(GUARD, "resumed is None:")],
    # Falsification: the shell is spared only in the pass that resumes it.
    "shell-window-one-pass": [(GUARD, "(resumed is None or clock <= resumed):")],
    # Falsification: the shell keeps 1 s of its window, shorter than its trap's 1.5 s command.
    "shell-window-1s": [(GUARD, "(resumed is None or clock < resumed + 1.0):")],
    "M05-no-trap-window": [("                kill_all = max(kill_all, clock + TRAP_SECONDS)\n", "")],
    "M06-root-killed-unresumed": [("(resumed is None or clock < kill_all)", "clock < kill_all")],
    "no-trap-window": [("kill_all = max(kill_all, clock + TRAP_SECONDS)", "kill_all = max(kill_all, clock)")],
    "trap-commands-no-window": [(TRAP_CHILD, "")],
    "trap-commands-1s": [("                    if (pid, start) not in initial and resumed is not None:\n",
                          "                    if (pid, start) not in initial and resumed is not None and clock < resumed + 1.0:\n")],
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

#!/usr/bin/env python3
"""Two spot-check mutants of scripts/owned_process.py, each one exact edit on a copy.

usage: spot_mutants.py HEAD_SCRIPTS_DIR OUT_DIR
"""
import shutil, sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
MUT = {
    # Pre-fix root rule: a notified shell is killed at the kill time even when never resumed.
    "root-killed-unresumed": [("(resumed is None or clock < kill_all)", "clock < kill_all")],
    # A trap-started command keeps only 1 s of the resumed shell's window.
    "trap-commands-1s": [("if (pid, start) not in initial and resumed is not None:",
                          "if (pid, start) not in initial and resumed is not None and clock < resumed + 1.0:")],
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

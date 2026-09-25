#!/usr/bin/env python3
"""Apply one exact-text mutant in a disposable tree, run a command, restore.

usage: mutate.py <tree> <name> <relpath> <old> <new> -- <cmd...>
Runs <cmd> from <tree> with the mutant applied (old must occur exactly once),
writes receipts/<name>.log/.exit, then restores the file with git checkout
and asserts the tree is clean again. Exit 0 means the harness ran; the
recorded exit is the command's own verdict.
"""
import datetime, pathlib, subprocess, sys

tree, name, rel, old, new = sys.argv[1:6]
cmd = sys.argv[sys.argv.index("--") + 1:]
out = pathlib.Path(__file__).resolve().parent.parent / "receipts"
path = pathlib.Path(tree) / rel
text = path.read_text()
assert text.count(old) == 1, f"{old!r} occurs {text.count(old)} times"
path.write_text(text.replace(old, new))
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    with open(out / f"{name}.log", "w") as log:
        rc = subprocess.run(cmd, cwd=tree, stdout=log, stderr=subprocess.STDOUT).returncode
finally:
    subprocess.run(["git", "checkout", "--", rel], cwd=tree, check=True)
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                           cwd=tree, capture_output=True, text=True).stdout
    assert dirty == "", dirty
(out / f"{name}.exit").write_text(
    f"mutant: {rel}: {old!r} -> {new!r}\ncmd: {' '.join(cmd)}\nstart: {start}\nexit: {rc}\n")
print(f"{name} exit={rc}")

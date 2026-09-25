#!/usr/bin/env python3
"""Apply one exact-text mutant in a disposable tree, run a command, restore.

usage: mutate3.py <tree> <receipt-dir> <name> <relpath> <old> <new> -- <cmd...>

<old> must occur exactly once in <tree>/<relpath>. The command runs from <tree>
with the mutant applied; its output goes to <receipt-dir>/<name>.log and its
exit code to <receipt-dir>/<name>.exit. The original bytes and mode are
restored afterwards (this also works for files inside submodules) and their
SHA-256 is asserted equal to the pre-mutation value. Python escape sequences
(\\n) in <old>/<new> are decoded.
"""
import datetime
import hashlib
import os
import pathlib
import subprocess
import sys

tree, rdir, name, rel, old, new = sys.argv[1:7]
old = old.encode().decode("unicode_escape")
new = new.encode().decode("unicode_escape")
cmd = sys.argv[sys.argv.index("--") + 1:]
out = pathlib.Path(rdir)
path = pathlib.Path(tree) / rel
orig = path.read_bytes()
mode = os.stat(path).st_mode
digest = hashlib.sha256(orig).hexdigest()
text = orig.decode()
assert text.count(old) == 1, f"{old!r} occurs {text.count(old)} times"
path.write_text(text.replace(old, new))
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    with open(out / f"{name}.log", "w") as log:
        rc = subprocess.run(cmd, cwd=tree, stdout=log,
                            stderr=subprocess.STDOUT).returncode
finally:
    path.write_bytes(orig)
    os.chmod(path, mode)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
(out / f"{name}.exit").write_text(
    f"mutant: {rel}: {old!r} -> {new!r}\ncmd: {' '.join(cmd)}\n"
    f"start: {start}\nexit: {rc}\nrestored sha256: {digest}\n")
print(f"{name} exit={rc}")

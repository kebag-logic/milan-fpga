#!/usr/bin/env python3
"""R584-12: export the tracked tree of <repo> at HEAD into <out-root> (git archive) and apply one textual mutant to
sw/firmware/ctrl/test/ctrl_build.py there (the old text must occur exactly once). <repo> itself is not written.

Usage: python3 -I make_mutant.py <repo> <out-root> <name>
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    # the hash check of every object read is skipped
    "no-hash": ("    if held != oid:\n", "    if False:\n"),
    # the helper no longer gives Git core.fsmonitor=false
    "no-fsmonitor-off": ('["git", "-c", "core.fsmonitor=false", "-C",', '["git", "-C",'),
    # the hash is taken with the wrong type header, so every genuine object would be refused (a fail-closed check)
    "wrong-header": ('b"%s %d\\0" % (kind.encode(),', 'b"%s %d\\0" % (b"blob",'),
    # candidate remedy for the lazy-fetch route: no lazy fetch (not a source fix; evidence of feasibility only)
    "remedy-no-lazy-fetch": ('GIT_ENVIRONMENT = {"GIT_NO_REPLACE_OBJECTS": "1",',
                             'GIT_ENVIRONMENT = {"GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1",'),
}

repo, out, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
archive = subprocess.run(["git", "-C", str(repo), "archive", "HEAD"], capture_output=True, check=True).stdout
subprocess.run(["tar", "-x", "-C", str(out)], input=archive, check=True)
old, new = MUTANTS[name]
f = out / "sw/firmware/ctrl/test/ctrl_build.py"
text = f.read_text(encoding="utf-8")
assert text.count(old) == 1, (name, text.count(old))
f.write_text(text.replace(old, new), encoding="utf-8")
print(f"mutant {name} written to {out}")

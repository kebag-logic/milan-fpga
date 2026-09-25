#!/usr/bin/env python3
"""Apply one textual mutant to a disposable tree, run one command, restore.

Usage: mutant.py TREE LABEL EXPECT FILE OLD NEW -- CMD...
  TREE    disposable copy of the reviewed checkout (never the review clone)
  EXPECT  'detect' (command must exit nonzero) or 'survive' (must exit 0)
  FILE    path relative to TREE; OLD must occur exactly once
  OLD/NEW literal strings; '\\n' is expanded to a newline
Prints one RESULT line and exits 0 when the observation matched EXPECT.
The file's original bytes are restored and re-hashed before exit.
"""
import hashlib
import subprocess
import sys
from pathlib import Path


def main() -> int:
    sep = sys.argv.index("--")
    tree, label, expect, rel, old, new = sys.argv[1:sep]
    cmd = sys.argv[sep + 1:]
    old = old.replace("\\n", "\n")
    new = new.replace("\\n", "\n")
    path = Path(tree) / rel
    original = path.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode()
    count = text.count(old)
    if count != 1:
        print(f"RESULT {label}: PLANT-ERROR old occurs {count} times in {rel}")
        return 2
    path.write_text(text.replace(old, new))
    try:
        proc = subprocess.run(cmd, cwd=tree, timeout=7200)
        rc = proc.returncode
    finally:
        path.write_bytes(original)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    observed = "detect" if rc != 0 else "survive"
    verdict = "AS-EXPECTED" if observed == expect else "UNEXPECTED"
    print(f"RESULT {label}: exit={rc} observed={observed} expected={expect} {verdict}")
    return 0 if observed == expect else 1


if __name__ == "__main__":
    sys.exit(main())

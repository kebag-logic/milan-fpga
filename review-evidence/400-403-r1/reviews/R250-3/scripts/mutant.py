#!/usr/bin/env python3
"""Apply one exact source replacement, run a default make target, restore.

Usage: mutant.py <checkout> <receipt> <file> <old> <new> <make-dir>

The replacement must match exactly once. The original bytes are restored
and their SHA-256 is re-verified even when the run fails or is interrupted.
The receipt records the mutant, make's exit status, wall clock, every
failing check line and each run's summary line.
"""
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    repo, receipt, rel, old, new, mdir = sys.argv[1:7]
    path = Path(repo) / rel
    orig = path.read_bytes()
    digest = hashlib.sha256(orig).hexdigest()
    text = orig.decode()
    if text.count(old) != 1:
        print(f"replacement matches {text.count(old)} times, expected 1")
        return 3
    env = dict(os.environ)
    if env.get("TOOLBIN"):
        env["PATH"] = env["TOOLBIN"] + ":" + env["PATH"]
    lines = [f"# head: {subprocess.check_output(['git', '-C', repo, 'rev-parse', 'HEAD'], text=True).strip()}",
             f"# file: {rel}", f"# original sha256: {digest}",
             f"# replace: {old!r}", f"# with:    {new!r}", f"# target: make -C {mdir}"]
    try:
        path.write_text(text.replace(old, new))
        t0 = time.monotonic()
        run = subprocess.run(["make", "-C", str(Path(repo) / mdir)], env=env,
                             capture_output=True, text=True)
        wall = time.monotonic() - t0
    finally:
        path.write_bytes(orig)
    restored = hashlib.sha256(path.read_bytes()).hexdigest()
    log = run.stdout + run.stderr
    keep = [l for l in log.splitlines()
            if "FAIL" in l or "failures" in l or "RESULT" in l
            or "declaration fixture" in l or "Error" in l or "error:" in l]
    lines += [f"# exit: {run.returncode}", f"# wall_seconds: {wall:.3f}",
              f"# restored sha256: {restored} {'OK' if restored == digest else 'MISMATCH'}",
              "# --- failing checks and summaries ---"] + keep
    Path(receipt).write_text("\n".join(lines) + "\n")
    Path(receipt + ".log").write_text(log)
    print("\n".join(lines[6:10]))
    return 0 if restored == digest else 4


if __name__ == "__main__":
    sys.exit(main())

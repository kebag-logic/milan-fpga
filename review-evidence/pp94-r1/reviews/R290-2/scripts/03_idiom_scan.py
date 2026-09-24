#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Scan only the PR's changed C++/Python files with the parent's own pure scan functions.

Not the parent gate: no ratchet, no tree walk, no submodule check. It imports the
checker modules copied from parent dev 9d328810 and calls their per-file scanners
on the base and head blobs of each changed file.
Usage: 03_idiom_scan.py <clone> <checker-dir>
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

BASE = "008edbbf486598ae237414273d75e385cf0e1a56"
HEAD = "cc077a6ffe20585d20b116f008e07189ba1bb7f8"


def load(path: Path):
    """Import one checker module from its file path."""
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blob(clone: str, rev: str, rel: str) -> str:
    """Return a file's text at a revision, or '' when absent."""
    r = subprocess.run(["git", "-C", clone, "show", f"{rev}:{rel}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def main() -> int:
    """Print nonzero per-file counts at base and head for every changed C++/Python file."""
    clone, tools = sys.argv[1], Path(sys.argv[2])
    cpp = load(tools / "check_cpp_idiom.py")
    py = load(tools / "check_py_idiom.py")
    names = subprocess.run(["git", "-C", clone, "diff", "--name-only", BASE, HEAD],
                           capture_output=True, text=True).stdout.split()
    for rel in names:
        if rel.endswith((".cpp", ".hpp", ".h", ".cc")):
            fn = cpp.scan
        elif rel.endswith(".py"):
            fn = py.scan
        else:
            continue
        for tag, rev in (("base", BASE), ("head", HEAD)):
            text = blob(clone, rev, rel)
            res = fn(text, rel) if text else None
            res = res[0] if isinstance(res, tuple) else res
            counts = {k: v for k, v in dict(res).items() if v} if text else "absent"
            print(f"{rel} {tag}: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

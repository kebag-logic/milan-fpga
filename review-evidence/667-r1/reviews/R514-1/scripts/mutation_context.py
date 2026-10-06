#!/usr/bin/env python3
"""Reviewer mutation-context search (R514-1, #667).

For every Python string literal (and adjacent-literal concatenation) in the
repository's tracked tb/ and scripts/ Python files, and every tracked
*.patch file's removed/context lines, report any fragment that occurs in the
packetizer at either revision, and require its occurrence count to be equal
at base and head (an exact-text mutation site neither lost nor duplicated).
Also reports whether any fragment overlaps a line the PR added.

usage: mutation_context.py TREE_ROOT BASE_RTL HEAD_RTL
"""
import ast
import subprocess
import sys
from pathlib import Path


def literals(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            yield node.value


def main() -> int:
    root, base_rtl, head_rtl = (Path(a) for a in sys.argv[1:4])
    base = base_rtl.read_text()
    head = head_rtl.read_text()
    added = [l for l in head.splitlines() if l not in base.splitlines()]
    files = subprocess.run(["git", "-C", str(root), "ls-files", "*.py", "*.patch"],
                           capture_output=True, text=True, check=True).stdout.split()
    hits = 0
    bad = 0
    for rel in files:
        p = root / rel
        if rel.endswith(".patch"):
            frags = [l[1:] for l in p.read_text(errors="replace").splitlines()
                     if l[:1] in "- " and len(l) > 12]
        else:
            frags = [s for s in literals(p) if len(s.strip()) >= 12]
        for s in frags:
            cb, ch = base.count(s), head.count(s)
            if cb or ch:
                hits += 1
                flag = "OK" if cb == ch else "COUNT-CHANGED"
                bad += cb != ch
                overl = any(s.strip() and (s.strip() in a or a.strip() in s) for a in added if a.strip())
                print(f"{flag} base={cb} head={ch} added-overlap={overl} {rel}: {s[:70]!r}")
    print(f"MUTATION-CONTEXT files={len(files)} fragments-in-packetizer={hits} count-changed={bad}")
    print(f"ADDED-LINES {len(added)}")
    for a in added:
        print(f"  + {a}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""List every `<file>:<line>[-<line>]` citation in a tree that points into a
file the PR changed, and compare the cited lines at head with the lines the
same citation text named at base. A citation whose text is unchanged but whose
cited lines changed is printed as MOVED.

usage: cite_check.py <base-tree> <head-tree> <changed-file> ...
"""
import re
import sys
from pathlib import Path

base, head = Path(sys.argv[1]), Path(sys.argv[2])
changed = sys.argv[3:]
by_name = {}
for c in changed:
    by_name.setdefault(Path(c).name, []).append(c)
pat = re.compile(r"([A-Za-z0-9_./-]*?([A-Za-z0-9_.-]+\.(?:sv|sh|py|cpp|md|tcl|v|yml|txt))):(\d+)(?:-(\d+))?")
TEXT = {".sv", ".sh", ".py", ".cpp", ".md", ".tcl", ".v", ".yml", ".txt", ".h", ".hpp", ""}


def lines(tree, rel, a, b):
    p = tree / rel
    if not p.exists():
        return None
    L = p.read_text(errors="replace").splitlines()
    return [L[i - 1].strip() if 0 < i <= len(L) else "<EOF>" for i in range(a, b + 1)]


def resolve(full, name, citer):
    if full in changed:
        return full
    cands = [c for c in by_name.get(name, []) if c.endswith(full.lstrip("./"))]
    if len(cands) == 1:
        return cands[0]
    cands = by_name.get(name, [])
    if len(cands) == 1:
        return cands[0]
    # same-directory relative reference
    rel = str((citer.parent / full).as_posix())
    return rel if rel in changed else None


n_moved = 0
for f in sorted(head.rglob("*")):
    if not f.is_file() or f.suffix not in TEXT or ".git" in f.parts:
        continue
    citer = f.relative_to(head)
    for ln, text in enumerate(f.read_text(errors="replace").splitlines(), 1):
        for m in pat.finditer(text):
            full, name, a = m.group(1), m.group(2), int(m.group(3))
            b = int(m.group(4) or a)
            if b < a or b - a > 60:
                continue
            tgt = resolve(full, name, citer)
            if not tgt:
                continue
            h = lines(head, tgt, a, b)
            o = lines(base, tgt, a, b)
            tag = "SAME " if h == o else "MOVED"
            if h != o:
                n_moved += 1
            print(f"{tag} {citer}:{ln} -> {tgt}:{a}-{b}")
            if h != o:
                print(f"      head: {h[:3]}")
                print(f"      base: {o[:3] if o else None}")
print(f"# {n_moved} citation(s) whose cited lines differ between base and head")

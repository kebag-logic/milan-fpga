#!/usr/bin/env python3
"""Apply the parent's wall-clock detector to every processor tb/ source file.

Usage: parent_wallclock_scan.py <parent-scripts-dir> <base-tree> <head-tree>

Only the parent gate's pure `uses_wall_clock()` is called (no parent tree, no
bank). The parent ratchet counts suite files, across the superproject and the
processor suites, that use a host clock or a process/socket deadline; this
prints which processor tb/ files it flags at base and at head.
"""
import importlib.util
import sys
from pathlib import Path

GATE_DIR, BASE, HEAD = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(GATE_DIR))
spec = importlib.util.spec_from_file_location("mte", GATE_DIR / "measure_test_evidence.py")
mte = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mte)

flagged = {}
for label, tree in (("base", BASE), ("head", HEAD)):
    flagged[label] = sorted(
        p.relative_to(tree).as_posix() for p in (tree / "tb").rglob("*")
        if p.is_file() and p.suffix in (".py", ".sh", ".cpp", ".h", ".hpp", "")
        and mte.uses_wall_clock(p.read_text(errors="replace"), mte.file_suffix(str(p))))
    print(f"{label}: {len(flagged[label])} processor tb/ files flagged: {flagged[label]}")
added = sorted(set(flagged["head"]) - set(flagged["base"]))
print("added by this PR:", added)
sys.exit(1 if added else 0)

#!/usr/bin/env python3
"""Which real pages does a pure blank-line edit move, through the 15-line scan window?

Usage: window_sweep.py CLONE. Compares each page's derived row (audience, purpose, describes,
status, evidence) before and after blank-line edits, without rendering the whole page per edit.
"""
import importlib.util
import json
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("inv", clone / "scripts/docs_inventory.py")
inv = importlib.util.module_from_spec(spec)
sys.modules["inv"] = inv
spec.loader.exec_module(inv)
tree = inv.listing(clone)
paths = inv.population(tree)
_, _, judged, _ = inv.load_data(clone, paths)


def row(text, path):
    return {"audience": inv.audience_of(text, path), "purpose": inv.purpose_of(text, path),
            "describes": inv.describes_of(tree, text, path), "status": inv.status(text, path, judged)}


def edits(text):
    lines = text.split("\n")
    yield "one blank line after line 1", "\n".join(lines[:1] + [""] + lines[1:])
    yield "five blank lines after line 1", "\n".join(lines[:1] + [""] * 5 + lines[1:])
    yield "twenty blank lines after line 1", "\n".join(lines[:1] + [""] * 20 + lines[1:])
    yield "one blank line appended", text + "\n"
    yield "first blank line removed", text.replace("\n\n", "\n", 1)
    blanks = [n for n, line in enumerate(lines[:30]) if not line.strip()]
    yield "every blank line in the first 30 removed", "\n".join(l for n, l in enumerate(lines) if n not in blanks)


moved = {}
for path in paths:
    if path == inv.OUTPUT:
        continue
    text = (clone / path).read_text(encoding="utf-8", errors="replace")
    before = row(text, path)
    for label, edited in edits(text):
        after = row(edited, path)
        for key in before:
            if before[key] != after[key]:
                moved.setdefault(label, []).append((path, key, before[key], after[key]))
print("pages swept:", len(paths) - 1)
for label in ("one blank line appended", "one blank line after line 1", "five blank lines after line 1",
              "twenty blank lines after line 1", "first blank line removed", "every blank line in the first 30 removed"):
    rows = moved.get(label, [])
    print(f"{label}: {len(rows)} cell(s) move")
    for path, key, a, b in rows[:12]:
        print(f"   {path} [{key}] {str(a)[:60]!r} -> {str(b)[:60]!r}")
own = sum(1 for p in paths if p != inv.OUTPUT and any(
    inv.AUDIENCE_LINE_RE.match(l.strip()) for l in (clone / p).read_text(encoding="utf-8", errors="replace").split("\n")[:15]))
print("pages taking the audience from their own line:", own)

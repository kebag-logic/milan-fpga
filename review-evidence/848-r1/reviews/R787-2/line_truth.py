#!/usr/bin/env python3
"""Check every line --findings-dir names, exactly: literal rows on that line, copies through the module's own normaliser.

Usage: line_truth.py CLONE. The named line must carry a literal statement, or start the normalised statement.
"""
import importlib.util
import pathlib
import re
import sys
import tempfile

clone = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("inv", clone / "scripts/docs_inventory.py")
inv = importlib.util.module_from_spec(spec)
sys.modules["inv"] = inv
spec.loader.exec_module(inv)
with tempfile.TemporaryDirectory() as lanes:
    inv.main(["--findings-dir", lanes], clone)
    entries = []
    for lane in sorted(pathlib.Path(lanes).glob("*.md")):
        entries += re.findall(r"^## (D0-\d+): (.+):(\d+|\?)\n\n- Statement: (.*)$", lane.read_text(encoding="utf-8"), re.M)
literal = normalised = wrong = unlocated = 0
for ident, path, line, statement in entries:
    if line == "?":
        unlocated += 1
        print("unlocated", ident, path)
        continue
    text = (clone / path).read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    number = int(line)
    if statement in lines[number - 1]:
        literal += 1
        continue
    # The statement must start on the named line once the page is flattened, as the generator reads it.
    flat, starts = inv.flatten(text)
    needle = inv.needle_of(statement)
    hit = flat.find(needle)
    ok = hit >= 0 and inv.bisect_right(starts, hit) == number and needle[:12] in inv.normal_form(lines[number - 1]) + " " + inv.normal_form(lines[number])
    normalised += ok
    wrong += not ok
    print("normalised" if ok else "WRONG", ident, f"{path}:{number}", repr(lines[number - 1].strip()[:70]))
print(f"entries {len(entries)}: literal on the named line {literal}, normalised {normalised}, unlocated {unlocated}, wrong {wrong}")

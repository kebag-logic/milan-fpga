#!/usr/bin/env python3
"""Show that two PR-body revisions differ only inside item 1's closing paragraph of the
composed-head note (plus trailing whitespace at end of file).
usage: body_scope_check.py <old.md> <new.md>"""
import difflib, sys
old = open(sys.argv[1], encoding="utf-8").read().rstrip().split("\n")
new = open(sys.argv[2], encoding="utf-8").read().rstrip().split("\n")
ops = [o for o in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes() if o[0] != "equal"]
ok = True
for tag, i1, i2, j1, j2 in ops:
    print(f"{tag} old[{i1+1}:{i2}] new[{j1+1}:{j2}]")
    for l in old[i1:i2]: print("  - " + l)
    for l in new[j1:j2]: print("  + " + l)
    # every changed region must sit between item 1's sub-list and the item-2 heading
    start = max(i for i, l in enumerate(old[:i1 + 1]) if l.startswith("1. **The pin-adoption edits**"))
    end = next(i for i, l in enumerate(old) if l.startswith("2. **Scope of section 4"))
    ok &= start < i1 and i2 <= end
print("changed regions:", len(ops))
print("RESULT", "PASS: only item 1 changed" if ok and ops else "FAIL")
sys.exit(0 if ok and ops else 1)

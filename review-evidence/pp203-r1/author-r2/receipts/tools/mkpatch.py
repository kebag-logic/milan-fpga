#!/usr/bin/env python3
"""mkpatch.py <tree> <out.patch> <relpath> <old> <new> [<relpath> <old> <new> ...]: a unified
diff (3 lines of context, a/ b/ prefixes) of exact, single-occurrence substitutions."""
import difflib, sys
from pathlib import Path

tree, out, rest = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
assert len(rest) % 3 == 0
edits = {}
for i in range(0, len(rest), 3):
    edits.setdefault(rest[i], []).append((rest[i + 1], rest[i + 2]))
chunks = []
for rel, subs in edits.items():
    text = (tree / rel).read_text()
    new = text
    for old, rep in subs:
        n = new.count(old)
        if n != 1:
            sys.exit(f"{rel}: {n} occurrences of {old!r}")
        new = new.replace(old, rep)
    diff = difflib.unified_diff(text.splitlines(True), new.splitlines(True),
                                f"a/{rel}", f"b/{rel}", n=3)
    chunks.append("".join(l.replace("--- a/" + rel + "\n", "--- a/" + rel + "\n") for l in diff))
out.write_text("".join(chunks))
print(out.name, sum(c.count("\n@@") + c.startswith("@@") for c in chunks), "hunks")

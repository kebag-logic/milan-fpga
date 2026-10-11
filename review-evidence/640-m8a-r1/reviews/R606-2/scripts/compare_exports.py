#!/usr/bin/env python3
"""Compare two SoC export directories file by file after normalisation.

    python3 -I compare_exports.py <export-a> <tree-a> <export-b> <tree-b>

Normalised: each export's own directory and source-tree paths become
placeholders; comment lines carrying a LiteX generation date are dropped;
LiteX's comment-only hierarchy tree block in the top Verilog is dropped.
Prints one line per file (same / DIFFER / only-in-a / only-in-b) and a total;
exits 1 when any file differs or is missing on one side.
"""
import re
import sys
from pathlib import Path

DATE = re.compile(r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})|(on \d{4}-\d{2}-\d{2})|"
                  r"((Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))")


def normalise(text: str, export: Path, tree: Path) -> str:
    text = text.replace(str(export), "<EXPORT>").replace(str(tree), "<TREE>")
    out, state = [], ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("//", "#", "/*", "*")) and DATE.search(line):
            continue
        # LiteX writes the module hierarchy after a "// Hierarchy" ruler as one
        # /* ... */ comment block; its order is not stable, so drop the block.
        if stripped == "// Hierarchy":
            state = "header"
            continue
        if state == "header":
            if stripped == "/*":
                state = "block"
            continue
        if state == "block":
            if stripped == "*/":
                state = ""
            continue
        out.append(line)
    return "\n".join(out)


def files(root: Path) -> dict[str, Path]:
    return {str(p.relative_to(root)): p for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    a, ta, b, tb = (Path(x).resolve() for x in sys.argv[1:5])
    fa, fb = files(a), files(b)
    bad = 0
    for name in sorted(set(fa) | set(fb)):
        if name not in fb:
            print(f"only-in-a {name}")
            bad += 1
            continue
        if name not in fa:
            print(f"only-in-b {name}")
            bad += 1
            continue
        try:
            na = normalise(fa[name].read_text(), a, ta)
            nb = normalise(fb[name].read_text(), b, tb)
        except UnicodeDecodeError:
            na, nb = fa[name].read_bytes(), fb[name].read_bytes()
        same = na == nb
        bad += not same
        print(f"{'same  ' if same else 'DIFFER'} {name}")
    print(f"TOTAL a={len(fa)} b={len(fb)} differ_or_missing={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

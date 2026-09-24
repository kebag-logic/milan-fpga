#!/usr/bin/env python3
"""Per-page answers of one tree's gen_toc over a fixed page population.

Usage: tracked_pages.py <tree> <pages-root> <list-file> <out.json>

<tree>/scripts is imported as gen_toc. Every path in <list-file> (one per
line, relative to <pages-root>) is read with Path.read_text(), exactly as
the generator reads it, and these answers are recorded: refusals, blocks,
line_kinds (when the tree has it), headings, plan, existing() span and
separator, generated_block, owns(), and whether apply() would change it.
"""
import json
import sys
from pathlib import Path


def main() -> int:
    tree, root = Path(sys.argv[1]), Path(sys.argv[2])
    paths = [p for p in Path(sys.argv[3]).read_text().splitlines() if p]
    sys.path.insert(0, str(tree / "scripts"))
    import gen_toc as g
    out = {}
    for rel in paths:
        text = (root / rel).read_text()
        e = {"refusals": [list(r) for r in g.refusals(text)]}
        e["blocks"] = g.blocks(text)
        e["line_kinds"] = g.line_kinds(text) if hasattr(g, "line_kinds") else None
        e["headings"] = [list(h) for h in g.headings(text)]
        p = g.plan(text)
        e["plan"] = None if p is None else [list(h) for h in p]
        desc, start, end, sep = g.existing(text)
        e["existing"] = [start, end, sep, sorted(desc)]
        gb = g.generated_block(text, rel)
        e["generated_block"] = None if gb is None else [gb[0], gb[1]]
        e["owns"] = g.owns(rel, text)
        e["apply_changes"] = g.apply(root / rel, text) is not None
        out[rel] = e
    Path(sys.argv[4]).write_text(json.dumps(out, ensure_ascii=False))
    print(f"{tree}: {len(out)} pages -> {sys.argv[4]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

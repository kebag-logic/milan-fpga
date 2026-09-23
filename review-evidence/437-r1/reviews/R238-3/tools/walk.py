#!/usr/bin/env python3
"""Run one checkout's Contents walk over a list of pages.

Usage: walk.py <scripts-dir> <pages.json> <out.json>
pages.json is a list of {"name", "page"}; out.json adds "walk" (every
listed heading as [level, raw]) and "blocks" (the per-line labels).
Run once per checkout, in its own process, so two `gen_toc` modules
never share an interpreter.
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main() -> int:
    scripts, pages, out = sys.argv[1:4]
    sys.path.insert(0, scripts)
    import gen_toc
    rows = json.loads(Path(pages).read_text())
    for row in rows:
        row["walk"] = [[lvl, raw] for lvl, raw, _ in gen_toc.headings(row["page"])]
        row["blocks"] = gen_toc.blocks(row["page"])
    Path(out).write_text(json.dumps(rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

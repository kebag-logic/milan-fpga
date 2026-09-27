#!/usr/bin/env python3
"""Render one page revision with the pinned cmark-gfm and report its tables.

Usage: table_probe.py <repo> <rev> <path>
Prints the number of rendered tables, the per-table header cell counts and
row cell counts, and the raw Markdown cell counts of every pipe-table line.
Exit 0 always; the receipt is the output.
"""
import subprocess
import sys

import cmarkgfm
import html5lib
from cmarkgfm.cmark import Options


def raw_cells(line: str) -> int:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return len(body.split("|"))


def main() -> None:
    repo, rev, path = sys.argv[1:4]
    text = subprocess.run(
        ["git", "-C", repo, "show", f"{rev}:{path}"],
        check=True, capture_output=True, text=True).stdout
    html = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE)
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    tables = doc.findall(".//table")
    print(f"rev {rev} path {path}")
    print(f"rendered tables: {len(tables)}")
    for i, t in enumerate(tables):
        head = [th for th in t.iter("th")]
        rows = t.findall(".//tbody/tr")
        counts = sorted({len(r.findall("td")) for r in rows})
        first = "".join(head[0].itertext()) if head else ""
        print(f"  table {i}: header cells {len(head)}, body rows {len(rows)}, "
              f"body cell counts {counts}, first header '{first}'")
    print("raw pipe lines with 'Cycle |' header or following rows:")
    lines = text.splitlines()
    for n, line in enumerate(lines, 1):
        if line.startswith("| Cycle | OFF duration"):
            for k in range(n - 1, min(n + 11, len(lines))):
                print(f"  L{k + 1}: {raw_cells(lines[k])} cells")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check that every table of a Markdown page has a constant cell count, both
as rendered (cmarkgfm GFM tables, parsed with the standard library's HTML
parser) and in the source (unescaped pipes per row).

usage: table_cells.py <page.md> [<page.md> ...]

Exit 1 when any table has a row whose cell count differs from its header's.
"""
import re
import sys
from html.parser import HTMLParser

import cmarkgfm
from cmarkgfm.cmark import Options


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.row = [], None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tables.append([])
        elif tag == "tr":
            self.row = 0
        elif tag in ("td", "th") and self.row is not None:
            self.row += 1

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row)
            self.row = None


def source_tables(text):
    out, cur = [], []
    for line in text.split("\n"):
        if line.startswith("|"):
            cur.append(len(re.findall(r"(?<!\\)\|", line.replace("\\\\", ""))) - 1)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def main():
    bad = 0
    for page in sys.argv[1:]:
        text = open(page).read()
        p = Tables()
        p.feed(cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE))
        src = source_tables(text)
        ok = len(p.tables) == len(src) and all(len(set(t)) == 1 for t in p.tables + src) and \
            all(r[0] == s[0] for r, s in zip(p.tables, src))
        bad += not ok
        print(f"{page}: {len(p.tables)} rendered, {len(src)} source tables; "
              f"rendered rows/cells {[(len(t), sorted(set(t))) for t in p.tables]}; "
              f"source rows/cells {[(len(t), sorted(set(t))) for t in src]}; {'OK' if ok else 'MISMATCH'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

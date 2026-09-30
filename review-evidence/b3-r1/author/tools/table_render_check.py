#!/usr/bin/env python3
"""Render-check every table of one Markdown page (pinned renderer venv).

usage: table_render_check.py <page.md> [<json_out>]

Renders with cmarkgfm (GFM tables) and parses the HTML with html5lib. A
table passes when every row has the header's cell count, both as rendered
and in the source (unescaped pipes per row). Exit 1 on any mismatch.
"""
import json
import re
import sys

import cmarkgfm
import html5lib
from cmarkgfm.cmark import Options


def source_tables(text):
    tables, cur = [], []
    for line in text.splitlines():
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            tables.append(cur)
            cur = []
    if cur:
        tables.append(cur)
    out = []
    for t in tables:
        counts = [len(re.sub(r"\\\|", "", row).strip().strip("|").split("|")) for row in t]
        out.append(counts)
    return out


def main():
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    html = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE)
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    rendered = []
    for tbl in doc.iter("table"):
        rows = list(tbl.iter("tr"))
        rendered.append([len([c for c in r if c.tag in ("td", "th")]) for r in rows])
    src = source_tables(text)
    ok = len(rendered) == len(src) and all(len(set(r)) == 1 for r in rendered) \
        and all(len(set(s)) == 1 for s in src) \
        and all(r[0] == s[0] for r, s in zip(rendered, src))
    result = dict(page=path.split("/")[-1], tables=len(rendered),
                  rendered=[dict(rows=len(r), cells=sorted(set(r))) for r in rendered],
                  source=[dict(rows=len(s), cells=sorted(set(s))) for s in src], ok=ok)
    s = json.dumps(result, indent=1)
    print(s)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(s + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

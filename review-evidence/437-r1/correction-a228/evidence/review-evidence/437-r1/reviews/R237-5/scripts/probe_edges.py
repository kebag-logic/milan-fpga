#!/usr/bin/env python3
"""Edge probes of the head walk: for each page, the headings gen_toc lists
(label, anchor), the renderer's own rendered heading text, and line kinds.
Usage: probe_edges.py <tree>"""
import sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc as g

PAGES = {
    "BOM then ATX h2": "﻿## Alpha\n\n## Beta\n",
    "block quote, tab after marker": ">\t## Q\n",
    "bullet item, tab after marker": "-\t## Item\n",
    "ordered item, tab after marker": "1.\t## Item\n",
    "nested item heading after tab indent": "- a\n\n\t## Deep\n",
    "block quote in item, heading": "- a\n\n  > ## BQ\n",
    "NUL inside heading": "## a\0b\n",
    "heading after NUL line": "x\0y\n\n## After\n",
    "unreferenced footnote holding a fence": "[^n]: note\n\n    ```\n    ## Contents\n    ```\n\n## Real\n",
    "link reference definition line": "[r]: /u\n\n## Real\n",
    "html block inside list item": "- item\n\n  <div>\n  ## Old\n  </div>\n\n## Real\n",
    "raw h2 wrapping markdown heading": "<h2>\n\n## Inner\n\n</h2>\n",
    "template raw element": "<template>\n\n## T\n\n</template>\n\n## Real\n",
    "noscript raw element": "<noscript>\n\n## N\n\n</noscript>\n\n## Real\n",
    "svg foreign content": "<svg>\n\n## S\n\n</svg>\n\n## Real\n",
    "math foreign content": "<math>\n\n## M\n\n</math>\n\n## Real\n",
    "textarea (tag-filtered)": "<textarea>\n\n## TA\n\n</textarea>\n\n## Real\n",
    "plaintext (tag-filtered)": "<plaintext>\n\n## PT\n\n## Real\n",
    "object raw element": "<object>\n\n## O\n\n</object>\n\n## Real\n",
    "frameset raw": "<frameset>\n\n## F\n\n## Real\n",
    "option raw": "<option>\n\n## Op\n\n## Real\n",
    "iframe (tag-filtered)": "<iframe>\n\n## IF\n\n</iframe>\n\n## Real\n",
    "cdata in raw": "<![CDATA[\n\n## CD\n\n]]>\n\n## Real\n",
    "declaration": "<!DOCTYPE x\n\n## DT\n\n## Real\n",
}
for name, page in PAGES.items():
    try:
        page_ = g._page(page)
        hs = g.headings(page)
        rh = g.rendered_headings(page)
        print(f"{name}: {page!r}")
        print(f"   listed  {[(l, r, a) for l, r, a in hs]}")
        print(f"   rendered {rh}")
        print(f"   kinds   {g.line_kinds(page)}")
    except Exception as exc:
        print(f"{name}: EXCEPTION {type(exc).__name__}: {exc}")

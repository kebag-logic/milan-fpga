#!/usr/bin/env python3
"""Scan every tracked page's cmark-gfm HTML (raw HTML kept, GitHub's
extensions) for raw constructs the N2 limitation names, and for any
case-variant of the renderer's position attribute in the page text.
Usage: scan_raw_html.py <tree> <list-file>"""
import re, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc_renderer as r
b = r.binding(); lib, ffi = b.lib, b.ffi
lib.cmark_gfm_core_extensions_ensure_registered()
opts = lib.CMARK_OPT_UNSAFE | lib.CMARK_OPT_FOOTNOTES | lib.CMARK_OPT_GITHUB_PRE_LANG
hits = 0
paths = [p for p in Path(sys.argv[2]).read_text().splitlines() if p]
for rel in paths:
    text = (Path(sys.argv[1]) / rel).read_text()
    p = lib.cmark_parser_new(opts)
    for n in r.EXTENSIONS:
        lib.cmark_parser_attach_syntax_extension(p, lib.cmark_find_syntax_extension(n.encode()))
    raw = text.encode(); lib.cmark_parser_feed(p, raw, len(raw))
    root = lib.cmark_parser_finish(p)
    html = ffi.string(lib.cmark_render_html(root, opts, lib.cmark_parser_get_syntax_extensions(p))).decode()
    lib.cmark_parser_free(p)
    for pat in (r"<\?", r"<select\b", r"<xmp\b", r"<!--"):
        for m in re.finditer(pat, html, re.I):
            hits += pat != r"<!--"
            if pat != r"<!--":
                print(f"{rel}: raw {pat!r} in rendered HTML: {html[m.start():m.start()+60]!r}")
    if re.search(r"data-sourcepos", text, re.I):
        print(f"{rel}: spells the position attribute (any case)")
print(f"{len(paths)} pages scanned, {hits} raw <? / <select / <xmp occurrence(s)")

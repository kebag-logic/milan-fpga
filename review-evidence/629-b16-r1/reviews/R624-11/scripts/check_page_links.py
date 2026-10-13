#!/usr/bin/env python3
"""Every link target in the named pages: a relative path must exist, and a fragment (same page or another
page) must be an anchor the repository's own gen_toc.headings() gives that page.

usage: <pinned-parser python> check_page_links.py <repo root> <page.md> [<page.md> ...]

Link targets are read from the pinned renderer's HTML (href of each <a>), so only links a reader sees count.
External http(s) and mailto targets are listed, not fetched. Exit 1 on any unresolved target.
"""
import html.parser
import sys
from pathlib import Path
from urllib.parse import unquote

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import gen_toc  # noqa: E402
import cmarkgfm  # noqa: E402
from cmarkgfm.cmark import Options  # noqa: E402


class A(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d = dict(attrs)
            if "href" in d:
                self.hrefs.append(d["href"])


def anchors(p):
    return {a for _, _, a in gen_toc.headings(p.read_text(encoding="utf-8"))}


bad = 0
for arg in sys.argv[2:]:
    page = (repo / arg).resolve()
    h = cmarkgfm.github_flavored_markdown_to_html(page.read_text(encoding="utf-8"), options=Options.CMARK_OPT_UNSAFE)
    a = A()
    a.feed(h)
    local = internal = external = 0
    for href in a.hrefs:
        if href.startswith(("http://", "https://", "mailto:")):
            external += 1
            continue
        path, _, frag = href.partition("#")
        tgt = (page.parent / unquote(path)).resolve() if path else page
        if not tgt.exists():
            bad += 1
            print(f"MISSING-FILE {arg} -> {href}")
            continue
        if path:
            local += 1
        if frag:
            internal += 1
            if tgt.suffix != ".md" or unquote(frag) not in anchors(tgt):
                bad += 1
                print(f"MISSING-ANCHOR {arg} -> {href}")
    print(f"{arg}: {len(a.hrefs)} links; {local} relative paths, {internal} fragments checked, {external} external listed")
print("RESULT", "FAIL" if bad else "PASS", f"{bad} unresolved")
sys.exit(1 if bad else 0)

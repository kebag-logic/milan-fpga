#!/usr/bin/env python3
"""Harvest every (page, GitHub gfm response HTML) pair from the published
#437 review packets into one cache keyed by page text.

Usage: harvest.py INPUT_DIR OUT.json
Only public, archived receipts are read. A page seen with two different
heading lists is reported and kept with every variant.
"""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path


class Headings(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found, self.level, self.text = [], 0, ""

    def handle_starttag(self, tag, attrs):
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self.level, self.text = int(tag[1]), ""

    def handle_endtag(self, tag):
        if self.level and tag == f"h{self.level}":
            self.found.append([self.level, " ".join(self.text.split())])
            self.level = 0

    def handle_data(self, data):
        if self.level:
            self.text += data


def headings(html):
    p = Headings()
    p.feed(html)
    p.close()
    return p.found


PAGE_KEYS = ("page", "text", "base_page_text")
HTML_KEYS = ("response_bytes", "html", "response_html", "renderer_response_html", "response")


def page_of(d):
    for k in PAGE_KEYS:
        if isinstance(d.get(k), str):
            return d[k]
    req = d.get("request") or d.get("request_bytes") or d.get("renderer_request_bytes")
    if isinstance(req, str):
        try:
            req = json.loads(req)
        except ValueError:
            return None
    if isinstance(req, dict) and isinstance(req.get("text"), str):
        return req["text"]
    return None


def html_of(d):
    for k in HTML_KEYS:
        v = d.get(k)
        if isinstance(v, str) and ("<" in v or v == ""):
            return v
    return None


def walk(node, out, src):
    if isinstance(node, dict):
        page, html = page_of(node), html_of(node)
        if page is not None and html is not None:
            out.setdefault(page, {}).setdefault(json.dumps(headings(html)), []).append(src)
        for v in node.values():
            walk(v, out, src)
    elif isinstance(node, list):
        for v in node:
            walk(v, out, src)


def main():
    root, dest = Path(sys.argv[1]), Path(sys.argv[2])
    out = {}
    for f in sorted(root.rglob("*.json*")):
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            continue
        docs = []
        try:
            docs = [json.loads(text)]
        except ValueError:
            for line in text.splitlines():
                try:
                    docs.append(json.loads(line))
                except ValueError:
                    pass
        for d in docs:
            walk(d, out, str(f.relative_to(root)))
    conflicts = {p: v for p, v in out.items() if len(v) > 1}
    cache = {p: json.loads(next(iter(v))) for p, v in out.items() if len(v) == 1}
    dest.write_text(json.dumps({"pages": cache, "conflicts": {p: list(v) for p, v in conflicts.items()}}, indent=0))
    print(f"{len(out)} unique pages, {len(conflicts)} with conflicting heading lists")
    for p, v in list(conflicts.items())[:10]:
        print("CONFLICT", repr(p)[:120], list(v))


if __name__ == "__main__":
    main()

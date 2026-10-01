#!/usr/bin/env python3
"""Check every intra-page '(#anchor)' link on a page against GitHub-style heading slugs.

Usage: anchor_check.py <page.md>
"""
import re
import sys


def slug(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def main(page):
    text = open(page, encoding="utf-8").read()
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    heads = [slug(m) for m in re.findall(r"^#{1,6} (.+)$", body, re.M)]
    links = re.findall(r"\]\(#([^)]+)\)", body)
    bad = [l for l in links if l not in heads]
    print(f"headings: {len(heads)}; intra-page links: {len(links)}; unresolved: {len(bad)}")
    for b in bad:
        print("  unresolved:", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

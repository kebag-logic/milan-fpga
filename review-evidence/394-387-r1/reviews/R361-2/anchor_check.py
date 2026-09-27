#!/usr/bin/env python3
"""Check every relative link+anchor on the page resolves to a rendered heading.

Usage: anchor_check.py <repo> <rev> [--mutate OLD NEW]
Headings are taken from the pinned cmark-gfm render of each target at <rev>;
anchors use GitHub's slug rule (lower-case, drop punctuation other than '-'
and '_', spaces to '-'), with -N suffixes for repeated slugs. --mutate
applies one textual substitution to the page first, as a negative control.
Exit 1 on any unresolved anchor.
"""
import os
import re
import subprocess
import sys

import cmarkgfm
import html5lib

PAGE = "docs/findings/394_387_E1_SWITCH_CYCLES.md"


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def anchors(text):
    doc = html5lib.parse(cmarkgfm.github_flavored_markdown_to_html(text),
                         namespaceHTMLElements=False)
    seen, out = {}, set()
    for el in doc.iter():
        if el.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            label = "".join(el.itertext()).strip().lower()
            slug = re.sub(r"[^\w\- ]", "", label).replace(" ", "-")
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            out.add(slug if n == 0 else f"{slug}-{n}")
    return out


def main() -> int:
    repo, rev = sys.argv[1:3]
    page = show(repo, rev, PAGE)
    if len(sys.argv) == 6 and sys.argv[3] == "--mutate":
        page = page.replace(sys.argv[4], sys.argv[5])
    bad = 0
    links = re.findall(r"\]\((?!https?:)([^)#\s]*)#([^)\s]+)\)", page)
    for target, anchor in links:
        path = os.path.normpath(os.path.join(os.path.dirname(PAGE), target)) if target else PAGE
        text = page if path == PAGE else show(repo, rev, path)
        ok = anchor in anchors(text)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {path}#{anchor}")
    print(f"links with anchors {len(links)}; RESULT", "PASS" if not bad else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

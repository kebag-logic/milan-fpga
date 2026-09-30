#!/usr/bin/env python3
"""Check every relative Markdown link on the added lines of a commit range.

usage: anchor_check.py <repo> <base> <head>

For each added line in docs/**.md, every relative link target must exist at
<head>, and a #fragment must equal a GitHub heading anchor of the target page:
headings as the pinned cmark-gfm renders them, slugged the GitHub way
(lowercase, drop characters other than word characters, hyphens and spaces,
spaces to hyphens, -N suffix on repeats). Needs cmarkgfm and html5lib.
"""
import os
import re
import subprocess
import sys

import cmarkgfm
import html5lib
from cmarkgfm.cmark import Options


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True,
                          check=True).stdout


def anchors(md):
    html = cmarkgfm.github_flavored_markdown_to_html(md, options=Options.CMARK_OPT_UNSAFE)
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    seen, out = {}, set()
    for el in doc.iter():
        if el.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = "".join(el.itertext()).strip().lower()
            slug = re.sub(r"[^\w\- ]", "", text).replace(" ", "-")
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            out.add(slug if n == 0 else f"{slug}-{n}")
    return out


def main():
    repo, base, head = sys.argv[1:4]
    diff = subprocess.run(["git", "-C", repo, "diff", "-U0", base, head, "--", "docs"], capture_output=True,
                          text=True, check=True).stdout
    cur, bad, n = None, 0, 0
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++") or not cur or not cur.endswith(".md"):
            continue
        for tgt in re.findall(r"\]\(([^)\s]+)\)", line):
            if re.match(r"[a-z]+:", tgt):
                continue
            n += 1
            path, _, frag = tgt.partition("#")
            tpath = os.path.normpath(os.path.join(os.path.dirname(cur), path)) if path else cur
            try:
                md = show(repo, head, tpath)
            except subprocess.CalledProcessError:
                print(f"MISSING {cur}: {tgt}")
                bad += 1
                continue
            if frag and frag not in anchors(md):
                print(f"BAD-ANCHOR {cur}: {tgt}")
                bad += 1
            else:
                print(f"OK {cur}: {tgt}")
    print(f"{n} relative links on added lines, {bad} bad")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

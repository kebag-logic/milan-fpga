#!/usr/bin/env python3
"""Resolve every Markdown link on the lines a diff ADDS.

Usage: check_added_links.py <repo> <base> <head>

Relative links must resolve to a file in <head>'s tree; a fragment must match
a GitHub-style slug of a heading in the target (or in the same page). External
https links are listed for separate confirmation. Exit 1 on any unresolved
relative link or fragment.
"""
import os
import re
import subprocess
import sys

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True,
                          capture_output=True, text=True).stdout


def slugs(text):
    out = set()
    counts = {}
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        s = m.group(2).strip().lower()
        s = re.sub(r"[`*_]", "", s)
        s = re.sub(r"[^\w\- ]", "", s)
        s = s.replace(" ", "-")
        n = counts.get(s, 0)
        counts[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def main():
    repo, base, head = sys.argv[1:4]
    diff = git(repo, "diff", "--no-ext-diff", "--no-color", "-U0",
               f"{base}..{head}", "--", "*.md")
    page = None
    bad = 0
    ext = set()
    checked = 0
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            page = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        for tgt in LINK.findall(line[1:]):
            if tgt.startswith(("http://", "https://")):
                ext.add(tgt)
                continue
            if tgt.startswith("mailto:"):
                continue
            path, _, frag = tgt.partition("#")
            if path:
                target = os.path.normpath(os.path.join(os.path.dirname(page),
                                                       path))
            else:
                target = page
            try:
                text = git(repo, "show", f"{head}:{target}")
            except subprocess.CalledProcessError:
                print(f"UNRESOLVED {page}: {tgt} -> {target} (no such file)")
                bad += 1
                continue
            checked += 1
            if frag and target.endswith(".md") and frag not in slugs(text):
                print(f"BAD-FRAGMENT {page}: {tgt} (#{frag} not a heading "
                      f"slug of {target})")
                bad += 1
            else:
                print(f"OK {page}: {tgt}")
    print(f"relative links checked: {checked}; unresolved: {bad}")
    print("external links on added lines:")
    for e in sorted(ext):
        print("  ", e)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

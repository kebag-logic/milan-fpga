#!/usr/bin/env python3
"""Resolve every fragment link on the lines a change adds, against GitHub-style
heading slugs of the target page at the head revision.

Usage: new_anchor_check.py <repo> <base> <head>"""
import posixpath
import re
import subprocess
import sys

LINK = re.compile(r"\]\(([^)\s]*?)#([^)\s]+)\)")


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True,
                          text=True).stdout


def slugs(text):
    out, seen, fence = set(), {}, False
    for ln in text.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", ln)
        if not m:
            continue
        h = re.sub(r"`", "", m.group(2))
        h = re.sub(r"\[([^]]*)\]\([^)]*\)", r"\1", h)
        s = re.sub(r"[^\w\- ]", "", h.lower(), flags=re.UNICODE).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def main():
    repo, base, head = sys.argv[1:4]
    diff = git(repo, "diff", "-U0", base, head, "--", "*.md")
    page = None
    bad = checked = 0
    for ln in diff.splitlines():
        if ln.startswith("+++ b/"):
            page = ln[6:]
            continue
        if not ln.startswith("+") or ln.startswith("+++"):
            continue
        for target, frag in LINK.findall(ln):
            if target.startswith("http"):
                continue
            path = page if not target else posixpath.normpath(
                posixpath.join(posixpath.dirname(page), target))
            try:
                text = git(repo, "show", f"{head}:{path}")
            except subprocess.CalledProcessError:
                print(f"MISSING PAGE {page}: {target}#{frag}")
                bad += 1
                continue
            checked += 1
            if frag not in slugs(text):
                print(f"UNRESOLVED {page}: {target}#{frag}")
                bad += 1
    print(f"new fragment links checked {checked}, unresolved {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

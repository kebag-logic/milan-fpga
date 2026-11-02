#!/usr/bin/env python3
"""Resolve every in-page fragment link on given lines of a Markdown page
against GitHub-style heading slugs. Usage: anchor_probe.py PAGE LINE...
A built-in mutant control (an unknown fragment) must be reported missing."""
import re
import sys


def slug(text):
    text = re.sub(r"`", "", text.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def main():
    page, lines = sys.argv[1], [int(n) for n in sys.argv[2:]]
    body = open(page, encoding="utf-8").read().splitlines()
    slugs, seen, fence = set(), {}, False
    for line in body:
        if line.startswith("```"):
            fence = not fence
        if fence:
            continue
        m = re.match(r"#{1,6}\s+(.*)", line)
        if m:
            s = slug(m.group(1))
            n = seen.get(s, 0)
            seen[s] = n + 1
            slugs.add(s if n == 0 else "%s-%d" % (s, n))
    bad = 0
    for n in lines:
        for frag in re.findall(r"\]\(#([^)]+)\)", body[n - 1]):
            ok = frag in slugs
            bad += not ok
            print("line %d #%s %s" % (n, frag, "RESOLVES" if ok else "MISSING"))
    control = "firmware-and-block-ram-ledgerx"
    print("control #%s %s" % (control, "RESOLVES" if control in slugs else "MISSING"))
    if control in slugs:
        return 3
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

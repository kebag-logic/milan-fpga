#!/usr/bin/env python3
"""Resolve every `#fragment` link in Markdown pages against GitHub heading slugs.

Usage: check_fragments.py <page.md>...

Same-page (`#x`) and relative cross-page (`other.md#x`) fragments are
resolved against the headings of the target page, slugged the way GitHub
does (lowercase, drop punctuation except `-` and `_`, spaces to `-`,
duplicate slugs suffixed `-1`, `-2`). Headings inside fenced code are
ignored. Prints each link and OK/MISSING; exits 1 on any MISSING.
"""
import re
import sys
from pathlib import Path


def slugs(path):
    out, seen, fence = set(), {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        text = re.sub(r"`([^`]*)`", r"\1", m.group(2))
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
        s = re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def main():
    bad = 0
    for arg in sys.argv[1:]:
        page = Path(arg)
        for target, frag in re.findall(r"\]\(([^)#\s]*)#([^)\s]+)\)", page.read_text(encoding="utf-8")):
            if target.startswith("http"):
                continue
            tpath = (page.parent / target).resolve() if target else page
            ok = tpath.is_file() and frag in slugs(tpath)
            bad += not ok
            print(f"{'OK     ' if ok else 'MISSING'} {page}: ({target}#{frag})")
    print("RESULT:", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

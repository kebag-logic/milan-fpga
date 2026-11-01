#!/usr/bin/env python3
"""Independent link probe: every Markdown link from or into the pages PR #828 changes must resolve.

usage: probe_links.py <clone>
Reads tracked Markdown at the checked-out tree, slugs headings by the GitHub rule, and reports
links whose file or fragment does not exist. Links from a historical page into a changed page
are included. External links are counted, not fetched.
"""
import os
import re
import subprocess
import sys

CHANGED = {
    "REQUIREMENTS.md",
    "docs/ARCHITECTURE_HW_SW_SPLIT.md",
    "docs/README.md",
    "docs/design/MARK_II_AREA_PLAN.md",
    "docs/design/MARK_II_STREAM_ENGINES.md",
    "docs/overview/ARCHITECTURE.md",
    "docs/reference/FR_NFR.md",
}
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def slug(text):
    text = re.sub(r"`", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path, cache={}):
    if path in cache:
        return cache[path]
    found, seen, fenced = set(), {}, False
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced:
                continue
            match = HEAD.match(line)
            if match:
                base = slug(match.group(2))
                count = seen.get(base, 0)
                seen[base] = count + 1
                found.add(base if count == 0 else f"{base}-{count}")
            for name in re.findall(r'(?:id|name)="([^"]+)"', line):
                found.add(name)
    cache[path] = found
    return found


def links(path):
    fenced = False
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced:
                continue
            for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
                yield number, target


def main():
    os.chdir(sys.argv[1])
    pages = subprocess.run(
        ["git", "ls-files", "*.md"], capture_output=True, text=True, check=True
    ).stdout.split("\n")
    pages = [page for page in pages if page]
    checked = external = 0
    bad = []
    for page in pages:
        for number, target in links(page):
            if re.match(r"[a-z][a-z0-9+.-]*:", target):
                external += page in CHANGED
                continue
            name, _, fragment = target.partition("#")
            dest = os.path.normpath(os.path.join(os.path.dirname(page), name)) if name else page
            if page not in CHANGED and dest not in CHANGED:
                continue
            checked += 1
            if not os.path.exists(dest):
                bad.append(f"{page}:{number}: missing file {target}")
            elif fragment and dest.endswith(".md") and fragment not in anchors(dest):
                bad.append(f"{page}:{number}: missing fragment {target}")
    print(f"pages {len(pages)} links_checked {checked} external_from_changed {external} unresolved {len(bad)}")
    print("\n".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

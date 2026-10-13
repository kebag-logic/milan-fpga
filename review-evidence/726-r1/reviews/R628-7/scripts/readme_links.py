#!/usr/bin/env python3
"""Check every relative link in docs/README.md at a git revision: the target
exists in that revision's tree, and a #fragment matches a heading slug there.

Usage: python3 -I readme_links.py <repo> <rev>
"""
import re
import subprocess
import sys
from posixpath import dirname, join, normpath

repo, rev = sys.argv[1], sys.argv[2]


def show(path):
    r = subprocess.run(["git", "-c", "core.commitGraph=false", "-C", repo, "show",
                        f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def is_dir(path):
    r = subprocess.run(["git", "-c", "core.commitGraph=false", "-C", repo, "cat-file",
                        "-t", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout.strip() == "tree"


def slugs(text):
    out = set()
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            s = re.sub(r"[^\w\- ]", "", m.group(1).strip().lower()).replace(" ", "-")
            out.add(s)
    return out


src = "docs/README.md"
text = show(src)
bad = checked = 0
for target in re.findall(r"\]\(([^)\s]+)\)", text):
    if re.match(r"^[a-z]+:", target):
        continue
    path, _, frag = target.partition("#")
    full = normpath(join(dirname(src), path)) if path else src
    checked += 1
    body = show(full)
    if body is None and not is_dir(full):
        print(f"MISSING {target} -> {full}")
        bad += 1
        continue
    if frag and body is not None and frag not in slugs(body):
        print(f"ANCHOR? {target}")
        bad += 1
print(f"{rev}: {checked} relative links checked, {bad} problems")
for needle in ("testing/726_STREAM_COUNTERS.md", "design/SPLIT_CONTROL_MEMORY.md"):
    print(f"  entry {needle}: {text.count(needle)} occurrence(s)")
sys.exit(1 if bad else 0)

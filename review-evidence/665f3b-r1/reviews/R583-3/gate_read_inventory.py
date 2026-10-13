#!/usr/bin/env python3
"""Independent gate-read inventory for a branch range (reviewer probe).

For every non-documentation file the branch changes (base..head, renames off),
list each line naming a documentation-classified page under docs/ (by whole
path or by bare file name of an existing docs page), and whether that page is
in scripts/ci_scope.py GATE_READ_DOCS. The reviewer then judges each hit by
reading it (a read by a gated job versus a comment or message).

Usage: python3 -I gate_read_inventory.py <repo> <base> <head>
"""
import pathlib
import re
import subprocess
import sys

repo, base, head = sys.argv[1:4]


def git(*args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, text=True).stdout


tree = git("ls-tree", "-r", "--name-only", head).splitlines()
doc_pages = [p for p in tree if p.startswith("docs/")
             and p.endswith((".md", ".drawio", ".svg", ".png"))]
src = git("show", f"{head}:scripts/ci_scope.py")
block = re.search(r"^GATE_READ_DOCS = \[(.*?)^\]", src, re.S | re.M).group(1)
gate_read = set(re.findall(r'"([^"]+)"', block))
by_name = {}
for p in doc_pages:
    by_name.setdefault(pathlib.PurePosixPath(p).name, []).append(p)

changed = git("diff", "--no-renames", "--name-only", base, head).splitlines()
present = set(tree)
hits = 0
for path in changed:
    if path not in present:
        continue
    if path.startswith("docs/") and path.endswith((".md", ".drawio", ".svg", ".png")):
        continue
    if "/" not in path and path.endswith(".md"):
        continue
    if path.startswith("LICENSES/"):
        continue
    if path.endswith((".png", ".svg", ".drawio")):
        continue
    try:
        text = git("show", f"{head}:{path}")
    except subprocess.CalledProcessError:
        continue
    for n, line in enumerate(text.splitlines(), 1):
        found = set()
        for m in re.finditer(r"docs/[A-Za-z0-9_./-]+", line):
            cand = m.group(0).rstrip(".,)`'\"")
            if cand in doc_pages:
                found.add(cand)
        for name, pages in by_name.items():
            if re.search(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", line):
                found.update(pages)
        for page in sorted(found):
            hits += 1
            tag = "GATE_READ" if page in gate_read else "doc-only"
            print(f"{tag}\t{page}\t{path}:{n}\t{line.strip()[:160]}")
print(f"# changed non-doc files scanned: {sum(1 for p in changed if p in present)}; hits: {hits}",
      file=sys.stderr)

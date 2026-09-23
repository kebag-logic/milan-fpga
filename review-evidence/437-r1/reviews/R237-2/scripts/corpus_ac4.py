#!/usr/bin/env python3
"""R237-2 AC4 probe: per-page blocks() and headings() under the base and head
walks, over every tracked *.md at each of the given revisions.

Usage: corpus_ac4.py --repo R --base REV --head REV TREE_REV...
Walks are loaded from `git show REV:scripts/gen_toc.py`; pages are read from
`git show TREE_REV:path` (text, as the generator reads them). Prints a line
per tree revision with the page count, the number of pages whose line
classification or heading list differs, and a SHA-256 over all
classifications per walk.
"""
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from probe import load_walk  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("trees", nargs="+")
    a = ap.parse_args()
    base, _ = load_walk(a.repo, a.base, "base")
    head, _ = load_walk(a.repo, a.head, "head")
    for tree in a.trees:
        paths = subprocess.run(["git", "-C", a.repo, "ls-tree", "-r", "--name-only", tree],
                               check=True, capture_output=True, text=True).stdout.split("\n")
        pages = [p for p in paths if p.endswith(".md")]
        hb, hh, diffs = hashlib.sha256(), hashlib.sha256(), []
        for p in pages:
            text = subprocess.run(["git", "-C", a.repo, "show", f"{tree}:{p}"],
                                  check=True, capture_output=True).stdout.decode("utf-8", "replace")
            text = text.replace("\r\n", "\n")
            kb, kh = base.blocks(text), head.blocks(text)
            gb, gh = base.headings(text), head.headings(text)
            hb.update(repr((p, kb, gb)).encode())
            hh.update(repr((p, kh, gh)).encode())
            if kb != kh or gb != gh:
                diffs.append(p)
        print(f"tree {tree[:8]}: {len(pages)} pages, {len(diffs)} differ "
              f"base={hb.hexdigest()[:16]} head={hh.hexdigest()[:16]} {diffs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

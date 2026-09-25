#!/usr/bin/env python3
"""Check markdown #anchors against GitHub's own rendered heading ids.

Usage: github_anchor_check.py <repo-root> <owner/repo> <ref> <file.md>...

For every relative link with a fragment in the given markdown files, fetch the
target file rendered by GitHub at <ref> (read-only GET through `gh api` with
the html media type) and report whether `user-content-<fragment>` or an
explicit `id="<fragment>"` exists in it. Prints one line per link and exits 1
if any fragment is absent.
"""
import re
import subprocess
import sys
from pathlib import Path

LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCED = re.compile(r"^```.*?^```", re.M | re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def rendered(repo, ref, rel, cache):
    if rel not in cache:
        out = subprocess.run(
            ["gh", "api", "-H", "Accept: application/vnd.github.html",
             f"repos/{repo}/contents/{rel}?ref={ref}"],
            check=True, capture_output=True, text=True).stdout
        cache[rel] = set(re.findall(r'id="(?:user-content-)?([^"]+)"', out))
    return cache[rel]


def main():
    root, repo, ref, files = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], sys.argv[4:]
    cache, bad = {}, 0
    for f in files:
        src = (root / f).resolve()
        body = INLINE_CODE.sub("", FENCED.sub("", src.read_text(encoding="utf-8")))
        for target in LINK.findall(body):
            if target.startswith(("http://", "https://", "mailto:")) or "#" not in target:
                continue
            path, _, frag = target.partition("#")
            tgt = src if not path else (src.parent / path).resolve()
            if tgt.suffix != ".md":
                continue
            rel = tgt.relative_to(root).as_posix()
            ok = frag in rendered(repo, ref, rel, cache)
            bad += not ok
            print(f"{'OK  ' if ok else 'DEAD'} {f} -> {rel}#{frag}")
    print(f"github-anchors: {bad} dead")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

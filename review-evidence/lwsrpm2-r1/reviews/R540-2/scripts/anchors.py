#!/usr/bin/env python3
"""List every Markdown source-line anchor with its label and the anchored lines."""
import re, sys, pathlib
root = pathlib.Path(sys.argv[1]).resolve()
pages = [root / "README.md", root / "CONTRIBUTING.md", *sorted((root / "doc").rglob("*.md"))]
for page in pages:
    for n, line in enumerate(page.read_text().splitlines(), 1):
        for label, target, a, b in re.findall(r"\[([^\]]+)\]\(([^)#]+)#L(\d+)(?:-L(\d+))?\)", line):
            path = (page.parent / target).resolve()
            src = path.read_text().splitlines()
            lo, hi = int(a), int(b or a)
            text = " | ".join(s.strip() for s in src[lo - 1:hi])[:160]
            print(f"{page.relative_to(root)}:{n} [{label}] {path.relative_to(root)}#L{lo}-{hi}: {text}")

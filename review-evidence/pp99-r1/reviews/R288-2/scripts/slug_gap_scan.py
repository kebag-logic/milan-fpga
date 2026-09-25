#!/usr/bin/env python3
"""List markdown links whose #anchor passes the repo's check-links slug (which
collapses whitespace runs) but differs from GitHub's slug (one hyphen per
space, so ' — ' becomes '--'). Usage: slug_gap_scan.py <repo-root>"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location("cl", Path(sys.argv[1]) / "scripts/check-links.py")
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)


def gh_slug(text):
    text = re.sub(r"`|\*|_", "", text.strip().lower())
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", "-")


n = 0
for src in cl.md_files():
    body = cl.strip_code(src.read_text(encoding="utf-8"))
    for target in cl.LINK.findall(body):
        if target.startswith(("http://", "https://", "mailto:")) or "#" not in target:
            continue
        path, _, anchor = target.partition("#")
        tgt = src if not path else (src.parent / path).resolve()
        if tgt.suffix != ".md" or not tgt.exists():
            continue
        tb = tgt.read_text(encoding="utf-8")
        if anchor in set(cl.EXPLICIT_ANCHOR.findall(tb)):
            continue
        heads = cl.HEADING.findall(tb)
        local = {cl.slug(h): h for h in heads}
        if anchor in local and gh_slug(local[anchor]) != anchor:
            n += 1
            print(f"{src.relative_to(cl.ROOT)} -> {target}  (GitHub slug: {gh_slug(local[anchor])})")
print(f"slug-gap links: {n}")

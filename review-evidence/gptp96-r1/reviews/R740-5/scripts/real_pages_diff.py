#!/usr/bin/env python3
"""Compare scanner hidden lines with parser fence lines on every Markdown page of a tree.

usage: python3 -I real_pages_diff.py <check_docs.py> <repo>
"""
import importlib.util, sys
from pathlib import Path
sys.dont_write_bytecode = True
from markdown_it import MarkdownIt
spec = importlib.util.spec_from_file_location("check_docs", sys.argv[1])
checker = importlib.util.module_from_spec(spec)
sys.path.insert(0, sys.argv[2])
spec.loader.exec_module(checker)
md = MarkdownIt("commonmark")
root = Path(sys.argv[2])
pages = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)
total = bad = fences = 0
for page in pages:
    text = page.read_text(encoding="utf-8")
    fence = set()
    for t in md.parse(text):
        if t.type == "fence":
            fences += 1
            fence.update(range(t.map[0] + 1, t.map[1] + 1))
    count = len(__import__("re").split(r"\r\n?|\n", text))
    kept = {n for n, _ in checker.unfenced_lines(text)}
    hidden = set(range(1, count + 1)) - kept
    total += 1
    only_scanner = sorted(hidden - fence)
    only_parser = sorted(fence - hidden)
    if only_scanner or only_parser:
        bad += 1
        print(f"{page.relative_to(root)}: scanner-only hidden {only_scanner[:12]} parser-only fence {only_parser[:12]}")
print(f"pages {total} fences {fences} pages-differing {bad}")

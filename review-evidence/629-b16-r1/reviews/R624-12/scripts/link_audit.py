#!/usr/bin/env python3
"""R624-12: audit every relative link and in-page anchor that targets the B16 findings page or its index.

usage: link_audit.py <repo root> <out.json>

Headings are slugged as GitHub does (lower case, punctuation other than '-' and '_' dropped, spaces to '-',
duplicates suffixed -1, -2, ...), outside fenced code. Every Markdown file under docs/ and the root is scanned
for links to docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md or docs/findings/README.md (with or without an
anchor), and the two files' own relative links are resolved on disk.
"""
import json
import re
import sys
from pathlib import Path

root, out = Path(sys.argv[1]), Path(sys.argv[2])
PAGE = root / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
INDEX = root / "docs/findings/README.md"
LINK = re.compile(r"\]\(([^)\s]+)\)")


def slugs(p):
    seen, out_, fence = {}, set(), False
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if fence or not re.match(r"#{1,6} ", line):
            continue
        t = re.sub(r"^#{1,6} ", "", line).strip()
        t = re.sub(r"`", "", t)
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
        s = re.sub(r"[^\w\- ]", "", t.lower()).replace(" ", "-")
        n = seen.get(s, 0)
        out_.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    return out_


cache = {}
problems, checked = [], 0
for md in sorted(root.glob("**/*.md")):
    if ".git" in md.relative_to(root).parts:
        continue
    rel = md.relative_to(root).as_posix()
    if rel.split("/")[0] in ("external", "gptp-processor", "protocol-processor", "third_party"):
        continue
    text = md.read_text(encoding="utf-8", errors="replace")
    for ln, line in enumerate(text.splitlines(), 1):
        for m in LINK.finditer(line):
            tgt = m.group(1)
            if tgt.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = tgt.partition("#")
            dest = md if path == "" else (md.parent / path).resolve()
            mine = md in (PAGE, INDEX)
            names_page = dest == PAGE.resolve() or dest == INDEX.resolve()
            if not (mine or names_page):
                continue
            checked += 1
            if not dest.exists():
                problems.append(dict(file=rel, line=ln, target=tgt, problem="missing path"))
                continue
            if anchor and dest.suffix == ".md":
                if dest not in cache:
                    cache[dest] = slugs(dest)
                if anchor not in cache[dest]:
                    problems.append(dict(file=rel, line=ln, target=tgt, problem="missing anchor"))
json.dump(dict(links_checked=checked, problems=problems), out.open("w"), indent=1)
print(json.dumps(dict(links_checked=checked, problems=len(problems))))
for p in problems[:40]:
    print(p)
sys.exit(1 if problems else 0)

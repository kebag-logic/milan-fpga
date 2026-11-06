#!/usr/bin/env python3
"""List Findings rows whose printed statement is on no single line of their page, so a text search cannot find them.

Usage: copy_spelling_r787.py REPO
"""
import re, sys
from pathlib import Path
repo = Path(sys.argv[1])
section = (repo / "docs/DOCUMENTATION_AUDIT.md").read_text().split("## Findings")[1]
rows = [[c.strip() for c in re.split(r"(?<!\\)\|", r)[1:-1]] for r in section.split("\n") if r.startswith("| D0")]
copies = sum(r[4].startswith("Copy of the") for r in rows)
hits = []
for r in rows:
    page = re.match(r"\[(.+?)(?: \(historical\))?\]", r[1]).group(1)
    quote = r[3].replace("\\|", "|")
    flat = [" ".join(line.split()) for line in (repo / page).read_text(errors="replace").split("\n")]
    if r[2] == "on page" and not any(" ".join(quote.split()) in line for line in flat):
        hits.append(f"{r[0]} | {page} | copy={r[4].startswith('Copy of the')} | {quote[:70]}")
print(f"findings rows {len(rows)}, copy rows {copies}, on-page rows not findable by a text search: {len(hits)}")
print("\n".join(hits))

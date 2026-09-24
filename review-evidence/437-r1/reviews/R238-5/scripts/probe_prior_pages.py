#!/usr/bin/env python3
"""Reviewer probe (R238-5): what the walk lists on the prior round's
published pages. Usage: python probe_prior_pages.py <repo-root> <pages.json>...
Prints each page's headings() and refusals() count; flags a listed
`Old` heading (every such page hides `Old` from GitHub)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "scripts"))
from gen_toc import headings, refusals  # noqa: E402

bad = 0
for path in sys.argv[2:]:
    for row in json.loads(Path(path).read_text()):
        listed = headings(row["page"])
        old = any(raw.startswith("Old") for _, raw, _ in listed)
        bad += old
        print(f"{'OLD LISTED' if old else 'ok'}: {Path(path).name}: "
              f"{row['name']}: {[(r, a) for _, r, a in listed]} "
              f"refusals={len(refusals(row['page']))}")
print(f"pages listing Old: {bad}")
sys.exit(1 if bad else 0)

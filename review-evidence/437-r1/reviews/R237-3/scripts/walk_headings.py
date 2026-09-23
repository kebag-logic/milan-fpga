#!/usr/bin/env python3
"""Run one tree's Contents walk over synthetic pages.

Usage: walk_headings.py <scripts-dir> <pages.json> <out.json>
pages.json is {"id": "markdown", ...}; out.json is
{"id": {"headings": [[level, text], ...], "labels": [...]}}.
The walk module is imported from <scripts-dir> only.
"""
import json
import sys

scripts, pages_path, out_path = sys.argv[1:4]
sys.path.insert(0, scripts)
import gen_toc  # noqa: E402

pages = json.load(open(pages_path))
out = {}
for key, text in pages.items():
    out[key] = {
        "headings": [[lvl, raw] for lvl, raw, _ in gen_toc.headings(text)],
        "labels": gen_toc.blocks(text),
    }
json.dump(out, open(out_path, "w"), indent=1, sort_keys=True)

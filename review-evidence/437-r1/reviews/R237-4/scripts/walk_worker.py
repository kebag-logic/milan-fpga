#!/usr/bin/env python3
"""Run one revision's Contents walk over pages read as JSON from stdin.

Usage: walk_worker.py <scripts-dir>  < pages.json  > answers.json

pages.json is a JSON list of page strings. The answer for each page is
{"headings": [[level, raw], ...], "blocks": [...], "plan_old": bool}, where
plan_old says whether the navigation plan of the page plus a three-section
tail lists an `old` anchor. The walk is imported from <scripts-dir> only.
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import gen_toc  # noqa: E402  (the revision under test, from argv)

TAIL = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"


def answer(page: str) -> dict:
    heads = gen_toc.headings(page)
    plan = gen_toc.plan(page + TAIL) or []
    return {"headings": [[lvl, raw] for lvl, raw, _ in heads],
            "blocks": gen_toc.blocks(page),
            "plan_old": "old" in [h[2] for h in plan]}


def main() -> int:
    pages = json.load(sys.stdin)
    json.dump([answer(p) for p in pages], sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())

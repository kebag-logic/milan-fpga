#!/usr/bin/env python3
"""Write the committed fixtures from render.py receipts.

Usage: make_fixture.py
Reads work/family-one-out.json and work/comment-out.json and writes
scripts/gen_toc_family_one.json and scripts/gen_toc_comment_shapes.json in
the lane. Every field is copied from the receipt; nothing is re-derived.
"""
import json
from pathlib import Path

LANE = Path("$LANES/437-container-paragraph-scopes")
WORK = Path(__file__).resolve().parent.parent / "work"
METHOD = ("Each page was sent to GitHub's Markdown API (POST /markdown, mode gfm, context "
          "kebag-logic/milan-fpga). request_bytes is the exact JSON body sent (keys sorted, no "
          "spaces, <, > and & escaped), response_bytes the exact HTML returned, each with its "
          "SHA-256; headings is every heading element of response_bytes as [level, text].")
ABOUT = {
    "gen_toc_family_one.json": (
        "Issue #437 acceptance 1 as restated on 2026-09-23: the family-one shape set. A list "
        "item's paragraph resumed after a blank line, at and past the item's content column "
        "(bullet, ordered and two-digit ordered markers), followed by a lone inline tag and by "
        "an unknown tag, outside and inside the item; and the boundaries that already agreed. "
        "r86_5 quotes the PR #428 R86-5 description a shape reproduces, or is null. The shapes "
        "are fresh bytes, not the unpublished R86-5 originals."),
    "gen_toc_comment_shapes.json": (
        "Issue #437 controls for a comment left open in raw HTML (the #516 shapes): the twelve "
        "published variants, then what opens, closes and does not close the rendered comment."),
}


def entry(r: dict, family_one: bool) -> dict:
    out = {"name": r["id"], "page": r["page"], "headings": r["github"],
           "recorded_utc": r["utc"], "request_bytes": r["request_bytes"],
           "request_sha256": r["request_sha256"], "response_bytes": r["response_bytes"],
           "response_sha256": r["response_sha256"]}
    if family_one:
        out.update(kind=r["kind"], r86_5=r["r86_5"])
    assert r["exit"] == 0 and r["request_length_matches_wire"]
    return out


def main() -> None:
    for name, src, fo in (("gen_toc_family_one.json", "family-one-out.json", True),
                          ("gen_toc_comment_shapes.json", "comment-out.json", False)):
        rows = json.load(open(WORK / src))
        doc = {"about": ABOUT[name], "method": METHOD,
               "shapes": [entry(r, fo) for r in rows]}
        (LANE / "scripts" / name).write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n",
                                             encoding="ascii")
        print(name, len(rows))


if __name__ == "__main__":
    main()

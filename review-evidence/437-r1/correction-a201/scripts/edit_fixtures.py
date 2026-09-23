#!/usr/bin/env python3
"""Rewrite the two comment-bearing fixtures for the A201 correction.

Removed: the ten controls that pinned a closure rule this correction removes
(the `<!-->` closure and the prose-comment end), on which the walk now
withholds exactly as the base did; their answers are kept in
receipts/removed-shapes.json. Marked `limitation`: every shape the walk now
answers differently from GitHub. Added: new shapes from receipts/renders.
Receipt bytes of kept shapes are untouched."""
import json
import sys
from pathlib import Path

PACKET = Path(__file__).resolve().parent.parent
CLONE = Path("$LANES/437-container-paragraph-scopes")
sys.path.insert(0, str(PACKET / "scripts"))
import render  # noqa: E402
import walks   # noqa: E402

BASE, PREV = "574c29fa111c74e5e5ed63e4670aff1f492e28e2", "e4906bfca65c61e7e109e3532ac1b2dd5b4c0096"
REMOVED = {
    "gen_toc_comment_shapes.json": ["abrupt empty comment line", "abrupt empty comment inline"],
    "gen_toc_container_walk.json": [
        "lazy indented comment opener is prose", "indented comment opener continues a paragraph",
        "lowercase declaration is no block", "heading after a prose opener",
        "heading after a code-span opener", "heading after a table-cell opener",
        "list item after a prose opener", "blank after an opener in an item"],
}
OWNER = "#516"
WITHHOLD_WHY = ("the comment reading as at the base: a `<!--` in a code span, after an escape or in an "
                "attribute opens one here; the base agreed only because it did not end the raw HTML "
                "block with its list item (R237-2 F2's rows)")
ESCAPE_WHY = "a raw-HTML comment GitHub leaves open hides the rest of its page; the walk reads Markdown's blocks"
PINS = {  # agreeing comment shapes of the container-walk fixture: what they hold now
    "a quote's optional space leaves a raw opener": "comments are read as at the base: an opener in a quote",
    "a continued quote's optional space leaves a raw opener": "comments are read as at the base: an opener in a quote",
    "double-quoted attribute": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "inline tag attribute": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "a quoted value hides a greater-than": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "attribute inside a block": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "CDATA is a bogus comment": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "--!> closes on its line": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "--!> closes on a later line": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "inline tag closes after the block": "boundary of the #516 limitation: an opener inside a raw HTML block the walk reads as that block",
    "type-5 block": "comments are read as at the base: an opener on a line of types 3 to 5, which the walk labels text",
    "type-3 block": "comments are read as at the base: an opener on a line of types 3 to 5, which the walk labels text",
    "type-4 block": "comments are read as at the base: an opener on a line of types 3 to 5, which the walk labels text",
    "raw HTML in an item": "comments are read as at the base: an opener in a list item",
    "raw HTML in a quote": "comments are read as at the base: an opener in a quote",
}
NEW = [  # (name, pins)
    ("R237-3 F2 definition-only item ends at a second blank", "R237-3 F2: a paragraph of link reference definitions leaves its item empty once it closes"),
    ("R237-3 F2 definition-only item survives one blank", "R237-3 F2: a paragraph of link reference definitions holds its item while it is open"),
    ("R237-3 F2 lazy text keeps a definition's item", "R237-3 F2: a lazy line of text fills the item"),
    ("R237-3 F2 indented text keeps a definition's item", "R237-3 F2: a line of text after a definition fills the item"),
    ("R237-3 F2 two definitions leave the item empty", "R237-3 F2: a paragraph of link reference definitions leaves its item empty once it closes"),
    ("R237-3 F2 titled definition leaves the item empty", "R237-3 F2: a paragraph of link reference definitions leaves its item empty once it closes"),
    ("R237-3 F2 E7", "R237-3 F2: a paragraph of link reference definitions leaves its item empty once it closes"),
    ("nested empty item holds the item", "a nested container is a block its item holds"),
    ("nested quote holds an empty item", "a nested container is a block its item holds"),
    ("R237-3 F4 a blank line ends a quote", "R237-3 F4: a blank line ends a block quote"),
    ("R238-2 F2 C17 a type-3 block ends at its marker", "R238-2 F2: a raw HTML block of types 3 to 5 ends at its end marker"),
    ("type-3 opener is no lazy line", "a raw HTML block of types 3 to 5 interrupts a paragraph, so it is no lazy line"),
    ("type-4 block leaves the gate to the walk", "R238-2 F1(d): inside types 3 to 5 the type-7 gate is the walk's own paragraph state"),
    ("type-3 block leaves the gate to the walk", "R238-2 F1(d): inside types 3 to 5 the type-7 gate is the walk's own paragraph state"),
    ("type-5 block leaves the gate to the walk", "R238-2 F1(d): inside types 3 to 5 the type-7 gate is the walk's own paragraph state"),
    ("comment block outlives its item", "comments are read as at the base: a container's end does not close one"),
    ("comment block outlives its quote", "comments are read as at the base: a container's end does not close one"),
    ("R237-3 E1 prose comment after an inline PI", "comments are read as at the base: a comment opened in prose stays open to -->"),
    ("R237-3 E2 prose comment after inline CDATA", "comments are read as at the base: a comment opened in prose stays open to -->"),
    ("R238-2 F1c empty comment after a type-3 opener", "comments are read as at the base: `<!-->` opens one"),
    ("item end uncovers an open quoted value", "a raw HTML block ends with its list item (R237-2 F1), uncovering a residue"),
    ("item end uncovers a type-3 block", "a raw HTML block ends with its list item (R237-2 F1), uncovering a residue"),
    ("item end uncovers a comment over a fence", "a raw HTML block ends with its list item (R237-2 F1), uncovering a residue"),
]
WHY = {
    "item end uncovers an open quoted value": (
        "raw HTML ending inside an open quoted value hides every later heading on GitHub (R237-3 F3); "
        "the base agreed only because it did not end the raw HTML block with its list item"),
    "item end uncovers a type-3 block": (
        "a raw HTML block of types 3 to 5 is labelled prose (#413, R238-2 F1); the base agreed only "
        "because it did not end the raw HTML block before it with its list item"),
    "item end uncovers a comment over a fence": (
        "the comment reading as at the base: `<!-->` opens one here, it covers a fence GitHub opens, and "
        "a `-->` inside that fence ends it; the base agreed only because it did not end the raw HTML "
        "block with its list item"),
}


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=1, sort_keys=True, ensure_ascii=True) + "\n", encoding="ascii")


def main():
    cands = json.loads((PACKET / "scratch" / "candidates.json").read_text())
    cands["R237-3 F2 titled definition leaves the item empty"] = cands.pop("R237-3 F2 titled definition outside the subset")
    removed = []
    for fx in ("gen_toc_comment_shapes.json", "gen_toc_container_walk.json"):
        path = CLONE / "scripts" / fx
        data = json.loads(path.read_text(encoding="ascii"))
        keep = [s for s in data["shapes"] if s["name"] not in REMOVED[fx]]
        gone = [s for s in data["shapes"] if s["name"] in REMOVED[fx]]
        assert len(gone) == len(REMOVED[fx])
        if fx == "gen_toc_container_walk.json":
            for name, pins in NEW:
                page = cands[name]
                rec = render.render(page)
                shape = {k: rec[k] for k in ("headings", "page", "recorded_utc", "request_bytes",
                                            "request_sha256", "response_bytes", "response_sha256")}
                shape["name"] = name
                shape["pins"] = pins or "R238-2 F3: HTML tree construction the walk does not model"
                keep.append(shape)
        pages = [s["page"] for s in keep + gone]
        res = {rev: walks.walk(rev, pages) for rev in (BASE, PREV, "work")}
        for i, s in enumerate(gone):
            j = len(keep) + i
            removed.append({"fixture": fx, "name": s["name"], "page": s["page"], "github": s["headings"],
                            "base": res[BASE][j]["headings"], "reviewed_head": res[PREV][j]["headings"],
                            "this_head": res["work"][j]["headings"]})
        for i, s in enumerate(keep):
            s.pop("limitation", None)
            walk = res["work"][i]["headings"]
            if s["name"] in PINS:
                s["pins"] = PINS[s["name"]]
            if walk == s["headings"]:
                continue
            wider = [h for h in walk if h not in s["headings"]]
            narrower = [h for h in s["headings"] if h not in walk]
            direction = "escape" if wider and not narrower else "withhold" if narrower and not wider else "mixed"
            assert direction != "mixed", s["name"]
            base_agrees = res[BASE][i]["headings"] == s["headings"]
            why = ESCAPE_WHY if direction == "escape" else WITHHOLD_WHY
            why = WHY.get(s["name"], why)
            s["limitation"] = {"owner": OWNER, "direction": direction, "walk": walk,
                               "base_agreed": base_agrees, "why": why}
        data["shapes"] = keep
        if fx == "gen_toc_comment_shapes.json":
            data["about"] = ("Issue #437 comment shapes (the #516 shapes): the twelve published variants, "
                             "then comments that raw HTML leaves open or closes. The walk reads comments as "
                             "the base did and does not model a comment GitHub's raw HTML leaves open: each "
                             "shape it answers differently carries `limitation` (#516, with the direction, "
                             "the walk's answer and whether the base agreed).")
        else:
            data["about"] = ("Issue #437 container walk: a tag under a nested block, a block opened in an "
                             "item, an empty item, lazy lines, link reference definitions, raw HTML of "
                             "types 3 to 5, and comments read as at the base. pins names the finding or "
                             "rule each shape holds; a shape the walk answers differently from GitHub "
                             "carries `limitation` (#516, with the direction, the walk's answer and "
                             "whether the base agreed).")
        dump(path, data)
    (PACKET / "receipts" / "removed-shapes.json").write_text(json.dumps(removed, indent=1) + "\n")
    print("removed", len(removed))


if __name__ == "__main__":
    main()

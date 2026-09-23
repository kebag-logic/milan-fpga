#!/usr/bin/env python3
"""Mutation rounds 2 to 4 and the survivor measurements of round R237-4,
as run (round 1 is scripts/mutate.py's own MUTANTS list).

Usage: mutate_rounds.py <head-scripts> <scratch> <receipts-mutation-dir> <cache> <corpus.json>...
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mutate  # noqa: E402
import survivor_impact as si  # noqa: E402

C, G = mutate.C, mutate.G
ROUNDS = {
    "round2": [
        ("footnote-whitespace-continues-guarded", C, "return at if not text else None", "return at if _blank(text) else None"),
        ("link-definition-title-any-token-guarded", G, r'(?:%(b)s+\"(?:%(t)s|\\.)*\")?', r"(?:%(b)s+%(d)s+)?"),
        ("inline-comment-opens-block", C, "if state == COMMENT and (label == TEXT or _lead(rem) > 3):", "if False:"),
        ("inline-comment-after-text-only", C, "if state == COMMENT and (label == TEXT or _lead(rem) > 3):",
         "if state == COMMENT and label == TEXT:"),
    ],
    "round3": [
        ("lazy-indented-not-lazy", C, "    if _lead(rem) >= TAB_STOP:\n        return True\n    starts",
         "    if _lead(rem) >= TAB_STOP:\n        return False\n    starts"),
        ("lazy-raw-3-5-lazy", C, "LIST_ITEM_RE, RAW_3_5_RE)\n    return _opens", "LIST_ITEM_RE)\n    return _opens"),
        ("lazy-footnote-lazy", C, "              FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE, RAW_3_5_RE)",
         "              LIST_ITEM_RE, RAW_3_5_RE)"),
        ("lazy-quote-lazy", C, "starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,",
         "starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE,"),
        ("lazy-heading-lazy", C, "starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,",
         "starts = (THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,"),
        ("quote-no-optional-space", C, '    return at + 1 if text[at:at + 1] == " " else at', "    return at"),
        ("cdata-ends-at-gt", C, 'RAW_ENDS = ("?>", "]]>", ">")', 'RAW_ENDS = ("?>", ">", ">")'),
        ("leaf-kept-on-open", C, "    if opened:\n        walk.leaf = _FRESH\n", ""),
        ("owner-always-page", G, "            owner = scope.held_by[-1]\n", "            owner = 0\n"),
        ("item-needs-more", C, "        if lead >= box.need:", "        if lead > box.need:"),
        ("hr-is-item", C, "        elif THEMATIC_BREAK_RE.match(rem):\n            break\n", ""),
        ("open-at-four", C, "    while not _blank(rem) and _lead(rem) < TAB_STOP:",
         "    while not _blank(rem) and _lead(rem) <= TAB_STOP:"),
        ("lazy-needs-paragraph-any", C, "        if state == TEXT and para == PARAGRAPH and _lazy(rem):",
         "        if state == TEXT and _lazy(rem):"),
        ("quote-lead-four", C, "        if lead > 3 or rest[lead:lead + 1] != \">\":",
         "        if lead > 4 or rest[lead:lead + 1] != \">\":"),
        ("tab-stop-two", C, "    text = line.expandtabs(TAB_STOP)", "    text = line.expandtabs(2)"),
    ],
    "round4": [
        ("lazy-hr-lazy", C, "starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,",
         "starts = (ATX_HEADING_RE, BLOCK_QUOTE_RE,"),
        ("lazy-item-lazy", C, "              FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE, RAW_3_5_RE)",
         "              FOOTNOTE_DEFINITION_RE, RAW_3_5_RE)"),
        ("lazy-block-open-lazy", C, "    return _opens(rem, HELD, TEXT)[0] == TEXT and not any(", "    return not any("),
        ("empty-item-content-at-marker", C,
         "    return end + 1 if not item.group(2) or padding > TAB_STOP else end + padding",
         "    return end + padding if not item.group(2) else end + 1 if padding > TAB_STOP else end + padding"),
    ],
}
EXTRA = {
    "round2": si.EXTRA[:],
    "round3": [
        "- a\n## H\n  ```\n## Old\n```\n\n## Real\n", "- a\n# H\n  <div>\n## Old\n\n## Real\n",
        "> a\n## H\n```\n## Old\n```\n\n## Real\n", "- a\n## H\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
        "> a\n    b\n<span>\n## Old\n</span>\n\n## Real\n", "- a\n      b\n  ```\n## Old\n```\n\n## Real\n",
        "> a\n    b\n```\n## Old\n```\n\n## Real\n", "- > a\n      b\n  ```\n## Old\n```\n\n## Real\n",
        "- > a\n    b\n  ```\n## Old\n```\n\n## Real\n", ">- a\n>  b\n>  ```\n## Old\n```\n\n## Real\n",
        ">- a\n>\n>  ```\n## Old\n```\n\n## Real\n", "<![CDATA[ a > b\n<span>\n## Old\n]]>\n\n## Real\n",
        "- a\n  <![CDATA[ a > b\n  ```\n## Old\n]]>\n\n## Real\n", "text\n-\n  <span>\n## Old\n  </span>\n\n## Real\n",
        "> a\n    > b\n<span>\n## Old\n</span>\n\n## Real\n",
    ],
    "round4": [
        "- a\n***\n  ```\n## Old\n```\n\n## Real\n", "- a\n___\n  <div>\n## Old\n\n## Real\n",
        "> a\n***\n```\n## Old\n```\n\n## Real\n", "- a\n* * *\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
    ],
}


def main() -> int:
    head, scratch, out, cache = sys.argv[1:5]
    corpora = sys.argv[5:]
    suffix = {"round2": "2", "round3": "3", "round4": "4"}
    for rnd, mutants in ROUNDS.items():
        mutate.MUTANTS[:] = mutants
        sys.argv = ["mutate.py", head, f"{scratch}/mut{suffix[rnd]}", f"{out}/mutants_{rnd}.json"]
        mutate.main()
        survivors = [m[0] for m in mutants]
        si.EXTRA[:] = EXTRA[rnd]
        sys.argv = (["x", head, cache, f"{out}/survivor_impact_{rnd}.json"] + corpora + ["--"]
                    + [f"{scratch}/mut{suffix[rnd]}/{name}" for name in survivors])
        si.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())

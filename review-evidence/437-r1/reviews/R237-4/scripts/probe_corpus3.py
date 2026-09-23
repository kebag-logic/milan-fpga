#!/usr/bin/env python3
"""Third probe corpus: list-item LIFETIME. A block opened at, below or past
an item's content column after 0, 1 or 2 blank lines, then a column-0
heading and a closer. If the walk and GitHub disagree about whether the item
is still open, the block is ended (or not) differently.

Usage: probe_corpus3.py > probes3.json
"""
import json
import sys

ITEMS = {
    "bullet": ("- a", 2),
    "star-pad2": ("*  a", 3),
    "pad4": ("-    a", 5),
    "pad5-code": ("-     a", 2),
    "tab": ("-\ta", 4),
    "marker-indent3": ("   - a", 5),
    "ordered-9digit": ("123456789. a", 11),
    "paren": ("1) a", 3),
    "empty": ("-", 2),
    "empty-pad": ("-   ", 2),
    "blank-start": ("-\n  a", 2),
    "html-start": ("- <div>", 2),
    "comment-start": ("- <!-- c -->", 2),
    "fence-start": ("- ```\n  x\n  ```", 2),
    "hr-start": ("- ***", 2),
    "heading-start": ("- # h", 2),
    "setext": ("- a\n  ---", 2),
    "nested-empty": ("- -", 2),
    "nested": ("- a\n  - b", 2),
    "nested-inner": ("- a\n  - b", 4),
    "quote-in": ("- > a", 2),
    "quote-in-lazy": ("- > a\nlazy", 2),
    "lazy": ("- a\nlazy", 2),
    "table": ("- | a |\n  | - |\n  | b |", 2),
    "footnote-in": ("- [^1]: a", 2),
    "def-and-text": ("- [a]: /u\n  b", 2),
    "sibling": ("- a\n- b", 2),
    "sibling-ordered": ("- a\n1. b", 3),
    "code-in": ("- a\n\n      code", 2),
    "html-in": ("- a\n\n  <div>\n  x", 2),
}
BLOCKS = {"fence": ("```", "```"), "div": ("<div>", None), "pre": ("<pre>", "</pre>"),
          "span": ("<span>", None)}


def rows() -> list:
    out = []
    for iname, (item, need) in ITEMS.items():
        for blanks in (0, 1, 2):
            for bname, (opener, closer) in BLOCKS.items():
                for delta in (-1, 0, 1):
                    col = need + delta
                    if col < 0 or col > 7:
                        continue
                    body = item + "\n" + "\n" * blanks + " " * col + opener + "\n## Old\n"
                    body += (closer + "\n" if closer else "") + "\n## Real\n"
                    out.append({"name": f"T {iname} blanks={blanks} {bname} col={col}", "page": body})
    return out


if __name__ == "__main__":
    json.dump(rows(), sys.stdout)
    sys.exit(0)

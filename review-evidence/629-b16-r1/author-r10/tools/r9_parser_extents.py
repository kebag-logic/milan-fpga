#!/usr/bin/env python3
"""Lane B16, round 9: where the pinned parser's source positions fall short, and what the check makes of them.

usage: <parser python> r9_parser_extents.py <check_b16_figures.py> <repo> <scratch dir> <out.json>

Each case is a small Markdown document written with the lines its node truly starts and ends on. The check is
loaded as a module (its main does not run) and its own reader is used: tree() for the parser's nodes and
positions, extents() for the extent the check judges a node by. For each case this records the node's kind,
the parser's reported lines, the true lines, the check's extent, and, for a paragraph or heading, whether the
check finds it misplaced (the parser's last line in it short of its source's). A case meets its expectation
when the check's extent equals the true lines and the misplacement is as stated. Offline; nothing on the bench
is read or written.
"""
import importlib.util
import json
import sys
from pathlib import Path

CHECK, REPO, SCRATCH, OUT = sys.argv[1:5]
SCRATCH = Path(SCRATCH)
SCRATCH.mkdir(parents=True, exist_ok=True)
sys.argv = [CHECK, str(SCRATCH / "page.md"), str(SCRATCH), str(SCRATCH / "r.tsv"), str(SCRATCH / "c.tsv"), "--repo", REPO]
spec = importlib.util.spec_from_file_location("check_b16_figures", CHECK)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

CASES = [  # (name, document, kind, occurrence, true first line, true last line, misplaced leaf or None)
    ("<pre> block over two lines", "p\n\n<pre>\nx\n</pre>\n", "html_block", 0, 3, 5, None),
    ("<pre> block closed on its second line", "p\n<pre>\nx</pre>\nq\n", "html_block", 0, 2, 3, None),
    ("<script> block", "<script>\nx\n</script>\n", "html_block", 0, 1, 3, None),
    ("<style> block", "<style>\nx\n</style>\n", "html_block", 0, 1, 3, None),
    ("<textarea> block", "<textarea>\nx\n</textarea>\n", "html_block", 0, 1, 3, None),
    ("a comment block over two lines", "<!--\nx -->\n", "html_block", 0, 1, 2, None),
    ("a comment block on one line", "p\n\n<!-- x -->\n", "html_block", 0, 3, 3, None),
    ("a <? block", "<?\nx\n?>\n", "html_block", 0, 1, 3, None),
    ("a <! block with a letter", "<!A\nx\n>\n", "html_block", 0, 1, 3, None),
    ("a CDATA block", "<![CDATA[\nx\n]]>\n", "html_block", 0, 1, 3, None),
    ("a <!-- block at the end without a line feed", "p\n<!--\nx -->", "html_block", 0, 2, 3, None),
    ("a <div> block, ended by a blank line", "<div>\nx\n\ny\n", "html_block", 0, 1, 2, None),
    ("a fenced code block", "```\nx\n```\n", "code_block", 0, 1, 3, None),
    ("an indented code block", "p\n\n    x\n    y\n", "code_block", 0, 3, 4, None),
    ("struck text over a line break", "a ~~b\nc~~ d\n", "strikethrough", 0, 1, 2, False),
    ("struck text on one line", "a ~~b~~ d\n", "strikethrough", 0, 1, 1, False),
    ("an image whose description runs over a line break", "a ![b\nc](x.png) d\n", "image", 0, 1, 2, False),
    ("an image with an empty description over a line break", "a ![\n](x.png) d\n", "image", 0, 1, 2, False),
    ("a link whose text runs over a line break", "a [b\nc](#x) d\n", "link", 0, 1, 2, False),
    ("a link whose text holds a code span over a line break", "a [`b\nc`\nd](#x) e\n", "link", 0, 1, 3, False),
    ("raw HTML inline over a line break", "a <span\nid=\"q\">b</span>\n", "html_inline", 0, 1, 2, False),
    ("a code span over a line break", "a `b\nc` d\n", "code", 0, 1, 2, False),
    ("emphasis over a line break", "a *b\nc* d\n", "emph", 0, 1, 2, False),
    ("a footnote reference", "a[^n] b\n\n[^n]: c\n", "footnote_reference", 0, 1, 1, False),
    ("a footnote definition over two lines", "a[^n]\n\n[^n]: c\n    d\n", "footnote_definition", 0, 3, 4, None),
    ("a thematic break", "a\n\n***\n", "thematic_break", 0, 3, 3, None),
    ("a task list item", "- [ ] a\n  b\n", "tasklist", 0, 1, 2, None),
    ("a setext heading over two lines of text", "a\nb\n---\n", "heading", 0, 1, 3, False),
    ("a table cell", "| a | b |\n|---|---|\n| c | d |\n", "table_cell", 3, 3, 3, False),
    ("a paragraph with a hard line break of two spaces", "a  \nb\nc\n", "paragraph", 0, 1, 3, False),
    ("a paragraph with a backslash line break", "a\\\nb\nc\n", "paragraph", 0, 1, 3, True),
    ("a paragraph with a link's title over a line break", "a [b](#x \"t\nu\") c\nd\n", "paragraph", 0, 1, 3, True),
    ("a paragraph with a link's target over a line break", "a [b](\n#x) c\nd\n", "paragraph", 0, 1, 3, True),
    ("a paragraph with a reference label over a line break", "a [b][r\nq] c\nd\n\n[r q]: #x\n", "paragraph", 0, 1, 3,
     True),
    ("a paragraph with an image's title over a line break", "a ![b](x.png \"t\nu\") c\nd\n", "paragraph", 0, 1, 3, True),
    ("a paragraph opened by a reference definition", "[r]: #x\nb\nc\n", "paragraph", 0, 1, 3, True),
    ("a paragraph in a block quote, continued lazily", "> a\nb\n", "paragraph", 0, 1, 2, False),
]


def main() -> int:
    out = []
    for name, doc, kind, k, first, last, misplaced in CASES:
        p = SCRATCH / "case.md"
        p.write_bytes(doc.encode())
        nodes = C.tree(p)
        src = C.lines_of(p)
        ext, lasts = C.extents(nodes, src)
        hits = [i for i, x in enumerate(nodes) if x[0] == kind]
        i = hits[k]
        _, sl, sc, el, ec, *_ = nodes[i]
        leaf = None
        if kind in C.LEAVES:
            leaf = bool(lasts[i]) and lasts[i] != el - (kind == "heading" and el > sl)
        r = dict(case=name, document=doc, kind=kind, reported=[sl, el], true=[first, last],
                 short_of_source=el < last or sl > first, extent=[ext[i][0], ext[i][2]],
                 parser_last_line=lasts[i] if kind in C.LEAVES else None, misplaced=leaf,
                 expect_misplaced=misplaced if kind in C.LEAVES else None)
        r["met"] = r["extent"] == [first, last] and leaf == r["expect_misplaced"]
        out.append(r)
        print(("MET " if r["met"] else "NOT ") + f"{kind:20s} reported {sl}-{el} true {first}-{last} "
              f"extent {r['extent'][0]}-{r['extent'][1]} misplaced {leaf}  {name}")
    Path(OUT).write_text(json.dumps(dict(
        note="Lane B16 round 9: the pinned parser's reported lines against each node's true lines, and the check's "
             "extent; offline, no bench action", cases=len(out), met=sum(x["met"] for x in out),
        short_of_source=sorted({x["kind"] for x in out if x["short_of_source"]}),
        misplaced=[x["case"] for x in out if x["misplaced"]], results=out), indent=1) + "\n")
    return 0 if all(x["met"] for x in out) else 1


if __name__ == "__main__":
    sys.exit(main())

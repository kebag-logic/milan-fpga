#!/usr/bin/env python3
"""[R238] census of the head tree for the shapes the findings need.

Replays the head walk's own loop with its own functions and counts, per
tracked Markdown page: lines where the head's paragraph state is HELD while
the base walk's would be PARAGRAPH (the only state the change converts),
lines the type-7 grammar matches, and column-0 block quote or footnote
definition lines that keep an item context alive.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_render import BASE, HEAD, OUT, SCRATCH  # noqa: E402


def replay(text: str) -> tuple[int, int, int]:
    state, delim, tag, prev = HEAD.TEXT, "", "", ""
    para = HEAD.NO_PARAGRAPH
    ctx = None
    converted = kept_by_block = 0
    for line in text.split("\n"):
        if state in (HEAD.FENCE, HEAD.COMMENT, HEAD.HTML):
            label = state
            state, delim, tag = HEAD._still_open(line, state, delim, tag)
        else:
            label, state, delim, tag = HEAD._opens(line, para, state)
        before = ctx
        # The head's own flat answer for this line, then its list answer.
        flat = HEAD._paragraph_after(line, label, para, prev)
        para, ctx = HEAD._list_paragraph_after(line, label, para, prev, ctx)
        if para == HEAD.HELD and flat == HEAD.PARAGRAPH:
            converted += 1
        if before and ctx and HEAD._indent_columns(line) < before[0] and (
                HEAD.BLOCK_QUOTE_RE.match(line) or HEAD.FOOTNOTE_DEFINITION_RE.match(line)):
            kept_by_block += 1
        prev = line
    tags = sum(1 for line in text.split("\n") if HEAD.HTML_TAG_LINE_RE.match(line))
    return converted, tags, kept_by_block


def main() -> int:
    root = SCRATCH / "clone-head"
    names = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "*.md"],
                           capture_output=True, text=True, check=True).stdout
    total = [0, 0, 0]
    rows = []
    for rel in sorted(filter(None, names.split("\0"))):
        text = (root / rel).read_text()
        got = replay(text)
        total = [a + b for a, b in zip(total, got)]
        if any(got):
            rows.append(f"  {rel}: converted={got[0]} type7-tag-lines={got[1]} "
                        f"context-kept-by-dedented-quote/footnote={got[2]}")
    out = [f"head tree census over tracked Markdown: lines converted PARAGRAPH->HELD "
           f"{total[0]}, type-7 tag lines {total[1]}, item contexts kept by a dedented "
           f"quote/footnote line {total[2]}"] + rows
    (OUT / "receipts" / "census.txt").write_text("\n".join(out) + "\n")
    print("\n".join(out[:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

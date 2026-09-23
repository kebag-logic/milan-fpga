#!/usr/bin/env python3
"""Build the family-one shape set and the rendered-comment control set.

Writes work/family-one-in.json and work/comment-in.json (lists of
{id, page, ...}) for render.py. Shape pages follow R86-5's form: a
predecessor, then a lone tag line wrapping `## Old`, then `## Real`.
"""
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent.parent / "work"
FENCE = "`" * 3

# (name, first line, content column)
ITEMS = [("bullet", "- item", 2), ("star", "* item", 2),
         ("ordered", "1. item", 3), ("two-digit ordered", "10. item", 4)]
TAGS = [("inline tag", "span"), ("unknown tag", "custom-tag")]
# R86-5's nine described shapes (PR #428 comment 5644834363), in its order.
R86_5 = {
    "bullet at column, inline tag outside": "`- item` + blank + `  text` (two spaces)",
    "bullet past column, inline tag outside": "the same at three spaces",
    "star at column, inline tag outside": "with `*`",
    "ordered at column, inline tag outside": "with `1. item` + `   text`",
    "bullet two paragraphs, inline tag outside": "with two container paragraphs",
    "task at column, inline tag outside": "with a task item",
    "interrupting bullet at column, inline tag outside": "with a list that follows a paragraph",
    "bullet at column, b tag outside": "with `<b>` in place of `<span>`",
    "bullet after two blanks, inline tag outside": "with two blank lines",
}


def page(prefix: str, tag: str, column: int) -> str:
    pad = " " * column
    return f"{prefix}\n{pad}<{tag}>\n## Old\n{pad}</{tag}>\n\n## Real\n"


def family_one() -> list[dict]:
    rows = []
    for item, first, col in ITEMS:
        for where, text_col in (("at", col), ("past", col + 1)):
            prefix = f"{first}\n\n{' ' * text_col}text"
            for tag_name, tag in TAGS:
                rows.append((f"{item} {where} column, {tag_name} outside", "resumed paragraph, tag outside the item",
                             page(prefix, tag, 0)))
                rows.append((f"{item} {where} column, {tag_name} inside", "resumed paragraph, tag inside the item",
                             page(prefix, tag, text_col)))
    for tag_name, tag in TAGS:
        rows.append((f"two-digit ordered below column, {tag_name} outside", "boundary: below the wider column",
                     page("10. item\n\n   text", tag, 0)))
    for name, prefix, tag in [
        ("bullet two paragraphs, inline tag outside", "- item\n\n  first\n\n  text", "span"),
        ("task at column, inline tag outside", "- [ ] item\n\n  text", "span"),
        ("interrupting bullet at column, inline tag outside", "text\n- item\n\n  text", "span"),
        ("bullet at column, b tag outside", "- item\n\n  text", "b"),
        ("bullet after two blanks, inline tag outside", "- item\n\n\n  text", "span"),
    ]:
        rows.append((name, "resumed paragraph, tag outside the item", page(prefix, tag, 0)))
    for name, prefix in [("one space", "- item\n\n text"), ("four spaces", "- item\n\n    text"),
                         ("block quote", "> item\n\n  text"),
                         ("footnote definition two spaces", "[^1]: note\n\n  text"),
                         ("footnote definition four spaces", "[^1]: note\n\n    text"),
                         ("tab", "- item\n\n\ttext")]:
        for tag_name, tag in TAGS:
            rows.append((f"boundary {name}, {tag_name}", "boundary that already agreed", page(prefix, tag, 0)))
    out = [{"id": n, "kind": k, "r86_5": R86_5.get(n), "page": p} for n, k, p in rows]
    assert len({r["id"] for r in out}) == len(out)
    assert all(any(r["id"] == n for r in out) for n in R86_5)
    return out


def comment_controls() -> list[dict]:
    """#516's twelve variants (exact public bytes) and the contract probes."""
    f, rows = FENCE, []
    for phase, prefix in (("first", "- item"), ("resumed", "- item\n\n  text")):
        for column in (0, 1):
            for form, tag in (("open", "<span>"), ("close", "</span>"), ("attribute", '<span title="x">')):
                rows.append((f"#516 {phase} tag column {column} {form}",
                             f"{prefix}\n{' ' * column}{tag}\n<!--\n\n## Old\n</span>\n\n## Real\n"))
    rows += [
        ("top-level tag leaves comment open", "<span>\n<!--\n\n## Old\n</span>\n\n## Real\n"),
        ("type-6 block leaves comment open", "<div>\n<!--\n</div>\n\n## Old\n\n## Real\n"),
        ("comment opened on the type-6 line", "<div><!--\n</div>\n\n## Old\n\n## Real\n"),
        ("closed then reopened in a block", "<div>\n<!-- a --> <!--\n</div>\n\n## Old\n\n## Real\n"),
        ("type-1 pre leaves comment open", "<pre>\n<!--\n</pre>\n\n## Old\n\n## Real\n"),
        ("type-1 script leaves comment open", "<script>\n<!--\n</script>\n\n## Old\n\n## Real\n"),
        ("closed inside the block", "<div>\n<!-- a -->\n</div>\n\n## Old\n\n## Real\n"),
        ("closed on a later block line", "<div>\n<!--\n-->\n</div>\n\n## Old\n\n## Real\n"),
        ("abrupt empty comment in a block", "<div>\n<!-->\n</div>\n\n## Old\n\n## Real\n"),
        ("abrupt dash comment in a block", "<div>\n<!--->\n</div>\n\n## Old\n\n## Real\n"),
        ("abrupt empty comment line", "<!-->\n\n## Old\n\n## Real\n"),
        ("abrupt empty comment inline", "text <!--> more\n\n## Old\n\n## Real\n"),
        ("closed by a later type-6 block", "<div>\n<!--\n</div>\n\n## Hidden\n\n<div>\n-->\n</div>\n\n## Old\n\n## Real\n"),
        ("closed by a later type-7 block", "<span>\n<!--\n\n## Hidden\n\n<span>\n-->\n\n## Old\n\n## Real\n"),
        ("closed by a later type-1 block", "<div>\n<!--\n</div>\n\n## Hidden\n\n<pre>\n-->\n</pre>\n\n## Old\n\n## Real\n"),
        ("closed by a type-2 block", "<div>\n<!--\n</div>\n\n## Hidden\n\n<!-- b -->\n\n## Old\n\n## Real\n"),
        ("closed by a multi-line type-2 block", "<div>\n<!--\n</div>\n\n## Hidden\n\n<!--\nnote\n-->\n\n## Old\n\n## Real\n"),
        ("closed by an abrupt comment in a block", "<div>\n<!--\n</div>\n\n## Hidden\n\n<div>\n<!-->\n</div>\n\n## Old\n\n## Real\n"),
        ("closed by an inline comment", "<div>\n<!--\n</div>\n\n## Hidden\n\ntext <!-- x --> more\n\n## Old\n\n## Real\n"),
        ("closed by a comment in a heading", "<div>\n<!--\n</div>\n\n## Hidden <!-- x -->\n\n## Old\n\n## Real\n"),
        ("prose arrow closes nothing", "<div>\n<!--\n</div>\n\n## Hidden\n\n-->\n\n## Old\n\n## Real\n"),
        ("heading arrow closes nothing", "<div>\n<!--\n</div>\n\n## Hidden -->\n\n## Old\n\n## Real\n"),
        ("code span arrow closes nothing", "<div>\n<!--\n</div>\n\n## Hidden\n\n`-->`\n\n## Old\n\n## Real\n"),
        ("fenced arrow closes nothing", f"<div>\n<!--\n</div>\n\n## Hidden\n\n{f}\n-->\n{f}\n\n## Old\n\n## Real\n"),
        ("indented arrow closes nothing", "<div>\n<!--\n</div>\n\n## Hidden\n\n    -->\n\n## Old\n\n## Real\n"),
        ("fenced opener opens nothing", f"{f}\n<!--\n{f}\n\n## Old\n\n## Real\n"),
        ("indented opener opens nothing", "    <!--\n\n## Old\n\n## Real\n"),
        ("type-7 arrow line opens nothing", "<span>\n-->\n\n## Old\n\n## Real\n"),
    ]
    return [{"id": n, "page": p} for n, p in rows]


if __name__ == "__main__":
    WORK.mkdir(exist_ok=True)
    fo, cc = family_one(), comment_controls()
    json.dump(fo, open(WORK / "family-one-in.json", "w"), indent=1)
    json.dump(cc, open(WORK / "comment-in.json", "w"), indent=1)
    print(len(fo), "family-one shapes;", len(cc), "comment controls")

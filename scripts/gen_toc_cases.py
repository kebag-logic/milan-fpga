#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test CASE TABLES of `gen_toc.py`: fixture pages and answers.

WHICH MODULE IS WHICH. `gen_toc.py` owns block classification for this
repository: the one walk, every rule that decides what a line is, and the
runner that scores these tables. None of that may live anywhere else, and
none of it moved here. THIS module owns no rule and no decision. It is
data: each arm is a name, a fixture page, and the answer that page must
produce, in five families - the block walk, the type-7 opener, the ATX
closing sequence, the lines a lone tag may follow, and provenance. An arm
here says what the generator must answer; `gen_toc.py` says why.

Split off in round 6 of PR #428 ([R86] suggestion, round 5): the tables
had grown to where the two halves together ran past rule 12's long-module
ratchet (docs/development/CODE_QUALITY.md), and the tables are the half
that carries no classification code. `gen_toc.selftest()` imports the five
families from inside its own body, so the import below is not a cycle.
"""
from gen_toc import (CODE, COMMENT, FENCE, HTML, TEXT, generated_block,
                     headings)


#: A page whose Contents block the generator owns: three sections, one
#: heading carrying text a label must copy verbatim, and the block itself.
_ARM_PAGE = """# Page

## Contents

- **[Alpha](#alpha)** -- What alpha holds.
- **[Beta](#beta)** -- What beta holds.
- **[Gamma](#gamma)** -- What gamma holds.

## Alpha

Body.

## Beta

Body.

## Gamma

Body.
"""


def walk_arms() -> list[tuple[str, str, object]]:
    """The block walk's arms: (name, page, predicate over `blocks(page)`).
    Every one was an escape or a false refusal measured on PR #384, so each
    states the rule it holds rather than a shape it happens to accept."""
    tick, tilde = "`" * 3, "~" * 3
    return [
        ("a fence delimiter inside a comment opens no fence",
         f"<!--\n{tick}\n-->\n\n## Contents\n",
         lambda k: k[:3] == [COMMENT] * 3 and k[4] == TEXT),
        ("a comment delimiter inside a fence opens no comment",
         f"{tick}\n<!--\n{tick}\n\n## Contents\n",
         lambda k: k[:3] == [FENCE] * 3 and k[4] == TEXT),
        ("a short delimiter inside a longer fence is content",
         f"{tick}`\n{tick}\n## Contents\n{tick}`\ntext\n",
         lambda k: k[:4] == [FENCE] * 4 and k[4] == TEXT),
        ("a tilde fence does not close on backticks",
         f"{tilde}\n{tick}\n## Contents\n{tilde}\ntext\n",
         lambda k: k[:4] == [FENCE] * 4 and k[4] == TEXT),
        ("a closer carrying an info string does not close",
         f"{tick}\n{tick} text\n## Contents\n{tick}\ntext\n",
         lambda k: k[:4] == [FENCE] * 4 and k[4] == TEXT),
        ("a backtick in a backtick opener's info string voids the opener",
         f"{tick} `x\ntext\n", lambda k: k[0] == TEXT),
        ("a backtick in a tilde opener's info string does not",
         f"{tilde} `x\ntext\n", lambda k: k[0] == FENCE),
        ("an opener indented three spaces still opens",
         f"   {tick}\ntext\n   {tick}\n", lambda k: k[:3] == [FENCE] * 3),
        ("four spaces after a blank line is code, not a fence",
         f"text\n\n    {tick}\n", lambda k: k[2] == CODE),
        ("an indented line continuing a paragraph is not code",
         "text\n    more text\n", lambda k: k[1] == TEXT),
        ("a raw HTML block's content is not Markdown",
         "<pre>\n## Contents\n</pre>\n\n## Real\n",
         lambda k: k[:3] == [HTML] * 3 and k[4] == TEXT),
        ("a raw HTML block closed on its own line ends there",
         "<pre>x</pre>\n\n## Real\n", lambda k: k[0] == HTML and k[2] == TEXT),
        ("a tight type-6 block hides the heading it wraps",
         "<div>\n## Alpha\n</div>\n\n## Real\n",
         lambda k: k[:3] == [HTML] * 3 and k[4] == TEXT),
        ("a type-6 block ends at the blank line, so the heading renders",
         "<div>\n\n## Alpha\n\n</div>\n",
         lambda k: k[0] == HTML and k[2] == TEXT),
        ("a details block hides its heading the same way",
         "<details>\n<summary>s</summary>\n## Alpha\n</details>\n\n## Real\n",
         lambda k: k[:4] == [HTML] * 4 and k[5] == TEXT),
        ("a tight type-7 block on an unknown tag hides the heading it wraps",
         '<custom-tag data-x="1" y>\n## Alpha\n</custom-tag>\n\n## Real\n',
         lambda k: k[:3] == [HTML] * 3 and k[4] == TEXT),
        ("an inline tag alone on its line opens a type-7 block the same way",
         "<span>\n## Alpha\n</span>\n\n## Real\n",
         lambda k: k[:3] == [HTML] * 3 and k[4] == TEXT),
        ("a lone closing tag opens a type-7 block",
         "</b>\n## Alpha\n\n## Real\n",
         lambda k: k[:2] == [HTML] * 2 and k[3] == TEXT),
        ("a type-7 block ends at the blank line, so the heading renders",
         "<span>\n\n## Alpha\n\n</span>\n",
         lambda k: k[0] == HTML and k[2] == TEXT),
        ("a lone inline tag after visible text continues the paragraph",
         "text\n<span>\n## Real\n</span>\n", lambda k: k[:3] == [TEXT] * 3),
        ("a tag line carrying anything but the tag opens no type-7 block",
         "<span>x\n## Real\n", lambda k: k[:2] == [TEXT] * 2),
        ("a comment opened after visible text leaves that line alone",
         "## Head <!-- note\n-->\n## B\n",
         lambda k: k[0] == TEXT and k[1] == COMMENT and k[2] == TEXT),
        ("a second comment opened on a closing line stays open",
         "<!-- first --> <!-- second\n## Contents\n-->\ntext\n",
         lambda k: k[:3] == [COMMENT] * 3 and k[3] == TEXT),
        ("a comment closed and reopened inside a span stays open",
         "<!--\nx --> y <!-- z\n## Contents\n-->\ntext\n",
         lambda k: k[:4] == [COMMENT] * 4 and k[4] == TEXT),
        ("a comment that really closes ends the span",
         "<!-- one --> two\n## Contents\n",
         lambda k: k[0] == COMMENT and k[1] == TEXT),
    ]


def tag_arms() -> list[tuple[str, str, object]]:
    """The type-7 opener's own arms, one per behaviour that shipped with no
    arm to hold it ([R86] F2, round 1 on PR #428): the order that reads a
    type-1 tag first, the three spaces of indentation the grammar allows
    and the four that make code instead, and the self-closing form. Four
    spaces under a list item reach the tag grammar, no code run opening
    there, and it must refuse them ([R86] F2, round 2); under a heading
    they are code, so the lone tag under THEM opens a block ([R85] F1,
    round 3). The grammar's first character was the last bound of the
    opener with no arm ([R86] F2, round 5): a name begins with an ASCII
    letter, so `<1>` is no tag and the heading under it renders."""
    return [
        ("a type-1 tag is read before the type-7 grammar, so its block "
         "survives a blank line",
         "<pre>\n\n## Alpha\n</pre>\n\n## Real\n",
         lambda k: k[:4] == [HTML] * 4 and k[5] == TEXT),
        ("a tag indented three spaces opens a type-7 block",
         "   <span>\n## Alpha\n</span>\n\n## Real\n",
         lambda k: k[:3] == [HTML] * 3 and k[4] == TEXT),
        ("a tag indented four spaces after a blank line is code",
         "    <span>\n## Alpha\n", lambda k: k[0] == CODE and k[1] == TEXT),
        ("a self-closing tag alone on its line opens a type-7 block",
         '<img src="x" />\n## Alpha\n\n## Real\n',
         lambda k: k[:2] == [HTML] * 2 and k[3] == TEXT),
        ("a tag indented four spaces under a list item is that item's text, "
         "so the heading under it renders",
         "- item\n    <span>\n## Old\n",
         lambda k: k[1] == TEXT and k[2] == TEXT),
        ("a tag indented four spaces under a heading is code, so a lone tag "
         "under it opens a block",
         "## Head\n    <span>\n<b>\n## Old\n",
         lambda k: k[1] == CODE and k[2:4] == [HTML] * 2),
        ("a name that does not begin with an ASCII letter is no tag, so the "
         "heading under it renders",
         "## Head\n<1>\n## Old\n", lambda k: k[1:3] == [TEXT] * 2),
    ]


def _expects(anchors: list[str]) -> object:
    """A predicate over a page: `headings()` assigns exactly these anchors."""
    return lambda text: [a for _, _, a in headings(text)] == anchors


def _listed(pairs: list[tuple[str, str]]) -> object:
    """A predicate over a page: `headings()` lists exactly these (text,
    anchor) pairs, so an arm can hold a label and its anchor together."""
    return lambda text: [(r, a) for _, r, a in headings(text)] == pairs


def heading_arms() -> list[tuple[str, str, object]]:
    """`HEAD_RE`'s own arms: the closing sequence of hashes CommonMark 4.2
    drops is a RUN of hashes with a space or a tab before it and nothing
    but blanks after it, and neither bound had an arm ([R86] F2, round 5
    on PR #428). Admitting anything after the run lists `## Old ## bar` as
    `Old` at `old`, where the page renders `Old ## bar` at `old--bar`;
    dropping the space before it lists `## Old#` as `Old`, a label the
    page does not carry at an anchor it does. Both are held whole, the
    rendered text beside the anchor, because it is the LABEL that a
    Contents entry mirrors."""
    return [
        ("a run of hashes that does not end the line is heading text",
         "## Old ## bar\n", _listed([("Old ## bar", "old--bar")])),
        ("a closing sequence takes a space or a tab before it",
         "## Old#\n", _listed([("Old#", "old")])),
    ]


def predecessor_arms() -> list[tuple[str, str, object]]:
    """`headings()` under a lone tag that follows each line after which no
    paragraph is open: with no blank line between, the tag opens a type-7
    block and the heading tucked inside it is text. The blank-line reading
    kept that heading in the first nine shapes ([R85] F1 and [R86] F1,
    round 1 on PR #428); the pipe once demanded of a delimiter row kept it
    under `:-:`, and a footnote definition was read as paragraph text
    ([R86] F1, round 2); an indented line directly under a block that
    closed was read as paragraph text where CommonMark 4.4 has code ([R85]
    F1, round 3); a list item interrupting a paragraph had no arm, so the
    clause that lets it could go with every arm green ([R86] F1, round 4).
    Round 5 left the INDENTATION of these lines unheld ([R86] F2, round
    5): the three spaces CommonMark allows an ATX opener, a block quote,
    a list item and a footnote definition, the opener with no text after
    its hashes, and a setext underline of hyphens rather than equals
    signs, each of which ends or holds a paragraph the renderer does not
    leave open, so dropping any of them reopens the escape on the shape
    beside it. The setext underline of one hyphen is held by the plain
    line AFTER it rather than by the tag directly under it: read as a
    delimiter row instead, `-` still keeps the tag's paragraph closed, and
    only the line after tells the two readings apart, one starting a fresh
    paragraph the tag continues and the other holding the line.

    The `keeps` are lines after which a paragraph IS open, so the same tag
    continues it and the heading renders: among them a delimiter row that
    does not match its header row's cells or is indented four spaces, an
    empty item, which cannot interrupt a paragraph, a footnote definition
    indented four spaces, which is no definition at all, and the plain
    line after a one-hyphen underline, each continuing the paragraph as
    the renderer continues it."""
    tick = "`" * 3
    hides = [
        ("an ATX heading", "## Alpha", ["alpha"]),
        ("a closing fence", f"{tick}\ncode\n{tick}", []),
        ("a thematic break", "***", []),
        ("a closing comment line", "<!-- note\n-->", []),
        ("a list item", "- item", []),
        ("a block quote", "> quoted", []),
        ("a table row", "| a | b |\n|---|---|\n| c | d |", []),
        ("a setext underline", "Alpha\n===", []),
        ("a type-1 block's closing tag", "<pre>\ncode\n</pre>", []),
        ("an indented code line", "    code", []),
        ("a plain line lazily continuing a list item", "- item\nlazy", []),
        ("a table row without a pipe", "| a |\n|---|\nrow", []),
        ("an empty list item", "-", []),
        ("a pipeless delimiter row under a paragraph line", "text\n:-:", []),
        ("a pipeless delimiter row under a pipe-led line", "| a |\n:-:", []),
        ("a footnote definition", "[^1]: note", []),
        ("a footnote definition interrupting a paragraph",
         "text\n[^1]: note", []),
        ("a plain line lazily continuing a footnote definition",
         "[^1]: note\nlazy", []),
        ("CommonMark 4.4's own `# Heading` then `    foo`",
         "# Heading\n    foo", ["heading"]),
        ("a tab-indented line under a heading", "# H\n\tcode", ["h"]),
        ("a pipeless delimiter row indented three spaces", "text\n   :-:", []),
        ("a list item interrupting a paragraph", "text\n- item", []),
        ("an ordered item interrupting a paragraph", "text\n1. item", []),
        ("a plain line lazily continuing an item that interrupted a "
         "paragraph", "text\n- item\nlazy", []),
        ("a closed ATX heading", "## Alpha ##", ["alpha"]),
        ("an ATX heading indented three spaces", "text\n   # H", []),
        ("an empty ATX heading", "text\n##", []),
        ("a block quote indented two spaces", "text\n  > quoted", []),
        ("a list item indented two spaces", "text\n  - item", []),
        ("a footnote definition indented two spaces",
         "text\n  [^1]: note", []),
    ]
    # The five above that closed, an indented code line between ([R85] F1).
    closed = ("a closing fence", "a thematic break", "a closing comment line",
              "a setext underline", "a type-1 block's closing tag")
    hides += [(f"an indented code line under {what}", before + "\n    code",
               own) for what, before, own in hides if what in closed]
    keeps = [
        ("paragraph text", "text"),
        ("a pipe-led line with no delimiter row under it", "| a |"),
        ("an ordered item that cannot interrupt a paragraph",
         "text\n2. item"),
        ("an equals-sign line that no paragraph precedes", "==="),
        ("a delimiter row with fewer cells than its header row",
         "| a | b |\n|---|"),
        ("a delimiter row with more cells than its header row",
         "| a |\n|---|---|"),
        ("a delimiter row whose header row's only pipe is escaped",
         "a \\| b\n-|-"),
        ("a pipeless delimiter row indented four spaces", "text\n    :-:"),
        ("a pipeless delimiter row indented by a tab", "text\n\t:-:"),
        ("an empty item that cannot interrupt a paragraph", "text\n*"),
        ("a footnote definition indented four spaces",
         "text\n    [^1]: note"),
        ("a plain line after a setext underline of one hyphen",
         "text\n-\nlazy"),
    ]
    wrapped = "\n<span>\n## Old\n</span>\n\n## Beta\n"
    return ([(f"a lone tag directly under {what} hides the heading it wraps",
              before + wrapped, _expects(own + ["beta"]))
             for what, before, own in hides]
            + [(f"a lone tag under {what} continues it, so the heading "
                "renders", before + wrapped, _expects(["old", "beta"]))
               for what, before in keeps])


def provenance_arms() -> list[tuple[str, str, object]]:
    """`generated_block`'s arms: what counts as this script's own output."""
    page = _ARM_PAGE
    return [
        ("a block this script would write has provenance", page,
         lambda t: generated_block(t) is not None),
        ("a hand-edited entry loses it for the block",
         page.replace("- **[Beta](#beta)** --", "- **[Beta](#beta)**  --"),
         lambda t: generated_block(t) is None),
        ("an entry indented four spaces loses it",
         page.replace("- **[Beta]", "    - **[Beta]"),
         lambda t: generated_block(t) is None),
        ("a block inside a fence is no block of this page",
         page.replace("## Contents", "```\n## Contents").replace(
             "\n## Alpha", "\n```\n\n## Alpha", 1),
         lambda t: generated_block(t) is None),
        ("a block inside a comment is no block of this page",
         page.replace("## Contents", "<!--\n## Contents").replace(
             "\n## Alpha", "\n-->\n\n## Alpha", 1),
         lambda t: generated_block(t) is None),
        ("a block inside a raw HTML block is no block of this page",
         page.replace("## Contents", "<pre>\n## Contents").replace(
             "\n## Alpha", "\n</pre>\n\n## Alpha", 1),
         lambda t: generated_block(t) is None),
        ("a heading inside a tight type-6 block is no heading",
         "<div>\n## Alpha\n</div>\n\n## Beta\n", _expects(["beta"])),
        ("a heading inside a type-6 block that closed IS a heading",
         "<div>\n\n## Alpha\n\n</div>\n\n## Beta\n", _expects(["alpha", "beta"])),
        ("a heading inside a tight type-7 block is no heading",
         "<span>\n## Alpha\n</span>\n\n## Beta\n", _expects(["beta"])),
        ("a heading after a tag that continues a paragraph IS a heading",
         "text\n<span>\n## Alpha\n</span>\n\n## Beta\n",
         _expects(["alpha", "beta"])),
        ("a heading inside a comment is no heading",
         "<!--\n## Alpha\n-->\n\n## Beta\n", _expects(["beta"])),
        ("a page this script skips has no provenance", page,
         lambda t: generated_block(t, "docs/README.md") is None),
        ("nor has a historical page", page,
         lambda t: generated_block(t, "docs/history/v1/X.md") is None),
        ("nor has a generator-owned page",
         page.replace("# Page",
                      "# Page\n\n**GENERATED** - do not hand-edit."),
         lambda t: generated_block(t, "docs/x.md") is None),
        ("a page this script owns still has provenance", page,
         lambda t: generated_block(t, "docs/x.md") is not None),
    ]

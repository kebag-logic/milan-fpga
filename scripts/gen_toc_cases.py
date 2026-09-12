#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test CASE TABLES of `gen_toc.py`: fixture pages and answers.

WHICH MODULE IS WHICH. `gen_toc.py` owns block classification for this
repository: the one walk, every rule that decides what a line is, and the
runner that scores these tables. None of that may live anywhere else, and
none of it moved here. THIS module owns no rule and no decision. It is
data: each arm is a name, a fixture page, and the answer that page must
produce, in six families - the block walk, the type-7 opener, the two
guards that hold these tables, the ATX closing sequence, the lines a lone
tag may follow, and provenance. An arm here says what the generator must
answer; `gen_toc.py` says why. The guard family is the one that carries
no page: its arms score the guards themselves and ignore theirs.

Split off in round 6 of PR #428 ([R86] suggestion, round 5): the tables
had grown to where the two halves together ran past rule 12's long-module
ratchet (docs/development/CODE_QUALITY.md), and the tables are the half
that carries no classification code. `gen_toc.selftest()` imports the
families from inside its own body, so the import below is not a cycle, and
it registers itself under its own name first so that this module's import
binds the runner's own walk rather than a second copy of the file ([R85]
suggestion, round 6).
"""
from pathlib import Path

from gen_toc import (ARM_FAMILIES, CODE, COMMENT, FENCE, HTML, MIN_ARMS, TEXT,
                     _owner_guards, _tally_guards, generated_block, headings)


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
    states the rule it holds rather than a shape it happens to accept.

    Round 7 adds four and extends a fifth, one per bound the systematic
    enumeration of that round found with no arm: the blank line an
    indented code run carries (which
    round 6 measured as pre-existing and unreachable, and which is cheaper
    to hold than to argue), a type-6 block interrupting a paragraph where
    a type-7 block may not, the closer of an INDENTED fence, a closer
    shorter than its opener at that indentation, and an indented backtick
    opener whose info string carries a backtick."""
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
        ("an opener indented three spaces still opens, and its closer at "
         "the same indentation still closes",
         f"   {tick}\ntext\n   {tick}\n## Real\n",
         lambda k: k[:3] == [FENCE] * 3 and k[3] == TEXT),
        ("an indented closer shorter than its opener does not close",
         f"{tick}`\n   {tick}\n## Old\n{tick}`\n## Real\n",
         lambda k: k[:4] == [FENCE] * 4 and k[4] == TEXT),
        ("a backtick in an INDENTED backtick opener's info string voids it "
         "the same way",
         f"   {tick} `x\ntext\n", lambda k: k[0] == TEXT),
        ("four spaces after a blank line is code, not a fence",
         f"text\n\n    {tick}\n", lambda k: k[2] == CODE),
        ("an indented line continuing a paragraph is not code",
         "text\n    more text\n", lambda k: k[1] == TEXT),
        ("an indented code run carries the blank line inside it",
         "    code\n\n    more\n## Real\n",
         lambda k: k[:3] == [CODE] * 3 and k[3] == TEXT),
        ("a raw HTML block's content is not Markdown",
         "<pre>\n## Contents\n</pre>\n\n## Real\n",
         lambda k: k[:3] == [HTML] * 3 and k[4] == TEXT),
        ("a raw HTML block closed on its own line ends there",
         "<pre>x</pre>\n\n## Real\n", lambda k: k[0] == HTML and k[2] == TEXT),
        ("a tight type-6 block hides the heading it wraps",
         "<div>\n## Alpha\n</div>\n\n## Real\n",
         lambda k: k[:3] == [HTML] * 3 and k[4] == TEXT),
        ("a type-6 block INTERRUPTS a paragraph, where a type-7 block "
         "may not",
         "text\n<div>\n## Alpha\n</div>\n\n## Real\n",
         lambda k: k[0] == TEXT and k[1:5] == [HTML] * 4 and k[5] == TEXT),
        ("a type-6 block ends at the blank line, so the heading renders",
         "<div>\n\n## Alpha\n\n</div>\n",
         lambda k: k[0] == HTML and k[2] == TEXT),
        ("a details block hides its heading the same way",
         "<details>\n<summary>s</summary>\n## Alpha\n</details>\n\n## Real\n",
         lambda k: k[:4] == [HTML] * 4 and k[5] == TEXT),
        ("a tight type-7 block on an unknown tag hides the heading it wraps",
         '<custom-tag a=1 _b=\'2\' :c = "3" d>\n## Alpha\n'
         '</custom-tag>\n\n## Real\n',
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


def _tag_page(tag: str) -> str:
    """A page whose only heading sits under `tag`, directly under a heading
    so that no paragraph is open and the tag grammar alone decides."""
    return f"## Head\n{tag}\n## Old\n\n## Real\n"


def _opens(tag: str) -> tuple[str, object]:
    """`tag` is a complete tag: it opens a type-7 block that runs to the
    blank line, so the heading it wraps is text."""
    return (_tag_page(tag),
            lambda k: k[1:4] == [HTML] * 3 and k[4] == TEXT)


def _refuses(tag: str) -> tuple[str, object]:
    """`tag` is NO tag: nothing opens and the heading under it renders."""
    return (f"## Head\n{tag}\n## Old\n", lambda k: k[1:3] == [TEXT] * 2)


#: One complete tag per bound of the grammar, and one line per bound that
#: is a bound because the grammar REFUSES what lies past it. Derived from
#: the expressions rather than from a report ([R86] F1, round 6 on PR
#: #428, which named five of them): every alternative, every member of
#: every character class and every repetition count `_HTML_TAG_NAME`,
#: `_HTML_ATTRIBUTE` and `HTML_TAG_LINE_RE` state is exercised here, and
#: each one removed fails an arm below. GitHub's renderer agrees with
#: every line of it (the fixture oracle over all arms).
_TAGS_OPEN = [
    ("a name of letters, digits and hyphens after its first letter",
     "<AbC0-9>"),
    ("an attribute name carrying every character the grammar allows after "
     "its first", "<x a0_.:-E>"),
    ("a tab between attributes, and tabs around an equals sign",
     "<x\ta=1\tb\t=\t2>"),
    ("a quoted value that is empty", '<x a=\'\' b="">'),
    ("blanks between the last attribute and the self-closing slash",
     '<x a="1" \t/>'),
    ("blanks after the closing angle bracket", "<x> \t"),
    ("blanks inside a CLOSING tag", "</b \t>"),
    ("an attribute name that starts with a capital", "<x Ab>"),
]
_TAGS_REFUSED = [
    ("an attribute that no blank separates from the name", "<A::>"),
    ("an attribute name that starts with a hyphen", "<x -a>"),
    ("an equals sign with no value after it", "<x a=>"),
    ("an unquoted value carrying a closing angle bracket", "<x a=b>c>"),
    ("an unquoted value carrying an opening angle bracket", "<x a=b<c>"),
    ("an unquoted value carrying an equals sign", "<x a=b=c>"),
    ("an unquoted value carrying a backtick", "<x a=b`c>"),
    ("an unquoted value carrying a single quote", "<x a=b'c>"),
    ("an unquoted value carrying a double quote", '<x a=b"c>'),
    ("an unquoted value and then a word no attribute name may start",
     "<x a=1 2>"),
    ("the same past a tab", "<x a=1\t2>"),
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
    opener a REPORT named ([R86] F2, round 5): a name begins with an ASCII
    letter, so `<1>` is no tag and the heading under it renders.

    Round 7 stops taking that list from a report. `_TAGS_OPEN` and
    `_TAGS_REFUSED` above carry one line per bound the grammar states,
    enumerated from the expressions themselves, and each bound removed
    fails one of them."""
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
    ] + [(f"a lone tag with {what} opens a type-7 block", *_opens(tag))
         for what, tag in _TAGS_OPEN] + [
        (f"a line with {what} is no tag, so the heading under it renders",
         *_refuses(tag)) for what, tag in _TAGS_REFUSED]


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
    Contents entry mirrors.

    Round 7 adds the four remaining bounds the expression states, taken
    from the expression rather than from a report: the TAB the closing
    sequence also accepts before it, the blanks the line may end with, the
    level cap of six hashes, and the empty text a heading may carry."""
    return [
        ("a run of hashes that does not end the line is heading text",
         "## Old ## bar\n", _listed([("Old ## bar", "old--bar")])),
        ("a closing sequence takes a space or a tab before it",
         "## Old#\n", _listed([("Old#", "old")])),
        ("a TAB before the closing sequence drops it too",
         "## Old\t#\n", _listed([("Old", "old")])),
        ("the blanks a heading line ends with are not its text",
         "## Old \t\n", _listed([("Old", "old")])),
        ("seven hashes are no heading at all",
         "####### Old\n", _listed([])),
        ("a heading may carry no text", "# \n", _listed([("", "")])),
    ]


#: The lines a lone tag may follow, and what the page then answers. A
#: `hides` row is a line after which NO paragraph is open, so the tag
#: directly under it opens a type-7 block and the heading it wraps is
#: text; the third field is the anchors the row's own lines contribute. A
#: `keeps` row is a line after which one IS open, so the same tag
#: continues it and the heading renders. Rounds 1 to 6 took these from
#: findings; round 7 adds one per bound the enumeration of every
#: expression in `gen_toc.py` found unheld, so the table is now as wide as
#: the grammar rather than as wide as the last report.
_HIDES = [
    ("an ATX heading", "## Alpha", ["alpha"]),
    ("a closing fence", "```\ncode\n```", []),
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
    ("a footnote definition interrupting a paragraph", "text\n[^1]: note", []),
    ("a plain line lazily continuing a footnote definition",
     "[^1]: note\nlazy", []),
    ("CommonMark 4.4's own `# Heading` then `    foo`",
     "# Heading\n    foo", ["heading"]),
    ("a tab-indented line under a heading", "# H\n\tcode", ["h"]),
    ("a pipeless delimiter row indented three spaces", "text\n   :-:", []),
    ("a list item interrupting a paragraph", "text\n- item", []),
    ("an ordered item interrupting a paragraph", "text\n1. item", []),
    ("a plain line lazily continuing an item that interrupted a paragraph",
     "text\n- item\nlazy", []),
    ("a closed ATX heading", "## Alpha ##", ["alpha"]),
    ("an ATX heading indented three spaces", "text\n   # H", []),
    ("an empty ATX heading", "text\n##", []),
    ("a block quote indented two spaces", "text\n  > quoted", []),
    ("a list item indented two spaces", "text\n  - item", []),
    ("a footnote definition indented two spaces", "text\n  [^1]: note", []),
    # Round 7, the thematic break: its indentation, its three characters
    # and the blanks CommonMark allows between and after them.
    ("a thematic break indented one space", " ***", []),
    ("a thematic break ending in a space", "*** ", []),
    ("a thematic break ending in a tab", "***\t", []),
    ("a thematic break of hyphens", "## H\n\n---", ["h"]),
    ("a thematic break of hyphens ending in a space", "## H\n\n--- ", ["h"]),
    ("a thematic break of hyphens ending in a tab", "## H\n\n---\t", ["h"]),
    ("a thematic break of underscores", "___", []),
    ("a thematic break of underscores ending in a space", "___ ", []),
    ("a thematic break of underscores ending in a tab", "___\t", []),
    # Round 7, the ATX opener: the tab it takes after its hashes.
    ("an ATX opener followed by a tab", "#\t", []),
    # Round 7, the list item: its three bullets, its two ordinal
    # terminators, and the blanks between a marker and its content.
    ("a bullet item introduced by a plus", "+ item", []),
    ("a bullet item introduced by an asterisk", "* item", []),
    ("an ordered item closed by a parenthesis", "7) item", []),
    ("an empty item followed by a space", "- ", []),
    ("an empty item followed by a tab", "-\t", []),
    ("an item whose content is separated by tabs", "-\t\titem", []),
    # Round 7, the setext underline: its indentation and its trailing
    # blanks.
    ("a setext underline indented one space", "text\n =", []),
    ("a setext underline ending in a space", "text\n= ", []),
    ("a setext underline ending in a tab", "text\n=\t", []),
    # Round 7, the delimiter row: the blanks GFM allows around each cell,
    # the colons that align it, and the cell count `_table_cells` reads.
    ("a delimiter row whose only cell ends in a space", "text\n-| ", []),
    ("a delimiter row whose only cell ends in a tab", "text\n-|\t", []),
    ("a delimiter row whose leading pipe is followed by a space",
     "text\n| -", []),
    ("a delimiter row whose leading pipe is followed by tabs",
     "text\n|\t\t-", []),
    ("a delimiter row whose cells end in spaces", "| a || b |\n-|- |- ", []),
    ("a delimiter row whose cells begin with spaces", "| a || b |\n-| -| -",
     []),
    ("a delimiter row whose cells end in tabs",
     "| a || b |\n-|-\t\t|-\t\t", []),
    ("a delimiter row whose cells begin with tabs",
     "| a || b |\n-|\t\t-|\t\t-", []),
    ("a delimiter row of right-aligned cells", "| a || b |\n-|-:|-:", []),
    ("a delimiter row of left-aligned cells", "| a || b |\n-|:-|:-", []),
    ("a one-cell delimiter row under a one-character header row", "a\n:-:",
     []),
    ("a delimiter row under a header row whose first cell is empty",
     "|| b |\n-|-", []),
    ("a delimiter row whose first cell ends in a space", "text\n:- |", []),
    ("a delimiter row whose first cell ends in tabs", "text\n:-\t\t|", []),
    # Round 7, the paragraph state itself: a hold that a second plain line
    # still continues.
    ("two plain lines lazily continuing a list item", "- item\nlazy\nmore",
     []),
]
#: The five above that closed, an indented code line between ([R85] F1).
_CLOSED = ("a closing fence", "a thematic break", "a closing comment line",
           "a setext underline", "a type-1 block's closing tag")
_HIDES += [(f"an indented code line under {what}", before + "\n    code", own)
           for what, before, own in _HIDES if what in _CLOSED]
_KEEPS = [
    ("paragraph text", "text"),
    ("a pipe-led line with no delimiter row under it", "| a |"),
    ("an ordered item that cannot interrupt a paragraph", "text\n2. item"),
    ("an equals-sign line that no paragraph precedes", "==="),
    ("a delimiter row with fewer cells than its header row",
     "| a | b |\n|---|"),
    ("a delimiter row with more cells than its header row", "| a |\n|---|---|"),
    ("a delimiter row whose header row's only pipe is escaped", "a \\| b\n-|-"),
    ("a pipeless delimiter row indented four spaces", "text\n    :-:"),
    ("a pipeless delimiter row indented by a tab", "text\n\t:-:"),
    ("an empty item that cannot interrupt a paragraph", "text\n*"),
    ("a footnote definition indented four spaces", "text\n    [^1]: note"),
    ("a plain line after a setext underline of one hyphen", "text\n-\nlazy"),
    # Round 7: the same bounds from the other side, each a line the
    # expression must REFUSE, and does.
    ("a run of seven hashes, which is no ATX opener", "####### x"),
    ("a run of hashes with text right after it", "#x"),
    ("an ATX opener indented four spaces", "text\n    # x"),
    ("a block quote indented four spaces", "text\n    > quoted"),
    ("a setext underline indented four spaces", "text\n    ="),
    ("an ordered item of ten digits", "7777777777) item"),
    ("an ordinal terminator with no ordinal before it", ") item"),
    ("a bullet whose content no blank separates", "-item"),
    ("a list item indented four spaces", "text\n    - item"),
    ("a hyphen run with text after it", "text\n-x"),
    ("a row of hyphens and pipes with an empty cell", "| a | b |\n-||"),
    ("a footnote label that is empty", "[^]: note"),
    ("a bracketed label with no caret before it", "[x]: note"),
    ("a footnote label with no colon after it", "[^x] note"),
    ("a footnote label carrying a closing bracket", "[^]]]:"),
    ("a footnote label of blanks", "[^  ]:"),
    ("a thematic break indented four spaces", "text\n    ***"),
    ("a run of asterisks with text after it", "***x"),
    ("a lone colon under a paragraph line", "text\n:"),
    ("a one-cell delimiter row that no paragraph precedes", "***\n:-:"),
]


def predecessor_arms() -> list[tuple[str, str, object]]:
    """`headings()` under a lone tag that follows each line of `_HIDES` and
    each line of `_KEEPS`. Under a `_HIDES` line no paragraph is open, so
    with no blank line between, the tag opens a type-7 block and the
    heading tucked inside it is text; under a `_KEEPS` line one is, so the
    tag continues it and the heading renders. The two tables carry the
    reasons; this assembles them."""
    wrapped = "\n<span>\n## Old\n</span>\n\n## Beta\n"
    return ([(f"a lone tag directly under {what} hides the heading it wraps",
              before + wrapped, _expects(own + ["beta"]))
             for what, before, own in _HIDES]
            + [(f"a lone tag under {what} continues it, so the heading "
                "renders", before + wrapped, _expects(["old", "beta"]))
               for what, before in _KEEPS])


#: The separator a Contents entry written before the em-dash rule carries.
#: 78 tracked pages still use it, and `existing()` reads it off the FIRST
#: entry so that `generated_block()` renders the block those pages
#: actually carry. It is assembled rather than spelled because the gate
#: that reads those pages refuses the character on an added line.
_OLD_SEPARATOR = chr(0x2014)


def guard_arms() -> list[tuple[str, str, object]]:
    """The two table GUARDS' own arms. They are scored like a page family
    and ignore the page: what each states is the answer a guard gives for
    a set of tables, which is the only way a guard ADDED to hold the
    tables is itself held. Round 6 of PR #428 was asked for the tally
    guard; round 7 adds it and this, because a guard with no arm is the
    same gap one layer up.

    `_tally_guards` must pass a full set, and name a family that is
    missing, a family that is present and empty, a total below the
    recorded floor, and a runner that scores fewer arms than the tables
    hold. `_owner_guards` must pass this module's own source and values,
    and name a module that imports the expression engine or holds a
    compiled expression. The compiled one is fetched inside this function
    on purpose: bound at the top of the module it would be exactly what
    the guard refuses."""
    from gen_toc import HEAD_RE
    plenty = {name: [None] * MIN_ARMS for name in ARM_FAMILIES}
    whole = MIN_ARMS * len(ARM_FAMILIES)
    short = {name: arms for name, arms in plenty.items() if name != "tag"}
    here = Path(__file__)
    return [
        ("the tally guard passes a full set of families", "",
         lambda t: _tally_guards(plenty, whole) == []),
        ("it names a family dropped from the runner's import", "",
         lambda t: len(_tally_guards(short, whole - MIN_ARMS)) == 1),
        ("it names a family that is present and empty", "",
         lambda t: len(_tally_guards(dict(plenty, tag=[]),
                                     whole - MIN_ARMS)) == 1),
        ("it names a total below the recorded floor", "",
         lambda t: [str(MIN_ARMS) in note for note in _tally_guards(
             {name: [None] for name in ARM_FAMILIES},
             len(ARM_FAMILIES))] == [True]),
        ("it names a runner that scores fewer arms than the tables hold",
         "", lambda t: len(_tally_guards(plenty, whole - 1)) == 1),
        ("the ownership guard passes this module's own source and values",
         "", lambda t: _owner_guards(here.name, here.read_text(),
                                     dict(globals())) == []),
        ("it names a module that imports the expression engine", "",
         lambda t: len(_owner_guards("x.py", "import re\n", {})) == 1),
        ("it names one that imports a name OUT of the engine", "",
         lambda t: len(_owner_guards("x.py", "from re import Pattern\n",
                                     {})) == 1),
        ("a package whose LAST segment is the engine's name is not it", "",
         lambda t: _owner_guards("x.py", "import a.re\nfrom a.re import b\n",
                                 {}) == []),
        ("nor is a relative import, which names no module at all", "",
         lambda t: _owner_guards("x.py", "from . import b\n", {}) == []),
        ("it names a module that holds a compiled expression", "",
         lambda t: len(_owner_guards("x.py", "x = 1\n", {"P": HEAD_RE})) == 1),
    ]


def provenance_arms() -> list[tuple[str, str, object]]:
    """`generated_block`'s arms: what counts as this script's own output."""
    page = _ARM_PAGE
    return [
        ("a block this script would write has provenance", page,
         lambda t: generated_block(t) is not None),
        ("a block written with the older separator keeps its provenance",
         page.replace("--", _OLD_SEPARATOR),
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
        ("a contents heading with nothing after it has no provenance",
         "# Page\n\n## Contents\n", lambda t: generated_block(t) is None),
        ("nor has one whose block runs to the last line of the page",
         page[:page.index("## Alpha")].rstrip() + "\n",
         lambda t: generated_block(t) is None),
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

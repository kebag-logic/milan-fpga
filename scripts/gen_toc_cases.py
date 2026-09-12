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

from gen_toc import (ARM_FAMILIES, CLASSES, CODE, COMMENT, FENCE,
                     HTML_BLOCK_TAGS, HTML, MIN_ARMS, RAW_HTML_TAGS, REFUSED,
                     TEXT, WALK_ROOTS, _class_guards, _owner_guards,
                     _tally_guards, generated_block, headings, refusal_notes,
                     refusals)


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
    ] + _html_walk_arms()


def _html_walk_arms() -> list[tuple[str, str, object]]:
    """The half of the walk family that reads a raw HTML block or a
    comment, split off so neither function runs past rule 12's length
    ratchet ([R85] suggestion, round 9 on PR #428)."""
    return [
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
        # Round 9: the line that ENDS a type-6 or type-7 block is blank as
        # CommonMark 2.1 has it, spaces and tabs, and not as `str.strip()`
        # reads it ([R85] F1(a), [R86] F1 R1 and R2).
        ("a line of a no-break space does not end a type-7 block",
         "<span>\n\u00a0\n## Alpha\n</span>\n\n## Real\n",
         lambda k: k[:4] == [HTML] * 4 and k[5] == TEXT),
        ("a line of a form feed does not end a type-6 block",
         "<div>\n\f\n## Alpha\n</div>\n\n## Real\n",
         lambda k: k[:4] == [HTML] * 4 and k[5] == TEXT),
        ("a line of spaces and tabs does end one",
         "<span>\n \t\n## Alpha\n",
         lambda k: k[0] == HTML and k[1] == HTML and k[2] == TEXT),
        # Round 9: `<pre` at the end of its line opens a type-1 block and
        # `<pre/>` opens none, which is the renderer's start condition
        # ([R85] F1, the type-1 opener).
        ("a type-1 name ending its line opens the block that survives a "
         "blank line", "<pre\n\n## Alpha\n</pre>\n\n## Real\n",
         lambda k: k[:4] == [HTML] * 4 and k[5] == TEXT),
        ("a self-closing type-1 name opens a type-7 block instead, which "
         "the blank line ends", "<pre/>\n## Alpha\n\n## Real\n",
         lambda k: k[:3] == [HTML] * 3 and k[3] == TEXT),
        # Round 9: the type-6 name list is the renderer's ([R86] F1 R9).
        ("a type-6 name the renderer carries interrupts a paragraph",
         "text\n<source>\n## Alpha\n\n## Real\n",
         lambda k: k[0] == TEXT and k[1:4] == [HTML] * 3 and k[4] == TEXT),
        ("a name the renderer does not carry is type 7, so it may not",
         "text\n<search>\n## Alpha\n",
         lambda k: k[:3] == [TEXT] * 3),
        # Round 9: the three ways the renderer lets a type-6 name end, and
        # the blank a type-1 name takes, each an alternative this change
        # spells and none of which an arm held.
        ("a type-6 name that ends its line opens the block",
         "text\n<div\n>\n## Alpha\n</div>\n\n## Real\n",
         lambda k: k[0] == TEXT and k[1:6] == [HTML] * 5 and k[6] == TEXT),
        ("a self-closing type-6 tag opens it too",
         "text\n<div/>\n## Alpha\n</div>\n\n## Real\n",
         lambda k: k[0] == TEXT and k[1:5] == [HTML] * 4 and k[5] == TEXT),
    ] + _round9_walk_arms()


def _round9_walk_arms() -> list[tuple[str, str, object]]:
    """The walk family's round-9 half: the blank line as the renderer reads
    it, in the three decisions that read one, and the alternatives the
    type-1 and type-6 openers state."""
    return [
        # The paragraph state reads the same blank line as the block end,
        # and an indented code run ends at a line that is not blank
        # ([R85] F1(b), round 9 on PR #428).
        ("a line of a no-break space after paragraph text does not close "
         "the paragraph, so a lone tag under it continues it",
         "text\n\u00a0\n<span>\n## Alpha\n</span>\n\n## Real\n",
         lambda k: k[:4] == [TEXT] * 4),
        ("a line of a form feed does not close it either",
         "text\n\f\n<span>\n## Alpha\n</span>\n\n## Real\n",
         lambda k: k[:4] == [TEXT] * 4),
        ("a line of a no-break space ends an indented code run, which only "
         "a blank line carries through",
         "## Head\n\n    code\n\u00a0\n    more\n\n## Alpha\n",
         lambda k: k[2] == CODE and k[3] == TEXT and k[4] == TEXT),
        ("a type-1 name a blank follows is still read first, so its block "
         "survives a blank line",
         "## Head\n<pre x>\n\n## Alpha\n</pre>\n\n## Real\n",
         lambda k: k[0] == TEXT and k[1:5] == [HTML] * 4 and k[5] == TEXT),
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
#: `_HTML_ATTRIBUTE` and `HTML_TAG_LINE_RE` state is exercised here, at
#: EVERY position that states it, and each one removed fails an arm
#: below. GitHub's renderer agrees with every line of it (the fixture
#: oracle over all arms).
#:
#: Two things the tables held at one point only, and the expressions state
#: at several, cost round 7 a finding each: the closing-tag branch was
#: armed at one lowercase letter, and the whitespace class was armed at
#: the tab alone. Both are now armed per position and per character, so
#: the rows below outnumber the bounds a reader would count off the
#: expression text ([R85] F1 and [R86] F1, round 7).
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
    # [R85] F1, round 7: the closing-tag branch was armed at one lowercase
    # letter, and six single edits of its name survived both self-tests.
    # This row fails under every one of them: drop the branch's optional
    # continuation, or any member of either of its classes, and the name
    # no longer matches.
    ("a CLOSING tag name of letters, digits and hyphens after its first "
     "letter", "</AbC0-9>"),
    # [R86] F1, round 7: the whitespace the renderer accepts inside a tag,
    # one row per character per position. Narrow any of them back to
    # `[ \t]` and its rows fail.
    ("a line tabulation between the tag name and an attribute",
     "<x\va=1>"),
    ("a form feed between the tag name and an attribute", "<x\fa=1>"),
    ("line tabulations around an equals sign", "<x a\v=\v1>"),
    ("form feeds around an equals sign", "<x a\f=\f1>"),
    ("a line tabulation before the self-closing slash", '<x a="1"\v/>'),
    ("a form feed before the self-closing slash", '<x a="1"\f/>'),
    ("a line tabulation inside a CLOSING tag", "</b\v>"),
    ("a form feed inside a CLOSING tag", "</b\f>"),
    ("a form feed after the closing angle bracket", "<x>\f"),
    # [R86] F2, round 9: the three attribute VALUE classes were armed at a
    # handful of characters each, so ADDING a character to one survived
    # both self-tests and reopened the escape for the commonest lone tag
    # of all, a quoted value carrying a space. Each row below carries
    # every character its class admits that the sweep names, so narrowing
    # the class anywhere fails it; `CLASSES` is the one place any of the
    # three is spelled and the guard family arms the table itself.
    ("a single-quoted value carrying everything but its own quote",
     "<x a='b c\t\v\f=<>`\"d\u00e9'>"),
    ("a double-quoted value carrying everything but its own quote",
     '<x a="b c\t\v\f=<>`\'d\u00e9">'),
    ("an unquoted value carrying every character that does not end it",
     "<x a=b/c#d:e.f\u00e9>"),
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
    ("a CLOSING tag name that does not begin with an ASCII letter",
     "</1>"),
    # [R86] F1, round 7: the wider class from the other side. After the
    # closing angle bracket the renderer takes space, tab and form feed
    # and NOT a line tabulation, so widening that class fails the first
    # row; a line tabulation and a form feed each END an unquoted value,
    # so narrowing the value's own bound fails the other two.
    ("a line tabulation after the closing angle bracket", "<x>\v"),
    ("an unquoted value a line tabulation ends, and then a word no "
     "attribute name may start", "<x a=b\v1>"),
    ("the same past a form feed", "<x a=b\f1>"),
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
    fails one of them. Round 8 stops taking the CLASSES from the
    specification's prose: each is what the renderer was measured to
    apply at that position, and a sweep of every position against every
    character of every class the specification names is the receipt
    ([R85] F1 and [R86] F1, round 7)."""
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
        # Round 9 ([R85] F1(c)): the blanks a heading reads are the
        # renderer's at both positions. A TAB after the hashes opens a
        # heading, and a run of hashes is a CLOSING sequence only when
        # blanks alone follow it, so a no-break space after the run leaves
        # the hashes in the text exactly as the renderer shows them.
        ("a tab after the hashes opens a heading",
         "#\tOld\n", _listed([("Old", "old")])),
        ("a no-break space after a run of hashes is not a closing sequence",
         "## Old #\u00a0\n", _listed([("Old #\u00a0", "old-")])),
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
    ("an ATX opener followed by a tab", "#\t", [""]),
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
    # Round 9: each recogniser the paragraph state reads takes the class
    # the RENDERER takes at that position, so each row below is a block
    # the renderer sees and the walk used to miss ([R85] F2, [R86] F1 R3
    # to R8). The indentation rows are the family that needs no exotic
    # character at all: one, two or three spaces and then a tab is four
    # COLUMNS, which is an indented code line (CommonMark 2.2).
    ("a footnote label carrying a no-break space", "[^a\u00a0b]: note", []),
    ("a footnote label carrying a form feed", "[^a\fb]: note", []),
    ("a delimiter row padded by a form feed", "text\n:-:\f", []),
    ("a delimiter row whose cell a line tabulation pads",
     "| a || b |\n-|-\v|-", []),
    ("an item whose content is a no-break space", "- \u00a0", []),
    ("an item interrupting a paragraph whose content is a form feed",
     "text\n- \f", []),
    ("a line indented by one space and a tab under a heading",
     "## H\n \tcode", ["h"]),
    ("a line indented by two spaces and a tab under a heading",
     "## H\n  \tcode", ["h"]),
    ("a line indented by three spaces and a tab under a heading",
     "## H\n   \tcode", ["h"]),
    ("a header row whose escaped backslash leaves its pipe escaped",
     "a\\\\|b\n:-", []),
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
    # Round 9, the same bounds from the other side.
    ("an ordered item whose ordinal is no ASCII digit", "text\n\u0661. item"),
    ("a line indented by a tab and nothing else under a paragraph",
     "text\n\tcode"),
    ("a footnote label carrying a space", "text\n[^a b]: note"),
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


#: THE RENDERER'S CLASSES AGAIN, spelled here as a literal and not read
#: from the table the walk reads. That is the whole point of the row: the
#: guard family below compares the two, so narrowing or widening any class
#: in `gen_toc.CLASSES` - adding a space to a quoted value's stop class,
#: dropping the form feed from the delimiter row's padding, taking the tab
#: out of the blank line - fails one arm, whatever else agrees ([R86] F2
#: and [R85] F1, round 9 on PR #428; the shape of the fix is [R85]'s
#: round-7 suggestion on the family list, which the guard's own arms were
#: reading).
_CLASSES_SPELLED = {
    "blank": " \t",
    "indent": " ",
    "tag blank": " \t\v\f",
    "tag tail": " \t\f",
    "delimiter blank": " \t\v\f",
    "tag name": "A-Za-z",
    "tag name rest": "A-Za-z0-9-",
    "attribute name": "A-Za-z_:",
    "attribute name rest": "A-Za-z0-9_.:-",
    "unquoted value stop": " \t\v\f\"'=<>`",
    "single-quoted value stop": "'",
    "double-quoted value stop": '"',
    "footnote label stop": " \t\\]\x00\r\n",
    "ordinal": "0-9",
    "bullet": "-+*",
    "cell stop": "|",
}


#: The renderer's type-6 name list, spelled here and not read from the
#: constant the walk reads, in the order CommonMark 0.29 gives it.
_TYPE_6_SPELLED = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col"
    "|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure"
    "|footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html"
    "|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup"
    "|option|p|param|section|source|summary|table|tbody|td|tfoot|th|thead"
    "|title|tr|track|ul")


def _guard_source(body: str = "return X.match(line)",
                  pattern: str = '"[A-Z]"') -> str:
    """A one-decision module for `_class_guards` to read: both walk roots,
    one compiled expression and one statement in the walk."""
    return ("import re\n"
            f"X = re.compile({pattern})\n"
            "def line_kinds(line):\n"
            "    return blocks(line)\n"
            "def blocks(line):\n"
            f"    {body}\n")


def _notes(body: str = "return X.match(line)",
           pattern: str = '"[A-Z]"') -> list[str]:
    """What `_class_guards` refuses in such a module."""
    return _class_guards(_guard_source(body, pattern))[1]


def _kinds(body: str = "return X.match(line)",
           pattern: str = '"[A-Z]"') -> str:
    """How it classifies that module's sites, one word per site."""
    return " ".join(sorted(site.split(": ")[1]
                           for site in _class_guards(
                               _guard_source(body, pattern))[0]))


def guard_arms() -> list[tuple[str, str, object]]:
    """The two table GUARDS' own arms, and the family list they read.
    They are scored like a page family and ignore the page: what each
    states is the answer a guard gives for a set of tables, which is the
    only way a guard ADDED to hold the tables is itself held. Round 6 of PR #428 was asked for the tally
    guard; round 7 adds it and this, because a guard with no arm is the
    same gap one layer up.

    `_tally_guards` must pass a full set, and name a family that is
    missing, a family that is present and empty, a total below the
    recorded floor, and a runner that scores fewer arms than the tables
    hold. `_owner_guards` must pass this module's own source and values,
    and name a module that imports the expression engine or holds a
    compiled expression. The compiled one is fetched inside this function
    on purpose: bound at the top of the module it would be exactly what
    the guard refuses.

    The first arm below spells the family names AGAIN, as a literal, and
    not from `ARM_FAMILIES`. Every other arm here builds its fixture from
    that constant, so the tally guard was reading the list its own arms
    were made of and all six single edits that drop a name from it
    survived both self-tests ([R85] suggestion, round 7 on PR #428). Drop
    a name now and this arm fails, whatever the rest agree on."""
    from gen_toc import HEAD_RE
    plenty = {name: [None] * MIN_ARMS for name in ARM_FAMILIES}
    whole = MIN_ARMS * len(ARM_FAMILIES)
    short = {name: arms for name, arms in plenty.items() if name != "tag"}
    here = Path(__file__)
    return [
        ("the family names are the seven the runner scores, spelled here "
         "and not read from the constant the guard reads", "",
         lambda t: ARM_FAMILIES == ("walk", "tag", "guard", "heading",
                                    "predecessor", "provenance",
                                    "refusal")),
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
    ] + _class_guard_arms()


def _class_guard_arms() -> list[tuple[str, str, object]]:
    """The guard family's round-9 half: the class table, the refusal set,
    the walk roots and the site enumerator itself. The first three are
    spelled in this module rather than read from what they hold, for the
    reason the family list was ([R85] suggestion, round 7): a table read
    by its own arms holds nothing."""
    return [
        ("the renderer's classes are the ones spelled here, and not read "
         "from the table the walk reads", "",
         lambda t: CLASSES == _CLASSES_SPELLED),
        ("the refused characters are exactly Python's whitespace less the "
         "space, the tab and the line feed", "",
         lambda t: set(REFUSED) == {chr(c) for c in range(0x110000)
                                    if chr(c).isspace()} - set(" \t\n")),
        ("the walk roots are the two functions the walk answers through",
         "", lambda t: WALK_ROOTS == ("blocks", "line_kinds")),
        # The renderer's two NAME lists, spelled here for the same reason
        # the classes are: the enumeration derives one mutant per name and
        # per character of every name, and no page family could ever carry
        # a fixture for each. One arm holds all of them, in both
        # directions, and it is the arm that fails when `search` is
        # written for `source` ([R86] F1 R9, round 9 on PR #428).
        ("the type-1 names are the renderer's four", "",
         lambda t: RAW_HTML_TAGS == ("pre", "script", "style", "textarea")),
        ("the type-6 names are the renderer's own list, which carries "
         "`source` and not `search`", "",
         lambda t: HTML_BLOCK_TAGS == _TYPE_6_SPELLED),
        ("the shipped walk carries no decision site of its own", "",
         lambda t: _class_guards(Path(gen_toc_file()).read_text())[1] == []),
        ("the shipped walk carries decision sites in both kinds", "",
         lambda t: {site.split(": ")[1] for site in _class_guards(
             Path(gen_toc_file()).read_text())[0]} == {"single source",
                                                       "refusal"}),
        ("a class spelled inline in an expression is refused", "",
         lambda t: len(_notes(pattern='"[ \\t]+"')) == 1),
        ("so is a blank quantified in one", "",
         lambda t: len(_notes(pattern='" +"')) == 1),
        ("so is a refused character in one", "",
         lambda t: len(_notes(pattern='"\u00a0"')) == 1),
        ("so is Python's digit class", "",
         lambda t: len(_notes(pattern=r'"\\d"')) == 1),
        ("so is a class inline in a string the expression interpolates",
         "", lambda t: len(_class_guards(
             "import re\nA = \"[ ]\"\nX = re.compile(A)\n"
             "def line_kinds(line):\n    return blocks(line)\n"
             "def blocks(line):\n    return X.match(line)\n")[1]) == 1),
        ("a class read from the table by name is not", "",
         lambda t: _notes(pattern='_cc("blank") + "+"') == []),
        ("a strip with a class of its own is refused", "",
         lambda t: len(_notes(body='return line.strip(" ")')) == 1),
        ("so is asking Python what a character is", "",
         lambda t: len(_notes(body="return line.isspace()")) == 1),
        ("a strip from the table is a single-sourced site", "",
         lambda t: _kinds(body='return line.strip(CLASSES["blank"])')
         == "single source single source"),
        ("a bare strip is a refusal site, not a refused one", "",
         lambda t: _kinds(body="return line.strip()")
         == "refusal single source"),
        ("and so is Python's whitespace class", "",
         lambda t: _kinds(pattern=r'"\\s"') == "refusal"),
        ("a decision the walk reaches through another function is in the "
         "enumeration", "",
         lambda t: _kinds(body="return helper(line)") .count("refusal") == 0
         and len(_class_guards(_guard_source("return helper(line)")
                               + "def helper(line):\n"
                                 "    return line.strip()\n")[0]) == 2),
        ("a decision the walk never calls is not", "",
         lambda t: len(_class_guards(
             _guard_source() + "def elsewhere(line):\n"
                               "    return line.strip()\n")[0]) == 1),
        ("a walk root that is no function of the module is named", "",
         lambda t: len(_class_guards("x = 1\n")[1]) == len(WALK_ROOTS)),
        # The guard's own two lists, held the way every other list here is:
        # spelled in this module and exercised one member at a time, so
        # dropping a name from either fails an arm rather than quietly
        # narrowing what the guard refuses ([R85] suggestion, round 7).
        ("every Python character test the guard names is refused", "",
         lambda t: all(len(_notes(body=f"return line.{test}()")) == 1
                       for test in ("isspace", "isalpha", "isdigit",
                                    "isalnum", "isnumeric", "isdecimal",
                                    "isupper", "islower", "istitle",
                                    "isascii"))),
        ("every strip the guard names is a site of its own", "",
         lambda t: all(_kinds(body=f"return line.{strip}()")
                       == "refusal single source"
                       for strip in ("strip", "lstrip", "rstrip", "split"))),
    ]


def gen_toc_file() -> str:
    """The generator's own path, for the arms that read its source."""
    import gen_toc
    return gen_toc.__file__


def refusal_arms() -> list[tuple[str, str, object]]:
    """What the walk REFUSES to read, and what a page carrying one gets.

    The second honest answer a decision site can give, and the only thing
    holding the positions this round does not single-source (the fence and
    type-1 closers of #440) and the ones nobody has found yet. A page
    carrying a character at which Python's whitespace and the renderer's
    disagree is named with its line, its column and its code point, and
    obtains no provenance, so no label copied from it can be exempt.
    """
    page = _ARM_PAGE
    return [
        ("no page of spaces and tabs is refused", "",
         lambda t: refusals("# H\n\n\t \n## A\n") == []),
        ("every refused character is refused, with its line and column",
         "", lambda t: all(refusals(f"x\ny{char}") == [(2, 2, char)]
                           for char in REFUSED)),
        ("a carriage return is one of them", "",
         lambda t: refusals("a\rb") == [(1, 2, "\r")]),
        ("the note names the page, the line, the column and the character",
         "", lambda t: refusal_notes("docs/x.md", "a\n b\u00a0c")[0].startswith(
             "docs/x.md:2: U+00A0 at column 3 ")),
        ("a page carrying one obtains no provenance",
         page.replace("Body.", "Body.\u2003", 1),
         lambda t: generated_block(t) is None),
        ("the same page without it does", page,
         lambda t: generated_block(t) is not None),
        ("nor does one whose Contents block carries one",
         page.replace("What beta holds.", "What\u00a0beta holds.", 1),
         lambda t: generated_block(t) is None),
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

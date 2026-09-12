#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Per-page annotated table of contents: generate, refresh, and gate.

Why this exists. The corpus is 157 pages and 885 sections, several past 600
lines, and a bare list of headings barely helps a reader landing on one, so
each entry carries a sentence saying what you get there. The split of
ownership is the point: THIS SCRIPT owns which sections exist, their order,
their nesting and their anchors, all read off the page so it cannot drift; A
HUMAN owns the description, the part that carries judgement. Descriptions
survive regeneration, keyed by anchor and copied forward, so a renamed
heading gets a fresh one rather than a stale sentence.

Anchors follow GitHub's algorithm (lowercase; drop everything that is not
alphanumeric, space or hyphen; spaces to hyphens; `-1`, `-2` on collision).
`--verify-anchors` checks it against every `file.md#fragment` link in the
tree, the only independent evidence we have that it is right.

Usage:
    python3 scripts/gen_toc.py --check           # gate (exit 1 on drift/missing)
    python3 scripts/gen_toc.py --write           # insert/refresh every TOC
    python3 scripts/gen_toc.py --write PATH...   # just these pages
    python3 scripts/gen_toc.py --verify-anchors  # anchor algorithm vs real links
    python3 scripts/gen_toc.py --sites           # the walk's decision sites
"""
import ast
import re
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

TOC_HEAD = "## Contents"
#: what the generator writes when it has no description yet. The gate REFUSES
#: this, so a freshly generated TOC is not mistakable for a finished one.
TODO = "TODO describe this section"

#: A page with fewer than this many top-level sections gets no TOC.
MIN_SECTIONS = 3

#: When `##` is thin but `###` carries the real structure (REGISTER_MAP.md
#: is 3 and 25), the TOC nests one level deeper.
NEST_WHEN_H2_BELOW = 5
NEST_WHEN_H3_ATLEAST = 8

#: The arm families `gen_toc_cases` carries, and a FLOOR under the total.
#: Nothing pinned an arm count, so a family dropped from the runner's
#: import printed a smaller total and exited 0 ([R86] suggestion, round 6
#: on PR #428). The floor rises with the corpus.
ARM_FAMILIES = ("walk", "tag", "guard", "heading", "predecessor",
                "provenance", "refusal")
MIN_ARMS = 267

#: Pages that are deliberately TOC-free, with the reason.
SKIP = {
    "README.md":       "landing page - it IS a table of contents",
    "docs/README.md":  "documentation index - it IS a table of contents",
}

#: THE RENDERER'S CHARACTER CLASSES, and the ONLY place this file spells
#: one. Every expression below is built from these bodies BY NAME, and
#: `_class_guards()` enumerates the walk's decision sites off this
#: module's syntax tree and refuses one that spells a class of its own.
#: Rounds 1 to 8 each closed a position a review had named - `\s` for a
#: blank line, `[ \t]` for the renderer's padding, `(\S)` for an item's
#: first content character, four SPACES for four columns - and every round
#: found another ([R85] F1 and F2, [R86] F1 and F2, round 9 on PR #428).
#: Each body is what the RENDERER was measured to accept AT THE POSITION
#: that reads it, and the case tables spell every body again, so narrowing
#: or widening one fails an arm. `blank` is CommonMark 2.1's "spaces or
#: tabs"; `indent` is the space alone, indentation being counted in
#: COLUMNS (`_indent_columns`); `delimiter blank` is the wider padding
#: GFM's delimiter-row scanner takes.
_BLANK = " \t"
CLASSES = {
    "blank": _BLANK,
    "indent": " ",
    "tag blank": _BLANK + "\v\f",
    "tag tail": _BLANK + "\f",
    "delimiter blank": _BLANK + "\v\f",
    "tag name": "A-Za-z",
    "tag name rest": "A-Za-z0-9-",
    "attribute name": "A-Za-z_:",
    "attribute name rest": "A-Za-z0-9_.:-",
    "unquoted value stop": _BLANK + "\v\f\"'=<>`",
    "single-quoted value stop": "'",
    "double-quoted value stop": '"',
    "footnote label stop": _BLANK + "\\]\x00\r\n",
    "ordinal": "0-9",
    "bullet": "-+*",
    "cell stop": "|",
}
#: The characters at which PYTHON'S notion of whitespace and the
#: renderer's disagree: everything `str.isspace()` accepts but the space,
#: the tab and the line feed. A page carrying one is REFUSED rather than
#: walked (`refusals()`), which holds every position this file does not
#: read the renderer's class at, the fence and type-1 closers #440
#: carries among them. An arm derives the set from the Unicode database.
REFUSED = ("\v\f\r\x1c\x1d\x1e\x1f\x85\xa0\u1680\u2000\u2001\u2002"
           "\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028"
           "\u2029\u202f\u205f\u3000")
#: The two functions the walk answers through. `_class_guards()` follows
#: the calls out of these to the decision sites; the case tables spell the
#: pair again, so renaming one fails an arm instead of emptying the
#: enumeration.
WALK_ROOTS = ("blocks", "line_kinds")
#: `str` predicates that answer with Python's notion of a character rather
#: than the renderer's. No decision of the walk may ask one.
_PYTHON_CLASSES = ("isspace", "isalpha", "isdigit", "isalnum", "isnumeric",
                   "isdecimal", "isupper", "islower", "istitle", "isascii")
_STRIPS = ("strip", "lstrip", "rstrip")


def _cc(name: str, negate: bool = False) -> str:
    """One class of `CLASSES` as regular-expression text."""
    return "[%s%s]" % ("^" if negate else "", CLASSES[name])


#: A page written by a generator must not be hand-edited: the next run
#: discards whatever was added. Both spellings this tree uses are matched,
#: `do not hand-edit` and a bare bold **GENERATED**; missing either made
#: `gen_module_matrix.py --check` report a page STALE.
GENERATED_RE = re.compile(
    r"auto-?generated|generated file|generated by|generated script"
    r"|regenerate with|do not hand-?edit|do not edit|\*\*GENERATED\b", re.I)
GENERATED_SCAN_LINES = 12

#: A fence delimiter line: at most three columns of indentation, a run of
#: three or more backticks or tildes, then the rest of the line. What the
#: run and the rest MEAN depends on the block already open, which is why
#: `blocks()` and not this expression decides it: a fence closes only on
#: the SAME character, at least as long, with nothing but blanks after
#: it, and a backtick opener's info string carries no backtick.
FENCE_RE = re.compile(r"^%s{0,3}(`{3,}|~{3,})(.*)$" % _cc("indent"))
#: An ATX heading and its text, the optional closing sequence of hashes
#: dropped as CommonMark 4.2 drops it ([R86] suggestion, round 4 on PR
#: #428): a RUN of hashes with a blank before it and nothing but blanks
#: after it, so `## Old ## bar` is the text `Old ## bar` and `## Old#` is
#: `Old#`, as the renderer shows both ([R86] F2, round 5). Every blank
#: here is the renderer's, so a heading whose hashes a TAB follows is
#: listed and a run of hashes closes one only when blanks alone follow
#: ([R85] F1(c), round 9).
HEAD_RE = re.compile(r"^(#{1,6})%s+(.*?)(?:%s+#+)?%s*$"
                     % (_cc("blank"), _cc("blank"), _cc("blank")))
#: Four COLUMNS of indentation start an indented code block, which renders
#: as code. Such a run cannot interrupt a paragraph but follows any block
#: that closed (CommonMark 4.4: `# Heading` then `    foo`), so it opens
#: only while no paragraph is open and no container holds the line ([R85]
#: F1, round 3 on PR #428, where it began only after a blank line).
INDENT_CODE_COLUMNS = 4
#: CommonMark's type-1 raw HTML block: its content is not parsed as
#: Markdown and it survives blank lines, so a Contents block inside one
#: renders as literal text ([R0] and [R10] round 5 on PR #384). It ends at
#: its closing tag. The name is followed by a blank, `>` or the END OF THE
#: LINE: reading `/` as one of those made `<pre/>` a type-1 block where
#: the renderer reads a type-7 tag, and leaving the line end out made
#: `<pre` ending a line no block at all ([R85] round 9 on PR #428).
RAW_HTML_TAGS = ("pre", "script", "style", "textarea")
RAW_HTML_OPEN_RE = re.compile(r"^%s{0,3}<(%s)(?:%s|>|$)"
                              % (_cc("indent"), "|".join(RAW_HTML_TAGS),
                                 _cc("blank")), re.IGNORECASE)
#: CommonMark's type-6 raw HTML block: a block-level tag on its own line
#: opens it and a BLANK LINE closes it, and nothing inside is parsed as
#: Markdown, so a `## Head` between `<div>` and `</div>` with no blank
#: line renders as text and its label is no evidence of an anchor ([R0]
#: and [R10] round 7 on PR #384). The LIST is the RENDERER's, CommonMark
#: 0.29's and not the latest edition's: it carries `source` and not
#: `search`. The other way round, `<source>` was a type-7 block that may
#: not interrupt a paragraph where the renderer interrupts it, and
#: `<search>` a type-6 block that does where it does not ([R86] F1 R9,
#: round 9 on PR #428).
HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col"
    "|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure"
    "|footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html"
    "|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup"
    "|option|p|param|section|source|summary|table|tbody|td|tfoot|th|thead"
    "|title|tr|track|ul")
HTML_BLOCK_OPEN_RE = re.compile(r"^%s{0,3}</?(?:%s)(?:%s|/?>|$)"
                                % (_cc("indent"), HTML_BLOCK_TAGS,
                                   _cc("blank")), re.IGNORECASE)
#: CommonMark's type-7 raw HTML block: ONE complete open or closing tag of
#: any other name (`<span>`, `<b>`, `<custom-tag>`, `</b>`), alone on its
#: line, opens it, and a blank line closes it exactly as a type-6 block.
#: The tag grammar is the specification's: a name is an ASCII letter then
#: letters, digits or hyphens; an attribute has an XML name and an
#: optional unquoted, single-quoted or double-quoted value. Unlike type 6
#: it may not interrupt a paragraph, so `_opens()` reads it only while no
#: paragraph is open ([R85] F1 and [R86] F1, round 1 on PR #428; the
#: footnote definition from [R86] F1, round 2). A type-1 name is read
#: first and never reaches here (#413). WHITESPACE is two classes here,
#: `tag blank` inside the tag and `tag tail` after the closing angle
#: bracket ([R86] F1 and [R85] F1, round 7).
_HTML_TAG_NAME = r"%s%s*" % (_cc("tag name"), _cc("tag name rest"))
_HTML_ATTRIBUTE = (r"(?:%s+%s%s*(?:%s*=%s*(?:%s+|'%s*'|\"%s*\"))?)"
                   % (_cc("tag blank"), _cc("attribute name"),
                      _cc("attribute name rest"), _cc("tag blank"),
                      _cc("tag blank"), _cc("unquoted value stop", True),
                      _cc("single-quoted value stop", True),
                      _cc("double-quoted value stop", True)))
HTML_TAG_LINE_RE = re.compile(
    r"^%s{0,3}(?:<%s%s*%s*/?>|</%s%s*>)%s*$"
    % (_cc("indent"), _HTML_TAG_NAME, _HTML_ATTRIBUTE, _cc("tag blank"),
       _HTML_TAG_NAME, _cc("tag blank"), _cc("tag tail")))
#: Whether a paragraph is open, for the one block that may not interrupt
#: one. NO_PARAGRAPH: none is, and the next plain line starts one.
#: PARAGRAPH: a top-level paragraph is open. HELD: a list item, a block
#: quote or a table holds the plain lines that follow (CommonMark's lazy
#: continuation, GFM's rows without a pipe), so none is open and a plain
#: line starts none; a blank line or an interrupting block ends the hold.
NO_PARAGRAPH, PARAGRAPH, HELD = "no paragraph", "paragraph", "held"
#: CommonMark's ATX opener, not `HEAD_RE`: an indented or empty heading
#: ends a paragraph even though `headings()` lists neither.
ATX_HEADING_RE = re.compile(r"^%s{0,3}#{1,6}(?:%s|$)"
                            % (_cc("indent"), _cc("blank")))
THEMATIC_BREAK_RE = re.compile(
    r"^%s{0,3}(?:(?:\*%s*){3,}|(?:-%s*){3,}|(?:_%s*){3,})$"
    % (_cc("indent"), _cc("blank"), _cc("blank"), _cc("blank")))
SETEXT_UNDERLINE_RE = re.compile(r"^%s{0,3}(?:=+|-+)%s*$"
                                 % (_cc("indent"), _cc("blank")))
BLOCK_QUOTE_RE = re.compile(r"^%s{0,3}>" % _cc("indent"))
#: A list item: group 1 is the ordinal (None for a bullet), group 2 the
#: first character of its content (None when the item is empty).
#: Interrupting a paragraph takes content and, when ordered, the ordinal 1.
LIST_ITEM_RE = re.compile(
    r"^%s{0,3}(?:%s|(%s{1,9})[.)])(?:%s+(%s)|%s*$)"
    % (_cc("indent"), _cc("bullet"), _cc("ordinal"), _cc("blank"),
       _cc("blank", True), _cc("blank")))
#: GFM's table delimiter row, which makes the paragraph line above it a
#: header row: cells of hyphens with optional colons, separated by pipes,
#: a leading and a trailing pipe optional (GFM 0.29 section 4.10), so
#: `:-:`, `:---`, `---:` and `:-` are one-cell rows. A pipeless row of
#: hyphens alone is a setext underline or a thematic break, both read
#: before it. It makes a table only when its cells number the header row's
#: (`_table_cells`, [R86] F1 round 2 on PR #428), and only at three
#: columns of indentation or fewer ([R85] F2, round 3).
TABLE_DELIMITER_RE = re.compile(
    r"^%s{0,3}(?:\|%s*)?:?-+:?%s*(?:\|%s*:?-+:?%s*)*\|?%s*$"
    % ((_cc("indent"),) + (_cc("delimiter blank"),) * 5))
#: One cell of a GFM table row, anything up to a pipe with a backslash
#: escaping the character after it; then the pipe that ends the cell and
#: the blanks after it.
TABLE_CELL_RE = re.compile(r"(?:\\\||%s)*" % _cc("cell stop", True))
TABLE_CELL_END_RE = re.compile(r"\|%s*" % _cc("blank"))
#: GFM's footnote definition (`[^1]: note`): `[^`, a label, then `]:`,
#: indented at most three columns. It is outside the 0.29 specification
#: text; the renderer reads it as a container like a list item, so it
#: interrupts a paragraph, holds the plain lines after it, and a lone tag
#: under it opens a type-7 block ([R86] F1, round 2 on PR #428). The
#: label's own class is the renderer's ([R86] F1 R5, round 9).
FOOTNOTE_DEFINITION_RE = re.compile(
    r"^%s{0,3}\[\^%s+\]:"
    % (_cc("indent"), _cc("footnote label stop", True)))
COMMENT_OPEN, COMMENT_CLOSE = "<!--", "-->"
#: What a line is, for every reader in this repository. The names are what a
#: finding calls the line, so they read as English in a message.
TEXT, FENCE, COMMENT, CODE, HTML = ("prose line", "fenced line",
                                    "commented line", "indented code line",
                                    "raw HTML line")


def _indent_columns(line: str) -> int:
    """How many COLUMNS of indentation a line carries, tab stops of four.

    CommonMark 2.2 expands a tab to the next multiple of four - its own
    second example of an indented code block is two spaces and a tab - so
    one to three spaces then a tab is four columns and the line is code.
    Counting CHARACTERS read ` \tcode` as paragraph text, and a lone tag
    under it continued a paragraph the renderer had closed ([R85] F2(d),
    [R86] F1 R8, round 9 on PR #428).
    """
    columns = 0
    for char in line:
        if char not in CLASSES["blank"]:
            break
        columns += 4 - columns % 4 if char == "\t" else 1
    return columns


def refusals(text: str) -> list[tuple[int, int, str]]:
    """Every position this walk REFUSES to read: (line, column, character),
    the second of the two honest answers a decision here can give. Where
    the walk reads the renderer's own class it answers (`CLASSES`); where
    it does not - the fence and type-1 closers #440 carries, and whatever
    a later reader finds that this round did not - it must not answer at
    all, and this is what stops it. Every character at which Python's
    notion of whitespace and the renderer's disagree is REFUSED, named
    with its page, line, column and code point, and the page obtains no
    provenance and so no exemption. There are 26 and no page in the corpus
    carries one. THE LINE MODEL puts the carriage return among them: a
    line here is what `text.split("\n")` gives, so a CR lands inside a
    line where the renderer ends one. Both shipped readers translate line
    endings first - `Path.read_text()` in the generator, git in text mode
    in the gate - which is the real reason that residue could not reach
    the exemption, and not the one round 8 gave ([R85] and [R86]
    suggestion, round 9).
    """
    return [(n, col, char)
            for n, line in enumerate(text.split("\n"), 1)
            for col, char in enumerate(line, 1) if char in REFUSED]


def refusal_notes(name: str, text: str) -> list[str]:
    """One message per refused position, naming the page and the character."""
    return [f"{name}:{n}: U+{ord(char):04X} at column {col} is neither a "
            f"space nor a tab, so this walk does not read the page (use a "
            f"space or a tab)" for n, col, char in refusals(text)]


def blocks(text: str) -> list[str]:
    """What every line of ``text`` is: TEXT, FENCE, COMMENT, CODE or HTML.

    ONE walk, and the only one in this repository that decides which lines
    are NAVIGATION: a gate that re-derived it disagreed with this
    generator about which lines are headings, five review rounds running
    on PR #384. THREE other gates carry a fence and comment toggle of
    their own for a different question (`docs_check.py` a wording
    deny-list, `check_feature_status.py` status tables, `check_doc_style.py`
    the sentence-length limits in its `prose_blocks()`); none decides what
    a line IS ([R86] suggestion, round 6 on PR #428, which named two; the
    third from [R85], round 7). It is a single state machine, so the block
    already open decides what a delimiter means ([R0] round 5 F3). The
    three kinds of raw HTML block are stated where each is spelled above:
    type 1 ends at its closing tag and survives blank lines, types 6 and 7
    end at the first BLANK line, and type 7 alone may not interrupt a
    paragraph. None parses its content as Markdown, so a heading inside
    any of them is text.

    WHAT THIS WALK ANSWERS FOR. Its domain is a page of ATX headings and
    the blocks above, read FLAT and from column 0, and inside it every
    rule is the one the RENDERER applies and not the one the
    specification's prose reads: every character class tested here comes
    from `CLASSES`, measured at the position that reads it, and
    `_class_guards()` refuses a decision that spells a class of its own.
    OUTSIDE that domain it does not answer at all: a page carrying a
    character at which Python's notion of whitespace and the renderer's
    disagree is REFUSED and named rather than walked (`refusals()`), and
    obtains no provenance and so no exemption. A line mixing commented and
    visible text is labelled by the block it STARTS in, which can withhold
    a heading but never invent one.

    CONTAINERS ARE FLAT, and indentation is counted in COLUMNS from column
    0 (`_indent_columns`, CommonMark 2.2's tab stops of four). Three
    residues follow, all carried by #437. Two WITHHOLD a heading the page
    renders, which a contributor sees at once because the generated list
    then omits the section: a block quote or list-item line holds the
    plain lines after it as that container's paragraph whatever the
    container held, and a line indented into a container's content column
    is read as this walk's own indentation, so a tag at four columns
    inside an item opens no block and a plain line at four columns is
    code. The third runs the other way: after a BLANK line inside a list
    item, a plain line at the item's content column (one to three columns)
    is a fresh top-level paragraph here where the renderer holds it inside
    the item, so a lone tag on the next line interrupts nothing the
    renderer has open, the renderer opens a block and reads the heading
    inside it as text, and this walk KEEPS it. That is the ESCAPE
    direction, and a label mirroring such a heading would be exempt. The
    test is the content column and not indentation as such, and telling a
    container's own paragraph from a top-level one is a change to the
    state model rather than a rule ([R86] F1, round 5 on PR #428; the
    columns R8, round 9).
    """
    out, state, delim, tag, prev, para = [], TEXT, "", "", "", NO_PARAGRAPH
    for line in text.split("\n"):
        if state in (FENCE, COMMENT, HTML):
            out.append(state)
            state, delim, tag = _still_open(line, state, delim, tag)
        else:
            label, state, delim, tag = _opens(line, para, state)
            out.append(label)
        para, prev = _paragraph_after(line, out[-1], para, prev), line
    return out


def _table_cells(row: str) -> int:
    """How many cells a GFM table row carries, counted as the renderer
    counts them: one leading pipe is skipped, a pipe ends a cell unless a
    backslash stands immediately before it, and a trailing pipe closes the
    last cell, so `| a |`, `a` and `||` are one cell each and a lone `|`
    is none. That scanner takes the LONGEST match, in which a backslash
    before a pipe always escapes it, so `a\\|b` is one cell where reading
    the pair as an escaped backslash made it two ([R86] F1 R7, round 9)."""
    rest = row.strip(CLASSES["blank"])
    if rest.startswith("|"):
        rest = rest[1:].lstrip(CLASSES["blank"])
    cells = 0
    while rest:
        cell = TABLE_CELL_RE.match(rest).end()
        end = TABLE_CELL_END_RE.match(rest, cell)
        cells += 1
        rest = rest[end.end() if end else cell:]
    return cells


def _paragraph_after(line: str, label: str, para: str, prev: str) -> str:
    """The paragraph state after a line, from the line's own label, its
    text, the state before it and the line before it.

    Only a plain TEXT line starts or continues a paragraph. A heading, a
    thematic break or a setext underline ends one and starts none; a list
    item, a block quote, a footnote definition or a table delimiter row
    starts a HOLD, which a plain line continues; an ordered item not
    numbered 1, or an empty item, continues the paragraph instead ([R85]
    F1 and [R86] F1, round 1 on PR #428). A delimiter row makes a table of
    `prev` only when the two carry the same number of cells (round 2).
    """
    if label != TEXT or not line.strip(CLASSES["blank"]) \
            or ATX_HEADING_RE.match(line) \
            or THEMATIC_BREAK_RE.match(line) \
            or (para == PARAGRAPH and SETEXT_UNDERLINE_RE.match(line)):
        return NO_PARAGRAPH
    item = LIST_ITEM_RE.match(line)
    interrupts = bool(item and item.group(2) and int(item.group(1) or 1) == 1)
    if BLOCK_QUOTE_RE.match(line) or FOOTNOTE_DEFINITION_RE.match(line) \
            or (item and (para != PARAGRAPH or interrupts)):
        return HELD
    if para == PARAGRAPH and TABLE_DELIMITER_RE.match(line) \
            and _table_cells(line) == _table_cells(prev):
        return HELD
    return HELD if para == HELD else PARAGRAPH


def _comment_after(line: str, inside: bool) -> bool:
    """Whether a comment is open AFTER this line, reading EVERY delimiter on
    it in order.

    One `-->` is not the end of the story: `<!-- first --> <!-- second`
    closes one and opens another, and reading only the first delimiter
    left the second span classified as text, which handed a block inside
    it the exemption ([R0] round 6 on PR #384). A comment is also the only
    block that can open after visible text.
    """
    scan = line
    while scan:
        if inside:
            at = scan.find(COMMENT_CLOSE)
            if at < 0:
                return True
            scan, inside = scan[at + len(COMMENT_CLOSE):], False
        else:
            at = scan.find(COMMENT_OPEN)
            if at < 0:
                return False
            scan, inside = scan[at + len(COMMENT_OPEN):], True
    return inside


def _still_open(line: str, state: str, delim: str,
                tag: str) -> tuple[str, str, str]:
    """The state after a line INSIDE a fence, comment or raw HTML block.
    Only that block's own closer is read, which is the whole precedence
    rule: nothing else on the line means anything while it is open."""
    if state == COMMENT:
        return (COMMENT if _comment_after(line, True) else TEXT), "", ""
    if state == HTML:
        if not tag:                     # type 6: a blank line ends it
            return (TEXT if not line.strip(CLASSES["blank"])
                    else HTML), "", tag
        return ((TEXT if re.search(r"</%s\s*>" % tag, line, re.IGNORECASE)
                 else HTML), "", tag)
    m = FENCE_RE.match(line)         # closes on the SAME character, a run
    if m and m.group(1)[0] == delim[0] and len(m.group(1)) >= len(delim) \
            and not m.group(2).strip():  # at least as long, nothing after it
        return TEXT, "", ""
    return FENCE, delim, ""


def _opens(line: str, para: str, state: str) -> tuple[str, str, str, str]:
    """(what this line is, the state after it, fence delimiter, HTML tag)
    for a line that no block encloses. The order is CommonMark's: an
    indented code run swallows the line before any delimiter is read; a
    type-1 tag is read before the type-7 grammar; a comment opening after
    visible text leaves THIS line ordinary. `para` gates the two blocks
    that may not interrupt a paragraph."""
    if state == CODE and (not line.strip(CLASSES["blank"])
                          or _indent_columns(line) >= INDENT_CODE_COLUMNS):
        return CODE, CODE, "", ""      # the run continues across blank lines
    if _indent_columns(line) >= INDENT_CODE_COLUMNS and para == NO_PARAGRAPH:
        return CODE, CODE, "", ""
    m = FENCE_RE.match(line)
    if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
        return FENCE, FENCE, m.group(1), ""
    html = RAW_HTML_OPEN_RE.match(line)
    if html:
        tag = html.group(1)
        closed = re.search(r"</%s\s*>" % tag, line, re.IGNORECASE)
        return HTML, (TEXT if closed else HTML), "", tag
    if HTML_BLOCK_OPEN_RE.match(line) or (para != PARAGRAPH
                                          and HTML_TAG_LINE_RE.match(line)):
        # Types 6 and 7 carry no tag here: the blank line, not a closing
        # tag, is what ends them. A lone `<span>` under paragraph text is
        # that paragraph's continuation, not a block, so the line stays
        # TEXT; under anything else it opens the block.
        return HTML, HTML, "", ""
    if COMMENT_OPEN in line:
        after = COMMENT if _comment_after(line, False) else TEXT
        starts = line.lstrip(CLASSES["blank"]).startswith(COMMENT_OPEN)
        return (COMMENT if starts else TEXT), after, "", ""
    return TEXT, TEXT, "", ""


def line_kinds(text: str) -> list[str]:
    """`blocks()`, refined for the lines that are ordinary Markdown text: a
    heading, a table row, or prose. This is what a finding names, and it is
    the owner's answer rather than a second reader's."""
    out = []
    for line, kind in zip(text.split("\n"), blocks(text)):
        if kind != TEXT:
            out.append(kind)
        elif HEAD_RE.match(line):
            out.append("heading")
        elif line.lstrip(CLASSES["blank"]).startswith("|"):
            out.append("table row")
        else:
            out.append(TEXT)
    return out


#: One Contents entry as this script writes it: the label, the anchor, the
#: separator (U+2014 on the pages that predate the em-dash rule, `--` on
#: every block written since) and the description. check_em_dash.py reads
#: entries with this expression, so the gate and the generator cannot
#: disagree on what an entry is. Indentation is bounded at three, which
#: still renders as a list item ([R0] round 4 on PR #384).
TOC_ENTRY_RE = re.compile(
    r"%s{0,3}-%s+(?:\*\*)?\[([^\]]*)\]\(#([^)]*)\)(?:\*\*)?"
    r"%s*(\u2014|--)%s*(.*)"
    % ((_cc("indent"),) + (_cc("blank"),) * 3))


def anchor(text: str, seen: dict[str, int]) -> str:
    """GitHub's heading-anchor algorithm."""
    a = text.strip().lower()
    a = re.sub(r"[^\w\- ]", "", a, flags=re.UNICODE)  # \w keeps digits/underscore
    a = a.replace(" ", "-")
    n = seen.get(a, 0)
    seen[a] = n + 1
    return a if n == 0 else f"{a}-{n}"


def strip_md(text: str) -> str:
    """Heading text as a reader sees it: no backticks, no link syntax, no bold."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    return text.strip()


def label(text: str) -> str:
    """strip_md, then make it safe as the text of a **bold** link.

    A heading like ``## 2. Per-module HDL pages (`hdl/**/doc/*.md`)`` keeps
    a literal `**` once the backticks come off, closing the entry's bold
    early, so any surviving asterisk is escaped."""
    return strip_md(text).replace("*", r"\*")


def headings(text: str) -> list[tuple[int, str, str]]:
    """(level, raw_text, anchor) for every heading that renders as one.

    A heading inside a fence, an indented code block, an HTML comment or a
    raw HTML block renders as text, so it is no heading and its label no
    evidence of an anchor ([R0] round 5 F2 on PR #384). Anchors are
    numbered over ALL headings, GitHub counting collisions page-wide."""
    seen, out = {}, []
    for line, kind in zip(text.split("\n"), blocks(text)):
        if kind != TEXT:
            continue
        m = HEAD_RE.match(line)
        if m:
            lvl, raw = len(m.group(1)), m.group(2)
            out.append((lvl, raw, anchor(strip_md(raw), seen)))
    return out


def plan(text: str) -> list[tuple[int, str, str]] | None:
    """Which headings belong in this page's TOC, or None if it gets none."""
    hs = headings(text)
    h2 = [h for h in hs if h[0] == 2 and h[1].strip() != TOC_HEAD[3:]]
    h3 = [h for h in hs if h[0] == 3]
    if len(h2) < MIN_SECTIONS:
        return None
    nest = len(h2) < NEST_WHEN_H2_BELOW and len(h3) >= NEST_WHEN_H3_ATLEAST
    want = {2, 3} if nest else {2}
    return [h for h in hs if h[0] in want and h[1].strip() != TOC_HEAD[3:]]


def existing(
        text: str) -> tuple[dict[str, str], int | None, int | None, str | None]:
    """Descriptions keyed by anchor, the TOC span, and its separator. The
    span is located through `blocks()`, so a `## Contents` heading inside
    a fence, a comment, an indented code block or a raw HTML block is an
    example and not this page's own."""
    lines, kinds = text.split("\n"), blocks(text)
    start = next((i for i, l in enumerate(lines)
                  if kinds[i] == TEXT and l.strip() == TOC_HEAD), None)
    if start is None:
        return {}, None, None, None
    end = start + 1
    while end < len(lines) and not (kinds[end] == TEXT
                                    and lines[end].startswith("## ")):
        end += 1
    desc, separator = {}, None
    for i in range(start, end):
        m = TOC_ENTRY_RE.match(lines[i]) if kinds[i] == TEXT else None
        if m:
            desc[m.group(2)] = m.group(4).strip()
            if separator is None:
                separator = m.group(3)
    return desc, start, end, separator


def render(items: list[tuple[int, str, str]], desc: dict[str, str],
           separator: str) -> list[str]:
    """The Contents block itself, with each surviving description put
    back. A heading with no description carried forward gets `TODO`, which
    the gate refuses: the sentence after the separator is a human's."""
    out = [TOC_HEAD, ""]
    for lvl, raw, anc in items:
        lab = label(raw)
        d = desc.get(anc, TODO)
        if lvl == 2:
            out.append(f"- **[{lab}](#{anc})** {separator} {d}")
        else:
            out.append(f"  - [{lab}](#{anc}) {separator} {d}")
    out.append("")
    return out


def apply(path: Path, text: str) -> str | None:
    """Return the page with its TOC inserted/refreshed, or None if unchanged."""
    items = plan(text)
    desc, start, end, separator = existing(text)
    lines = text.split("\n")

    if items is None:
        if start is None:
            return None
        del lines[start:end]                      # too few sections now
        return "\n".join(lines)

    # A page keeps the separator it has; a block written for the first time
    # uses `--`, the only separator the em-dash rule lets a change add.
    block = render(items, desc, separator or "--")
    if start is not None:
        lines[start:end] = block
    else:
        first = next((i for i, l in enumerate(lines) if l.startswith("## ")), None)
        if first is None:
            return None
        lines[first:first] = block
    new = "\n".join(lines)
    return None if new == text else new


def owns(relpath: str, text: str) -> bool:
    """Whether THIS script writes the Contents block of ``relpath``. One
    population, read by `pages()` and by every tool that asks about
    provenance: the historical tree is frozen, `SKIP` names the two
    indexes that ARE tables of contents, and a generator-owned page
    belongs to its generator ([R0] round 6 on PR #384)."""
    if relpath.startswith("docs/history/v1/") or relpath in SKIP:
        return False
    head = "\n".join(text.split("\n")[:GENERATED_SCAN_LINES])
    return not GENERATED_RE.search(head)


def generated_block(text: str,
                    relpath: str | None = None) -> tuple[int, list[str]] | None:
    """Where this page's Contents block starts and the exact lines THIS
    SCRIPT renders for it, or None when the page carries no block, its
    block is not what this script would write, or the walk refuses it.
    It is the provenance answer other tools ask for: a line is generated
    navigation if it is byte-identical to the line here, at its own
    position, on a page this script owns and READS -- a page outside
    `owns()` answers None, and so does one the walk refuses
    (`refusals()`). `check_em_dash.py` exempts a copied heading label only
    on that answer, so no second reader decides what navigation is; five
    rounds of PR #384 showed that it decides differently.
    """
    if refusals(text) or (relpath is not None and not owns(relpath, text)):
        return None
    items = plan(text)
    desc, start, end, separator = existing(text)
    if items is None or start is None:
        return None
    block = render(items, desc, separator or "--")
    if text.split("\n")[start:end] != block:
        return None
    return start, block


def pages() -> Iterator[Path]:
    """Every hand-written .md the gate has an opinion about.

    The corpus comes from `git ls-files`, THE INDEX, which can name a page
    that is not on disk. That raised FileNotFoundError and took the whole
    run down, and a gate that dies on one path reports NOTHING about the
    other hundred-odd, so a vanished page is SKIPPED and NAMED.
    """
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "-z", "*.md"],
                         capture_output=True, text=True, check=True).stdout
    for p in sorted(filter(None, out.split("\0"))):
        md = REPO / p
        if not md.is_file():
            if owns(p, ""):
                print(f"  GONE  {p}: tracked in the index but not on disk "
                      f"(stage the deletion, or restore the file) - skipped")
            continue
        if owns(p, md.read_text()):
            yield md


def verify_anchors() -> int:
    """Check the anchor algorithm against `file.md#frag` links people wrote."""
    ok = bad = 0
    for md in pages():
        for m in re.finditer(r"\]\(([^)\s]+\.md)#([^)\s]+)\)", md.read_text()):
            tgt = (md.parent / m.group(1))
            if not tgt.exists():
                continue
            if m.group(2) in {a for _, _, a in headings(tgt.read_text())}:
                ok += 1
            else:
                bad += 1
                print(f"  MISS {md.relative_to(REPO)} -> {m.group(1)}#{m.group(2)}")
    print(f"anchor check: {ok} existing cross-page fragment links reproduced"
          f"{f', {bad} NOT reproduced' if bad else ''}")
    return 1 if bad else 0


def _tally_guards(families: dict[str, list], scored: int) -> list[str]:
    """What the ARM TALLY must satisfy before a single arm is scored: every
    family present and carrying arms, at least `MIN_ARMS` in all, and
    every arm the tables hold reaching the runner. A family dropped from
    the runner's import printed `PASS (94/94 arm(s))` and exited 0 ([R86]
    suggestion, round 6 on PR #428); `scored` is what it really reads.
    """
    bad = [f"arm family {name!r} is missing or empty"
           for name in ARM_FAMILIES if not families.get(name)]
    total = sum(len(arms) for arms in families.values())
    if total < MIN_ARMS:
        bad.append(f"{total} arm(s) in all, below the {MIN_ARMS} recorded")
    if scored != total:
        bad.append(f"{scored} arm(s) reach the runner of the {total} the "
                   "tables hold")
    return bad


def _owner_guards(name: str, source: str, values: dict) -> list[str]:
    """That the case-table module carries no classification of its OWN: it
    imports no expression engine and holds no compiled expression, so a
    rule cannot migrate out of this script, which #413 names as the one
    owner of block classification ([R85] suggestion, round 6 on PR #428).
    The imports are read off its syntax tree and the compiled expressions
    off its values, so prose naming the engine cannot trip it and an alias
    cannot slip past it. WHAT IT CANNOT SEE: those two and nothing else,
    so plain string methods, an engine reached through `importlib` and a
    third-party engine all pass it, each measured ([R85] suggestion, round
    7). It is a structural proxy; the proof is that the runner and every
    arm live here.
    """
    bad, imported = [], set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    if re.__name__ in imported:
        bad.append(f"{name} imports the expression engine: every expression "
                   "that classifies a line belongs beside the walk")
    compiled = sorted(n for n, v in values.items() if isinstance(v, re.Pattern))
    if compiled:
        bad.append(f"{name} holds compiled expression(s) {compiled}: "
                   "the same rule")
    return bad


def _pattern_texts(node: ast.AST, assign: dict,
                   seen: frozenset = frozenset()) -> Iterator[str]:
    """Every string an expression reaches, `_cc()`'s own argument apart:
    that call IS the named source, read by name."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "_cc":
        return
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
    elif isinstance(node, ast.Name) and node.id in assign \
            and node.id not in seen:
        yield from _pattern_texts(assign[node.id], assign, seen | {node.id})
    for child in ast.iter_child_nodes(node):
        yield from _pattern_texts(child, assign, seen)


def _class_guards(source: str) -> tuple[list[str], list[str]]:
    r"""Every DECISION SITE of the walk, classified, and what is wrong with
    one that is neither honest kind.

    A site is a position that reads a character class: a compiled
    expression of this module, or a call inside the walk that hands a
    string to a scanner. They are ENUMERATED from the syntax tree, out
    from `WALK_ROOTS`, not from a list kept by hand, so a decision added
    later is in the enumeration whether or not anyone remembers it. Each
    is one of two things, and `--sites` prints which. SINGLE SOURCE:
    every class it reads comes from `CLASSES`, whose bodies the case
    tables spell again, so narrowing or widening one fails an arm.
    REFUSAL: it spells Python's own whitespace, whose excess over the
    renderer's blank is exactly `REFUSED`, so a page that could tell the
    two apart is refused before the site is asked. Anything else is a
    note and the self-test fails: a
    class spelled inline, Python's `\d`, `\w`, `\W` or `\D`, a
    `str.is*()` test, or a strip with a class of its own ([R85] F1 and F2,
    [R86] F1 and F2, round 9 on PR #428). WHAT IT CANNOT SEE: it reads
    this module's syntax tree, so a class reached through `getattr`, built
    at run time or imported passes it, as does a rule the walk never
    calls. It is a structural proxy; the refusal holds the rest.
    """
    tree = ast.parse(source)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assign = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign)
              for t in n.targets if isinstance(t, ast.Name)}
    notes = [f"the walk root {root!r} is no function of this module"
             for root in WALK_ROOTS if root not in funcs]
    walk, queue = set(), [root for root in WALK_ROOTS if root in funcs]
    while queue:                        # the calls out of the roots
        name = queue.pop()
        if name not in walk:
            walk.add(name)
            queue += [c.func.id for c in ast.walk(funcs[name])
                      if isinstance(c, ast.Call)
                      and isinstance(c.func, ast.Name) and c.func.id in funcs]

    def judge(where: str, node: ast.AST) -> str:
        """One site, classified; a class of its own is a note."""
        kind = "single source"
        for text in _pattern_texts(node, assign):
            kind = "refusal" if r"\s" in text or r"\S" in text else kind
            notes.extend(
                f"{where} spells {own}, which is Python's class and not "
                "the renderer's"
                for own in (r"\d", r"\w", r"\W", r"\D") if own in text)
            for i, char in enumerate(text):
                if char in REFUSED or (char in CLASSES["blank"] and not (
                        text[i - 1:i].isalnum()
                        and text[i + 1:i + 2].isalnum())):
                    notes.append(f"{where} spells a blank of its own; every "
                                 "class the walk reads is in CLASSES")
                    break
        return f"{where}: {kind}"

    sites = [judge(name, node) for name, node in assign.items()
             if any(isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Attribute)
                    and c.func.attr == "compile" for c in ast.walk(node))]
    for name in walk:
        for call in ast.walk(funcs[name]):
            if not isinstance(call, ast.Call) \
                    or not isinstance(call.func, ast.Attribute):
                continue
            attr, where = call.func.attr, f"{name}() {call.func.attr}()"
            if attr in _PYTHON_CLASSES:
                notes.append(f"{where} asks Python what a character is; the "
                             "renderer's answer is in CLASSES")
            elif (attr in _STRIPS or attr == "split") and not call.args:
                sites.append(f"{where}: refusal")
            elif attr in _STRIPS:
                arg = call.args[0]
                if isinstance(arg, ast.Subscript) \
                        and isinstance(arg.value, ast.Name) \
                        and arg.value.id == "CLASSES":
                    sites.append(f"{where}: single source")
                else:
                    notes.append(f"{where} strips a class of its own")
            elif isinstance(call.func.value, ast.Name) \
                    and call.func.value.id == "re" and call.args:
                sites.append(judge(where, call.args[0]))
    return sorted(sites), notes


def selftest() -> int:
    """Run every arm family. 0 when every one holds.

    The RUNNER and every rule it scores live here because this script owns
    the walk: a gate that carried its own copy refused a legitimate page
    and exempted three that render nothing ([R0] rounds 4 and 5 on PR
    #384). Only the case TABLES sit next door ([R86] suggestion, round 5
    on PR #428). The import is inside this body because that module
    imports this one, and this module is registered under its own NAME
    first, or the families would be scored against a second copy of the
    walk ([R85] suggestion, round 6).
    """
    sys.modules.setdefault("gen_toc", sys.modules[__name__])
    import gen_toc_cases as cases
    families = {"walk": cases.walk_arms(), "tag": cases.tag_arms(),
                "guard": cases.guard_arms(), "heading": cases.heading_arms(),
                "predecessor": cases.predecessor_arms(),
                "provenance": cases.provenance_arms(),
                "refusal": cases.refusal_arms()}
    on_walk = families["walk"] + families["tag"]
    on_page = (families["provenance"] + families["predecessor"]
               + families["heading"] + families["guard"]
               + families["refusal"])
    arms = len(on_walk) + len(on_page)
    src = Path(cases.__file__)
    notes = (_tally_guards(families, arms)
             + _owner_guards(src.name, src.read_text(), vars(cases))
             + _class_guards(Path(__file__).read_text())[1])
    for note in notes:
        print(f"  GUARD {note}")
    problems = len(notes)
    for name, page, holds in on_walk:
        if not holds(blocks(page)):
            problems += 1
            print(f"  FAIL [{name}]: {blocks(page)}")
    for name, page, holds in on_page:
        if not holds(page):
            problems += 1
            print(f"  FAIL [{name}]")
    print(f"TOC selftest: {'PASS' if not problems else 'FAIL'} "
          f"({arms - problems}/{arms} arm(s))")
    return 1 if problems else 0


def main() -> int:
    """Run one arm: `--sites`, `--verify-anchors`, `--write`, or the gate.

    `--check` is the default: it separates a page with no contents list
    from one whose list has drifted, and refuses a page the walk does not
    read, because the three need different work from whoever reads it.
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}

    if "--selftest" in flags:
        return selftest()
    if "--verify-anchors" in flags:
        return verify_anchors()
    if "--sites" in flags:
        print("\n".join(_class_guards(Path(__file__).read_text())[0]))
        return 0

    targets = [Path(a).resolve() for a in args] if args else list(pages())
    changed, missing, stale, refused = [], [], [], []

    for md in targets:
        text = md.read_text()
        rel = md.relative_to(REPO)
        notes = refusal_notes(str(rel), text)
        for note in notes:
            print(f"  REFUSED   {note}")
        if notes:
            refused.append(rel)
            continue
        new = apply(md, text)
        if "--write" in flags:
            if new is not None:
                md.write_text(new)
                changed.append(rel)
            continue
        # --check
        if new is not None:
            (missing if TOC_HEAD not in text else stale).append(rel)
        elif TOC_HEAD in text:
            desc, _, _, _ = existing(text)
            if any(d == TODO or not d for d in desc.values()):
                stale.append(rel)

    if "--write" in flags:
        todo = sum(1 for md in targets
                   if TOC_HEAD in md.read_text()
                   for d in existing(md.read_text())[0].values() if d == TODO)
        print(f"TOC: {len(changed)} page(s) written"
              f"{f', {todo} description(s) still {TODO!r}' if todo else ''}")
        return 0

    if missing or stale or refused:
        for p in missing:
            print(f"  NO TOC    {p}  (>= {MIN_SECTIONS} sections and no '{TOC_HEAD}')")
        for p in stale:
            print(f"  TOC DRIFT {p}  (headings changed, or a description is "
                  f"still {TODO!r})")
        print(f"\n{len(missing) + len(stale) + len(refused)} page(s) need "
              f"attention. Run: python3 scripts/gen_toc.py --write <page>\n"
              f"then WRITE the description for each entry - the generator "
              f"cannot, and a list that only repeats the headings is not "
              f"worth the space it takes.")
        return 1

    n = sum(1 for md in targets if TOC_HEAD in md.read_text())
    print(f"TOC gate: OK ({n} page(s) carry an annotated contents list, "
          f"{len(targets) - n} below the {MIN_SECTIONS}-section threshold)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

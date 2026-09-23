#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The walk's CONTAINER LAYER: block quotes, list items and footnote definitions.

WHICH MODULE IS WHICH. The walk is three modules (`gen_toc.WALK_MODULES`).
`gen_toc.py` holds every expression and character class, the leaf machine
and `blocks()`, which labels each line. THIS module holds no expression and
no class: it applies CommonMark 0.31.2 sections 5.1 and 5.2, and GFM's
footnote definitions, to decide which container each line belongs to, and
runs the leaf machine of `gen_toc` on the line's content INSIDE those
containers. `gen_toc_html.py` reads what this layer marks raw. The class
guard enumerates all three; the tables beside the walk hold no rule.

Why it exists (#437). A flat walk read a container's own paragraph as a
top-level one, and every targeted fix exposed another base error that the
first had hidden: a tag under a nested block counted as paragraph text, and
a fence opened inside an item outlived the item (R237-2 F1). The renderer's
rules are structural, so this layer is too:

- A container continues on a line that carries its prefix: `>` (then one
  optional column) for a quote; the item's content column for an item, or a
  blank line once the item holds anything; four columns, or an empty line,
  for a footnote definition. Columns are counted with tab stops of four.
- A line that leaves containers unmatched still continues them LAZILY when
  the deepest open block is a paragraph and the line starts no block.
- A lone type-7 tag meets `Scope.gate`: the paragraph state of the deepest
  block the line matches, so it continues a paragraph only when that block
  is the open paragraph (`_opens`, CommonMark 4.6).
- `Scope.held_by` names the containers open after each line, so `blocks()`
  ends a fence, raw HTML block or comment when the container it opened in
  ends.

It changes no label on its own: `blocks()` keeps the column-0 labels and
asks this layer only the three questions above. Setext headings and headings
inside containers stay outside the listing domain (#437 family two).
"""
from dataclasses import dataclass
from re import Match
from typing import NamedTuple

from gen_toc import (ATX_HEADING_RE, BLOCK_QUOTE_RE, CLASSES, COMMENT, FENCE,
                     FOOTNOTE_DEFINITION_RE, HELD, HTML, LIST_ITEM_RE,
                     NO_PARAGRAPH, PARAGRAPH, RAW_3_5_RE, TEXT,
                     THEMATIC_BREAK_RE, _opens, _paragraph_after, _still_open)

QUOTE, ITEM, NOTE = "block quote", "list item", "footnote definition"
#: The end conditions of raw HTML blocks of types 3 to 5, by `RAW_3_5_RE`
#: group: a processing instruction, a CDATA section, a declaration.
RAW_ENDS = ("?>", "]]>", ">")
TAB_STOP = 4
#: The leaf state a new container starts with: (state, fence delimiter, HTML
#: tag or raw end, paragraph state, previous content line).
_FRESH = (TEXT, "", "", NO_PARAGRAPH, "")


class Scope(NamedTuple):
    """What the container layer answers for one line."""

    gate: str               # the paragraph state a lone type-7 tag meets
    held_by: tuple          # serials of the containers open after it; 0 is the page
    plain: bool             # paragraph text, with no container opened or closed
    cont: bool              # it continues the paragraph open before it
    raw: str | None         # its content, when GitHub emits it as raw HTML
    text: str | None        # its content, when GitHub parses it as inline text


@dataclass
class _Box:
    """One open container: its kind, the columns its content starts after,
    whether it holds anything yet, and a serial no other container reuses."""

    kind: str
    need: int
    filled: bool
    serial: int


def _lead(text: str) -> int:
    """Columns of indentation on a line whose tabs are already expanded."""
    return len(text) - len(text.lstrip(CLASSES["indent"]))


def _blank(text: str) -> bool:
    """Whether a tab-expanded line carries nothing but indentation."""
    return not text.strip(CLASSES["indent"])


def _quote_content(text: str, at: int) -> int:
    """Where a block quote's content starts, given where its `>` is: after
    the marker and one optional column (CommonMark 5.1)."""
    at += 1
    return at + 1 if text[at:at + 1] == " " else at


def _continues(box: _Box, text: str, at: int) -> int | None:
    """Where this container's content starts on the line, or None when the
    line does not carry its prefix (CommonMark 5.1 and 5.2; GFM footnotes)."""
    rest = text[at:]
    lead = _lead(rest)
    if box.kind == QUOTE:
        if lead > 3 or rest[lead:lead + 1] != ">":
            return None
        return _quote_content(text, at + lead)
    if box.kind == ITEM:
        if lead >= box.need:
            return at + box.need
        return len(text) if box.filled and _blank(rest) else None
    if lead >= TAB_STOP:
        return at + TAB_STOP
    return at if not text else None


def _lazy(rem: str) -> bool:
    """Whether a line that leaves containers unmatched continues their open
    paragraph: it is not blank and starts no block (CommonMark 5.1)."""
    if _blank(rem):
        return False
    if _lead(rem) >= TAB_STOP:
        return True
    starts = (ATX_HEADING_RE, THEMATIC_BREAK_RE, BLOCK_QUOTE_RE,
              FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE, RAW_3_5_RE)
    return _opens(rem, HELD, TEXT)[0] == TEXT and not any(
        start.match(rem) for start in starts)


def _content_column(rem: str, item: Match[str]) -> int:
    """The columns a list item's content starts after: the marker, then one
    to four columns of padding, or one when the item is empty or its padding
    is wider (its content is then indented code)."""
    end = _lead(rem) + (len(item.group(1)) + 1 if item.group(1) else 1)
    padding = _lead(rem[end:])
    return end + 1 if not item.group(2) or padding > TAB_STOP else end + padding


@dataclass
class _Walk:
    """The open containers, the one open leaf block and the last serial. The
    functions below are module-level so the class guard follows every call."""

    stack: list
    leaf: tuple = _FRESH
    serial: int = 0


def _step(walk: _Walk, line: str) -> Scope:
    """One line: match the open containers, then continue lazily, or close
    the unmatched ones, open new ones and read the leaf."""
    text = line.expandtabs(TAB_STOP)
    at, matched = 0, 0
    for box in walk.stack:
        start = _continues(box, text, at)
        if start is None:
            break
        at, matched = start, matched + 1
    rem, closed = text[at:], matched < len(walk.stack)
    state, _, _, para, _ = walk.leaf
    if not closed and state in (FENCE, COMMENT, HTML):
        return _inside(walk, rem)
    if closed:
        if state == TEXT and para == PARAGRAPH and _lazy(rem):
            return _scope(walk, HELD, (True, True), rem, TEXT)
        del walk.stack[matched:]
        walk.leaf = _FRESH
    rem, opened = _open(walk, rem)
    return _leaf_line(walk, rem, closed or opened)


def _inside(walk: _Walk, rem: str) -> Scope:
    """A line inside an open fence, comment or raw HTML block."""
    state, delim, tag, _, _ = walk.leaf
    label = state
    if tag in RAW_ENDS:
        state, tag = (TEXT, "") if tag in rem else (HTML, tag)
    else:
        state, delim, tag = _still_open(rem, state, delim, tag)
    walk.leaf = (state, delim, tag, NO_PARAGRAPH, rem)
    return _scope(walk, NO_PARAGRAPH, (False, False), rem, label)


def _open(walk: _Walk, rem: str) -> tuple[str, bool]:
    """Open every container this line starts, outermost first. A list item
    interrupts an open paragraph only with content and, when ordered, the
    ordinal 1, so a setext underline is none; a thematic break is no item."""
    para, opened = walk.leaf[3], False
    while not _blank(rem) and _lead(rem) < TAB_STOP:
        lead, item = _lead(rem), LIST_ITEM_RE.match(rem)
        interrupting = para == PARAGRAPH and not opened
        if BLOCK_QUOTE_RE.match(rem):
            rem = rem[_quote_content(rem, lead):]
            _push(walk, QUOTE, 0, True)
        elif THEMATIC_BREAK_RE.match(rem):
            break
        elif FOOTNOTE_DEFINITION_RE.match(rem):
            rem = rem[FOOTNOTE_DEFINITION_RE.match(rem).end():]
            _push(walk, NOTE, TAB_STOP, True)
        elif item and not (interrupting and not (
                item.group(2) and int(item.group(1) or 1) == 1)):
            need = _content_column(rem, item)
            rem = rem[need:] if item.group(2) else ""
            _push(walk, ITEM, need, bool(item.group(2)))
        else:
            break
        opened = True
    if opened:
        walk.leaf = _FRESH
    return rem, opened


def _push(walk: _Walk, kind: str, need: int, filled: bool) -> None:
    """Open one container inside the innermost one."""
    walk.serial += 1
    walk.stack.append(_Box(kind, need, filled, walk.serial))


def _leaf_line(walk: _Walk, rem: str, changed: bool) -> Scope:
    """The leaf machine on the line's content inside its containers, after
    a container opened or closed on it or not. An inline comment starts no
    block; types 3 to 5 are raw until their end."""
    state, delim, tag, para, prev = walk.leaf
    if not _blank(rem):
        for box in walk.stack:
            box.filled = True
    label, state, delim, tag = _opens(rem, para, state)
    if state == COMMENT and (label == TEXT or _lead(rem) > 3):
        label, state = TEXT, TEXT
    raw = RAW_3_5_RE.match(rem) if (label, state) == (TEXT, TEXT) else None
    if raw:
        end = RAW_ENDS[0 if raw.group(1) else 1 if raw.group(2) else 2]
        label, state, tag = HTML, TEXT if end in rem[_lead(rem):] else HTML, end
    after = _paragraph_after(rem, label, para, prev)
    walk.leaf = (state, delim, tag, after, rem)
    plain = label == TEXT and after == PARAGRAPH and not changed
    return _scope(walk, para, (plain, plain and para == PARAGRAPH), rem, label)


def _scope(walk: _Walk, gate: str, flags: tuple[bool, bool], rem: str,
           label: str) -> Scope:
    """The answer for this line. Footnote content is neither raw nor inline
    here: GitHub renders it at the end of the page."""
    noted = any(box.kind == NOTE for box in walk.stack)
    raw = rem if label in (HTML, COMMENT) and not noted else None
    text = rem if label == TEXT and not _blank(rem) and not noted else None
    held = (0,) + tuple(box.serial for box in walk.stack)
    return Scope(gate, held, flags[0], flags[1], raw, text)


def container_lines(lines: list[str]) -> list[Scope]:
    """What the container layer answers for every line of a page."""
    walk = _Walk([])
    return [_step(walk, line) for line in lines]

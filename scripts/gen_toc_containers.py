#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The walk's CONTAINER LAYER: block quotes, list items and footnote definitions.

WHICH MODULE IS WHICH. The walk is two modules (`gen_toc.WALK_MODULES`).
`gen_toc.py` holds every expression and character class, the leaf machine
and `blocks()`, which labels each line. THIS module holds no expression and
no class: it applies CommonMark 0.31.2 sections 5.1 and 5.2, and GFM's
footnote definitions, to decide which container each line belongs to, and
runs the leaf machine of `gen_toc` on the line's content INSIDE those
containers. The class guard enumerates both; the tables beside the walk
hold no rule.

Why it exists (#437). A flat walk read a container's own paragraph as a
top-level one, and every targeted fix exposed another base error that the
first had hidden: a tag under a nested block counted as paragraph text, and
a fence opened inside an item outlived the item (R237-2 F1). The renderer's
rules are structural, so this layer is too:

- A container continues on a line that carries its prefix: `>` (then one
  optional column) for a quote; the item's content column for an item, or a
  blank line while the item holds a block; four columns, or an empty line,
  for a footnote definition. Columns are counted with tab stops of four. A
  nested container is a block its parent holds. A paragraph made only of
  link reference definitions is one only while it is open: the renderer
  drops it when it closes (CommonMark 4.7, R237-3 F2).
- A line that leaves containers unmatched still continues them LAZILY when
  the deepest open block is a paragraph and the line starts no block.
- A lone type-7 tag meets `Scope.gate`: the paragraph state of the deepest
  block the line matches, so it continues a paragraph only when that block
  is the open paragraph (`_opens`, CommonMark 4.6). A raw HTML block of
  types 3 to 5 holds no container and ends at its end marker, but
  `blocks()` labels its lines text (#413), so inside one the gate is None
  and `blocks()` answers with its own paragraph state, as the base did.
- `Scope.held_by` names the containers open after each line, so `blocks()`
  ends a fence or raw HTML block when the container it opened in ends.

It changes no label on its own: `blocks()` keeps the column-0 labels and
asks this layer only the two questions above. Setext headings and headings
inside containers stay outside the listing domain (#437 family two).
"""
from dataclasses import dataclass
from re import Match
from typing import NamedTuple

from gen_toc import (ATX_HEADING_RE, BLOCK_QUOTE_RE, CLASSES, COMMENT, FENCE,
                     FOOTNOTE_DEFINITION_RE, HELD, HTML, LINK_DEFINITION_RE,
                     LIST_ITEM_RE, NO_PARAGRAPH, PARAGRAPH, RAW_3_5_RE, TEXT,
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

    gate: str | None        # the paragraph state a lone type-7 tag meets
    held_by: tuple          # serials of the containers open after it; 0 is the page


@dataclass
class _Box:
    """One open container: its kind, the columns its content starts after,
    whether it holds a block yet, and a serial no other container reuses."""

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


def _continues(box: _Box, text: str, at: int, holds: bool) -> int | None:
    """Where this container's content starts on the line, or None when the
    line does not carry its prefix (CommonMark 5.1 and 5.2; GFM footnotes).
    `holds`: whether the container holds a block, an open paragraph too."""
    rest = text[at:]
    lead = _lead(rest)
    if box.kind == QUOTE:
        if lead > 3 or rest[lead:lead + 1] != ">":
            return None
        return _quote_content(text, at + lead)
    if box.kind == ITEM:
        if lead >= box.need:
            return at + box.need
        return len(text) if holds and _blank(rest) else None
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
    state, _, _, para, _ = walk.leaf
    for box in walk.stack:
        holds = box.filled or (box is walk.stack[-1] and para == PARAGRAPH)
        start = _continues(box, text, at, holds)
        if start is None:
            break
        at, matched = start, matched + 1
    rem, closed = text[at:], matched < len(walk.stack)
    if not closed and state in (FENCE, COMMENT, HTML):
        return _inside(walk, rem)
    if closed:
        if state == TEXT and para == PARAGRAPH and _lazy(rem):
            walk.stack[-1].filled = True
            return _scope(walk, HELD)
        del walk.stack[matched:]
        walk.leaf = _FRESH
    return _leaf_line(walk, _open(walk, rem))


def _inside(walk: _Walk, rem: str) -> Scope:
    """A line inside an open fence, comment or raw HTML block. `blocks()`
    labels the lines of types 3 to 5 text (#413), so there the gate is its
    own paragraph state, as at the base."""
    state, delim, tag, _, _ = walk.leaf
    raw_3_5 = tag in RAW_ENDS
    if raw_3_5:
        state, tag = (TEXT, "") if tag in rem else (HTML, tag)
    else:
        state, delim, tag = _still_open(rem, state, delim, tag)
    walk.leaf = (state, delim, tag, NO_PARAGRAPH, rem)
    return _scope(walk, None if raw_3_5 else NO_PARAGRAPH)


def _open(walk: _Walk, rem: str) -> str:
    """Open every container this line starts, outermost first. A list item
    interrupts an open paragraph only with content and, when ordered, the
    ordinal 1, so a setext underline is none; a thematic break is no item."""
    para, opened = walk.leaf[3], False
    while not _blank(rem) and _lead(rem) < TAB_STOP:
        lead, item = _lead(rem), LIST_ITEM_RE.match(rem)
        interrupting = para == PARAGRAPH and not opened
        if BLOCK_QUOTE_RE.match(rem):
            rem = rem[_quote_content(rem, lead):]
            _push(walk, QUOTE, 0)
        elif THEMATIC_BREAK_RE.match(rem):
            break
        elif FOOTNOTE_DEFINITION_RE.match(rem):
            rem = rem[FOOTNOTE_DEFINITION_RE.match(rem).end():]
            _push(walk, NOTE, TAB_STOP)
        elif item and not (interrupting and not (
                item.group(2) and int(item.group(1) or 1) == 1)):
            need = _content_column(rem, item)
            rem = rem[need:] if item.group(2) else ""
            _push(walk, ITEM, need)
        else:
            break
        opened = True
    if opened:
        walk.leaf = _FRESH
    return rem


def _push(walk: _Walk, kind: str, need: int) -> None:
    """Open one container inside the innermost one, which then holds it."""
    if walk.stack:
        walk.stack[-1].filled = True
    walk.serial += 1
    walk.stack.append(_Box(kind, need, False, walk.serial))


def _leaf_line(walk: _Walk, rem: str) -> Scope:
    """The leaf machine on the line's content inside its containers. An
    inline comment starts no block; types 3 to 5 are raw until their end. A
    line fills its container unless it is blank, or a link reference
    definition while the container holds only such a paragraph."""
    state, delim, tag, para, prev = walk.leaf
    label, state, delim, tag = _opens(rem, para, state)
    if state == COMMENT and (label == TEXT or _lead(rem) > 3):
        label, state = TEXT, TEXT
    raw = RAW_3_5_RE.match(rem) if (label, state) == (TEXT, TEXT) else None
    if raw:
        end = RAW_ENDS[0 if raw.group(1) else 1 if raw.group(2) else 2]
        label, state, tag = HTML, TEXT if end in rem[_lead(rem):] else HTML, end
    if walk.stack and not _blank(rem) and (
            walk.stack[-1].filled or label != TEXT
            or not LINK_DEFINITION_RE.match(rem)):
        walk.stack[-1].filled = True
    walk.leaf = (state, delim, tag, _paragraph_after(rem, label, para, prev), rem)
    return _scope(walk, para)


def _scope(walk: _Walk, gate: str | None) -> Scope:
    """The answer for this line: the gate, and the containers open after it."""
    return Scope(gate, (0,) + tuple(box.serial for box in walk.stack))


def container_lines(lines: list[str]) -> list[Scope]:
    """What the container layer answers for every line of a page."""
    walk = _Walk([])
    return [_step(walk, line) for line in lines]

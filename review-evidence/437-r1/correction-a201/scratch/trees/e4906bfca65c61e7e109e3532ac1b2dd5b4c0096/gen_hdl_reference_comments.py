#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Read `//!` documentation out of SystemVerilog text, without a parser.

This is the pure-text half of ``scripts/gen_hdl_reference.py``: a lexical
comment scanner and the four readers built on it.  It is kept apart because it
is the half that has no optional dependency -- nothing here imports `pyslang`,
touches the filesystem or raises a refusal, so it can be read, reasoned about
and exercised on a machine where the pinned parser is not installed.

``strip_comments`` is the one primitive: it blanks every comment while
preserving line and column numbers, so a caller can index the blanked text and
the raw text with the same offsets.  ``doc_comments`` uses exactly that to tell
a real `//!` from one inside a string literal, and the three readers above it
(``leading_docs``, ``declaration_docs``, ``item_description``) only ever ask
which contiguous block of those comments belongs to a given line.
"""

import re
from collections.abc import Sequence


def strip_comments(source: str) -> str:
    """Blank comments while preserving lines and quoted strings."""
    result = []
    index = 0
    state = "code"
    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""
        if state == "line":
            if char == "\n":
                result.append(char)
                state = "code"
            else:
                result.append(" ")
        elif state == "block":
            if char == "*" and following == "/":
                result.extend((" ", " "))
                index += 1
                state = "code"
            else:
                result.append("\n" if char == "\n" else " ")
        elif state == "string":
            result.append(char)
            if char == "\\" and following:
                result.append(following)
                index += 1
            elif char == '"':
                state = "code"
        elif char == "/" and following == "/":
            result.extend((" ", " "))
            index += 1
            state = "line"
        elif char == "/" and following == "*":
            result.extend((" ", " "))
            index += 1
            state = "block"
        else:
            result.append(char)
            if char == '"':
                state = "string"
        index += 1
    return "".join(result)


def doc_comments(source: str) -> dict[int, tuple[bool, str]]:
    """Map line numbers to documentation comments outside strings.

    Returns {line: (owns_line, text)} for every `//!` comment, where
    owns_line is True when no code precedes the comment on its line.
    """
    stripped = strip_comments(source)
    comments = {}
    for number, (raw, bare) in enumerate(
            zip(source.splitlines(), stripped.splitlines()), start=1):
        start = None
        for index in range(len(raw) - 1):
            if (raw[index:index + 2] == "//"
                    and bare[index:index + 2] == "  "):
                start = index
                break
        if start is None or raw[start:start + 3] != "//!":
            continue
        comments[number] = (not bare[:start].strip(),
                           raw[start + 3:].strip())
    return comments


def leading_docs(comments: dict[int, tuple[bool, str]], line: int) -> tuple[str, ...]:
    """Collect the contiguous documentation block above one line."""
    collected = []
    cursor = line - 1
    while cursor in comments and comments[cursor][0]:
        collected.append(comments[cursor][1])
        cursor -= 1
    return tuple(reversed(collected))


PREAMBLE_RE = re.compile(r"^(?:`.*|import\s[^;]*;)$")


def declaration_docs(comments: dict[int, tuple[bool, str]],
                     bare_lines: list[str], line: int) -> tuple[str, ...]:
    """Find the description block above one declaration.

    Blank lines, compiler directives, and package imports may
    separate the block; any other code ends the search.
    """
    cursor = line - 1
    while cursor >= 1:
        entry = comments.get(cursor)
        if entry is not None and entry[0]:
            return leading_docs(comments, cursor + 1)
        bare = bare_lines[cursor - 1].strip() if cursor <= len(bare_lines) else ""
        if bare and not PREAMBLE_RE.fullmatch(bare):
            return ()
        cursor -= 1
    return ()


def description_paragraphs(lines: Sequence[str]) -> tuple[str, ...]:
    """Join documentation lines into blank-line-split paragraphs."""
    paragraphs = []
    current = []
    for line in lines:
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return tuple(paragraphs)


def item_description(comments: dict[int, tuple[bool, str]],
                     first_line: int, name_line: int) -> str:
    """Prefer a same-line comment, then the block above the item."""
    trailing = comments.get(name_line)
    if trailing is not None and not trailing[0]:
        return trailing[1]
    above = leading_docs(comments, first_line)
    return " ".join(part for part in above if part)

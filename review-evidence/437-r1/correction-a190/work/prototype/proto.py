"""Prototype: container-aware block walk reusing gen_toc's leaf machine.

Scratch only. `blocks_b(text)` labels every line by the leaf machine applied to
the line's content inside its containers (CommonMark 5.1/5.2, GFM footnotes).
"""
import sys
sys.path.insert(0, "$LANES/437-container-paragraph-scopes/scripts")
import gen_toc as g
from gen_toc import (TEXT, FENCE, COMMENT, CODE, HTML, NO_PARAGRAPH, PARAGRAPH, HELD,
                     BLOCK_QUOTE_RE, FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE,
                     THEMATIC_BREAK_RE, SETEXT_UNDERLINE_RE, ATX_HEADING_RE,
                     _opens, _still_open, _paragraph_after)

QUOTE, ITEM, NOTE = "quote", "item", "note"


def _lead(s):
    return len(s) - len(s.lstrip(" "))


def _match(c, exp, i):
    """Whether open container c continues on this line, and where its content starts."""
    rest = exp[i:]
    lead = _lead(rest)
    blank = not rest.strip(" ")
    if c[0] == QUOTE:
        if not blank and lead <= 3 and rest[lead] == ">":
            j = i + lead + 1
            return True, j + 1 if exp[j:j + 1] == " " else j
        return False, i
    if c[0] == ITEM:
        if lead >= c[1] and not blank:
            return True, i + c[1]
        if blank and c[2]:
            return True, len(exp)
        return False, i
    if lead >= 4:           # GFM footnote definition: four columns, or an empty line
        return True, i + 4
    return (exp == ""), i


def _is_lazy(rem):
    """Whether a line that leaves containers unmatched continues their paragraph."""
    if not rem.strip(" "):
        return False
    label, state, _, _ = _opens(rem, HELD, TEXT)
    if label != TEXT:
        return False
    if ATX_HEADING_RE.match(rem) or THEMATIC_BREAK_RE.match(rem):
        return False
    if BLOCK_QUOTE_RE.match(rem) or FOOTNOTE_DEFINITION_RE.match(rem):
        return False
    if LIST_ITEM_RE.match(rem) and _lead(rem) <= 3:
        return False
    return True


def _open_item(rem, m):
    """(need, has_child, consumed) for a list item marker match m on rem."""
    lead = _lead(rem)
    if m.group(1):
        marker_end = lead + len(m.group(1)) + 1
    else:
        marker_end = lead + 1
    after = rem[marker_end:]
    spaces = _lead(after)
    if not after.strip(" ") or spaces > 4:
        need = marker_end + 1
    else:
        need = marker_end + spaces
    return need, bool(after.strip(" ")), min(need, len(rem))


def model(text):
    """Per line: (label, depth, lazy, raw, gate) from the container-aware walk."""
    out = []
    stack = []            # [kind, need, has_child]
    state, delim, tag, para, prev = TEXT, "", "", NO_PARAGRAPH, ""
    for line in text.split("\n"):
        exp = line.expandtabs(4)
        i, matched = 0, 0
        for c in stack:
            ok, j = _match(c, exp, i)
            if not ok:
                break
            i, matched = j, matched + 1
        rem = exp[i:]
        blank = not rem.strip(" ")
        if matched == len(stack) and state in (FENCE, COMMENT, HTML):
            label = state
            state, delim, tag = _still_open(rem, state, delim, tag)
            para = NO_PARAGRAPH
            out.append((label, len(stack), False, rem))
            prev = rem
            continue
        if matched < len(stack):
            if state == TEXT and para == PARAGRAPH and _is_lazy(rem):
                label, state, delim, tag = _opens(rem, HELD, TEXT)
                prev = rem
                out.append((label, len(stack), True, rem))
                continue
            del stack[matched:]
            state, delim, tag, para, prev = TEXT, "", "", NO_PARAGRAPH, ""
        opened = False
        while True:
            lead = _lead(rem)
            if not rem.strip(" ") or lead >= 4:
                break
            if BLOCK_QUOTE_RE.match(rem):
                j = lead + 1
                rem = rem[j + 1:] if rem[j:j + 1] == " " else rem[j:]
                stack.append([QUOTE, 0, True])
            elif THEMATIC_BREAK_RE.match(rem) or (
                    para == PARAGRAPH and not opened and SETEXT_UNDERLINE_RE.match(rem)):
                break
            elif FOOTNOTE_DEFINITION_RE.match(rem):
                rem = rem[FOOTNOTE_DEFINITION_RE.match(rem).end():]
                stack.append([NOTE, 4, True])
            else:
                m = LIST_ITEM_RE.match(rem)
                interrupts = bool(m and m.group(2) and int(m.group(1) or 1) == 1)
                if not m or (para == PARAGRAPH and not opened and not interrupts):
                    break
                need, has_child, consumed = _open_item(rem, m)
                rem = rem[consumed:] if has_child else ""
                stack.append([ITEM, need, has_child])
            opened = True
            state, delim, tag, para, prev = TEXT, "", "", NO_PARAGRAPH, ""
        if rem.strip(" "):
            for c in stack:
                if c[0] == ITEM:
                    c[2] = True
        label, state, delim, tag = _opens(rem, para, state)
        para = _paragraph_after(rem, label, para, prev)
        prev = rem
        out.append((label, len(stack), False, rem))
    return out


def blocks_b(text):
    return [row[0] for row in model(text)]


def headings_with(blocks_fn, text):
    seen, out = {}, []
    for line, kind in zip(text.split("\n"), blocks_fn(text)):
        if kind != TEXT:
            continue
        m = g.HEAD_RE.match(line)
        if m:
            lvl, raw = len(m.group(1)), m.group(2)
            out.append((lvl, raw, g.anchor(g.strip_md(raw), seen)))
    return out

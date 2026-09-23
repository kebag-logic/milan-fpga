"""Prototype A: base labels, container-aware gate, lifetime and rendered comment.

Scratch only.
"""
import re
import sys
sys.path.insert(0, "$LANES/437-container-paragraph-scopes/scripts")
import gen_toc as g
from gen_toc import (TEXT, FENCE, COMMENT, CODE, HTML, NO_PARAGRAPH, PARAGRAPH, HELD,
                     BLOCK_QUOTE_RE, FOOTNOTE_DEFINITION_RE, LIST_ITEM_RE,
                     THEMATIC_BREAK_RE, SETEXT_UNDERLINE_RE, ATX_HEADING_RE,
                     FENCE_RE, RAW_HTML_OPEN_RE, HTML_BLOCK_OPEN_RE, HTML_TAG_LINE_RE,
                     COMMENT_OPEN, INDENT_CODE_COLUMNS, CLASSES,
                     _still_open, _paragraph_after, _comment_after, _type_1_end, _indent_columns)

QUOTE, ITEM, NOTE = "quote", "item", "note"
_RAW_3_5_RE = re.compile(r"^ {0,3}<(?:(\?)|!\[CDATA\[|![A-Z])")


def _raw_3_5_end(rem, end):
    return end in rem


def _opens(line, para, state, gate=None):
    """gen_toc._opens with the type-7 gate separated from the code gate."""
    gate = para if gate is None else gate
    if state == CODE and (not line.strip(CLASSES["blank"])
                          or _indent_columns(line) >= INDENT_CODE_COLUMNS):
        return CODE, CODE, "", ""
    if _indent_columns(line) >= INDENT_CODE_COLUMNS and para == NO_PARAGRAPH:
        return CODE, CODE, "", ""
    m = FENCE_RE.match(line)
    if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
        return FENCE, FENCE, m.group(1), ""
    html = RAW_HTML_OPEN_RE.match(line)
    if html:
        tag = html.group(1)
        closed = _type_1_end(line)
        return HTML, (TEXT if closed else HTML), "", tag
    if HTML_BLOCK_OPEN_RE.match(line) or (gate != PARAGRAPH and HTML_TAG_LINE_RE.match(line)):
        return HTML, HTML, "", ""
    if COMMENT_OPEN in line:
        after = COMMENT if _comment_after(line, False) else TEXT
        starts = line.lstrip(CLASSES["blank"]).startswith(COMMENT_OPEN)
        return (COMMENT if starts else TEXT), after, "", ""
    return TEXT, TEXT, "", ""


def _lead(s):
    return len(s) - len(s.lstrip(" "))


def _match(c, exp, i):
    rest = exp[i:]
    lead = _lead(rest)
    blank = not rest.strip(" ")
    if c[0] == QUOTE:
        if not blank and lead <= 3 and rest[lead] == ">":
            j = i + lead + 1
            return True, j + 1 if exp[j:j + 1] == " " else j
        return False, i
    if c[0] == ITEM:
        if lead >= c[1]:
            return True, i + c[1]
        if blank and c[2]:
            return True, len(exp)
        return False, i
    if lead >= 4:
        return True, i + 4
    return (exp == ""), i


def _is_lazy(rem):
    if not rem.strip(" "):
        return False
    label, state, _, _ = _opens(rem, HELD, TEXT)
    if label != TEXT:
        return False
    if ATX_HEADING_RE.match(rem) or THEMATIC_BREAK_RE.match(rem):
        return False
    if BLOCK_QUOTE_RE.match(rem) or FOOTNOTE_DEFINITION_RE.match(rem) or LIST_ITEM_RE.match(rem):
        return False
    return True


def _open_item(rem, m):
    lead = _lead(rem)
    marker_end = lead + len(m.group(1)) + 1 if m.group(1) else lead + 1
    after = rem[marker_end:]
    spaces = _lead(after)
    need = marker_end + 1 if not after.strip(" ") or spaces > 4 else marker_end + spaces
    return need, bool(after.strip(" "))


def containers(text):
    """Per line: dict(gate, cont, stack, raw, inline, joins)."""
    out = []
    stack = []
    keep = []
    state, delim, tag, para, prev = TEXT, "", "", NO_PARAGRAPH, ""
    for line in text.split("\n"):
        keep.extend(stack)
        exp = line.expandtabs(4)
        i, matched = 0, 0
        for c in stack:
            ok, j = _match(c, exp, i)
            if not ok:
                break
            i, matched = j, matched + 1
        rem = exp[i:]
        depth0 = len(stack)
        was_para = para == PARAGRAPH and state == TEXT
        rec = {"gate": NO_PARAGRAPH, "cont": False, "raw": None, "inline": None, "plain": False}
        if matched == len(stack) and state in (FENCE, COMMENT, HTML) and tag in ("?>", ">", "]]>"):
            label = HTML
            state = TEXT if tag in rem else HTML
            tag = tag if state == HTML else ""
            para, prev = NO_PARAGRAPH, rem
        elif matched == len(stack) and state in (FENCE, COMMENT, HTML):
            label = state
            state, delim, tag = _still_open(rem, state, delim, tag)
            para, prev = NO_PARAGRAPH, rem
        elif matched < len(stack) and was_para and _is_lazy(rem):
            label, rec["gate"], rec["cont"], rec["plain"] = TEXT, HELD, True, True
            prev = rem
        else:
            if matched < len(stack):
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
                    need, has_child = _open_item(rem, m)
                    rem = rem[need:] if has_child else ""
                    stack.append([ITEM, need, has_child])
                opened = True
                state, delim, tag, para, prev = TEXT, "", "", NO_PARAGRAPH, ""
            if rem.strip(" "):
                for c in stack:
                    if c[0] == ITEM:
                        c[2] = True
            rec["gate"] = para
            label, state, delim, tag = _opens(rem, para, state)
            if state == COMMENT and (label == TEXT or _lead(rem) > 3):
                label, state = TEXT, TEXT          # an inline comment opens no block
            m35 = _RAW_3_5_RE.match(rem) if label == TEXT and state == TEXT else None
            if m35:
                end = "?>" if m35.group(1) else ("]]>" if rem.lstrip(" ").startswith("<![CDATA[") else ">")
                label = HTML
                closed = end in rem[m35.end():] if end != ">" else ">" in rem[m35.end():]
                state, tag = (TEXT, "") if closed else (HTML, end)
            before = para
            para = _paragraph_after(rem, label, para, prev)
            rec["cont"] = before == PARAGRAPH and label == TEXT and para == PARAGRAPH
            rec["plain"] = label == TEXT and para == PARAGRAPH and not opened and matched == depth0
            prev = rem
        in_note = any(c[0] == NOTE for c in stack)
        if label in (HTML, COMMENT) and not in_note:
            rec["raw"] = rem
        elif label == TEXT and rem.strip(" ") and not in_note:
            rec["inline"] = rem
        rec["stack"] = [id(c) for c in stack]
        rec["label"] = label
        out.append(rec)
    return out


# ---- rendered comment -------------------------------------------------------
_WS = " \t\n\f"
_FILTERED = ("title", "textarea", "style", "xmp", "iframe", "noembed", "noframes",
             "script", "plaintext")
_HTML_MARKUP_RE = re.compile(
    r"(?P<comment><!--)"
    r"|<!(?!--)[^>]*(?:>|\Z)"
    r"|<\?[^>]*(?:>|\Z)"
    r"|</(?![A-Za-z])[^>]*(?:>|\Z)"
    r"|</?(?P<name>[A-Za-z][^%(ws)s/>]*)"
    r"(?:[%(ws)s/]+|(?:=|[^%(ws)s/>=])[^%(ws)s/>=]*(?:[%(ws)s]*=[%(ws)s]*"
    r"(?:\"[^\"]*(?:\"|\Z)|'[^']*(?:'|\Z)|[^%(ws)s>]+)?)?)*(?:>|\Z)" % {"ws": _WS})
_HTML_COMMENT_END_RE = re.compile(r"--!?>")
_HTML_ABRUPT_RE = re.compile(r"-?>")


def rendered_after(raw, inside):
    """HTML's tokenizer over raw bytes GitHub emits verbatim: in a comment after them?"""
    at = 0
    while True:
        if inside:
            m = _HTML_COMMENT_END_RE.search(raw, at)
            if not m:
                return True
            at, inside = m.end(), False
            continue
        m = _HTML_MARKUP_RE.search(raw, at)
        if not m:
            return False
        if m.group("comment"):
            abrupt = _HTML_ABRUPT_RE.match(raw, m.end())
            at, inside = (abrupt.end(), False) if abrupt else (m.end(), True)
        elif m.group("name") and m.group("name").lower() in _FILTERED and (
                raw[m.end("name"):m.end("name") + 1] in tuple(_WS + ">")
                or raw[m.end("name"):m.end("name") + 2] == "/>"):
            at = m.start() + 1          # the tag filter escapes its `<`: the rest is text
        else:
            at = m.end()


# CommonMark inline raw HTML (section 6.6), code spans and escapes.
_S = r"(?:[ \t]+\n?[ \t]*|\n[ \t]*)"
_O = r"[ \t]*\n?[ \t]*"
_INLINE_RE = re.compile(
    r"\\[!-/:-@\[-`{-~]"
    r"|(?P<ticks>`+)"
    r"|(?P<html><[A-Za-z][A-Za-z0-9-]*"
    r"(?:" + _S + r"[A-Za-z_:][A-Za-z0-9_.:-]*(?:" + _O + "=" + _O +
    r"(?:[^ \t\n\"'=<>`]+|'[^']*'|\"[^\"]*\"))?)*" + _O + r"/?>"
    r"|</[A-Za-z][A-Za-z0-9-]*" + _O + r">"
    r"|<!-->|<!--->|<!--(?:(?!-->)[\s\S])*-->"
    r"|<\?(?:(?!\?>)[\s\S])*\?>"
    r"|<![A-Z]+[ \t\n]+[^>]*>"
    r"|<!\[CDATA\[(?:(?!\]\]>)[\s\S])*\]\]>)")


def inline_closes(text):
    """Whether inline raw HTML in this Markdown text carries a comment closer."""
    at = 0
    while True:
        m = _INLINE_RE.search(text, at)
        if not m:
            return False
        if m.group("ticks"):
            run = m.group("ticks")
            close = re.compile(r"(?<!`)%s(?!`)" % run).search(text, m.end())
            at = close.end() if close else m.end()
        elif m.group("html"):
            if _HTML_COMMENT_END_RE.search(m.group("html")):
                return True
            at = m.end()
        else:
            at = m.end()


def hidden_lines(recs):
    """Per line: whether GitHub's page hides it inside a comment left open."""
    out, inside, run, unit = [], False, [], []
    for rec in recs:
        if rec["raw"] is not None:
            if unit:
                inside = inside and not inline_closes("\n".join(unit))
                unit = []
            out.append(inside)
            run.append(rec["raw"])
            continue
        if run:
            inside, run = rendered_after("\n".join(run), inside), []
        if rec["inline"] is not None and rec["cont"] and unit:
            unit.append(rec["inline"])
            out.append(inside)
            continue
        if unit:
            inside = inside and not inline_closes("\n".join(unit))
        out.append(inside)
        unit = [rec["inline"]] if rec["inline"] is not None else []
    return out


def blocks_a(text):
    recs = containers(text)
    hidden = hidden_lines(recs)
    out, state, delim, tag, prev, para = [], TEXT, "", "", "", NO_PARAGRAPH
    owner, prose = [], False
    for line, rec, hide in zip(text.split("\n"), recs, hidden):
        if state in (FENCE, COMMENT, HTML) and (
                (owner and owner[-1] not in rec["stack"]) or (prose and not rec["plain"])):
            state = TEXT
        if state in (FENCE, COMMENT, HTML):
            out.append(state)
            state, delim, tag = _still_open(line, state, delim, tag)
        else:
            label, state, delim, tag = _opens(line, para, state, rec["gate"])
            out.append(label)
            owner, prose = rec["stack"], label == TEXT and state == COMMENT
        para, prev = _paragraph_after(line, out[-1], para, prev), line
        if hide and out[-1] == TEXT:
            out[-1] = COMMENT
    return out


def headings(text):
    seen, out = {}, []
    for line, kind in zip(text.split("\n"), blocks_a(text)):
        if kind != TEXT:
            continue
        m = g.HEAD_RE.match(line)
        if m:
            lvl, raw = len(m.group(1)), m.group(2)
            out.append((lvl, raw, g.anchor(g.strip_md(raw), seen)))
    return out

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The walk's HTML STAGE: where raw HTML leaves GitHub's page inside a comment.

WHICH MODULE IS WHICH. The walk is three modules (`gen_toc.WALK_MODULES`).
`gen_toc_containers.py` marks the lines GitHub emits verbatim as raw HTML and
the lines it parses as inline text. THIS module reads them the way the page
that reaches a reader is read: GitHub's renderer passes raw HTML through
(escaping the leading `<` of the tags GFM's tag filter names), and an HTML
parser then tokenizes the whole page. A `<!--` it meets in DATA state opens
a comment that hides everything after it, headings included, until a comment
closer: the #516 shapes, measured on #437. Its character classes come from
`gen_toc.CLASSES` by name, so the class guard reads them with the rest.

The model, HTML's tokenizer reduced to what decides a comment:

- In DATA, a start or end tag is skipped whole, a quoted attribute value
  included; `<!` not followed by `--`, `<?` and `</` not followed by a
  letter start a bogus comment that ends at the next `>` (CDATA outside
  foreign content is one); `<!--` opens a comment, and `<!-->` and `<!--->`
  close it again at once.
- In a comment, `-->` or `--!>` closes it.
- Markdown text escapes `<` and `>`, so it carries a closer only inside
  inline raw HTML (CommonMark 0.31.2 section 6.6, with the uppercase
  declaration name GitHub measured), never in a code span or after a
  backslash escape; it can open nothing, every inline comment being closed.
- Footnote content is not read: GitHub renders it at the end of the page.

What it does not model. Measured on #437: a raw run that ends inside a tag
or a bogus comment turns GitHub's next heading into text, and one that ends
inside a quoted value hides every later heading; this walk lists them, as
the base did (an escape). Unmeasured: foreign content's real CDATA, and a
DOCTYPE's quoted identifiers.
"""
import re

from gen_toc import ASCII_FOLD, _cc

#: GFM's tag filter: the leading `<` of these tags is escaped, so what
#: follows it is text to the tokenizer.
FILTERED_TAGS = ("title", "textarea", "style", "xmp", "iframe", "noembed",
                 "noframes", "script", "plaintext")
_SPACE = _cc("html space")
_HTML = {"s": _SPACE, "name": _cc("tag name"),
         "text": r"(?:(?!%s)[^/>])" % _SPACE}
#: One piece of markup in DATA state: a comment opener, a bogus comment, or
#: a start or end tag with its attributes (a value is quoted only after `=`).
HTML_MARKUP_RE = re.compile(
    r"(?P<comment><!--)|<!(?!--)[^>]*(?:>|\Z)|<\?[^>]*(?:>|\Z)"
    r"|</(?!%(name)s)[^>]*(?:>|\Z)"
    r"|</?%(name)s%(text)s*(?:(?:%(s)s|/)+|=?(?:(?!=)%(text)s)*(?:%(s)s*=%(s)s*"
    r"(?:\"[^\"]*(?:\"|\Z)|'[^']*(?:'|\Z)|(?:(?!%(s)s)[^>])*))?)*(?:>|\Z)"
    % _HTML)
HTML_FILTERED_RE = re.compile(r"</?(?:%s)(?=%s|/?>)" % (
    "|".join(FILTERED_TAGS), _SPACE), ASCII_FOLD)
HTML_COMMENT_END_RE = re.compile(r"--!?>")
HTML_ABRUPT_END_RE = re.compile(r"-?>")
_B = _cc("blank")
_NL = r"\n"
#: Whitespace in inline raw HTML: blanks and at most one line ending, each
#: spelled one way only so a long run cannot be split in two.
_INLINE = {"ws": r"(?:%s+(?:%s%s*)?|%s%s*)" % (_B, _NL, _B, _NL, _B),
           "opt": r"%s*(?:%s%s*)?" % (_B, _NL, _B),
           "tag": _cc("tag name") + _cc("tag name rest") + "*",
           "attr": _cc("attribute name") + _cc("attribute name rest") + "*",
           "bare": r"(?:(?!%s)%s)+" % (_NL, _cc("unquoted value stop", True)),
           "decl": _cc("declaration name"), "esc": _cc("escapable")}
#: Markdown text, left to right: a backslash escape, a backtick run, or one
#: inline raw HTML construct (CommonMark 0.31.2 section 6.6).
INLINE_HTML_RE = re.compile(
    r"\\%(esc)s|(?P<ticks>`+)|(?P<html><%(tag)s(?:%(ws)s%(attr)s(?:%(opt)s="
    r"%(opt)s(?:%(bare)s|'[^']*'|\"[^\"]*\"))?)*%(opt)s/?>|</%(tag)s%(opt)s>"
    r"|<!-->|<!--->|<!--(?:(?!-->).)*-->|<\?(?:(?!\?>).)*\?>"
    r"|<!%(decl)s+%(ws)s[^>]*>|<!\[CDATA\[(?:(?!\]\]>).)*\]\]>)" % _INLINE,
    re.DOTALL)
BACKTICKS_RE = re.compile(r"`+")


def rendered_after(raw: str, inside: bool) -> bool:
    """Whether HTML's tokenizer is inside a comment after these raw bytes,
    given whether it was before them."""
    at = 0
    while True:
        if inside:
            close = HTML_COMMENT_END_RE.search(raw, at)
            if not close:
                return True
            at, inside = close.end(), False
            continue
        mark = HTML_MARKUP_RE.search(raw, at)
        if not mark:
            return False
        if mark.group("comment"):
            abrupt = HTML_ABRUPT_END_RE.match(raw, mark.end())
            at, inside = (abrupt.end(), False) if abrupt else (mark.end(), True)
        elif HTML_FILTERED_RE.match(raw, mark.start()):
            at = mark.start() + 1
        else:
            at = mark.end()


def inline_closes(text: str) -> bool:
    """Whether Markdown text carries a comment closer GitHub emits, which
    only inline raw HTML can: a code span or an escape hides one."""
    at = 0
    while True:
        mark = INLINE_HTML_RE.search(text, at)
        if not mark:
            return False
        if mark.group("html") and HTML_COMMENT_END_RE.search(mark.group("html")):
            return True
        at = mark.end()
        if mark.group("ticks"):
            run = len(mark.group("ticks"))
            closer = next((m for m in BACKTICKS_RE.finditer(text, at)
                           if len(m.group()) == run), None)
            at = closer.end() if closer else at


def hidden_lines(scopes: list) -> list[bool]:
    """Per line, whether GitHub's page hides it inside a comment left open.

    A run of raw lines is read whole when it ends, and a paragraph's text
    when the paragraph ends, so a construct spanning lines is read as one;
    a heading is one line of its own. Lines inside a run or a paragraph are
    judged by the state they start in, which moves no heading."""
    out, inside, raw, text = [], False, [], []
    for scope in scopes:
        if raw and scope.raw is None:
            inside, raw = rendered_after("\n".join(raw), inside), []
        if text and not (scope.text is not None and scope.cont):
            inside, text = inside and not inline_closes("\n".join(text)), []
        out.append(inside)
        if scope.raw is not None:
            raw.append(scope.raw)
        elif scope.text is not None:
            text.append(scope.text)
    return out

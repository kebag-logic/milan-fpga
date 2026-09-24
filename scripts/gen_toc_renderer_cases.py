#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The renderer's own case tables (#437, #516): fixture pages and answers.

One arm per property of the parser-backed walk in `gen_toc.py` and of the
pin in `gen_toc_renderer.py`, each failing when that property is removed:
the lines a block covers, what the HTML parse swallows, which headings are
listed and with what label, and that the lock and the installed releases
are the ones the renderer requires. `gen_toc_cases.py` folds them into its
walk, heading and guard families. Split off from those tables because they
had reached rule 12's long-module ratchet (docs/development/CODE_QUALITY.md).
Only data lives here: this module holds no Markdown rule and imports no
expression engine (`gen_toc._owner_guards`).

The first correction round on PR #538 added an arm for each property the
reviews R237-5 and R238-4 showed could be removed with every arm green: the
position attribute in any spelling a page can give it, a page nested past
the recursion limit, each kind of block that renders as its own element,
the heading tag matched to its level, the strikethrough extension, the
drift refusal as `bind()` itself raises it, and the extensions attached.
"""
import importlib.metadata

from gen_toc import (CODE, COMMENT, FENCE, HEADING_LINE, HTML, TABLE_ROW,
                     TEXT, headings, label, line_kinds, rendered_headings)
from gen_toc_renderer import (CMARK_GFM, EXTENSIONS, LOCK, PINNED,
                              RendererError, bind, lock_pins, verify)

#: Three plain sections, then a heading that a raw comment left open hides
#: from GitHub (#516). With `FORGED` these are the file-view pages the
#: em-dash gate is also run on (`gen_toc_shape_cases.em_dash_rows`).
_SECTIONS = ("# Page\n\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\n"
             "Body.\n\n")
_HIDDEN = "<span>\n<!--\n\n## Old \u2014 heading\n</span>\n"
#: That page with a raw element carrying the hidden heading's position, in
#: each spelling the HTML parse reads as the renderer's own attribute
#: (R237-5 and R238-4 F1 on PR #538). A raw `<h2>` spells it in upper or
#: mixed case. In the last two a raw `<h2>` is left open in a quoted value
#: that the paragraph closes, so its text is read as attributes, and the
#: text spells the attribute through a character reference or a backslash
#: escape, which cmark-gfm writes out decoded. Each position is the hidden
#: heading's own: line 20, or 22 once the paragraph is added.
FORGED = {
    "in upper case": _SECTIONS + '<h2 DATA-SOURCEPOS="20:1-20:18">x</h2>\n\n'
    + _HIDDEN,
    "in mixed case": _SECTIONS + '<h2 Data-SourcePos="20:1-20:18">x</h2>\n\n'
    + _HIDDEN,
    "through a character reference": _SECTIONS + "<h2 title='\n\n"
    "z' &#100;ata-sourcepos=22:1-22:18 y\n\n" + _HIDDEN,
    "through a backslash escape": _SECTIONS + "<h2 title='\n\n"
    "z' data\\-sourcepos=22:1-22:18 y\n\n" + _HIDDEN,
}
#: A raw comment left open, then a blank line: what follows renders as
#: nothing on GitHub.
_OPEN = "<span>\n<!--\n\n"
#: Block quotes nested past the 1000 frames CPython allows by default.
_DEEP = 1100


def listed(pairs: list[tuple[str, str]]) -> object:
    """A predicate over a page: `headings()` lists exactly these (text,
    anchor) pairs, so an arm can hold a label and its anchor together."""
    return lambda text: [(r, a) for _, r, a in headings(text)] == pairs


def _answers(pairs: list[tuple[str, str]]) -> object:
    """`listed(pairs)`, false rather than raising when the walk runs out of
    stack, so a page nested too deep fails its arm by name (R237-5 F2)."""
    def holds(text: str) -> bool:
        """Whether `text` lists exactly `pairs`, no stack left counting as
        no."""
        try:
            return listed(pairs)(text)
        except RecursionError:
            return False
    return holds


def _refusal(**releases: str | None) -> str:
    """Why `bind()` refuses the pinned releases with these replaced, or ""
    when it binds them. A release of None is one not installed at all."""
    def installed(name: str) -> str:
        """The release `bind()` is told is installed for `name`."""
        release = dict(PINNED, **releases)[name]
        if release is None:
            raise importlib.metadata.PackageNotFoundError(name)
        return release
    try:
        bind(installed)
    except RendererError as exc:
        return str(exc)
    return ""


def renderer_walk_arms() -> list[tuple[str, str, object]]:
    """The labels the renderer gives (#437), one arm per property of
    `gen_toc._page()`: a block's extent, a container's content, and what
    the HTML parse swallows. Each fails when its property is removed."""
    return [
        ("I437 a comment block its end condition closes covers its closing "
         "line", "<!--\nx\n-->\n## Real\n",
         lambda k: k[:3] == [COMMENT] * 3 and k[3] == TEXT),
        ("I437 an indented code block ends at its last code line",
         "    code\n\n    more\n\ntext\n",
         lambda k: k[:3] == [CODE] * 3 and k[3:5] == [TEXT] * 2),
        ("I437 a fence in a list item is a fence",
         "- item\n\n  ```\n  ## Old\n  ```\n\n## Real\n",
         lambda k: k[2:5] == [FENCE] * 3 and k[6] == TEXT),
        ("I437 a fence in a block quote is a fence",
         "> ```\n> ## Old\n> ```\n\n## Real\n",
         lambda k: k[:3] == [FENCE] * 3 and k[4] == TEXT),
        ("I437 a line indented into a nested item's content is its text",
         "- item\n  - nested\n\n    text\n", lambda k: k[3] == TEXT),
        ("I437 what a raw comment left open swallows is commented (#516)",
         "<span>\n<!--\n\n## Old\n</span>\n\n## Real\n",
         lambda k: k[:2] == [HTML] * 2 and k[3] == COMMENT
         and k[6] == COMMENT),
        ("I437 what an open quoted attribute value swallows is commented",
         '<div title="\n\n## Old\n\ntext\n',
         lambda k: k[2] == COMMENT and k[4] == COMMENT),
        ("I437 a heading a select swallows is commented, the next renders",
         "<select>\n\n## X\n\n</select>\n\n\n## Y\n",
         lambda k: k[2] == COMMENT and k[7] == TEXT),
        ("I437 an item the HTML parse swallows is commented, its list not",
         '- <div title="\n- two\n\n## Old\n',
         lambda k: k[0] == HTML and k[1] == COMMENT and k[3] == COMMENT),
        ("I437 a list the HTML parse swallows is commented item by item",
         "<!-- a --> <!-- b\n- one\n- two\n",
         lambda k: k[1:3] == [COMMENT] * 2),
        ("I437 a tight list's bare paragraphs render",
         "- a\n- b\n\n## Real\n", lambda k: k[:2] == [TEXT] * 2),
        ("I437 a task list's items render",
         "- [ ] a\n- [x] b\n", lambda k: k[:2] == [TEXT] * 2),
        ("I437 a lone carriage return ends a line for the renderer",
         "```\r```\n## Probe\n", lambda k: k[:2] == [FENCE, TEXT]),
        # One per kind that renders as its own element (R237-5 F3): the
        # lines of a block the open comment swallows are commented.
        ("I437 a block quote an open comment swallows is commented, its "
         "blank line too", _OPEN + "> a\n>\n> b\n",
         lambda k: k[3:6] == [COMMENT] * 3),
        ("I437 a list an open comment swallows is commented, the blank "
         "line only the list holds too", _OPEN + "-\n\n- b\n",
         lambda k: k[3:6] == [COMMENT] * 3),
        ("I437 a fence an open comment swallows is commented",
         _OPEN + "```\ncode\n```\n", lambda k: k[3:6] == [COMMENT] * 3),
        ("I437 a thematic break an open comment swallows is commented",
         _OPEN + "***\n", lambda k: k[3] == COMMENT),
        ("I437 a table an open comment swallows is commented",
         _OPEN + "| a |\n|---|\n| b |\n", lambda k: k[3:6] == [COMMENT] * 3),
    ]


def renderer_heading_arms() -> list[tuple[str, str, object]]:
    """The headings the renderer draws (#437, #516), each listed with the
    anchor the same rule gives, and each fails when its property of
    `gen_toc._page()` is removed. The old walk withheld the first six."""
    footnote = ("[^1]: note\n\n    ## Same\n\n## Top\n\n## Same\n\n"
                "ref[^1]\n")
    return [
        ("I437 a setext heading is listed with its rendered text",
         "Alpha\n===\n", listed([("Alpha", "alpha")])),
        ("I437 a setext heading over two lines keeps its break for the "
         "anchor, and its label reads it as a space", "Alpha\nbeta\n---\n",
         lambda t: listed([("Alpha\nbeta", "alphabeta")])(t)
         and label(headings(t)[0][1]) == "Alpha beta"),
        ("I437 an ATX heading indented three spaces is listed",
         "   # H\n", listed([("H", "h")])),
        ("I437 an empty ATX heading is listed with no text", "##\n",
         listed([("", "")])),
        ("I437 a heading in a block quote is read off its own line",
         "> ## Q ##\n", listed([("Q", "q")])),
        ("I437 a heading in a list item is read off its own line",
         "- item\n\n  ## Inner `x` ##\n", listed([("Inner `x`", "inner-x")])),
        ("I437 a heading in a referenced footnote is listed where the "
         "renderer places it, and numbered there", footnote,
         listed([("Top", "top"), ("Same", "same"), ("Same", "same-1")])),
        ("I437 a heading in an unreferenced footnote is not listed",
         "[^1]: note\n\n    ## FN\n\n## Top\n", listed([("Top", "top")])),
        ("I437 a heading the HTML parse moves out of an open table is "
         "listed", "<table>\n***\n\n   ## H1\n\n## H2\n",
         listed([("H1", "h1"), ("H2", "h2")])),
        ("I437 a heading written as raw HTML is not listed",
         "<h2>Raw</h2>\n\n## Real\n", listed([("Real", "real")])),
        ("I437 a heading after a raw comment the page leaves open is not "
         "listed (#516)", "- item\n\n  text\n<span>\n<!--\n\n## Old\n"
         "</span>\n\n## Real\n", listed([])),
        ("I437 a page spelling the renderer's position attribute lists "
         "nothing", "## A\n\ndata-sourcepos\n\n## B\n", listed([])),
        ("I437 a heading an open raw comment hides is not listed, the "
         "page's other headings are", _SECTIONS + _HIDDEN,
         listed([("Page", "page"), ("Alpha", "alpha"), ("Beta", "beta"),
                 ("Gamma", "gamma")])),
    ] + [
        (f"I437 a page whose raw element carries the position attribute "
         f"spelled {how} lists nothing", page, listed([]))
        for how, page in FORGED.items()
    ] + [
        ("I437 a page nesting an element 200 deep is read",
         "## A\n\n" + ">" * 199 + " x\n\n## B\n",
         listed([("A", "a"), ("B", "b")])),
        ("I437 a page nesting one 201 deep lists nothing: GitHub drops "
         "what it nests 256 deep and all after it",
         "## A\n\n" + ">" * 200 + " x\n\n## B\n", listed([])),
        ("I437 a page nested past the interpreter's recursion limit is "
         "read, and lists nothing", "## A\n\n" + ">" * _DEEP + " x\n\n## B\n",
         _answers([])),
        ("I437 a heading whose position an open raw tag reads as an "
         "attribute is not listed: the tag is not its level's",
         "<div foo\n\n## Old\n\n## Real\n", listed([("Real", "real")])),
        ("I437 the same, the position read as an unquoted value",
         "<div title=\n\n## Old\n\n## Real\n", listed([("Real", "real")])),
        ("I437 a setext heading's strikethrough renders as GitHub's does",
         "a ~~b~~\n---\n", listed([("a b", "a-b")])),
        ("I437 the rendered text of a heading is what GitHub shows",
         "## a `b` *c*\n", lambda t: rendered_headings(t) == [(2, "a b c")]),
        ("I437 a table in a block quote is a table row",
         "> | a |\n> |---|\n> | b |\n",
         lambda t: line_kinds(t)[:3] == [TABLE_ROW] * 3),
        ("I437 a pipe-led line that is no table is prose", "text\n|a| b\n",
         lambda t: line_kinds(t)[:2] == [TEXT] * 2),
        ("I437 every line of a setext heading is a heading line",
         "Alpha\n===\n", lambda t: line_kinds(t)[:2] == [HEADING_LINE] * 2),
    ]


#: THE LOCK AGAIN, spelled here as a literal and not read from the file the
#: renderer checks: every distribution it pins, at its version. The guard
#: family below compares the two, so a release moved in the lock without
#: this table fails an arm, whatever else agrees ([R85] suggestion, round 7
#: on PR #428, for the same reason the family list is spelled twice).
_LOCK_SPELLED = {"cmarkgfm": "2025.10.22", "cffi": "2.1.1",
                 "pycparser": "3.0", "html5lib": "1.1", "six": "1.17.0",
                 "webencodings": "0.6.1"}
#: GitHub's extensions spelled again for the same reason: dropping the
#: autolink or the task list changes no heading measured, so only this
#: holds them (R238-4 S3 on PR #538).
_EXTENSIONS_SPELLED = ("table", "strikethrough", "autolink", "tagfilter",
                       "tasklist")


def renderer_guard_arms() -> list[tuple[str, str, object]]:
    """The pin's own arms (#437): the lock the documentation gates install
    from is the one the renderer checks, every distribution in it is an
    exact release with a hash, and a drifted release or bundled cmark-gfm
    is refused by name rather than rendered with."""
    pins = lock_pins(LOCK.read_text())
    return [
        ("I437 the lock pins exactly the distributions and releases spelled "
         "here", "",
         lambda t: {name: version for name, (version, _) in pins.items()}
         == _LOCK_SPELLED),
        ("I437 every distribution in the lock carries at least one hash", "",
         lambda t: all(count >= 1 for _, count in pins.values())),
        ("I437 the releases the renderer checks are the lock's", "",
         lambda t: all(pins[name][0] == want
                       for name, want in PINNED.items())),
        ("I437 the pinned releases pass the renderer's check", "",
         lambda t: verify(dict(PINNED), CMARK_GFM) == []),
        ("I437 another cmarkgfm release is refused by name", "",
         lambda t: [("cmarkgfm" in note) for note in verify(
             dict(PINNED, cmarkgfm="2025.10.20"), CMARK_GFM)] == [True]),
        ("I437 another html5lib release is refused by name", "",
         lambda t: [("html5lib" in note) for note in verify(
             dict(PINNED, html5lib="1.0.1"), CMARK_GFM)] == [True]),
        ("I437 a missing distribution is refused", "",
         lambda t: len(verify({"html5lib": "1.1"}, CMARK_GFM)) == 1),
        ("I437 another bundled cmark-gfm is refused", "",
         lambda t: [("cmark-gfm" in note) for note in verify(
             dict(PINNED), "0.29.0.gfm.12")] == [True]),
        ("I437 the binding binds the pinned releases", "",
         lambda t: _refusal() == ""),
        ("I437 the binding itself refuses another cmarkgfm release by name",
         "", lambda t: "cmarkgfm '2025.10.20'" in _refusal(
             cmarkgfm="2025.10.20")),
        ("I437 the binding itself refuses a missing html5lib by name", "",
         lambda t: "html5lib None" in _refusal(html5lib=None)),
        ("I437 the renderer attaches exactly the extensions spelled here",
         "", lambda t: EXTENSIONS == _EXTENSIONS_SPELLED),
        ("I437 a hash that is not a sha256 counts none", "",
         lambda t: lock_pins("a==1 --hash=md5:00\n") == {"a": ("1", 0)}),
        ("I437 a requirement with no hash counts none", "",
         lambda t: lock_pins("a==1\nb==2 \\\n    --hash=sha256:00\n")
         == {"a": ("1", 0), "b": ("2", 1)}),
    ]

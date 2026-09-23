#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The renderer the Contents walk reads: cmark-gfm, then an HTML5 parse.

WHY THIS EXISTS. `gen_toc.py` used to classify Markdown with a walk of its
own. Eight review rounds on PR #515 found shapes where that walk and GitHub
disagreed, and every fix exposed the next one. So the owner replaced the
walk with the renderer GitHub itself uses (#437 and #516, decision of
2026-09-23 17:45). This module is that renderer, pinned to one release.
`gen_toc.py` asks it one question per page and still owns what the answer
MEANS for navigation.

WHAT IT RUNS. Two stages, both pinned with hashes in
`tools/markdown/requirements.txt`:

1. cmark-gfm, through the `cmarkgfm` binding, with GitHub's extensions
   (tables, strikethrough, autolinks, the tag filter and task lists), raw
   HTML kept and footnotes on. It parses the page into a syntax tree and
   renders that tree as HTML carrying each block's source position. The
   binding's Python surface only parses and renders, but its extension
   exports the whole C API. `_CDEF` declares the node calls read here, and
   they are called on that same library.
2. html5lib parses that HTML as a browser does. This stage is what hides the
   #516 family: cmark-gfm emits a heading after a raw `<!--` as a heading,
   and only the HTML parse puts it inside the comment. An open quoted
   attribute value or a `<select>` hides a heading the same way. The
   positions are written unquoted first (`unquoted()`), so the bytes the
   parser reads tokenize as GitHub's own position-free bytes do. The
   standard library's parser is not used: its comment rules changed in the
   2025 security releases, so its answer depends on the interpreter's patch
   level, and it builds no tree.

WHAT IT ANSWERS. `render()` gives every block node in document order, and
every element that survives the HTML parse and carries a source position or
is a heading, in the parsed document's order. An element the parse swallowed
into a comment, an attribute or a `<select>` is simply absent. Nothing here
decides what a line is; `gen_toc.py` does that from these two lists.

WHAT IT CANNOT TELL. cmark-gfm marks its own elements with a position
attribute, and raw HTML on the page could spell the same attribute. A page
whose text carries that attribute name is therefore reported as rendering
nothing: no element and so no heading. That withholds a heading and cannot
invent one.
"""
import functools
import importlib.metadata
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

#: The lock the documentation gates install from, and the releases in it
#: that decide what a page renders. The other pinned distributions are only
#: their dependencies. A different release of either is refused by name.
LOCK = Path(__file__).resolve().parent.parent / "tools/markdown/requirements.txt"
PINNED = {"cmarkgfm": "2025.10.22", "html5lib": "1.1"}
#: The cmark-gfm release the pinned binding carries.
CMARK_GFM = "0.29.0.gfm.13"
#: GitHub's syntax extensions, attached in this order.
EXTENSIONS = ("table", "strikethrough", "autolink", "tagfilter", "tasklist")
#: The attribute cmark-gfm writes a block's source position into.
POSITION = "data-sourcepos"
HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
#: The node calls this module reads. None of them allocates, and none of
#: them needs a structure layout, so they are declared by name only.
_CDEF = """
typedef struct cmark_node cmark_node;
typedef struct cmark_mem {
    void *(*calloc)(size_t, size_t);
    void *(*realloc)(void *, size_t);
    void (*free)(void *);
} cmark_mem;
cmark_mem *cmark_get_default_mem_allocator(void);
cmark_node *cmark_node_first_child(cmark_node *node);
cmark_node *cmark_node_next(cmark_node *node);
int cmark_node_get_type(cmark_node *node);
const char *cmark_node_get_type_string(cmark_node *node);
int cmark_node_get_start_line(cmark_node *node);
int cmark_node_get_start_column(cmark_node *node);
int cmark_node_get_end_line(cmark_node *node);
int cmark_node_get_end_column(cmark_node *node);
const char *cmark_node_get_literal(cmark_node *node);
int cmark_node_get_heading_level(cmark_node *node);
int cmark_node_get_fenced(cmark_node *node, int *length, int *offset,
                          char *character);
int cmark_node_get_list_tight(cmark_node *node);
void cmark_node_free(cmark_node *node);
"""
#: The block kinds cmark-gfm renders as an element carrying the block's
#: source position, whatever holds them. A paragraph is one too unless a
#: tight list holds it, and every child of a list is an item whatever an
#: extension names it (a task list item is `tasklist`).
_OWN_ELEMENT = ("block_quote", "list", "heading", "code_block",
                "thematic_break", "table")
#: cmark-gfm's node type carries its class in two bits: `_BLOCK` under
#: `_CLASS` for every block node, extensions' own included, and another
#: value for an inline node. The walk reads no inline node.
_CLASS, _BLOCK = 0xC000, 0x8000


class RendererError(Exception):
    """The pinned renderer is missing, drifted, or cannot be read."""


@dataclass(frozen=True)
class Node:
    """One block of the syntax tree, as the renderer placed it.

    `first`, `last` and `column` are the renderer's own source position:
    1-based lines and a 1-based byte column. `literal` is the raw text of a
    code or raw HTML block, whose line count is its extent. `element` says
    whether the block renders as an element carrying that position."""

    kind: str
    first: int
    last: int
    column: int
    end_column: int
    level: int = 0
    fenced: bool = False
    literal: str = ""
    element: bool = False

    @property
    def position(self) -> str:
        """The position exactly as the renderer writes it into its HTML."""
        return f"{self.first}:{self.column}-{self.last}:{self.end_column}"


@dataclass(frozen=True)
class Rendered:
    """What one page renders: its blocks in document order, and the
    elements that survive the HTML parse as (tag, position, text) in the
    parsed document's order. A position is empty on raw HTML's elements."""

    nodes: tuple[Node, ...]
    shown: tuple[tuple[str, str, str], ...]


def lock_pins(text: str) -> dict[str, tuple[str, int]]:
    """Every requirement the lock carries: name to (version, hash count).
    A requirement is `name==version` then its `--hash=sha256:` options,
    continued over lines ending in a backslash."""
    pins, name = {}, None
    for line in text.splitlines():
        words = line.split("#", 1)[0].replace("\\", " ").split()
        for word in words:
            if "==" in word:
                name, version = word.split("==", 1)
                pins[name] = (version, 0)
            elif word.startswith("--hash=sha256:") and name in pins:
                version, count = pins[name]
                pins[name] = (version, count + 1)
    return pins


def verify(versions: dict[str, str | None], core: str) -> list[str]:
    """Why these installed releases are not the pinned ones, if they are
    not: each package that decides rendering at its locked release, and
    the cmark-gfm release the binding carries."""
    bad = [f"{name} {versions.get(name)!r} is installed where {LOCK.name} "
           f"pins {want}" for name, want in PINNED.items()
           if versions.get(name) != want]
    if core != CMARK_GFM:
        bad.append(f"the binding carries cmark-gfm {core!r}, not {CMARK_GFM}")
    return bad


@functools.cache
def binding() -> SimpleNamespace:
    """The pinned renderer, loaded once, or a RendererError naming how to
    install it. The binding's own module and the declared node calls on the
    library it loaded are both returned."""
    try:
        import cffi
        import html5lib
        from cmarkgfm import _cmark
    except ImportError as exc:
        raise RendererError(
            f"the pinned Markdown renderer is not installed ({exc.name}); "
            f"run: python3 -m pip install --require-hashes -r "
            f"{LOCK.relative_to(LOCK.parents[2])}") from exc
    versions = {}
    for name in PINNED:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    core = _cmark.ffi.string(_cmark.lib.cmark_version_string()).decode()
    bad = verify(versions, core)
    if bad:
        raise RendererError("; ".join(bad))
    ffi = cffi.FFI()
    ffi.cdef(_CDEF)
    try:
        api = ffi.dlopen(_cmark.__file__)
        api.cmark_node_first_child
    except (OSError, AttributeError) as exc:
        raise RendererError(f"the binding at {_cmark.__file__} does not "
                            f"export the node calls: {exc}") from exc
    return SimpleNamespace(lib=_cmark.lib, ffi=_cmark.ffi, api=api,
                           node_ffi=ffi, html5lib=html5lib)


def _node(bound: SimpleNamespace, node: object, element: bool) -> Node:
    """One block as the renderer placed it."""
    api, ffi = bound.api, bound.node_ffi
    kind = ffi.string(api.cmark_node_get_type_string(node)).decode()
    literal = api.cmark_node_get_literal(node)
    fenced = kind == "code_block" and bool(api.cmark_node_get_fenced(
        node, ffi.new("int *"), ffi.new("int *"), ffi.new("char *")))
    return Node(kind=kind,
                first=api.cmark_node_get_start_line(node),
                last=api.cmark_node_get_end_line(node),
                column=api.cmark_node_get_start_column(node),
                end_column=api.cmark_node_get_end_column(node),
                level=api.cmark_node_get_heading_level(node),
                fenced=fenced,
                literal=("" if literal == ffi.NULL
                         or kind not in ("code_block", "html_block")
                         else ffi.string(literal).decode("utf-8", "replace")),
                element=element or kind in _OWN_ELEMENT)


def _nodes(bound: SimpleNamespace, parent: object, holder: str = "",
           bare: bool = False) -> list[Node]:
    """Every block under `parent`, depth first in document order.

    `holder` is `tight` or `loose` when `parent` is a list, whose every
    child renders as an item element. `bare` says `parent` is an item of a
    tight list, whose paragraphs render without an element of their own:
    cmark-gfm's rule is a paragraph whose grandparent is a tight list."""
    api, ffi = bound.api, bound.node_ffi
    out = []
    child = api.cmark_node_first_child(ffi.cast("cmark_node *", parent))
    while child != ffi.NULL:
        if api.cmark_node_get_type(child) & _CLASS != _BLOCK:
            child = api.cmark_node_next(child)
            continue
        node = _node(bound, child, bool(holder) or bool(
            ffi.string(api.cmark_node_get_type_string(child)) == b"paragraph"
            and not bare))
        out.append(node)
        if node.kind == "list":
            tight = api.cmark_node_get_list_tight(child)
            out += _nodes(bound, child, "tight" if tight else "loose")
        else:
            out += _nodes(bound, child, bare=holder == "tight")
        child = api.cmark_node_next(child)
    return out


def render(text: str) -> Rendered:
    """What `text` renders, as GitHub's renderer and a browser's parser
    draw it. A page carrying the renderer's own position attribute renders
    nothing here, which withholds rather than invents (module docstring)."""
    if POSITION in text:
        return Rendered((), ())
    bound = binding()
    lib, ffi = bound.lib, bound.ffi
    lib.cmark_gfm_core_extensions_ensure_registered()
    options = (lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE
               | lib.CMARK_OPT_FOOTNOTES | lib.CMARK_OPT_GITHUB_PRE_LANG)
    parser = lib.cmark_parser_new(options)
    try:
        for name in EXTENSIONS:
            lib.cmark_parser_attach_syntax_extension(
                parser, lib.cmark_find_syntax_extension(name.encode()))
        raw = text.encode("utf-8")
        lib.cmark_parser_feed(parser, raw, len(raw))
        root = lib.cmark_parser_finish(parser)
        html_ptr = lib.cmark_render_html(
            root, options, lib.cmark_parser_get_syntax_extensions(parser))
        html = ffi.string(html_ptr).decode("utf-8", "replace")
        nodes = tuple(_nodes(bound, root))
        memory = bound.api.cmark_get_default_mem_allocator()
        memory.free(bound.node_ffi.cast("void *", html_ptr))
        bound.api.cmark_node_free(bound.node_ffi.cast("cmark_node *", root))
    finally:
        lib.cmark_parser_free(parser)
    return Rendered(nodes, _shown(bound, html))


def unquoted(html: str) -> str:
    """cmark-gfm's HTML with every position attribute written unquoted.

    GitHub renders without positions, so its HTML carries no quote where
    this one carries two per element, and a quote closes a quoted value a
    raw tag left open: `<div title="` then a heading hides the heading and
    everything after it on GitHub, but the heading's own position quote
    ended the value here. Unquoted, a position adds only a space, the
    attribute name, digits, colons and hyphens, which leave every tokenizer
    state a raw fragment can leave open where GitHub's bytes leave it. Every
    occurrence is the renderer's own: `render()` reads no page that spells
    the attribute."""
    head, *rest = html.split(f' {POSITION}="')
    return head + "".join(f" {POSITION}=" + chunk.replace('"', "", 1)
                          for chunk in rest)


def _elements(bound: SimpleNamespace, html: str) -> list[object]:
    """Every element an HTML fragment keeps once parsed, in document order.

    The `dom` tree builder is the one read: html5lib's `etree` builder
    drops the nodes the parse moves out of an open table ("foster
    parenting") when it builds a fragment, and GitHub keeps them before the
    table, as the specification does (measured on a raw `<table>` left
    open above two headings)."""
    tree = bound.html5lib.parseFragment(html, treebuilder="dom",
                                        namespaceHTMLElements=False)
    out, stack = [], list(reversed(tree.childNodes))
    while stack:
        node = stack.pop()
        if node.nodeType == node.ELEMENT_NODE:
            out.append(node)
            stack.extend(reversed(node.childNodes))
    return out


def _text(element: object) -> str:
    """An element's own text, line breaks kept, less the blanks around it."""
    parts, stack = [], list(reversed(element.childNodes))
    while stack:
        node = stack.pop()
        if node.nodeType == node.TEXT_NODE:
            parts.append(node.data)
        else:
            stack.extend(reversed(node.childNodes))
    return "".join(parts).strip()


def _shown(bound: SimpleNamespace, html: str) -> tuple[tuple[str, str, str],
                                                       ...]:
    """(tag, position, text) of every element the HTML parse keeps that
    carries a position or is a heading, in document order."""
    return tuple((element.tagName, element.getAttribute(POSITION),
                  _text(element))
                 for element in _elements(bound, unquoted(html))
                 if element.getAttribute(POSITION)
                 or element.tagName in HEADING_TAGS)


def headings_of(html: str) -> list[tuple[int, str]]:
    """(level, text) of every heading element an HTML fragment keeps once
    parsed, blanks collapsed: how a recorded GitHub rendering is read, with
    the same parser that reads the walk's own rendering."""
    return [(int(element.tagName[1]), " ".join(_text(element).split()))
            for element in _elements(binding(), html)
            if element.tagName in HEADING_TAGS]

#!/usr/bin/env python3
"""Dump cmark-gfm's node tree (kind, start line:col, end line:col, depth, literal) for a Markdown file,
with the extensions and options of the lane B16 figures check. usage: <parser python> dump_tree.py <repo> <file>"""
import importlib.util, sys
from pathlib import Path
import cffi
from cmarkgfm import _cmark
REPO, F = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("gen_toc_renderer", REPO / "scripts/gen_toc_renderer.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
ffi = cffi.FFI()
ffi.cdef("""typedef struct cmark_node cmark_node;
cmark_node *cmark_node_first_child(cmark_node *node); cmark_node *cmark_node_next(cmark_node *node);
const char *cmark_node_get_type_string(cmark_node *node); int cmark_node_get_start_line(cmark_node *node);
int cmark_node_get_start_column(cmark_node *node); int cmark_node_get_end_line(cmark_node *node);
int cmark_node_get_end_column(cmark_node *node); const char *cmark_node_get_literal(cmark_node *node);""")
api = ffi.dlopen(_cmark.__file__); lib = _cmark.lib
lib.cmark_gfm_core_extensions_ensure_registered()
p = lib.cmark_parser_new(lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE | lib.CMARK_OPT_FOOTNOTES | lib.CMARK_OPT_GITHUB_PRE_LANG)
for n in R.EXTENSIONS:
    lib.cmark_parser_attach_syntax_extension(p, lib.cmark_find_syntax_extension(n.encode()))
raw = F.read_bytes(); lib.cmark_parser_feed(p, raw, len(raw)); root = lib.cmark_parser_finish(p)
s = lambda c: "" if c == ffi.NULL else ffi.string(c).decode("utf-8", "replace")
def walk(n, d):
    while n != ffi.NULL:
        print(f"{'  '*d}{s(api.cmark_node_get_type_string(n))} {api.cmark_node_get_start_line(n)}:{api.cmark_node_get_start_column(n)}-"
              f"{api.cmark_node_get_end_line(n)}:{api.cmark_node_get_end_column(n)} {s(api.cmark_node_get_literal(n))[:70]!r}")
        walk(api.cmark_node_first_child(n), d + 1); n = api.cmark_node_next(n)
walk(ffi.cast("cmark_node *", root), 0)

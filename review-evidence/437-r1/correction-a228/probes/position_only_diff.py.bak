"""Evidence: cmark-gfm's HTML with positions is its HTML without them plus
one ` data-sourcepos="L:C-L:C"` per positioned element, and nothing else.
Usage: position_only_diff.py <repo> <pages.json>..."""
import json, re, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc_renderer as r

b = r.binding()
lib, ffi = b.lib, b.ffi
lib.cmark_gfm_core_extensions_ensure_registered()
OPT = (lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE | lib.CMARK_OPT_FOOTNOTES
       | lib.CMARK_OPT_GITHUB_PRE_LANG)


def both(text):
    p = lib.cmark_parser_new(OPT)
    for name in r.EXTENSIONS:
        lib.cmark_parser_attach_syntax_extension(p, lib.cmark_find_syntax_extension(name.encode()))
    raw = text.encode()
    lib.cmark_parser_feed(p, raw, len(raw))
    root = lib.cmark_parser_finish(p)
    ext = lib.cmark_parser_get_syntax_extensions(p)
    a = ffi.string(lib.cmark_render_html(root, OPT, ext))
    c = ffi.string(lib.cmark_render_html(root, OPT & ~lib.CMARK_OPT_SOURCEPOS, ext))
    lib.cmark_parser_free(p)
    return a, c


pages = []
for f in sys.argv[2:]:
    d = json.load(open(f))
    rows = d["shapes"] if isinstance(d, dict) else d
    pages += [x["page"] if isinstance(x, dict) else x for x in rows]
same = differ = 0
for page in pages:
    a, c = both(page)
    stripped = re.sub(rb' data-sourcepos="\d+:\d+-\d+:\d+"', b"", a)
    if stripped == c:
        same += 1
    else:
        differ += 1
        print("DIFFER", repr(page)[:120])
print(f"{len(pages)} pages: {same} identical once positions are removed, {differ} differ")

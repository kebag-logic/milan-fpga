"""Tracked pages at this head: which pages `apply()` would rewrite and
whether gen_toc owns any of them (what `--write` touches), and the deepest
element any tracked page nests in the renderer's own parse.
Usage: tracked_depth.py <repo>"""
import subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc as g, gen_toc_renderer as r
b = r.binding(); lib, ffi = b.lib, b.ffi
lib.cmark_gfm_core_extensions_ensure_registered()
OPT = lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE | lib.CMARK_OPT_FOOTNOTES | lib.CMARK_OPT_GITHUB_PRE_LANG
rewrite, owned, depth = [], [], []
for p in subprocess.run(["git", "-C", str(repo), "ls-files", "*.md"], capture_output=True, text=True).stdout.split():
    f = repo / p
    if not f.is_file():
        continue
    t = f.read_text()
    if g.apply(f, t) is not None:
        rewrite.append(p)
        owned += [p] if g.owns(p, t) else []
    parser = lib.cmark_parser_new(OPT)
    for name in r.EXTENSIONS:
        lib.cmark_parser_attach_syntax_extension(parser, lib.cmark_find_syntax_extension(name.encode()))
    raw = t.encode(); lib.cmark_parser_feed(parser, raw, len(raw)); root = lib.cmark_parser_finish(parser)
    html = ffi.string(lib.cmark_render_html(root, OPT, lib.cmark_parser_get_syntax_extensions(parser))).decode()
    lib.cmark_parser_free(parser)
    depth.append((r._elements(b, r.unquoted(html))[1], p))
print("apply() would rewrite:", rewrite)
print("of them owned by gen_toc (what --write touches):", owned)
print("deepest element per page, top five:", sorted(depth)[-5:], "; bound DEEPEST =", r.DEEPEST)

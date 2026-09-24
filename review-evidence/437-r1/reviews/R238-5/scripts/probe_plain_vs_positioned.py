#!/usr/bin/env python3
"""Reviewer probe (R238-5): the two renderings `render()` makes differ only
by the renderer's position attributes, and how deep tracked pages nest.

Usage: python probe_plain_vs_positioned.py <repo-root> [fuzz-count] [seed]

For every tracked *.md page, every fixture page (shapes and file view) and
`fuzz-count` generated pages, renders the page with and without source
positions through the pinned binding exactly as `render()` does, deletes
every ` data-sourcepos="..."` from the positioned HTML and requires the
result to equal the plain HTML byte for byte. Also reports the deepest
element of each tracked page as `_elements()` measures it.
"""
import json
import random
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
count = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 238
sys.path.insert(0, str(root / "scripts"))
import gen_toc_renderer as R  # noqa: E402

POS_RE = re.compile(rb' data-sourcepos="[0-9]+:[0-9]+-[0-9]+:[0-9]+"')


def both(text: str) -> tuple[bytes, bytes]:
    bound = R.binding()
    lib, ffi = bound.lib, bound.ffi
    lib.cmark_gfm_core_extensions_ensure_registered()
    options = (lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE
               | lib.CMARK_OPT_FOOTNOTES | lib.CMARK_OPT_GITHUB_PRE_LANG)
    parser = lib.cmark_parser_new(options)
    try:
        for name in R.EXTENSIONS:
            lib.cmark_parser_attach_syntax_extension(
                parser, lib.cmark_find_syntax_extension(name.encode()))
        raw = text.encode("utf-8")
        lib.cmark_parser_feed(parser, raw, len(raw))
        root_node = lib.cmark_parser_finish(parser)
        ext = lib.cmark_parser_get_syntax_extensions(parser)
        a = ffi.string(lib.cmark_render_html(root_node, options, ext))
        b = ffi.string(lib.cmark_render_html(
            root_node, options & ~lib.CMARK_OPT_SOURCEPOS, ext))
    finally:
        lib.cmark_parser_free(parser)
    return a, b


ATOMS = ["# H", "## H2", "text", "> ", ">", "- ", "1. ", "10) ", "  ", "    ",
         "\t", "```", "~~~", "<div>", "</div>", "<!--", "-->", "<span>",
         "</span>", '<a title="', '"', "'", "<h2 x", "<?", "?>", "<select>",
         "| a | b |", "|---|---|", "***", "---", "===", "[^1]", "[^1]: n",
         "&#100;", "\\-", "<table>", "*em*", "~~s~~", "`c`", "[l](u)",
         "<https://x.y>", "- [ ] t", "<pre>", "</pre>", "<xmp>", "<b>", "\\"]


def fuzz(rng: random.Random) -> str:
    lines = []
    for _ in range(rng.randint(1, 14)):
        lines.append("".join(rng.choice(ATOMS) for _ in range(rng.randint(0, 4))))
    return "\n".join(lines) + "\n"


def main() -> int:
    pages = []
    tracked = subprocess.run(["git", "-C", str(root), "ls-files", "*.md"],
                             capture_output=True, text=True).stdout.split()
    if not tracked:  # an export without git metadata
        tracked = [str(p.relative_to(root)) for p in root.rglob("*.md")]
    for rel in tracked:
        path = root / rel
        if path.is_file():
            pages.append(("tracked " + rel,
                          path.read_text(encoding="utf-8", errors="replace")))
    fixture = json.loads((root / "scripts/gen_toc_shapes.json").read_text())
    for part in ("shapes", "file_view"):
        pages += [(f"{part} {s['name']}", s["page"]) for s in fixture[part]]
    rng = random.Random(seed)
    pages += [(f"fuzz {i}", fuzz(rng)) for i in range(count)]
    diff = 0
    deepest = {}
    for name, text in pages:
        a, b = both(text)
        if POS_RE.sub(b"", a) != b:
            diff += 1
            print(f"DIFFERS: {name}")
        if name.startswith("tracked "):
            _, depth = R._elements(R.binding(), R.unquoted(
                a.decode("utf-8", "replace")))
            deepest[name] = depth
    top = sorted(deepest.items(), key=lambda kv: -kv[1])[:5]
    print(f"pages: {len(pages)} ({len(deepest)} tracked, "
          f"{sum(1 for n, _ in pages if n.startswith(('shapes', 'file_view')))}"
          f" fixture, {count} fuzz seed {seed}); differing beyond positions: "
          f"{diff}")
    print("deepest tracked pages:", ", ".join(f"{n[8:]}={d}" for n, d in top))
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main())

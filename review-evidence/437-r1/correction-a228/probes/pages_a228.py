"""The pages A228 records: every new arm page of gen_toc_renderer_cases.
Usage: pages_a228.py <repo> <out.json>"""
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc as g  # noqa: F401  (registers the module the cases import)
import gen_toc_renderer_cases as c

SRC = "the page of a gen_toc_renderer_cases I437 arm (A228, PR #538 correction round 1), exact page"
gfm = [
    ("I437 arm page: a heading an open raw comment hides, after three sections", c._SECTIONS + c._HIDDEN),
    ("I437 arm page: an open raw tag reads a heading's position as an attribute", "<div foo\n\n## Old\n\n## Real\n"),
    ("I437 arm page: an open raw tag reads a heading's position as an unquoted value", "<div title=\n\n## Old\n\n## Real\n"),
    ("I437 arm page: a setext heading with strikethrough", "a ~~b~~\n---\n"),
    ("I437 arm page: a block quote an open comment swallows", c._OPEN + "> a\n>\n> b\n"),
    ("I437 arm page: a list an open comment swallows, an empty item first", c._OPEN + "-\n\n- b\n"),
    ("I437 arm page: a fence an open comment swallows", c._OPEN + "```\ncode\n```\n"),
    ("I437 arm page: a thematic break an open comment swallows", c._OPEN + "***\n"),
    ("I437 arm page: a table an open comment swallows", c._OPEN + "| a |\n|---|\n| b |\n"),
    ("I437 arm page: an element nested 200 deep between two headings", "## A\n\n" + ">" * 199 + " x\n\n## B\n"),
]
view = [("position attribute: none, the heading hidden by an open raw comment", c._SECTIONS + c._HIDDEN)]
view += [(f"position attribute spelled {how} on a raw h2", page) for how, page in c.FORGED.items()]
view += [("an open raw tag reads a heading's position as an attribute", "<div foo\n\n## Old\n\n## Real\n"),
         ("an open raw tag reads a heading's position as an unquoted value", "<div title=\n\n## Old\n\n## Real\n"),
         ("a setext heading with strikethrough", "a ~~b~~\n---\n")]
view += [(f"an element nested {n + 1} deep between two headings", "## A\n\n" + ">" * n + " x\n\n## B\n")
         for n in (200, 255, c._DEEP)]
rows = [{"mode": "gfm", "set": "renderer", "name": n, "source": SRC, "page": p} for n, p in gfm]
rows += [{"mode": "markdown", "set": "file view", "name": n,
          "source": "R237-5 F1, R238-4 F1 and F2 on PR #538: the page of a gen_toc_renderer_cases I437 arm, exact page",
          "page": p} for n, p in view]
Path(sys.argv[2]).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
print(len(rows), "pages")

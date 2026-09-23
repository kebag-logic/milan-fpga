"""Write scripts/gen_toc_shapes.json from rendered.json (recorded GitHub renderings)."""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc_renderer as r
rows = json.loads(Path(sys.argv[2]).read_text())
# name converted arms by their current case-table names
sys.modules.setdefault("gen_toc", __import__("gen_toc"))
import gen_toc_cases as cases, gen_toc_closer_cases as closers
by_page = {}
for fam in (cases.walk_arms(), cases.tag_arms(), cases.predecessor_arms(), cases.heading_arms(), closers.closer_arms()):
    for name, page, _ in fam:
        by_page.setdefault(page, name)
shapes = []
keys = ("set", "name", "source", "kind", "r86_5", "pins", "reconstructed", "page",
        "request_bytes", "request_sha256", "response_bytes", "response_sha256", "recorded_utc")
for s in rows:
    if s["set"] == "arm":
        s["name"] = "arm: " + by_page[s["page"]]
    out = {k: s[k] for k in keys if k in s}
    out["headings"] = [list(h) for h in r.headings_of(s["response_bytes"])]
    if 'class="sr-only"' in s["response_bytes"] and [2, "Footnotes"] in out["headings"]:
        out["github_only"] = {"headings": [[2, "Footnotes"]],
                              "why": ("GitHub opens the footnote section of a page with a referenced footnote with a visually "
                                      "hidden `<h2 id=\"footnote-label\" class=\"sr-only\">Footnotes</h2>`; the pinned cmark-gfm "
                                      "0.29.0.gfm.13 emits the section without it, so the walk lists no such heading. A finding "
                                      "reported on #437, not a page section; no tracked page references a footnote.")}
    shapes.append(out)
doc = {
    "about": ("Issue #437 and #516: the committed shape set, each page with GitHub's recorded rendering. "
              "Sets: family one (acceptance 1 as restated 2026-09-23; `r86_5` maps the nine publicly described R86-5 shapes), "
              "#516 (the twelve unclosed-comment variants), comment and container (the pages of superseded PR #515's fixtures), "
              "R237 and R238 (every page the reviews on PR #515 published; `reconstructed` where a review gave a description, not the bytes), "
              "family two (the five withheld heading forms, now listed), arm (every case-table arm the renderer answers differently from the old walk) "
              "and corpus (a synthetic reproduction of each class of tracked-page difference). `headings` is what the response carries, "
              "read with the renderer's HTML parser; gen_toc_shape_cases.py checks it and compares it with the renderer's own answer."),
    "method": ("Each page was sent as `gh api --method POST markdown --input -` with the exact JSON in `request_bytes` "
               "(keys context, mode, text; mode gfm; context kebag-logic/milan-fpga), and `response_bytes` is the exact body returned. "
               "Recorded 2026-09-23 (UTC times per shape). Re-send `request_bytes` to reproduce a rendering."),
    "renderer": {"cmarkgfm": r.PINNED["cmarkgfm"], "cmark-gfm": r.CMARK_GFM, "html5lib": r.PINNED["html5lib"]},
    "shapes": shapes,
}
(repo / "scripts" / "gen_toc_shapes.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(shapes), "shapes written")

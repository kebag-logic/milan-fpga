"""Parser vs GitHub markdown-mode rendering: headings (level, text) and anchors (user-content ids)."""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1]); data = Path(sys.argv[2])
sys.path.insert(0, str(repo / "scripts"))
import gen_toc, gen_toc_renderer as r
def github(html):
    b = r.binding(); els = r._elements(b, html)
    heads = []
    for e in els:
        if e.tagName in r.HEADING_TAGS:
            heads.append([int(e.tagName[1]), " ".join(r._text(e).split()), None])
        elif e.tagName == "a" and e.getAttribute("class") == "anchor" and heads:
            heads[-1][2] = e.getAttribute("href").lstrip("#")
    return heads
rows = json.loads(data.read_text())
hd = an = 0; hd_rows, an_rows = [], []
for s in rows:
    gh = github(s["response_bytes"])
    ours_text = gen_toc.rendered_headings(s["page"])
    ours_anchor = [a for _, _, a in gen_toc.headings(s["page"])]
    if [(l, t) for l, t, _ in gh] != ours_text:
        hd += 1; hd_rows.append({"name": s["name"], "page": s["page"], "github": gh, "parser": ours_text})
    elif [a for _, _, a in gh] != ours_anchor:
        an += 1; an_rows.append({"name": s["name"], "page": s["page"], "github": gh, "parser": ours_anchor})
print(len(rows), "pages;", hd, "differ in headings;", an, "agree on headings but differ in anchors")
for x in hd_rows[:30]: print("HEAD", x["name"], repr(x["page"])[:110], x["github"], x["parser"])
for x in an_rows[:30]: print("ANCHOR", x["name"], repr(x["page"])[:110], x["github"], x["parser"])
if len(sys.argv) > 3:
    Path(sys.argv[3]).write_text(json.dumps({"pages": len(rows), "heading_differences": hd_rows, "anchor_differences": an_rows}, indent=1, ensure_ascii=False))

"""List every same-page (#frag) link in one page and whether gen_toc's
GitHub heading-anchor walk produces that anchor.  usage: <repo> <page.md>"""
import re, sys
from pathlib import Path
repo, page = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(repo / "scripts"))
import gen_toc
text = (repo / page).read_text()
anchors = {a for _, _, a in gen_toc.headings(text)}
bad = 0
for m in re.finditer(r"\]\(#([^)\s]+)\)", text):
    frag = m.group(1)
    ok = frag in anchors
    bad += not ok
    if "batched" in frag or not ok:
        print(f"{page}#{frag}: {'RESOLVES' if ok else 'MISSING'}")
print(f"{page}: {len(anchors)} heading anchors; '23-batched-merges' present: {'23-batched-merges' in anchors}; unresolved same-page links: {bad}")
sys.exit(1 if bad else 0)

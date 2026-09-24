"""Check every cross-page fragment link on the pages the #548 composition
changes against the pinned renderer's heading anchors, independent of
whether gen_toc's --verify-anchors corpus owns the linking page.
Usage: python anchor_probe.py <repo>"""
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import gen_toc  # noqa: E402

changed = ["docs/findings/117_GPTP_SILICON_EVIDENCE.md",
           "docs/reference/REGISTER_MAP.md"]
owned = {str(p.relative_to(repo)) for p in gen_toc.pages()}
bad = 0
checked = 0
for rel in changed:
    md = repo / rel
    text = md.read_text()
    print(f"{rel}: in --verify-anchors corpus: {rel in owned}")
    for m in re.finditer(r"\]\(([^)\s]*?)#([^)\s]+)\)", text):
        if re.match(r"[a-z]+://", m.group(1)):
            continue  # external URL, not a repository page
        tgt = (md.parent / m.group(1)) if m.group(1) else md
        checked += 1
        if not tgt.exists():
            print(f"  NOFILE {m.group(1)}#{m.group(2)}")
            bad += 1
            continue
        anchors = {a for _, _, a in gen_toc.headings(tgt.read_text())}
        if m.group(2) not in anchors:
            print(f"  MISS {m.group(1) or '(self)'}#{m.group(2)}")
            bad += 1
    print(f"  {checked} repository fragment link(s) checked so far")
if not bad:
    print("anchor probe: every fragment link on the changed pages resolves")
sys.exit(1 if bad else 0)

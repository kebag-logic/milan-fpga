"""[R293] R293-3: read the candidate's CONTRIBUTING.md through the pinned renderer.

Usage: python anchor_probe.py <repo>. Prints the anchors gen_toc derives for
section 2 headings, whether the two new cross-page fragments resolve, and the
headings the renderer finds inside CONTRIBUTING section 2.1 step 7.
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import gen_toc  # noqa: E402

text = (repo / "CONTRIBUTING.md").read_text(encoding="utf-8")
heads = gen_toc.headings(text)
anchors = {a for _, _, a in heads}
for level, title, anc in heads:
    if title.startswith("2"):
        print(f"h{level} {anc!r} <- {title!r}")
print("fragment 21-the-issue-to-merge-lane resolves:",
      "21-the-issue-to-merge-lane" in anchors)
print("heading count:", len(heads), "rendered:", len(gen_toc.rendered_headings(text)))
lines = text.splitlines()
start = next(i for i, l in enumerate(lines) if "Their `contained` diagnostics" in l)
end = next(i for i in range(start, len(lines)) if lines[i].startswith("   Exit codes remain"))
inside = [h for h in gen_toc.rendered_headings(text) if start + 1 <= h[0] <= end + 1]
print(f"step-7 block lines {start + 1}..{end + 1}; rendered headings inside: {inside}")

#!/usr/bin/env python3
"""End to end through the shipped em-dash gate: is a copied label exempt?

Usage: emdash_e2e.py <scripts-dir> <label>
Imports check_em_dash (and the walk modules beside it) from <scripts-dir>,
builds real Git base and head commits the way the head's own
`gen_toc_container_cases.em_dash_arms` does (base page: the shape with
`## Old <U+2014> heading`; head page: generated navigation copying that
label), and prints (findings, exempt) per shape. GitHub's rendering of each
shape is in the public R237-2 receipts (Old renders in none): an exemption for a heading GitHub does
not render is an ESCAPE, a refusal of one it renders is a WITHHOLD.
"""
import sys
import tempfile
from pathlib import Path

SHAPES = [
    ("R237-2 nested quote, tag at column, fence swallowed", "- item\n  > quote\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n"),
    ("R237-2 nested list, tag at column, fence swallowed", "- item\n  - nested\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n"),
    ("R237-2 plain bullet, in-item fence, later real fence", "- item\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n"),
]
SHAPES_E = [
    ("E1 inline PI carrying > then <!--", "Text <?p > <!-- ?> more.\n\n## Old\n"),
    ("E2 inline CDATA carrying > then <!--", "Text <![CDATA[ > <!-- ]]> more.\n\n## Old\n"),
    ("E5 type 4 block exposed by an empty comment", "<![CDATA[\nx <!---> y\n\n## Old\n"),
    ("E6 open quoted value after a prose comment", "t <!--\n\n<div title='\n\n## Old\n"),
    ("E3 image alt carries the closer", "<div>\n<!--\n\n![<b title=\"-->\">](u)\n\n## Old\n"),
    ("E4 link reference title carries the closer",
     "<div>\n<!--\n\n[r]: /u '<b title=\"-->\">'\n\n## Old\n"),
    ("E7 reference-only item ends at the second blank", "- [r]: /u\n\n\n    <!--\n\n## Old\n"),
    ("C2 control: closer in inline HTML", "<div>\n<!--\n\nx <b title=\"-->\">\n\n## Old\n"),
    ("C3 control: prose comment then heading", "t <!--\n\n## Old\n"),
]


def main() -> int:
    scripts, tag = sys.argv[1], sys.argv[2]
    sys.path.insert(0, scripts)
    import check_em_dash as gate
    heading = "## Old — heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    navigation = ("## Contents\n\n"
                  "- **[Old — heading](#old--heading)** -- Copied.\n"
                  "- **[Alpha](#alpha)** -- What alpha holds.\n"
                  "- **[Beta](#beta)** -- What beta holds.\n"
                  "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    with tempfile.TemporaryDirectory(prefix="r237-3.emdash.") as work:
        repo = Path(work)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for i, (_, page) in enumerate(SHAPES):
            (repo / f"page{i}.md").write_text(
                "# Page\n\n" + page.replace("## Old\n", heading) + tail, encoding="utf-8")
        base = gate._commit(repo, "base")
        for i in range(len(SHAPES)):
            (repo / f"page{i}.md").write_text("# Page\n\n" + navigation + heading + tail,
                                              encoding="utf-8")
        gate._commit(repo, "head")
        for i, (name, _) in enumerate(SHAPES):
            verdict = gate.Verdict()
            gate.judge_page(repo, base, gate.Change(f"page{i}.md", f"page{i}.md"), verdict)
            print(f"walk={tag} findings={len(verdict.findings)} exempt={verdict.exempt} | {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

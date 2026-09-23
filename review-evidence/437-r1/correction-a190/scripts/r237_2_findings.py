#!/usr/bin/env python3
"""R237-2's own rows at the lane's HEAD: every REGRESSION row of its two
render receipts (F1, F2), its F3 and S1 pages, and the em-dash verdict of
its three escape shapes through real Git commits and the shipped gate.

Usage: r237_2_findings.py OUT.json
"""
import json, sys, tempfile
from pathlib import Path

PKT = Path("$REVIEWS/437-a190-packet")
LANE = "$LANES/437-container-paragraph-scopes"
R237 = PKT / "inputs/review-evidence/437-r1/reviews/R237-2/receipts"
sys.path.insert(0, f"{LANE}/scripts")
import gen_toc  # noqa: E402
sys.modules.setdefault("gen_toc", gen_toc)
import check_em_dash as gate  # noqa: E402

ESCAPES = ["- item\n  > quote\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n",
           "- item\n  - nested\n  <span>\n  ```\n\n## Old\n\n## Real\n",
           "- item\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n"]
F3 = ["-\n  <span>\n  ```\n\n## Old\n\n## Real\n",
      "-\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n"]
S1 = ["- item\n\n    <!--\n\n## Old\n\n## Real\n", "- item\n\n    <div><!--\n\n## Old\n\n## Real\n"]


def walk(page):
    return [[lvl, raw] for lvl, raw, _ in gen_toc.headings(page)]


def rows_of(name):
    d = json.loads((R237 / name).read_text())
    return d["rows"] if isinstance(d, dict) else d


def emdash(pages):
    heading = "## Old — heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    nav = ("## Contents\n\n- **[Old — heading](#old--heading)** -- Copied.\n"
           "- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n"
           "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for i, page in enumerate(pages):
            (repo / f"p{i}.md").write_text("# Page\n\n" + page.replace("## Old\n", heading)
                                            .replace("\n## Real\n", "") + tail, encoding="utf-8")
        base = gate._commit(repo, "base")
        for i in range(len(pages)):
            (repo / f"p{i}.md").write_text("# Page\n\n" + nav + heading + tail, encoding="utf-8")
        gate._commit(repo, "head")
        for i, page in enumerate(pages):
            v = gate.Verdict()
            gate.judge_page(repo, base, gate.Change(f"p{i}.md", f"p{i}.md"), v)
            out.append({"page": page, "findings": v.findings, "exempt": v.exempt})
    return out


def main():
    report, bad = {}, 0
    for name, finding in (("combinatorial-render.json", "F1"), ("comment-rule-render.json", "F2")):
        rows = [r for r in rows_of(name) if r["class"] == "REGRESSION"]
        agree = [r for r in rows if walk(r["page"]) == r["rendered"]]
        col0 = [r for r in rows if walk(r["page"]) != r["rendered"]]
        report[finding] = {"source": name, "regression_rows": len(rows), "agree_at_head": len(agree),
                           "disagree_at_head": [{"page": r["page"], "rendered": r["rendered"],
                                                 "head": walk(r["page"])} for r in col0]}
        print(f"R237-2 {finding}: {len(rows)} REGRESSION rows of {name}; {len(agree)} agree at HEAD, "
              f"{len(col0)} disagree")
    cache = {}
    for n in ("fixture-rerender-compare.txt",):
        pass
    for label, pages in (("F3", F3), ("S1", S1)):
        report[label] = [{"page": p, "head": walk(p)} for p in pages]
        print(f"R237-2 {label}: " + "; ".join(f"{p!r} -> {walk(p)}" for p in pages))
    report["emdash_escapes"] = emdash(ESCAPES)
    for row in report["emdash_escapes"]:
        print(f"em-dash {row['page']!r}: findings={len(row['findings'])} exempt={row['exempt']}")
    Path(sys.argv[1]).write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

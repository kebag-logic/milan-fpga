#!/usr/bin/env python3
"""End-to-end em-dash probe: for each page shape, build a real Git base
commit carrying the shape with `## Old <U+2014> heading`, and a head commit
whose Contents block copies that label; then ask the revision's shipped gate
(`check_em_dash.judge_page`) for its findings and exemptions.

Usage: emdash_e2e.py <scripts-dir>    (prints one line per shape)
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import check_em_dash as gate  # noqa: E402

SHAPES = [
    ("angle destination, fence", "- [a]: <u>\n\n\n  ```\n## Old\n```\n"),
    ("single-quoted title, div", "- [a]: /u 't'\n\n\n  <div>\n## Old\n"),
    ("multi-line destination, pre", "1. [a]:\n   /u\n\n\n   <pre>\n## Old\n</pre>\n"),
    ("paren title, span", "- [a]: /u (t)\n\n\n  <span>\n## Old\n  </span>\n"),
    ("control: bare destination, fence", "- [a]: /u\n\n\n  ```\n## Old\n```\n"),
]
HEADING = "## Old — heading\n"
TAIL = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
NAV = ("## Contents\n\n- **[Old — heading](#old--heading)** -- Copied.\n"
       "- **[Alpha](#alpha)** -- What alpha holds.\n- **[Beta](#beta)** -- What beta holds.\n"
       "- **[Gamma](#gamma)** -- What gamma holds.\n\n")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="r237-4.emdash.") as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for i, (_, page) in enumerate(SHAPES):
            (repo / f"page{i}.md").write_text("# Page\n\n" + page.replace("## Old\n", HEADING) + TAIL, encoding="utf-8")
        base = gate._commit(repo, "base")
        for i in range(len(SHAPES)):
            (repo / f"page{i}.md").write_text("# Page\n\n" + NAV + HEADING + TAIL, encoding="utf-8")
        gate._commit(repo, "head")
        for i, (name, _) in enumerate(SHAPES):
            verdict = gate.Verdict()
            gate.judge_page(repo, base, gate.Change(f"page{i}.md", f"page{i}.md"), verdict)
            why = "mirrors no heading" if any("mirrors no heading" in f for f in verdict.findings) else "-"
            print(f"{name}: findings={len(verdict.findings)} exempt={verdict.exempt} reason={why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

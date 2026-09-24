#!/usr/bin/env python3
"""Reviewer probe: what `gen_toc.py --check` and `--write` do to a page that
carries a hand-written Contents block and that the renderer reads as
rendering nothing without `refusals()` naming it.

Pages: a control, the attribute spelled literally in inline code (named by
`refusals()`), through a backslash escape and a character reference (not
named), and block quotes nested 199+1 and 201+1 deep.

Usage: check_write_unrefused.py PYTHON HEAD_TREE WORK_DIR
(HEAD_TREE is a `git archive <rev> scripts tools/markdown` extraction; it
is copied, never modified.)
"""
import shutil
import subprocess
import sys
from pathlib import Path

BLOCK = ["## Contents", "", "- **[Alpha](#alpha)** -- a words",
         "- **[Beta](#beta)** -- b words", "- **[Gamma](#gamma)** -- c words",
         ""]
BODY = ["## Alpha", "", "Text.", "", "## Beta", "", "Text.", "", "## Gamma",
        "", "Text.", ""]
PAGES = {
    "control": [],
    "literal-in-code": ["Say `data-sourcepos` here.", ""],
    "escape": ["Say data\\-sourcepos here.", ""],
    "charref": ["Say &#100;ata-sourcepos here.", ""],
    "quote-199": [">" * 199 + " x", ""],
    "quote-201": [">" * 201 + " x", ""],
}


def main() -> int:
    py, head, work = sys.argv[1:]
    tree = Path(work) / "tree"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(head, tree)
    (tree / "docs").mkdir()
    for name, extra in PAGES.items():
        text = "\n".join(["# Probe", ""] + BLOCK + BODY + extra)
        page = tree / "docs" / f"{name}.md"
        page.write_text(text, encoding="utf-8")
        check = subprocess.run([py, "scripts/gen_toc.py", "--check",
                                f"docs/{name}.md"], cwd=tree,
                               capture_output=True, text=True)
        said = [l.strip() for l in check.stdout.splitlines() if l.strip()][:2]
        subprocess.run([py, "scripts/gen_toc.py", "--write",
                        f"docs/{name}.md"], cwd=tree, capture_output=True)
        after = page.read_text(encoding="utf-8")
        print(f"{name:16} check rc={check.returncode} "
              f"said={said!r} | after --write: Contents block "
              f"{'KEPT' if '## Contents' in after else 'DELETED'}, "
              f"hand-written descriptions kept "
              f"{sum(' words' in l for l in after.splitlines())}/3")
    return 0


if __name__ == "__main__":
    sys.exit(main())

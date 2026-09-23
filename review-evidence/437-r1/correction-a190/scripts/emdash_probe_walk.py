#!/usr/bin/env python3
# A190: R237-2 scripts/emdash_probe.py with the walk modules added to the copied list; nothing else changed.
"""R237-2 reviewer probe: does check_em_dash exempt a label copied from a
heading GitHub renders inside a fence?

Usage: emdash_probe.py --repo R --rev REV
Loads scripts/check_em_dash.py and scripts/gen_toc.py from `git show REV:`
into a temporary directory and replays the head arm construction of
`gen_toc_container_cases.em_dash_arms` (real Git base and head commits):
the base page carries the shape with `## Old <em dash> heading`, the head
page adds generated navigation copying that label. Prints, per shape,
(findings, exempt). An exemption for a heading GitHub does not render is an
ESCAPE; the rendered headings were recorded by probe.py.
"""
import argparse
import importlib
import subprocess
import sys
import tempfile
from pathlib import Path

F = "```"
SHAPES = [
    ("nested quote, tag at column, fence swallowed, later real fence",
     f"- item\n  > quote\n  <span>\n  {F}\n\ntext\n\n{F}\n## Old\n{F}\n"),
    ("nested list, tag at column, fence swallowed, later real fence",
     f"- item\n  - nested\n  <span>\n  {F}\n\ntext\n\n{F}\n## Old\n{F}\n"),
    ("plain bullet paragraph, tag at column, in-item fence, later real fence",
     f"- item\n  <span>\n  {F}\n\ntext\n\n{F}\n## Old\n{F}\n"),
    ("pre-existing: item comment opener at four columns after a blank",
     "- item\n\n    <!--\n\n## Old\n"),
    ("control: plain fence (renderer and walk both hide)",
     f"text\n\n{F}\n## Old\n{F}\n"),
    ("control: plain heading (renderer and walk both show)",
     "text\n\n## Old\n"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="r237emdash."))
    for name in ("check_em_dash.py", "gen_toc.py", "gen_toc_containers.py", "gen_toc_html.py"):
        got = subprocess.run(["git", "-C", a.repo, "show", f"{a.rev}:scripts/{name}"],
                             capture_output=True)
        if got.returncode:
            continue
        src = got.stdout
        (tmp / name).write_bytes(src)
    sys.path.insert(0, str(tmp))
    gate = importlib.import_module("check_em_dash")
    heading = "## Old — heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    navigation = ("## Contents\n\n"
                  "- **[Old — heading](#old--heading)** -- Copied.\n"
                  "- **[Alpha](#alpha)** -- What alpha holds.\n"
                  "- **[Beta](#beta)** -- What beta holds.\n"
                  "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    with tempfile.TemporaryDirectory(prefix="r237.emdash.") as work:
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
            print(f"rev={a.rev[:8]} findings={len(verdict.findings)} exempt={verdict.exempt} | {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

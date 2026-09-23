#!/usr/bin/env python3
"""End-to-end em-dash provenance probe through real Git commits.

Usage: emdash_probe.py <walk-root> <cases.json> <tmpdir>
For each case the BASE page carries `prefix` and then `## Old <U+2014> heading`
plus three plain sections; the HEAD page drops the prefix and adds the generated Contents block
whose first label mirrors that heading (as the shipped I437 rows do). The walk-root revision's own
check_em_dash.judge_page decides. Prints findings/exempt per case.
"""
import json
import sys
import tempfile
from pathlib import Path

root = sys.argv[1]
sys.path.insert(0, root + "/scripts")
import check_em_dash as gate  # noqa: E402

cases = json.load(open(sys.argv[2], encoding="utf-8"))
heading = "## Old — heading\n"
tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
navigation = ("## Contents\n\n"
              "- **[Old — heading](#old--heading)** -- Copied.\n"
              "- **[Alpha](#alpha)** -- What alpha holds.\n"
              "- **[Beta](#beta)** -- What beta holds.\n"
              "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
with tempfile.TemporaryDirectory(prefix="r238.emdash.", dir=sys.argv[3]) as tmp:
    repo = Path(tmp)
    gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
    for i, case in enumerate(cases):
        (repo / f"page{i}.md").write_text("# Page\n\n" + case["prefix"] + heading + tail, encoding="utf-8")
    base = gate._commit(repo, "base")
    for i, case in enumerate(cases):
        (repo / f"page{i}.md").write_text("# Page\n\n" + navigation + heading + tail, encoding="utf-8")
    gate._commit(repo, "head")
    for i, case in enumerate(cases):
        verdict = gate.Verdict()
        gate.judge_page(repo, base, gate.Change(f"page{i}.md", f"page{i}.md"), verdict)
        print(json.dumps({"name": case["name"], "findings": len(verdict.findings),
                          "exempt": verdict.exempt, "notes": verdict.findings}))

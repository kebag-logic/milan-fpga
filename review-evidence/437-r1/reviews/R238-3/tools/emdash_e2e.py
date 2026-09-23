#!/usr/bin/env python3
"""End-to-end em-dash consumer probe, through the shipped gate with real Git.

Usage: emdash_e2e.py <scripts-dir> <probes.json>
For each probe page, the base commit carries the page with `## Old` spelled
`## Old <U+2014> heading`; the head commit adds a Contents block that copies
that label. Prints the gate's (findings, exempt) per probe, the same
construction as the shipped `gen_toc_container_cases.em_dash_arms`.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True


def main() -> int:
    scripts, probes = sys.argv[1], sys.argv[2]
    sys.path.insert(0, scripts)
    import check_em_dash as gate
    rows = json.loads(Path(probes).read_text())
    heading = "## Old — heading\n"
    tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
    navigation = ("## Contents\n\n"
                  "- **[Old — heading](#old--heading)** -- Copied.\n"
                  "- **[Alpha](#alpha)** -- What alpha holds.\n"
                  "- **[Beta](#beta)** -- What beta holds.\n"
                  "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
    with tempfile.TemporaryDirectory(prefix="r238-3.emdash.") as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        for i, row in enumerate(rows):
            page = row["page"].replace("## Old\n", heading).replace("\n## Real\n", "")
            (repo / f"page{i}.md").write_text("# Page\n\n" + page + tail, encoding="utf-8")
        base = gate._commit(repo, "base")
        for i in range(len(rows)):
            (repo / f"page{i}.md").write_text("# Page\n\n" + navigation + heading + tail, encoding="utf-8")
        gate._commit(repo, "head")
        for i, row in enumerate(rows):
            verdict = gate.Verdict()
            gate.judge_page(repo, base, gate.Change(f"page{i}.md", f"page{i}.md"), verdict)
            print(f"{row['name']}: findings={len(verdict.findings)} exempt={verdict.exempt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

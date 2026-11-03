#!/usr/bin/env python3
"""Round 7's PR body with a Round 8 section and the shared sections brought to this head.

usage: python3 -I build_body.py <round 7 body> <round 8 section> <head> <docs.yml row> <out>
"""
import sys
from pathlib import Path

old, section, head, docsyml, out = sys.argv[1:6]
text = Path(old).read_text()
round8 = Path(section).read_text().replace("HEAD_SHA", head).replace("DOCSYML_ROW", Path(docsyml).read_text().strip())
edits = [
    ("[A726g]\n", "[A726h]\n"),
    ("- **[Definition of Done](#definition-of-done)**",
     "- **[Round 8](#round-8)** — Round 7's findings with both review IDs: a resume-timing matrix over every class of"
     " pass, each at its earliest and latest, alone or with a trap command; every round 7 reviewer mutant; each"
     " domain note naming its cells; an edge mutant per cell; the residue, the suggestions and the gates.\n"
     "- **[Definition of Done](#definition-of-done)**"),
    ("head `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` (round 7). Round 7's gates are in [Round 7](#round-7).",
     f"head `{head}` (round 8). Round 8's gates are in [Round 8](#round-8)."),
    ("Rounds 2 to 7 change only files round 1 changed", "Rounds 2 to 8 change only files round 1 changed"),
    ("`[A726g]` (round 7)\n", "`[A726g]` (round 7), `[A726h]` (round 8)\n"),
    ("| `scripts/process_test_support.py` | `FINISH_SECONDS`; every published mutant of the owner and the campaign"
     " that runs them (round 5) |",
     "| `scripts/process_test_support.py` | `FINISH_SECONDS`; every published mutant of the owner and the campaign"
     " that runs them (round 5); the starved owner's clock that `owner_stated_seconds` runs on (round 8) |"),
    ("`owned-process mutants: PASS (99 mutants, 96 with a control that must fail)`; `mutant lifecycle: PASS`",
     "`owned-process mutants: PASS (119 mutants, 116 with a control that must fail)`; `mutant lifecycle: PASS`"),
    ("as in [Round 7 gates](#round-7-gates)", "as in [Round 8 gates](#round-8-gates)"),
    ("and round 7 adds no measurable time.", "and rounds 7 and 8 add no measurable time."),
    ("## Definition of Done\n", round8 + "## Definition of Done\n"),
]
for before, after in edits:
    assert text.count(before) == 1, before[:80]
    text = text.replace(before, after)
Path(out).write_text(text)

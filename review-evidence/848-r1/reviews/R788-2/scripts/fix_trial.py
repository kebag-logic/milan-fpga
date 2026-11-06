#!/usr/bin/env python3
"""Show that the open Tests gaps close inside the 1000-line limit, on a disposable copy only.

Usage: python3 -I fix_trial.py HEAD_SCRIPT OUT_SCRIPT

Nothing here is a prescribed design: it only proves the required outcomes are reachable without raising the ratchet.
"""
import sys
from pathlib import Path

EDITS = [
    # A lane-file heading is graded on the lane files too, so a needle can bind an entry to its lane.
    ('if text not in (listed if text.startswith("## D0-") else rendered):',
     'if text not in (listed if text.startswith(("# D0", "## D0-")) else rendered):'),
    # F1: the copy's entry opens the reference lane's own file, under that lane's title.
    ('"## D0-002: REQUIREMENTS.md:3\\n", "## D0-001: docs/guides/A.md:3\\n\\n- Statement: resets to 0x1\\n"',
     '"# D0 findings: reference\\n\\nVerified against dev `0000000`.\\nSource lines cite dev `1111111`.\\n\\n"\n'
     '          "## D0-002: REQUIREMENTS.md:3\\n\\n- Statement: All five default to firmware.\\n"\n'
     '          "- Contradicted by: Copy of the D0-002 statement on `README.md`. `scripts/tool.py` line 1\\n",\n'
     '          "## D0-001: docs/guides/A.md:3\\n\\n- Statement: resets to 0x1\\n"'),
    # F2: the banner sits on line 16 for the arm that must not read it, and on line 15 for the arm that must.
    ('append("docs/guides/B.md", "\\n" * 15 + banner), 0, "", "is fresh"),',
     'append("docs/guides/B.md", "\\n" * 11 + banner), 0, "", "is fresh"),'),
    ('("supersession banner", append("docs/guides/B.md", banner), 1,',
     '("supersession banner", append("docs/guides/B.md", "\\n" * 10 + banner), 1,'),
    # S1 and S2: the route's second sentence, and each baseline in its own sentence.
    ('("`Located`", "--findings-dir DIR", "search misses")),',
     '("`Located`", "--findings-dir DIR", "search misses",\n          "still names its line")),'),
    ('("at dev `1111111`", "at dev `0000000`")),', '\n         ("lines at dev `1111111`", "checked at dev `0000000`")),'),
]
#: The opening line of a table or list joined to its first entry, to pay for the added lines; each stays within 120 columns.
JOINS = [
    ('OWN_HEAD = ("# Documentation audit", "",\n            "**GENERATED**', 'OWN_HEAD = ("# Documentation audit", "", "**GENERATED**'),
    ('RULES = (\n    "| Status | Rule | Evidence shown |"', 'RULES = ("| Status | Rule | Evidence shown |"'),
    ('out = list(OWN_HEAD) + ["",\n           "Regenerate', 'out = list(OWN_HEAD) + ["", "Regenerate'),
    ('return (\n        ("the README\'s statement', 'return (("the README\'s statement'),
    ('controls = (\n        ("unchanged tree', 'controls = (("unchanged tree'),
]


def main():
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    for old, new in EDITS + JOINS:
        if text.count(old) != 1:
            print(f"NOT APPLIED ({text.count(old)} matches): {old[:70]}")
            continue
        text = text.replace(old, new)
    Path(sys.argv[2]).write_text(text, encoding="utf-8")
    lines = text.split("\n")
    print("lines:", text.count("\n"), "longest:", max(len(line) for line in lines))


if __name__ == "__main__":
    main()

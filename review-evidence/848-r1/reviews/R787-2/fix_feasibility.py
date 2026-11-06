#!/usr/bin/env python3
"""Apply a disposable sketch of the open findings' fixes to a copy of the script, to show they fit the limit.

Usage: fix_feasibility.py HEAD_SCRIPT OUT_SCRIPT. Never touches the reviewed clone. Not a prescribed design.
"""
import pathlib
import sys

text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
EDITS = [
    # A needle naming a lane entry is graded on the lane files, wherever in the needle the entry sits.
    ('if text not in (listed if text.startswith("## D0-") else rendered):',
     'if text not in (listed if "## D0-" in text else rendered):'),
    ('A `needle` opening `## D0-` is graded on the `--findings-dir` files alone, the only output naming a finding\'s line.',
     'A `needle` naming `## D0-` is graded on the `--findings-dir` files alone, the only output with a finding\'s line.'),
    # The copy opens its own lane's file, straight after that file's baselines, so a misfiled entry fails the needle.
    ('"## D0-002: REQUIREMENTS.md:3\\n", "## D0-001: docs/guides/A.md:3\\n\\n- Statement: resets to 0x1\\n"\n',
     '"`.\\n\\n## D0-002: REQUIREMENTS.md:3\\n", "## D0-001: docs/guides/A.md:3\\n\\n- Statement: resets to 0x1\\n"\n'),
    # The window's two edges: a banner on line 15 is read, one on line 16 is not.
    ('("supersession banner", append("docs/guides/B.md", banner), 1,', '("supersession banner", append("docs/guides/B.md", "\\n" * 10 + banner), 1,'),
    ('("a banner past line 15 is not read", append("docs/guides/B.md", "\\n" * 15 + banner), 0, "", "is fresh"),',
     '("a banner past line 15 is not read", append("docs/guides/B.md", "\\n" * 11 + banner), 0, "", "is fresh"),'),
    # Both route sentences on one needle.
    ('("`Located`", "--findings-dir DIR", "search misses")', '("`Located`", "--findings-dir DIR", "copy.\\nThat")'),
]
for old, new in EDITS:
    if text.count(old) != 1:
        raise SystemExit(f"no unique match: {old[:70]!r}")
    text = text.replace(old, new)
pathlib.Path(sys.argv[2]).write_text(text, encoding="utf-8")

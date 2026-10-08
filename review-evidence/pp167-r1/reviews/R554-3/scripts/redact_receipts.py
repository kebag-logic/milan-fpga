#!/usr/bin/env python3
"""Replace host path prefixes in receipt logs with neutral placeholders; result lines are untouched.
usage: redact_receipts.py FILE..."""
import sys
SUBS = (("$REVIEWS/pp167-r554-3-packet", "<PACKET>"),
        ("$VALIDATION_TOOLS/pinned-verilator-5.050", "<PINNED_VERILATOR>"),
        ("$WORKSPACE_HOME/.local/share", "<TOOLROOT>"))
for p in sys.argv[1:]:
    s = open(p).read()
    for a, b in SUBS:
        s = s.replace(a, b)
    open(p, "w").write(s)

#!/usr/bin/env python3
"""R296-2: replace host-specific paths in receipts with neutral placeholders.

The host paths come from the environment (PACKET, REVIEW_CLONE, PINNED_TOOLS,
DATA_ROOT, HOME), so this script carries none of them.
Usage: PACKET=... REVIEW_CLONE=... PINNED_TOOLS=... DATA_ROOT=... redact.py FILE...
"""

import os
import sys
from pathlib import Path

SUBS = [(os.environ[k], f"<{k}>") for k in
        ("PACKET", "REVIEW_CLONE", "PINNED_TOOLS", "DATA_ROOT", "HOME")
        if os.environ.get(k)]

for name in sys.argv[1:]:
    p = Path(name)
    s = p.read_text(errors="replace")
    for a, b in SUBS:
        s = s.replace(a, b)
    p.write_text(s)

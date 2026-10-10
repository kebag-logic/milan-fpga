#!/usr/bin/env python3
"""Reviewer check of a prior SUGGESTION: plant `led_tag_r <= 1` (stuck-at-1)
and `led_tag_r <= 0` (stuck-at-0) in private copies and run gptp_tables.
Usage: python3 -I tag_probe.py <repo> <workdir>   (reuses extra_mutants.py)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import extra_mutants as em  # noqa: E402
OLD = "      led_tag_r [led_tail_w] <= alloc_tagged_i;"
em.CONTROLS = [
    ("ledger_tag_stuck_1", em.RET, OLD, "      led_tag_r [led_tail_w] <= 1'b1;",
     "prior finding says this survives"),
    ("ledger_tag_stuck_0", em.RET, OLD, "      led_tag_r [led_tail_w] <= 1'b0;",
     "ledger lockstep fails"),
]
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], "2"]
sys.exit(em.main())

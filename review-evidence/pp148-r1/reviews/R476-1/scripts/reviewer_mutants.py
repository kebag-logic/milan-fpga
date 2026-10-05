#!/usr/bin/env python3
"""Reviewer R476-1 disposable controls for issue #148, run through the lane's own
driver (tb/pp_top/notify_mutants.py) so the verdict rule is the lane's.

Usage: reviewer_mutants.py TREE OUTDIR VERILATOR JOBS [NAME ...]
TREE is an extracted copy of the processor at the head; its notify_mutants.py
is extended IN THAT COPY ONLY with the controls below, then run with --only.
Each control is run against every suite that could grade it; the named check
is the one the review expects to fail, and a SURVIVED verdict is the finding.
"""
import subprocess
import sys
from pathlib import Path

tree, out, verilator, jobs = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
drv = tree / "tb/pp_top/notify_mutants.py"

EXTRA = r'''
_WIN = ("            && (!ctr_sent_r[c]\n"
        "                || ((now_ms_i - ctr_last_r[c]) >= 32'd1000))) begin\n")
_WIN999 = _WIN.replace("32'd1000", "32'd999")
_STAMP_SLOT0 = STAMP.replace("ctr_last_r[em_ctr_ix_r]", "ctr_last_r[CTX_W_C'(0)]")
_STAMP_ANY = STAMP.replace("if (em_kind_r == PP_UNS_CTRS_C) ", "")
REVIEW = (
    Mutant("r476_window_999_tw", INDEX, ((NTFY, _WIN, _WIN999),), ("TW1:", "TW2:")),
    Mutant("r476_window_999_cs", SPACING, ((NTFY, _WIN, _WIN999),), ("CS2a:",)),
    Mutant("r476_window_999_st", NOTIFY, ((NTFY, _WIN, _WIN999),), ("ST2b:",)),
    Mutant("r476_stamp_slot0_tw", INDEX, ((NTFY, STAMP, _STAMP_SLOT0),), ("TW1:", "TW2:")),
    Mutant("r476_stamp_slot0_cs", SPACING, ((NTFY, STAMP, _STAMP_SLOT0),), ("CS2b:",)),
    Mutant("r476_stamp_any_kind_tw", INDEX, ((NTFY, STAMP, _STAMP_ANY),), ("TW1:",)),
    Mutant("r476_stamp_any_kind_st", NOTIFY, ((NTFY, STAMP, _STAMP_ANY),), ("ST2:",)),
)
MUTANTS = MUTANTS + REVIEW
'''

text = drv.read_text()
anchor = "TALLY = re.compile("
assert text.count(anchor) == 1
drv.write_text(text.replace(anchor, EXTRA + "\n" + anchor, 1))
names = sys.argv[5:] or ["r476_window_999_tw", "r476_window_999_cs", "r476_window_999_st",
                         "r476_stamp_slot0_tw", "r476_stamp_slot0_cs",
                         "r476_stamp_any_kind_tw", "r476_stamp_any_kind_st"]
rc = subprocess.run([sys.executable, str(drv), "--output", out, "--verilator", verilator,
                     "--jobs", jobs, "--only", *names]).returncode
sys.exit(rc)

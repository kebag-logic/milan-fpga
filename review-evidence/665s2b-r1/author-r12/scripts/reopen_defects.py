#!/usr/bin/env python3
"""Plant only the two-pass reset's defects through srp_mutants.campaign, for a quick look before the full campaign."""
import sys
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(ROOT / 'sw/firmware/ctrl/test'), str(ROOT / 'sw/firmware/gtest')]
import srp_mutants
import srp_reopen_mutants
srp_mutants.DEFECTS = srp_reopen_mutants.defects(srp_mutants.Defect)
out = Path(sys.argv[2])
raise SystemExit(1 if srp_mutants.campaign(out, ROOT / 'third_party/lwSRP', 4, int(sys.argv[3])) else 0)

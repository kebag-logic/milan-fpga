#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run ctrl_srp_image.py unchanged, its fixture sources read from a variant directory.

The first argument is the directory build.py's variant_fixture wrote; the rest
are ctrl_srp_image.py's own arguments. Only the module's HERE, the directory
it reads ctrl_aecp_image.c (and the flat-layout fixture) from, changes.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

if __name__ == '__main__':
    sys.path[:0] = [str(ROOT / 'sw/firmware/ctrl/test'), str(ROOT / 'sw/firmware/gtest')]
    import ctrl_srp_image
    ctrl_srp_image.HERE = Path(sys.argv[1])
    sys.argv = [str(ROOT / 'sw/firmware/ctrl/test/ctrl_srp_image.py'), *sys.argv[2:]]
    raise SystemExit(ctrl_srp_image.main())

#!/usr/bin/env python3
"""Use the exact image recipe; select the actual base source population."""
import sys
from pathlib import Path
repo=Path(sys.argv.pop(1))
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import ctrl_image
if '--without-srp' in sys.argv:
    ctrl_image.PORTABLE=tuple(p for p in ctrl_image.PORTABLE if not p.startswith('maap/'))
raise SystemExit(ctrl_image.main())

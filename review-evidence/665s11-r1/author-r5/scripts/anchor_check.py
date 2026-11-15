#!/usr/bin/env python3
"""anchor_check.py TREE: every AECP campaign defect (aecp_mutants.DEFECTS, its row tables included) has exactly one
planting site in TREE's sources, as the campaign requires before it plants; prints those that do not and exits 1."""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / 'sw/firmware/ctrl/test'), str(tree / 'sw/firmware/gtest')]
import aecp_mutants as m  # noqa: E402

ctrl = tree / 'sw/firmware/ctrl'
bad = [(d.name, d.path, (ctrl / d.path).read_text().count(d.old)) for d in m.DEFECTS
       if (ctrl / d.path).read_text().count(d.old) != 1]
print(f'{len(m.DEFECTS)} defects; {len(bad)} without exactly one planting site: {bad}')
sys.exit(1 if bad else 0)

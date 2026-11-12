#!/usr/bin/env python3
"""arcs.py CHECKOUT KEEP_DIR FILE: the firmware coverage gate's own gcov reader over a kept coverage build
(fw_coverage.py --keep), printing each line of FILE with an unexecuted line or an untaken arc, its arcs in gcov's
order (counts), and the source line."""
import sys
from pathlib import Path
root, keep, rel = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import fw_coverage  # noqa: E402
merged = fw_coverage.collect([keep])
src = merged[rel]
text = (root / rel).read_text().splitlines()
for n in sorted(src.lines):
    ln = src.lines[n]
    if ln.count == 0 or any(a == 0 for a in ln.arcs):
        print(f'{n:5d} count={ln.count} arcs={ln.arcs} | {text[n - 1].strip()}')

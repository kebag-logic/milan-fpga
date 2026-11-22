#!/usr/bin/env python3
"""boundary_census.py CTRL_TEST_DIR: the firmware builders found by text (ctrl_configs.checkout_builders) that none
of ctrl_configs.BUILDERS, PART_OF, OUTSIDE or SUITES classifies, i.e. those ctrl_boundary.py's held() refuses unless
a capture shows them compiling. Exit 1 when any is found."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import ctrl_configs as c  # noqa: E402

known = {b.path for b in c.BUILDERS}
bad = []
for path, text in c.builder_texts().items():
    name = c.rel(path)
    if name in known or name in c.OUTSIDE or name in c.SUITES or name in c.PART_OF:
        continue
    bad.append((name, "program" if c.program(path, text) else "module"))
for name, kind in bad:
    print(f"UNCLASSIFIED {kind}: {name}")
print(f"{len(bad)} unclassified builder(s) found by text")
sys.exit(1 if bad else 0)

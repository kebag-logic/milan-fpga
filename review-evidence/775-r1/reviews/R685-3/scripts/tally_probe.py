#!/usr/bin/env python3
"""Feed avtp_rxmon logs through the tree's own scripts/suite_tally.scan and
print the parsed tally lines. usage: tally_probe.py <tree> <log>..."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import suite_tally  # noqa: E402
for log in sys.argv[2:]:
    c, f, matched, unparsed, skipped = suite_tally.scan(Path(log).read_text(errors="replace"))
    print(f"== {Path(log).parent.name}/{Path(log).name}: checks {c} failures {f} unparsed {len(unparsed)}")
    for name, cc, ff, line in matched:
        print(f"   {name}: {cc}/{ff} :: {line[:110]}")
    for u in unparsed:
        print(f"   UNPARSED :: {u[:110]}")

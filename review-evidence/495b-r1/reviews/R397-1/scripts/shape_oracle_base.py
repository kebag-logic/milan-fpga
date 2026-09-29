#!/usr/bin/env python3
"""Control for shape_oracle.py: the base (eaa88a32) MAC parser must disagree
with the disposition oracle, proving the comparison can fail.
Usage: shape_oracle_base.py <base-tree>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import shape_oracle as so
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
def base_mac_shape(s):
    try:
        eb._mac48(s, "f")
    except eb.ConfigError as exc:
        m = str(exc)
        return not ("is not a MAC-48" in m or "out of MAC-48 range" in m)
    return True
bad = [s for s in so.structured() if so.oracle_mac_shape(s) != base_mac_shape(s)]
for s in ("2", "-2", "0:2", " 020000000002", "+020000000002"):
    print(f"base {s!r}: {'accept' if base_mac_shape(s) else 'refuse'}")
print(f"base disagreements over {len(so.structured())} structured spellings: {len(bad)}")
sys.exit(0 if bad else 1)

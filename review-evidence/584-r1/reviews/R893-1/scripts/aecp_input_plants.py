"""Run only the #584 AECP input-port plants (aecp_input_mutants.ROWS) through the repository's own campaign.
Usage: python3 aecp_input_plants.py <repo> <outdir>"""
import sys
from pathlib import Path
repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_mutants as m
import aecp_input_mutants as im
m.controls()                      # the full table's own controls first
names = {row[0] for row in im.ROWS}
m.DEFECTS = tuple(d for d in m.DEFECTS if d.name in names)
assert len(m.DEFECTS) == len(im.ROWS), m.DEFECTS
m.controls = lambda: None
print("plants:", [d.name for d in m.DEFECTS], flush=True)
escaped = m.campaign(out, jobs=8, stack=(repo / "third_party/tsn-c-stack").resolve())
print("ESCAPED" if escaped else "ALL CAUGHT")
sys.exit(int(escaped))

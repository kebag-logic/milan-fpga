"""Run aecp_mutants.campaign on the #763 defects only, after the full table's own controls pass."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import aecp_mutants
aecp_mutants.controls()
names = ("nvm-empty-map-keeps-defaults", "nvm-unused-payload-reads-erased")
aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
assert len(aecp_mutants.DEFECTS) == 2
aecp_mutants.controls = lambda: None
sys.exit(int(aecp_mutants.campaign(Path(sys.argv[2]))))

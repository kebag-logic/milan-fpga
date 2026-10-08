from pathlib import Path
import sys
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import ctrl_mutants
from ctrl_reuse import cut_reuse
r=Path(__file__).resolve().parent
indices=[i for i,m in enumerate(ctrl_mutants.MUTANTS) if m.name=="acmp-open-unguarded"]
assert len(indices)==1
reuse=r/"reentry-oracle/reuse";cut_reuse(reuse)
raise SystemExit(ctrl_mutants.campaign(r/"reentry-oracle/mutants",reuse,4,shard=[indices[0],len(ctrl_mutants.MUTANTS)]))

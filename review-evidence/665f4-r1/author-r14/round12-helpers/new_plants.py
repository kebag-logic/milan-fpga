from pathlib import Path
import sys
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import srp_mutants
r=Path(__file__).resolve().parent
srp_mutants.DEFECTS=tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(("feedback-","r10-","p11-")))
failed=False
for n in (1,2):
 failed=srp_mutants.campaign(r/f"new-plants-if{n}",Path.cwd()/"third_party/lwSRP",4,n) or failed
raise SystemExit(failed)

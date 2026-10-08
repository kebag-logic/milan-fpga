from pathlib import Path
import sys
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import srp_mutants
r=Path(__file__).resolve().parent
names={"feedback-leave-clears-advertise-only","feedback-failed-indication-as-advertise","feedback-change-clears-both-kinds"}
srp_mutants.DEFECTS=tuple(d for d in srp_mutants.DEFECTS if d.name in names)
assert len(srp_mutants.DEFECTS)==3
failed=False
for n in (1,2):
 failed=srp_mutants.campaign(r/f"named-plants-if{n}",Path.cwd()/"third_party/lwSRP",4,n) or failed
raise SystemExit(failed)

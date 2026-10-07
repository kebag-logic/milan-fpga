import os,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import srp_mutants
original=srp_mutants.arm_srp
def arm(tree,lwsrp,interfaces,**kwargs):
 return original(tree,lwsrp,1,**kwargs)
srp_mutants.arm_srp=arm
srp_mutants.DEFECTS=srp_mutants.DEFECTS[90:]
raise SystemExit(srp_mutants.campaign(Path(os.environ["SCRATCH"])/"new-plants-if1",Path.cwd()/"third_party/lwSRP",4))

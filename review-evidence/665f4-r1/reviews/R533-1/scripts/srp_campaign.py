#!/usr/bin/env python3
import sys,pathlib
repo=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
import srp_mutants,ctrl_mutants
from ctrl_build import Refusal
failed=srp_mutants.campaign(packet/'scratch/srp-campaign',repo/'third_party/lwSRP',4)
failed=bool(ctrl_mutants.lwsrp_pin_arms(packet/'scratch/pin-controls',repo/'third_party/lwSRP')) or failed
print('R533 SRP campaign complete:', 'FAIL' if failed else 'PASS',flush=True)
sys.exit(1 if failed else 0)

"""cut_plants.py CLONE OUT: the SRP cut's planted defects (srp_reclaim_mutants.PREFIX) through srp_mutants.campaign
as test_ctrl_firmware.run_srp_mutants runs them: at two interfaces (each at its entity, 8x8/2if), then at 1x1/1if and
8x8/1if. Scratch only."""
import sys
from pathlib import Path
clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import srp_mutants  # noqa: E402
import srp_reclaim_mutants  # noqa: E402
lwsrp = clone / "third_party/lwSRP"
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(srp_reclaim_mutants.PREFIX))
print(len(srp_mutants.DEFECTS), "defects", flush=True)
failed = srp_mutants.campaign(out / "if2", lwsrp, 4)
failed = srp_mutants.campaign(out / "if1", lwsrp, 4, 1) or failed
failed = srp_mutants.campaign(out / "8x8-if1", lwsrp, 4, 1, srp_reclaim_mutants.ENTITY) or failed
print("FAILED" if failed else "ALL CAUGHT")
sys.exit(1 if failed else 0)

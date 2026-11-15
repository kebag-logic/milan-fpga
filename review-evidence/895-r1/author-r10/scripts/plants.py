#!/usr/bin/env python3
"""plants.py TREE OUT PREFIX [INTERFACES...]: the SRP campaign (srp_mutants.campaign) of TREE with its defect table cut
to the names starting with PREFIX, at each interface count given (2: the two-interface campaign, each Talker defect at
its 8x8/2if entity; 1: the one-interface campaign at 1x1/1if), as test_ctrl_firmware.run_srp_mutants runs them. Exit
1 when any planted defect escaped or was refused."""
import sys
from pathlib import Path

tree_root, out, prefix = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
counts = [int(a) for a in sys.argv[4:]] or [2, 1]
sys.path.insert(0, str(tree_root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree_root / 'sw/firmware/gtest'))
import srp_mutants  # noqa: E402

lwsrp = (tree_root / 'third_party/lwSRP').resolve()
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(prefix))
print(f"{len(srp_mutants.DEFECTS)} defects: {', '.join(d.name for d in srp_mutants.DEFECTS)}", flush=True)
failed = False
for n in counts:
    failed = srp_mutants.campaign(out / f"if{n}", lwsrp, 4, n) or failed
print(f"plants {prefix} at {counts}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)

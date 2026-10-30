#!/usr/bin/env python3
"""Run only the builder's bare-metal profile contract (the enable choke-point
data-flow census) at the checkout given as argv[1], with the pinned RV32 SDK."""
import sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.argv = [str(repo / 'sw/builder/test_builder.py'), '--require-rv32']
sys.path.insert(0, str(repo / 'sw/builder'))
import test_builder  # noqa: E402
test_builder.test_baremetal_profile_contract()
print('CHOKE_POINT_GATE: test_baremetal_profile_contract passed')

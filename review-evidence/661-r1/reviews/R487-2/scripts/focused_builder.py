#!/usr/bin/env python3
"""Run only the affected boundary gates, never the full builder bank."""
from pathlib import Path
import sys

root, scratch = (Path(arg).resolve() for arg in sys.argv[1:])
sys.path.insert(0, str(root / "sw/builder"))
import test_builder as test
test.OUT = scratch / "builder-output"
for function in (test.test_name_count_fits_the_nvm_name_block,
                 test.test_shipping_image_contract,
                 test.test_soc_shipping_image_contract,
                 test.test_shipping_image_contract_presence):
    print("RUN " + function.__name__, flush=True)
    function()
    print("PASS " + function.__name__, flush=True)
assert not test.SKIPPED, test.SKIPPED
print("FOCUSED BUILDER: 4 gates PASS; no skipped arms")

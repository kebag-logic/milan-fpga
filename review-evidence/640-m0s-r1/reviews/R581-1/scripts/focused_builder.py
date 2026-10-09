#!/usr/bin/env python3
"""Run only the builder's resource and shipping-image checks, outside the full bank."""
import importlib.util
from pathlib import Path
import sys

root, scratch = map(lambda x: Path(x).resolve(), sys.argv[1:3])
sys.path.insert(0, str(root / "sw/builder"))
spec = importlib.util.spec_from_file_location("review_builder", root / "sw/builder/test_builder.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.OUT = scratch / "builder-output"
module.OUT.mkdir(parents=True, exist_ok=True)
for name in (
    "test_resource_determinism", "test_resource_verdicts",
    "test_optional_blocks_default_present", "test_optional_block_prune_accounting",
    "test_shipping_image_contract", "test_soc_shipping_image_contract",
    "test_shipping_image_contract_presence", "test_pp_shadow_audio_unit_rates_match_config",
):
    print(name, flush=True)
    getattr(module, name)()
assert not module.SKIPPED, module.SKIPPED
print("PASS: 8 focused builder checks; full bank and physical calibration NOT RUN")

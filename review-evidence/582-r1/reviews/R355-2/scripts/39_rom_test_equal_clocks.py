#!/usr/bin/env python3
"""Reviewer probe: run the head's test_gptp_rom_clock over a builder-accepted
variant whose sys_clk_hz equals milan_clk_hz (the 1x1 at 50/50 MHz).

Usage: 39_rom_test_equal_clocks.py <head-tree> <scratch-dir>
Records whether the builder accepts the variant and whether the test passes.
"""
import sys
from pathlib import Path

import yaml

TREE, X = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
X.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(TREE / "sw/builder"))
import endstation_builder as eb  # noqa: E402
import test_clock_contract as t  # noqa: E402

raw = yaml.safe_load((TREE / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
raw["board"]["constraints"]["sys_clk_hz"] = raw["board"]["constraints"]["milan_clk_hz"]
variant = X / "endstation_equal_clocks.yaml"
variant.write_text(yaml.safe_dump(raw))
cfg = eb.load_config(variant)
print(f"builder accepts the variant: sys {cfg['constraints']['sys_clk_hz']} milan {cfg['constraints']['milan_clk_hz']}")
t.CONFIGS = [variant]
try:
    t.test_gptp_rom_clock()
    print("test_gptp_rom_clock: PASS")
except AssertionError as exc:
    print(f"test_gptp_rom_clock: FAIL: {exc}")

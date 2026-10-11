#!/usr/bin/env python3
"""soc_gates.py CLONE - run only the test_builder.py gates that elaborate
sw/litex/milan_soc.py (every gate that asks _litex_or_skip or
_instance_params), from CLONE, with the --require-elaboration verdict.

A focused subset, not the builder bank: these are the gates whose input the
composition changes (milan_soc.py carries both the M2 crossings and the
mailbox window's publication ports).
"""
import importlib.util
import os
import sys

clone = os.path.abspath(sys.argv[1])
builder = os.path.join(clone, "sw/builder")
os.chdir(clone)
sys.path.insert(0, builder)
sys.argv = [os.path.join(builder, "test_builder.py"), "--require-elaboration"]
spec = importlib.util.spec_from_file_location("test_builder", sys.argv[0])
tb = importlib.util.module_from_spec(spec)
sys.modules["test_builder"] = tb
spec.loader.exec_module(tb)

GATES = (
    "test_datapath_params_match_the_instance",
    "test_datapath_params_gate_bites",
    "test_every_recipe_elaborates",
    "test_recipe_smoke_gate_bites",
    "test_optional_blocks_reach_the_instance",
    "test_optional_block_instance_gate_bites",
    "test_optional_block_consumption_gate_bites",
    "test_gptp_plane_reaches_the_instance",
    "test_gptp_plane_instance_gate_bites",
    "test_clock_plan_reaches_the_instance",
    "test_clock_plan_instance_gate_bites",
    "test_clock_crossing_constraints",
    "test_commercial_timing_grade",
    "test_soc_option_refusals",
    "test_toolchain_patches_are_applied",
    "test_toolchain_patch_gate_bites",
)
for name in GATES:
    print(f"{name}:", flush=True)
    getattr(tb, name)()
print(f"{len(GATES)} gate(s) run")
if tb.SKIPPED:
    for gate, why, _kind in tb.SKIPPED:
        print(f"  SKIP [{gate}] {why}")
sys.exit(tb._require_elaboration_verdict(tb.SKIPPED))

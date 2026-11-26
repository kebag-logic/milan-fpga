#!/usr/bin/env python3
"""Reviewer control: run the campaign dispatch proof (campaign_cases) for each divided phase of a checkout,
and report which mutation partition main() would hand each leg. Usage: probe_dispatch.py CHECKOUT"""
import sys, argparse
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import test_ctrl_firmware as drv
import test_ctrl_firmware_shards as proof
rc = 0
for phase, count in ((1, 4), (2, 2), (3, 2)):
    try:
        with redirect_stdout(StringIO()):
            proof.campaign_cases(drv, (phase, 4), count)
        print(f"phase {phase}/4 legs {count}: proof PASS")
    except AssertionError as exc:
        rc = 1
        print(f"phase {phase}/4 legs {count}: proof REFUSED: {str(exc)[:160]}")
# What main() hands the run for a leg: stop at the first mutation partition consumer.
seen = {}
def capture(args, *a, **k):
    seen["mutation_shard"] = args.mutation_shard
    return False
with mock.patch.object(proof, "campaign_cases", lambda *a, **k: None), \
     mock.patch.object(proof, "run_cases", lambda *a, **k: None), \
     mock.patch.object(drv, "run_selected", capture), \
     mock.patch.object(drv, "Tree", lambda *a, **k: argparse.Namespace(reuse=None)), \
     mock.patch.object(drv, "stack_pin", lambda *a, **k: "stub"), \
     mock.patch.object(drv, "cut_reuse", lambda *a, **k: None), \
     mock.patch.object(drv.fw_gtest, "toolchain", lambda *a, **k: "stub"):
    with redirect_stdout(StringIO()):
        drv.main(["--shard", "1/4", "--self-test", "--campaign-shard", "1", "4"])
print("main() leg 1/4 of phase 1 hands mutation_shard =", seen.get("mutation_shard", "<not reached>"))
sys.exit(rc)

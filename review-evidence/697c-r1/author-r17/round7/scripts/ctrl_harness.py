"""Scratch harness (round 7): run the gate's controls against a base made of the gate's own image-builder runs,
with a stand-in invocation for every other builder, so the control machinery can be exercised without the
40-minute firmware steps. Not the gate; never committed.

usage: ctrl_harness.py <checkout> <work> [name-substring ...]
"""
import sys
import time
from dataclasses import replace
from pathlib import Path

checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(checkout / "sw/firmware/ctrl/test"), str(checkout / "sw/firmware/gtest")]

import ctrl_boundary  # noqa: E402
import ctrl_capture  # noqa: E402
import ctrl_configs  # noqa: E402
import ctrl_plants  # noqa: E402
import ctrl_runs  # noqa: E402

wanted = sys.argv[3:]
cap = work / "base-capture"
start = time.monotonic()
if not (cap / "records.jsonl").is_file():
    print("\n".join(ctrl_runs.owned(cap, work / "images")), flush=True)
base = ctrl_capture.load(cap)
print(f"base: {len(base.invocations)} invocations, {time.monotonic() - start:.0f} s", flush=True)
stand_in = ctrl_capture.Invocation("cc", (), str(checkout), (), None, "", (),
                                   frozenset(b.path for b in ctrl_configs.BUILDERS) |
                                   frozenset(ctrl_configs.rel(p) for p in ctrl_configs.builder_texts()))
base = base + ctrl_capture.Capture((), (), (stand_in,), ())
scope = ctrl_configs.Scope(frozenset({"verilator"}))
if wanted:
    ctrl_plants.PLANTS = tuple(p for p in ctrl_plants.PLANTS if any(w in p.name for w in wanted))
    ctrl_boundary.PLANTS = ctrl_plants.PLANTS
start = time.monotonic()
bad, count = ctrl_boundary.controls(work / "controls", base, scope)
print(f"controls: {count} run, {bad} misbehaved, {time.monotonic() - start:.0f} s")

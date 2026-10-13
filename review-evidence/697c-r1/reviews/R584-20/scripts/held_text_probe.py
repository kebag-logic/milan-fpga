#!/usr/bin/env python3
"""held_text_probe.py <tree>: run the boundary gate's own ctrl_configs.held() over a
stand-in capture that holds every known builder's run and no compile, so the only
refusals it can return are the text cross-check's. A program that names the
firmware's tree and is in none of BUILDERS, PART_OF, OUTSIDE, SUITES is refused
whatever a capture holds; exits 1 if there is any such program. Read-only: it writes nothing in <tree>."""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree / "sw/firmware/gtest"))
import ctrl_configs  # noqa: E402
from ctrl_build import Refusal  # noqa: E402


class StandIn:
    """A capture holding every known builder's own run, and no compile."""
    ran = frozenset(b.path for b in ctrl_configs.BUILDERS)
    builders = frozenset()
    bypassed = ()
    leaves = ()


print(f"tree: {tree}")
print(f"known builders: {len(ctrl_configs.BUILDERS)}: " + ", ".join(str(b.path) for b in ctrl_configs.BUILDERS))
found = [p for p in ctrl_configs.builder_texts()]
print(f"builders found by text: {len(found)}")
try:
    ctrl_configs.held(StandIn(), ctrl_configs.Scope())
except Refusal as refusal:
    reasons = str(refusal).split("; ")
    for reason in reasons:
        print("REFUSED:", reason)
    programs = [r for r in reasons if "and is a program" in r]
    print(f"program refusals (independent of what any capture holds): {len(programs)}")
    for reason in programs:
        print("  PROGRAM:", reason.split(" names the firmware")[0])
    sys.exit(1 if programs else 0)
print("held: no refusal from the text cross-check")
print("program refusals (independent of what any capture holds): 0")

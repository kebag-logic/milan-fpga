#!/usr/bin/env python3
"""Count Makefile targets whose build reaches the pinned stack, per Makefile, using
the checkout's own ctrl_pin.stack_targets and ctrl_boundary.makefiles.
Usage: count_stack_targets.py <checkout>"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_boundary, ctrl_pin
out = {}
for mk in ctrl_boundary.makefiles():
    reaching, pins, findings = ctrl_pin.stack_targets(mk, root / "third_party/tsn-c-stack")
    out[mk.relative_to(root).as_posix()] = {"reaching": len(reaching), "findings": len(findings)}
print(json.dumps({"total_reaching": sum(v["reaching"] for v in out.values()), "per_makefile": out}, indent=1))

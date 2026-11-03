#!/usr/bin/env python3
"""Plant one named mutant into a disposable copy of the reviewed tree.

Usage: python3 -I plant_mutants.py <copy-root> <m1|m2|m3|m4|m5|m6>
Each mutant replaces exactly one source span and refuses if the span is not unique.
"""
import pathlib
import sys

MUTANTS = {
    "m1": ("scripts/ci_gate_workflows.py", "    caches = BUILDER_CACHES.get(name)\n",
           "    return workflow\n    caches = BUILDER_CACHES.get(name)\n"),
    "m2": ("scripts/ci_gate_workflows.py",
           '        raise ValueError(name + ": a LiteX leg shares a worker with a builder leg")', "        pass"),
    "m3": ("scripts/ci_litex_legs.py", 'if type(receipt["exit"]) is not int or receipt["exit"] != 0:',
           'if receipt["exit"] != 0:'),
    "m4": ("scripts/ci_litex_legs.py", "        if executed != legs[leg]:\n", "        if False:\n"),
    "m5": ("scripts/ci_gate_workflows.py",
           "        if sorted(found for found in names if found in caches) != sorted(caches):\n",
           "        if not set(caches) <= set(names):\n"),
    "m6": ("scripts/ci_gate_workflows.py", '"Cache the Scala toolchain", "Cache the generated CPU metadata")}',
           '"Cache the Scala toolchain")}'),
}

root, name = pathlib.Path(sys.argv[1]), sys.argv[2]
path, old, new = MUTANTS[name]
text = (root / path).read_text()
if text.count(old) != 1:
    sys.exit(f"{name}: span not unique in {path}")
(root / path).write_text(text.replace(old, new))
print(f"{name}: planted in {path}")

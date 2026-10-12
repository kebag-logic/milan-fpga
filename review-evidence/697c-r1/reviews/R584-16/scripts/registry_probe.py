#!/usr/bin/env python3
"""registry_probe.py <checkout>: classify every builder the boundary gate finds by text.

Imports the checkout's own ctrl_configs (no build, no capture) and reports,
for each file that names the firmware's tree, which registry holds it. Then
removes the OUTSIDE entry added at 27ee16b5 in memory and shows the program
the text scan would refuse by name. Exit 0 when the head classifies every
program and the removal produces exactly that one refusal.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_configs as cc  # noqa: E402

SHARDS = "sw/firmware/ctrl/test/test_ctrl_firmware_shards.py"


def unclassified(outside):
    names = {b.path for b in cc.BUILDERS}
    bad = []
    for path, text in cc.builder_texts().items():
        name = cc.rel(path)
        where = ("BUILDERS" if name in names else "OUTSIDE" if name in outside else
                 "SUITES" if name in cc.SUITES else "PART_OF" if name in cc.PART_OF else None)
        is_prog = cc.program(path, text)
        if where is None and is_prog:
            bad.append(name)
        yield name, where, is_prog, bad


rows = list(unclassified(cc.OUTSIDE))
for name, where, is_prog, _ in rows:
    print(f"HEAD {name:60} {where or '-':9} program={is_prog}")
head_bad = rows[-1][3] if rows else []
print("HEAD unclassified programs:", head_bad)
print("HEAD shard proof found by text:", any(r[0] == SHARDS for r in rows),
      "classified:", cc.OUTSIDE.get(SHARDS))
reduced = {k: v for k, v in cc.OUTSIDE.items() if k != SHARDS}
rows2 = list(unclassified(reduced))
removed_bad = rows2[-1][3] if rows2 else []
print("ENTRY REMOVED unclassified programs:", removed_bad)
ok = head_bad == [] and removed_bad == [SHARDS]
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)

#!/usr/bin/env python3
"""probe_boundary_classes.py TREE - which programs naming the firmware's tree TREE's ctrl_configs.py leaves
unclassified, as built and with each of the three twin entries removed in turn (in memory only)."""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_configs as cc  # noqa: E402

def unclassified():
    names = {b.path for b in cc.BUILDERS}
    found = []
    for path, text in cc.builder_texts().items():
        name = cc.rel(path)
        if name in names or name in cc.OUTSIDE or name in cc.SUITES or name in cc.PART_OF:
            continue
        found.append((name, "program" if cc.program(path, text) else "not a program"))
    return found

twin = sorted(n for n, _ in ((cc.rel(p), t) for p, t in cc.builder_texts().items()) if "milan_dp/twin" in n)
print("builders naming the firmware's tree among the twin's files:", twin)
base = unclassified()
print("unclassified programs as built:", [n for n, k in base if k == "program"], "; non-programs left to the capture rule:", len(base))
ok = not [n for n, k in base if k == "program"] and not [n for n, _ in base if "milan_dp/twin" in n]
for table, key in ((cc.OUTSIDE, "tb/verilator/milan_dp/twin_compare.py"), (cc.OUTSIDE, "tb/verilator/milan_dp/twin_decode.py"),
                   (cc.SUITES, "tb/verilator/milan_dp/twin_fw.py")):
    saved = table.pop(key)
    got = unclassified()
    print(f"{key} removed: now unclassified {[x for x in got if x not in base]}")
    ok &= any(n == key for n, _ in got)
    table[key] = saved
print(f"probe_boundary_classes: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)

#!/usr/bin/env python3
"""Every TEST/TEST_F/TEST_P name of the dev files that moved or shrank must exist at head, in milan-fpga's
test/ or the stack's tests/. usage: test_names.py DEV_TREE HEAD_TREE"""
import re, sys
from pathlib import Path
dev, head = Path(sys.argv[1]), Path(sys.argv[2])
pat = re.compile(r"^\s*TEST(?:_F|_P)?\(\s*(\w+)\s*,\s*(\w+)\s*\)", re.M)
files = ["test_adp.cpp", "test_acmp.cpp", "test_adp_reentry.cpp", "test_maap.cpp", "test_maap_debug.cpp"]
def names(paths):
    return {f"{a}.{b}" for p in paths if p.exists() for a, b in pat.findall(p.read_text())}
before = names([dev / "sw/firmware/ctrl/test" / f for f in files])
after_paths = list((head / "sw/firmware/ctrl/test").glob("*.cpp")) + list((head / "third_party/tsn-c-stack/tests").glob("*.cpp"))
after = names(after_paths)
lost = sorted(before - after)
added = sorted(names([head / "third_party/tsn-c-stack/tests" / f for f in files] +
                     [head / "sw/firmware/ctrl/test" / f for f in files]) - before)
print(f"dev names {len(before)}; lost at head {len(lost)}; new at head {len(added)}")
for n in lost: print("LOST", n)
for n in added: print("NEW", n)
sys.exit(1 if lost else 0)

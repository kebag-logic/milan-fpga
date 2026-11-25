#!/usr/bin/env python3
"""Build ADP cores with single defects and run the ADP test binary of a given tree against each.
Usage: own_mutants.py TREE WORK OP   (OP: the comparison the tree's core uses, '<' or '!=')"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, work, op = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
work.mkdir(parents=True, exist_ok=True)
F = "(wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) " + op + " ADP_CONTROL_DATA_LENGTH"
M = {
 "control-unmutated": F,
 "mask-0x03FF": F.replace("0x07FFu", "0x03FFu"),
 "mask-0x01FF": F.replace("0x07FFu", "0x01FFu"),
 "mask-0x00FF": F.replace("0x07FFu", "0x00FFu"),
 "mask-0x007F": F.replace("0x07FFu", "0x007Fu"),
 "mask-0x003F": F.replace("0x07FFu", "0x003Fu"),
 "mask-0x0FFF": F.replace("0x07FFu", "0x0FFFu"),
 "mask-0x17FF": F.replace("0x07FFu", "0x17FFu"),
 "low-octet-only": "frame[ADP_HEADER_BYTES + 3u] " + op + " ADP_CONTROL_DATA_LENGTH",
 "high-octet-only": "(frame[ADP_HEADER_BYTES + 2u] & 0x07u) " + op + " ADP_CONTROL_DATA_LENGTH",
 "cap-84": F + " || (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) > 84u",
 "cap-1488": F + " || (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) > 1488u",
 "cap-2046": F + " || (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) > 2046u",
 "gap-85-to-2046": F + " || ((wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) > 84u && (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) < 2047u)",
 "gap-128-to-255": F + " || ((wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) >= 128u && (wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) < 256u)",
 "surplus-refused": F + " || len > ADP_FRAME_BYTES + 100u",
}
env = dict(os.environ)
flags = subprocess.check_output(["pkg-config", "--cflags", "gtest", "gmock"], text=True).split()
libs = subprocess.check_output(["pkg-config", "--libs", "gtest", "gmock"], text=True).split()
src = (tree / "src/adp.c").read_text()
assert src.count(F) == 1, "expected one occurrence"
tobj, mobj = work / "test_adp.o", work / "main.o"
for s, o in (("tests/test_adp.cpp", tobj), ("tests/main.cpp", mobj)):
    subprocess.check_call(["g++", "-std=c++20", "-O0", "-I" + str(tree / "include"), "-I" + str(tree / "examples"), *flags, "-c", str(tree / s), "-o", str(o)])
def one(item):
    name, expr = item
    c, o, b = work / (name + ".c"), work / (name + ".o"), work / (name + ".bin")
    c.write_text(src.replace(F, expr))
    subprocess.check_call(["gcc", "-std=c11", "-O0", "-DNDEBUG", "-DCTRL_REENTRY_ASSERT", "-I" + str(tree / "include"), "-c", str(c), "-o", str(o)])
    subprocess.check_call(["g++", str(o), str(tobj), str(mobj), *libs, "-o", str(b)])
    r = subprocess.run([str(b), "--gtest_brief=1"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    failed = sorted({l.split("[  FAILED  ] ")[1].split(",")[0].split(" ")[0] for l in r.stdout.splitlines() if l.startswith("[  FAILED  ] ") and "." in l})
    return name, r.returncode, failed
with ThreadPoolExecutor(8) as ex:
    for name, rc, failed in ex.map(one, M.items()):
        print(f"{'CAUGHT' if rc else 'SURVIVED'} rc={rc} {name}: {', '.join(failed[:3])}{' ...' if len(failed) > 3 else ''}")

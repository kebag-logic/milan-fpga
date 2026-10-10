#!/usr/bin/env python3
"""Every GoogleTest case removed from milan-fpga's core tests must exist after the move.

Names are read with a whitespace-tolerant regex over TEST/TEST_F/TEST_P (and
INSTANTIATE_TEST_SUITE_P prefixes) from git objects:
  base = milan-fpga <base> test files; head = milan-fpga <head> test files
  plus tsn-c-stack <pin> tests/. Prints the base names absent at head.
usage: test_names.py <milan-git> <base> <head> <stack-git> <pin>
"""
import re, subprocess, sys
TEST = re.compile(r"\b(TEST(?:_F|_P)?)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)")
INST = re.compile(r"\bINSTANTIATE_TEST_SUITE_P\s*\(\s*(\w+)\s*,\s*(\w+)\s*,")
FILES = ["test_acmp.cpp", "test_adp.cpp", "test_adp_reentry.cpp", "test_maap.cpp", "test_maap_debug.cpp"]

def show(git, rev, path):
    r = subprocess.run(["git", "-C", git, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""

def names(text):
    return {f"{s}.{n}" for _, s, n in TEST.findall(text)} | {f"INST {p}/{s}" for p, s in INST.findall(text)}

mg, base, head, sg, pin = sys.argv[1:6]
before = {f: names(show(mg, base, f"sw/firmware/ctrl/test/{f}")) for f in FILES}
after_milan = {f: names(show(mg, head, f"sw/firmware/ctrl/test/{f}")) for f in FILES}
after_stack = {f: names(show(sg, pin, f"tests/{f}")) for f in FILES}
missing = 0
for f in FILES:
    now = after_milan[f] | after_stack[f]
    lost = sorted(before[f] - now)
    added = sorted(now - before[f])
    print(f"{f}: base {len(before[f])}, head milan {len(after_milan[f])} + stack {len(after_stack[f])}, "
          f"lost {len(lost)}, added {len(added)}")
    for t in lost: print(f"  LOST {t}")
    for t in added: print(f"  added {t}")
    missing += len(lost)
print(f"lost in total: {missing}")
sys.exit(1 if missing else 0)

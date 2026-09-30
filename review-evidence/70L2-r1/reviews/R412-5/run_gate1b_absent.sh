#!/bin/sh
# Gate 1b alone with every cross-compiler candidate hidden: a fake HOME (no
# provisioned SDK selector) and shims that make riscv64-elf-gcc and
# riscv32-unknown-elf-gcc not answer. No --require-rv32. Usage: run_gate1b_absent.sh <tree>
cd "$(dirname "$0")" || exit 2
H=$(pwd)/scratch/hide
T=$(cd "$1" && pwd)
HOME=$H/home PATH=$H/bin:$PATH python3 - "$T" <<'PY'
import os, sys, time
tree = sys.argv[1]
sys.argv = [tree + "/sw/builder/test_builder.py"]
sys.path.insert(0, tree + "/sw/builder")
os.chdir(tree)
t = time.time()
import test_builder
try:
    test_builder.test_baremetal_profile_contract()
except AssertionError as exc:
    print(f"GATE1B ABSENT REFUSED ({time.time()-t:.0f} s): {str(exc)[:600]}"); sys.exit(3)
print(f"GATE1B ABSENT PASS ({time.time()-t:.0f} s)")
PY

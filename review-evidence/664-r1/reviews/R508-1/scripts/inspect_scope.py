#!/usr/bin/env python3
"""Read-only scope, VERSION and cited-simulation receipt."""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1])
base = "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"
head = "a27808375427859dc357f6bfd0a88842062b20ed"
paths = subprocess.check_output(["git", "-C", str(root), "diff", "--name-only", base, head], text=True).splitlines()
assert len(paths) == 21 and all(p.endswith(".md") for p in paths)
print("PASS: all 21 changed paths are documentation")
print("\n".join(paths))
for filename in ["hdl/common/csr/milan_csr.sv", "tb/verilator/csr/sim_main.cpp", "tb/verilator/milan_dp/sim_main.cpp", "tb/verilator/milan_dp/sim_nxn.cpp", "tb/verilator/milan_dp/sim_gptp.cpp", "tb/verilator/milan_dp/sim_prune.cpp"]:
    before = subprocess.check_output(["git", "-C", str(root), "show", f"{base}:{filename}"])
    after = subprocess.check_output(["git", "-C", str(root), "show", f"{head}:{filename}"])
    assert before == after
    lines = after.decode().splitlines()
    matches = [(n, s.strip()) for n, s in enumerate(lines, 1) if "0x00020060" in s or "32'h0002_0060" in s]
    assert matches, filename
    for n, s in matches:
        print(f"PASS unchanged {filename}:{n}: {s}")
assert not (root / "tb/verilator/hostplane").exists()
print("PASS retired hostplane directory absent; replacement assertion is a future landing obligation")
subprocess.run(["git", "-C", str(root), "diff", "--check", base, head], check=True)
print("PASS diff whitespace check")

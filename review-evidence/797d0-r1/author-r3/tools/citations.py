#!/usr/bin/env python3
"""Print every source line this round's corrections and moved citations rest on, at the lane's HEAD.

Usage: python3 -I citations.py LANE
"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
TOP = "protocol-processor/hdl/top/protocol_processor_top.sv"
DP = "hdl/milan/milan_datapath.sv"
FW = "sw/firmware/milan_baremetal/milan_baremetal.c"
SOC = "sw/litex/milan_soc.py"
CELLS = [
    ("D0-001 correction", [(SOC, 2854, 2856), (SOC, 4097, 4098)]),
    ("D0-001 copy, REQUIREMENTS.md", [("REQUIREMENTS.md", 25, 31)]),
    ("D0-017 correction", [(FW, 1671, 1671), (FW, 1099, 1102), (FW, 1106, 1106), (FW, 1900, 1903), (FW, 1914, 1914)]),
    ("D0-027 correction", [("sw/firmware/gtest/README.md", 3, 13), ("sw/firmware/milan_baremetal/Makefile", 6, 6)]),
    ("D0-035 correction", [(FW, 1860, 1892), (FW, 1913, 1915)]),
    ("D0-062 source", [("docs/reference/SUBMODULES.md", 511, 517), ("docs/design/AREA_BUDGET.md", 149, 150),
                       ("docs/integration/BAREMETAL_FIRMWARE.md", 2291, 2291)]),
    ("D0-063 correction, selector 0 flags", [(DP, 6194, 6217), (TOP, 3641, 3641)]),
    ("D0-063 correction, selectors 1 and 3", [(DP, 6401, 6401), (DP, 6421, 6421)]),
    ("D0-063 correction, selector 2", [(DP, 6413, 6414), (TOP, 3642, 3642)]),
    ("D0-063 correction, selector 4", [(DP, 6430, 6432), (TOP, 3628, 3628), (TOP, 3643, 3643)]),
    ("D0-063 correction, selectors 5 and 7", [(TOP, 3593, 3595), (TOP, 3629, 3629), (TOP, 3633, 3633)]),
    ("D0-063 correction, selector 6", [(TOP, 3631, 3632), (DP, 6444, 6451)]),
    ("D0-063 correction, Stream Output", [(TOP, 3624, 3626)]),
    ("D0-064 correction", [(DP, 6048, 6053), (TOP, 3621, 3622), (TOP, 3639, 3648)]),
    ("D0-065 correction", [(TOP, 3628, 3633)]),
    ("D0-066 correction", [("docs/guides/VERIFICATION_DEVELOPER.md", 25, 25), ("sw/trace/test_trace_roundtrip.py", 17, 18)]),
]
head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
pins = subprocess.run(["git", "-C", str(root), "ls-tree", "HEAD", "protocol-processor"], capture_output=True, text=True).stdout.split()[2]
print(f"lane head {head}; protocol-processor pin {pins}")
for cell, cites in CELLS:
    print(f"\n## {cell}")
    for path, first, last in cites:
        lines = (root / path).read_text(encoding="utf-8", errors="replace").split("\n")
        for number in range(first, last + 1):
            print(f"{path}:{number}: {lines[number - 1].rstrip()[:110]}")

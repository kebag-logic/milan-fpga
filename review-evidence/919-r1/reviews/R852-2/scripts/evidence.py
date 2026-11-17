#!/usr/bin/env python3
"""Extract auditable lines from immutable public receipts, without reading review reports."""
import hashlib, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
archive = "d8bc5057f25ee85a2f19bd3a4149e7919dd7465d"
base = "review-evidence/919-r1/author-r4/receipts/"
files = {
"boot/boot-1x1-1a1e6665.log": ["head ","PHY ","ctrl_split_boot:","rc="],
"boot/boot-8x8-1a1e6665.log": ["head ","PHY ","ctrl_split_boot:","rc="],
"boot/boot-self-test-1a1e6665.log": ["head ","PLANT ","NATIVE-CONTROL", "controls:","plants:","rc="],
"boot/plat-ledger-self-test-1a1e6665.log": ["head ","POINT ","controls:","plat_ledger:","rc="],
"workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log": ["# head ", "plat-phy-", "mutants:","test_ctrl_firmware:"],
"workflows/logs/rtl-fast__firmware-unit__ci_step_12.log": ["# head ","ctrl_plat_phy.c", "firmware coverage:"],
"probes/r852-retry-probe-1a1e6665.log": ["RETRY-PROBE", "PASSED"],
"probes/r852-retry-control-1a1e6665.log": ["RETRY-PROBE", "PASSED"],
"budget/harness-image-identity-1a1e6665.txt": [""],
"measure/rom-banking.txt": [""],
"measure/rom-per-file.txt": [""],
"probes/r851-mutants-1a1e6665.txt": [""],
}
print("Public author receipts; not reviewer or manager full-bank executions")
for name, needles in files.items():
    data = subprocess.check_output(["git", "show", archive+":"+base+name], cwd=root)
    print("\nARTIFACT", archive+":"+base+name)
    print("sha256", hashlib.sha256(data).hexdigest())
    for line in data.decode().splitlines():
        if any(n in line for n in needles): print(line)

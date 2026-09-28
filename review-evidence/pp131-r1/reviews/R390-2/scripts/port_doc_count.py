#!/usr/bin/env python3
"""Reviewer focused re-count of the parent port-contract ratchet for the
protocol-processor tree only: first-party module ports (not parameters) with
no `//!` contract, through the parent's own scripts/sv_ports.py declarations()
and lint_rtl_policy.LINT_EXCLUDE (both fetched read-only from milan-fpga
7a7582f0). Usage: port_doc_count.py <parent-scripts-dir> <processor-clone> <rev> ..."""
import subprocess, sys
sys.path.insert(0, sys.argv[1])
from sv_ports import declarations
from lint_rtl_policy import LINT_EXCLUDE
clone = sys.argv[2]
for rev in sys.argv[3:]:
    files = subprocess.run(["git", "-C", clone, "ls-tree", "-r", "--name-only", rev, "hdl"],
                           capture_output=True, text=True, check=True).stdout.split()
    files = [f for f in files if f.endswith((".sv", ".svh"))
             and "protocol-processor/" + f not in LINT_EXCLUDE]
    total, undoc = 0, []
    for f in files:
        text = subprocess.run(["git", "-C", clone, "show", f"{rev}:{f}"],
                              capture_output=True, text=True, check=True).stdout
        for _m, name, doc, _mb, kind in declarations(text):
            if kind == "param":
                continue
            total += 1
            if not doc.strip():
                undoc.append(f"{f}:{name}")
    print(f"{rev[:10]}: {len(files)} files, {total} ports, {len(undoc)} undocumented")
    if rev == sys.argv[-1]:
        new = [u for u in undoc if "nvm_writer" in u or "rx_validator" in u]
        print("  undocumented in the writer/validator at this rev:", new)

#!/usr/bin/env python3
"""Count each planted pattern of the three drivers that edit the processor tree.

Reads the driver modules at the exact head by path and counts every edit's
search text in its target file. Writes nothing.
Usage: python3 -I anchor_scan_r786.py <clone>
"""
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
md = root / "tb/verilator/milan_dp"
sys.path.insert(0, str(root / "scripts"))
total = bad = 0
for name in ("unb_mutants", "gsi_mutants", "dynmap_mutants"):
    spec = importlib.util.spec_from_file_location(name, md / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    arms = getattr(mod, "MUTATIONS", None) or getattr(mod, "MUTANTS", None) or getattr(mod, "ARMS", [])
    kinds = {}
    for arm in arms:
        edits = getattr(arm, "edits", None)
        if edits is None:
            continue
        for edit in edits:
            key, old = edit[0], edit[1]
            kinds[key] = kinds.get(key, 0) + 1
            total += 1
            if key != "pp":
                continue
            text = (root / "protocol-processor/hdl/top/protocol_processor_top.sv").read_text()
            n = text.count(old)
            print(f"{name}: pp anchor x{n}: {old[:70]!r}")
            if n != 1:
                bad += 1
    print(f"{name}: {len(arms)} arms, edit targets {kinds}")
print(f"edits {total}, pp anchors not matching exactly once: {bad}")
sys.exit(1 if bad else 0)

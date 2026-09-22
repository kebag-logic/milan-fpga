#!/usr/bin/env python3
"""Compare a tracked avdecc/aem_rom.json with its regeneration from the same
tree and name the differing ROM bytes.

    decode_aem_rom_drift.py <checkout> <rev>

Regenerates in a `git archive` scratch extract; the checkout is not written.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

checkout, rev = Path(sys.argv[1]).resolve(), sys.argv[2]
tracked = json.loads(subprocess.run(
    ["git", "-C", str(checkout), "show", f"{rev}:avdecc/aem_rom.json"],
    check=True, capture_output=True, text=True).stdout)
with tempfile.TemporaryDirectory(prefix="aem464-drift-") as tmp:
    arc = subprocess.run(["git", "-C", str(checkout), "archive", rev,
                          "avdecc", "hdl/common/csr"],
                         check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", tmp], input=arc, check=True)
    subprocess.run([sys.executable, "-B", "avdecc/gen_aem_store.py"],
                   cwd=tmp, check=True, capture_output=True)
    regen = json.loads((Path(tmp) / "avdecc/aem_rom.json").read_text())
print(f"tracked avdecc/aem_rom.json at {rev} vs regenerated from the same tree")
print("keys equal:", sorted(tracked) == sorted(regen))
for key in sorted(tracked):
    if tracked[key] == regen.get(key):
        continue
    if key != "rom_hex":
        print(f"  {key}: differs")
        continue
    a, b = bytes.fromhex(tracked[key]), bytes.fromhex(regen[key])
    diff = [i for i in range(max(len(a), len(b))) if a[i:i + 1] != b[i:i + 1]]
    print(f"  rom_hex: {len(a)} vs {len(b)} bytes; differing offsets {diff}")
    for i in diff:
        print(f"    offset {i}: tracked 0x{a[i]:02x} regenerated 0x{b[i]:02x}")

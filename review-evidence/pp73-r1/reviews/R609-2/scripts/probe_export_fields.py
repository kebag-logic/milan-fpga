#!/usr/bin/env python3
"""Show which purported prose-only documented fields affect semantic verdicts."""
import argparse
import copy
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--root", type=Path, required=True)
a = ap.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(a.root / "scripts"))
from aecp_gate.inputs import load, DOC
from aecp_gate.gate import check
from aecp_gate.doc import regenerated

base = load(a.root)
assert not check(base)
for field, value in (("gdi", False), ("rtl", "GDI_GET_VIDEO_FORMAT_C"), ("opcode", "0x007E")):
    inp = copy.deepcopy(base)
    row = next(d for d in inp.table["documented"] if d["name"] == "GET_VIDEO_FORMAT")
    row[field] = value
    inp.texts[DOC] = regenerated(inp.table, inp.texts[DOC])
    findings = check(inp)
    semantic = [f for f in findings if "decode:" in f or "engine:" in f]
    assert semantic and not any("F06.14:" in f for f in findings)
    print(f"documented[].{field}={value!r}; regenerated F06.14 matches; semantic findings:")
    print("\n".join(semantic))
print("PASS: all three documented fields are consumed as machine semantics")

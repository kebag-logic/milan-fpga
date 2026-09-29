#!/usr/bin/env python3
"""Scratch: the issue #64 timer mutations as srp_top patch arms."""
import subprocess, sys, tempfile
from pathlib import Path
REPO = Path(sys.argv[1]); TOP = "hdl/srp/KL_srp_top.sv"
SPECS = {
    "join-ms-400": [("    parameter int unsigned JOIN_MS_P     = 200,\n",
                     "    parameter int unsigned JOIN_MS_P     = 400,\n")],
    "periodic-ms-3000": [("    parameter int unsigned PERIODIC_MS_P = 1000,\n",
                          "    parameter int unsigned PERIODIC_MS_P = 3000,\n")],
    "draw-kind-0": [("  assign draw_kind_o = 3'd3;   // T-MRP-LEAVEALL range (F08.2)\n",
                     "  assign draw_kind_o = 3'd0;   // T-MRP-LEAVEALL range (F08.2)\n")],
}
for label, reps in SPECS.items():
    text = (REPO / TOP).read_text(); new = text
    for old, rep in reps:
        assert new.count(old) == 1, (label, old)
        new = new.replace(old, rep)
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp) / "a", Path(tmp) / "b"; a.write_text(text); b.write_text(new)
        res = subprocess.run(["diff", "-u", "--label", f"a/{TOP}", "--label", f"b/{TOP}", str(a), str(b)],
                             capture_output=True, text=True)
    assert res.returncode == 1
    (REPO / "tb/srp_top/mutations" / f"{label}.patch").write_text(res.stdout)
    print("wrote", label)

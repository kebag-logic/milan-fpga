#!/usr/bin/env python3
"""Plant cuts of the datapath's shape wiring on a disposable tree and run gate 1h for real.

usage: gate_1h_cuts.py <disposable tree at the head under review>
Each cut edits hdl/milan/milan_datapath.sv, runs the committed gate by name, and restores the bytes.
"""
import re, subprocess, sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
dp = tree / "hdl/milan/milan_datapath.sv"
orig = dp.read_text()
TICK = ".ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),"
CYC = ".ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),"
assert orig.count(TICK) == 1 and orig.count(CYC) == 1
DTICK = "parameter int unsigned GPTP_ETH_TICK_NS_P = 8,"
DCYC = "parameter int unsigned GPTP_ETH_CYC_PER_OCTET_P = 1,"
assert orig.count(DTICK) == 1 and orig.count(DCYC) == 1
CUTS = [
    ("shipped, no cut", orig, "accept"),
    ("tick binding deleted", orig.replace(TICK, ""), "refuse"),
    ("cycle binding deleted", orig.replace(CYC, ""), "refuse"),
    ("tick tied to 8", orig.replace(TICK, ".ETH_TICK_NS_P (8),"), "refuse"),
    ("cycle tied to 1", orig.replace(CYC, ".ETH_CYC_PER_OCTET_P(1),"), "refuse"),
    ("the two bindings swapped",
     orig.replace(TICK, ".ETH_TICK_NS_P (GPTP_ETH_CYC_PER_OCTET_P),")
         .replace(CYC, ".ETH_CYC_PER_OCTET_P(GPTP_ETH_TICK_NS_P),"), "refuse"),
    ("tick default moved to 40", orig.replace(DTICK, DTICK.replace("= 8", "= 40")), "refuse"),
    ("cycle default moved to 2", orig.replace(DCYC, DCYC.replace("= 1", "= 2")), "refuse"),
    ("plane instance renamed", orig.replace("u_gptp_shadow (", "u_gptp_other ("), "refuse"),
    ("tick binding line-commented", orig.replace(TICK, "// " + TICK), "refuse"),
    ("cycle binding line-commented", orig.replace(CYC, "// " + CYC), "refuse"),
    ("tick binding block-commented", orig.replace(TICK, "/* " + TICK + " */"), "refuse"),
    ("tick tied, old text kept in a comment",
     orig.replace(TICK, ".ETH_TICK_NS_P (8), // " + TICK), "refuse"),
    ("tick default commented, real default 40 on the next line",
     orig.replace(DTICK, "// " + DTICK + "\n  parameter int unsigned GPTP_ETH_TICK_NS_P = 40,"), "refuse"),
    ("tick bound through an arithmetic no-op",
     orig.replace(TICK, ".ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P + 0),"), "either"),
]
env_gate = ["python3", "sw/builder/test_builder.py", "--gates",
            "test_gptp_datapath_carries_the_launch_shape"]
bad = 0
try:
    for name, text, want in CUTS:
        assert want == "accept" or text != orig, name
        dp.write_text(text)
        r = subprocess.run(env_gate, cwd=tree, capture_output=True, text=True)
        tail = [l for l in (r.stdout + r.stderr).splitlines() if "AssertionError" in l or "ALL GATES" in l]
        got = "accept" if r.returncode == 0 else "refuse"
        ok = want in ("either", got)
        bad += not ok
        print(f"{'ok ' if ok else 'ESCAPE'} rc={r.returncode} want={want:6} {name}: {tail[-1] if tail else ''}")
finally:
    dp.write_text(orig)
print(f"cuts: {len(CUTS)} not as wanted: {bad}")

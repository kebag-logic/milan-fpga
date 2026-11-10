#!/usr/bin/env python3
"""Scratch: srp_mutants' defects killed in srp_rx_retry.cpp, planted by srp_mutants.campaign: every one at two
interfaces (the gate's main campaign), and at one interface the retry rule's plants and the deadline's (their tests
are interface-free; the gate's one-interface campaign plants a named subset only). usage: srp_rx_retry_campaign.py
CHECKOUT OUT"""
import sys
from pathlib import Path
ck, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ck / "sw/firmware/ctrl/test")); sys.path.insert(0, str(ck / "sw/firmware/gtest"))
import srp_mutants
import srp_retry_mutants
table = tuple(d for d in srp_mutants.DEFECTS if d.suite == "srp_rx_retry.cpp")
retry = {d.name for d in srp_retry_mutants.defects(srp_mutants.Defect)} | {"receive-retention-short"}
bad = False
for i, chosen in ((2, table), (1, tuple(d for d in table if d.name in retry))):
    srp_mutants.DEFECTS = chosen
    print(f"== {i} interface(s): {len(chosen)} defects", flush=True)
    bad |= srp_mutants.campaign(out / f"if{i}", (ck / "third_party/lwSRP").resolve(), 8, i)
sys.exit(int(bad))

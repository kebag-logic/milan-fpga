#!/usr/bin/env python3
"""Reviewer plants for sw/mailbox/placement_identity.py, beyond its own self-test: defects inside
an all-fabric generate scope (g_af_amr), where the tool removes the scope prefix and relabels the
cells Yosys made. Each must change the recipe shape's digest.

Usage: identity_probes.py <repo checkout>   (SV2V and YOSYS set to the pinned tools)
"""
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw/mailbox"))
import placement_identity as pi  # noqa: E402

dp = repo / "hdl/milan/milan_datapath.sv"
text = dp.read_text()
PLANTS = (
    ("a constant of a made adder inside g_af_amr",
     "      else if (amr_tick_r && (amr_wd_r != 11'h7FF)) amr_wd_r <= amr_wd_r + 11'd1;",
     "      else if (amr_tick_r && (amr_wd_r != 11'h7FF)) amr_wd_r <= amr_wd_r + 11'd2;"),
    ("a reset value inside g_af_amr",
     "      amr_go_r    <= 1'b0;\n      amr_agg_x_r <= 1'b0;",
     "      amr_go_r    <= 1'b1;\n      amr_agg_x_r <= 1'b0;"),
    ("a comparison inside g_af_amr turned around",
     "        if (32'(amr_agg_r) >= AMR_RS_AGG_MS_P) amr_agg_x_r <= 1'b1;",
     "        if (32'(amr_agg_r) > AMR_RS_AGG_MS_P) amr_agg_x_r <= 1'b1;"),
)
clean = pi.dump(repo, 1, None, only=0)["shapes"]["recipe"]["digest"]
print(f"clean recipe digest {clean}", flush=True)
bad = 0
for name, old, new in PLANTS:
    if text.count(old) != 1:
        print(f"ANCHOR-MISSING {name}")
        bad += 1
        continue
    got = pi.dump(repo, 1, None, {dp: text.replace(old, new)}, only=0)["shapes"]["recipe"]["digest"]
    ok = got != clean
    bad += not ok
    print(f"{'caught' if ok else 'MISSED'} {name}: digest {got}", flush=True)
print(f"identity probes: {len(PLANTS) - bad} of {len(PLANTS)} change the digest")
sys.exit(1 if bad else 0)

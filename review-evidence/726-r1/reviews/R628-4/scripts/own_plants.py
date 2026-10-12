#!/usr/bin/env python3
"""Reviewer-owned plants for PR #729 (issue #726), driven through the PR's own
stream-counter fixture so detection and check-omission escape use the same rule
as the shipped mutants: the plant must fail only its named group, and pass with
that group omitted.

Usage: own_plants.py <repo-root> <variant> <work-dir> [--shape N]

Variants (group):
  aaf-interval  (RX)       AAF FRAMES_RX commits +1 per occupied interval
  aaf-guard     (CADENCE)  AAF engine restores both pre-#726 healthy-dirty guards
  crf-nodirty   (CADENCE)  CRF receiver drops its per-AVTPDU dirty pulse
  tx-saturate   (TX)       FRAMES_TX saturates at 0xFFFFFFFF instead of wrapping
"""
import argparse
import os
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("root", type=Path)
ap.add_argument("variant")
ap.add_argument("work", type=Path)
ap.add_argument("--shape", type=int, default=1)
args = ap.parse_args()

sys.path.insert(0, str(args.root / "tb/verilator/milan_dp"))
import stream_counters as sc  # noqa: E402

AAF, RX, TX = sc.AAF, sc.RX, sc.TX
EDITS = {
    "aaf-interval": ("RX", [(AAF,
        "? 32'(frx_add_r) : 32'd1)",
        "? 32'd1 : 32'd1)")]),
    "aaf-guard": ("CADENCE", [
        (AAF, "if (iv_seen_r[iv_s_w] != '0)",
              "if ((iv_seen_r[iv_s_w] & ~(12'b1 << C_FRX_C)) != '0)"),
        (AAF, "            dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;",
              "            if (!cur_w.tv || lock_now_w ||\n"
              "                (seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C)))\n"
              "              dirty_p_o[ev_s_r] <= 1'b1;\n"
              "            monst_r <= monst_next_w;")]),
    "crf-nodirty": ("CADENCE", [(RX,
        "pdu_count_o <= pdu_count_o + 32'd1;\n        dirty_p_o <= 1'b1;",
        "pdu_count_o <= pdu_count_o + 32'd1;")]),
    "tx-saturate": ("TX", [(TX,
        "ftx_r[c] <= ftx_r[c] + 32'd1;",
        "ftx_r[c] <= (ftx_r[c] == 32'hFFFFFFFF) ? ftx_r[c] : ftx_r[c] + 32'd1;")]),
}
group, edits = EDITS[args.variant]
orig_plant = sc.plant


def plant(variant, work, output_condition):
    paths = orig_plant("clean", work, output_condition)
    for rel, old, new in edits:
        dest = work / Path(rel).name
        text = dest.read_text()
        dest.write_text(sc.replace_once(text, old, new))
    return paths


sc.plant = plant
sc.GROUPS[args.variant] = group
sc.run(args.shape, args.variant, args.work.resolve(),
       os.environ.get("VERILATOR", "verilator"), "uncertain")
print(f"OWN-PLANT {args.variant} group={group}: detected by name and escaped with that group omitted")

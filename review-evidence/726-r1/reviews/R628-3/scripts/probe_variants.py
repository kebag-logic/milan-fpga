#!/usr/bin/env python3
"""Reviewer probes for PR #729: extra plants on top of the PR's own driver.

Usage: probe_variants.py REPO_OR_MIRROR VARIANT WORK [--shape N]
Imports tb/verilator/milan_dp/stream_counters.py from the given tree, stages
the clean sources, applies one reviewer plant to the staged copy only, then
requires the named failure group and an escape with that group omitted.
"""
import argparse, importlib.util, os, sys
from pathlib import Path

PLANTS = {
    # restore the c6bd08c6 healthy-traffic dirty guards in the AAF engine only;
    # packet counting stays per AVTPDU
    "aaf-guard": ("CADENCE", "KL_avtp_rx_monitor_ctx.sv", [
        ("if (iv_seen_r[iv_s_w] != '0)",
         "if ((iv_seen_r[iv_s_w] & ~(12'b1 << C_FRX_C)) != '0)"),
        ("            dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;",
         "            if (!cur_w.tv || lock_now_w ||\n"
         "                (seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C)))\n"
         "              dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;")]),
    # restore only the CRF healthy FRAMES_RX dirty exclusion
    "crf-guard": ("CADENCE", "KL_crf_rx.sv", [
        ("        pdu_count_o <= pdu_count_o + 32'd1;\n        dirty_p_o <= 1'b1;",
         "        pdu_count_o <= pdu_count_o + 32'd1;")]),
    # CRF era wipe on both bind edges (unbind must preserve the total)
    "crf-unbind-wipe": ("RX_RESET", "KL_crf_rx.sv", [
        ("wire w_bind_rise_w = en_i && !en_q;", "wire w_bind_rise_w = en_i != en_q;")]),
    # FRAMES_TX saturates instead of wrapping at 32 bits
    "tx-saturate": ("TX", "KL_talker_diag_ctx.sv", [
        ("ftx_r[c] <= ftx_r[c] + 32'd1;",
         "ftx_r[c] <= (ftx_r[c] == 32'hFFFF_FFFF) ? ftx_r[c] : ftx_r[c] + 32'd1;")]),
}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path); ap.add_argument("variant")
    ap.add_argument("work", type=Path); ap.add_argument("--shape", type=int, default=1)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location(
        "sc", a.tree / "tb/verilator/milan_dp/stream_counters.py")
    sc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
    orig = sc.plant
    if a.variant in PLANTS:
        group, fname, edits = PLANTS[a.variant]
        def plant(variant, work, cond):
            paths = orig("clean", work, cond)
            p = work / fname
            t = p.read_text()
            for old, new in edits:
                if t.count(old) != 1:
                    raise SystemExit(f"anchor count {t.count(old)}: {old!r}")
                t = t.replace(old, new)
            p.write_text(t)
            return paths
        sc.plant = plant
        sc.GROUPS[a.variant] = group
        variant = a.variant
    else:
        variant = a.variant  # clean / existing
    work = a.work.resolve()
    sc.run(a.shape, variant, work, os.environ.get("VERILATOR", "verilator"), "uncertain")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reviewer-owned disposable mutation probes for PR #729 (issue #726).

Usage: probe_counters.py <clone> <variant> <work> [--shape N] [--output-condition C]

Loads the clone's tb/verilator/milan_dp/stream_counters.py, plants one extra
defect into the scratch RTL copies it writes below <work>, and reuses the
driver's own detection rule: the defect must fail only its named check group,
and the run must pass with exactly that group omitted. Nothing in the clone is
written. Variants:

  aaf-rx-interval  AAF FRAMES_RX publishes +1 per interval, not the batch
  crf-rx-nodirty   CRF receiver stops marking a healthy accepted PDU dirty
  tx-saturate      FRAMES_TX saturates at 0xFFFFFFFF instead of wrapping
  crf-tx-noreset   only the CRF output keeps its FRAMES_TX across a start
  crf-unbind-wipe  CRF receiver also clears FRAMES_RX on bound -> not bound
  aaf-tx-nodirty   only AAF output 0 loses its per-AVTPDU dirty event
"""
import argparse
import importlib.util
import os
from pathlib import Path

PROBES = {
    "aaf-rx-interval": ("RX", "AAF",
        "? 32'(frx_add_r) : 32'd1);", "? 32'd1 : 32'd1);"),
    "crf-rx-nodirty": ("CADENCE", "RX",
        "pdu_count_o <= pdu_count_o + 32'd1;\n        dirty_p_o <= 1'b1;",
        "pdu_count_o <= pdu_count_o + 32'd1;"),
    "tx-saturate": ("TX", "TX",
        "ftx_r[c] <= ftx_r[c] + 32'd1;",
        "ftx_r[c] <= (ftx_r[c] == 32'hFFFFFFFF) ? ftx_r[c] : ftx_r[c] + 32'd1;"),
    "crf-tx-noreset": ("TX_RESET", "TX",
        "ftx_r[c]    <= {31'd0, ev_f_w[c]};",
        "ftx_r[c]    <= (c == N_CTX_P-1) ? ftx_r[c] : {31'd0, ev_f_w[c]};"),
    "crf-unbind-wipe": ("RX_RESET", "RX",
        "      if (w_bind_fall_w && locked_o) begin",
        "      if (w_bind_fall_w) pdu_count_o <= '0;\n      if (w_bind_fall_w && locked_o) begin"),
    "aaf-tx-nodirty": ("OUTPUT_CADENCE", "TX",
        "ftx_r[c] <= ftx_r[c] + 32'd1;\n          dirty_p_o[c] <= 1'b1;",
        "ftx_r[c] <= ftx_r[c] + 32'd1;\n          if (c != 0) dirty_p_o[c] <= 1'b1;"),
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("clone", type=Path)
    p.add_argument("variant", choices=sorted(PROBES))
    p.add_argument("work", type=Path)
    p.add_argument("--shape", type=int, default=1, choices=(1, 8))
    p.add_argument("--output-condition", default=None,
                   choices=("uncertain", "frames-only"))
    a = p.parse_args()
    drv = a.clone.resolve() / "tb/verilator/milan_dp/stream_counters.py"
    spec = importlib.util.spec_from_file_location("stream_counters", drv)
    sc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sc)
    group, key, old, new = PROBES[a.variant]
    target = getattr(sc, key)
    orig = sc.plant

    def plant(variant, work, cond):
        paths = orig("clean", work, cond)
        dest = work / Path(target).name
        text = dest.read_text()
        dest.write_text(sc.replace_once(text, old, new))
        return paths

    sc.plant = plant
    sc.GROUPS[a.variant] = group
    cond = a.output_condition or ("frames-only" if group == "OUTPUT_CADENCE" else "uncertain")
    sc.run(a.shape, a.variant, a.work.resolve(), os.environ.get("VERILATOR", "verilator"), cond)
    print(f"PROBE {a.variant} shape={a.shape} cond={cond}: detected by {group}, escapes without it")


if __name__ == "__main__":
    main()

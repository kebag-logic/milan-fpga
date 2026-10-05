#!/usr/bin/env python3
"""Reviewer-owned RTL defect probes for the packet mailbox (R496-2).

Usage: reviewer_rtl_probes.py TREE SCRATCH [--jobs N]

Plants defects NOT in the lane's mutants.py table into a copy of
TREE/hdl/milan/mailbox, using TREE/tb/verilator/mbx/mutants.py's own plant and
build helpers, and reports which checks fail. A probe "is caught" when the
suite exits 1 with at least one [FAIL]; the first failing check is printed.
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == "--jobs" else 3
sys.path.insert(0, str(tree / "tb/verilator/mbx"))
import mutants as mx  # noqa: E402

A = mx.Arm
PROBES = (
    # AXI4-Lite: a combinational input-to-output path the A0 probe must see
    A("p-axil-bready-to-awready", "KL_mbx_axil.sv", "assign s_awready_o  = !aw_full_r;",
      "assign s_awready_o  = !aw_full_r || s_bready_i;", 1, ""),
    A("p-axil-rready-to-arready", "KL_mbx_axil.sv", "assign s_arready_o  = !ar_full_r;",
      "assign s_arready_o  = !ar_full_r || (rvalid_r && s_rready_i);", 1, ""),
    A("p-axil-wdata-to-rdata", "KL_mbx_axil.sv", "assign s_rdata_o    = rdata_r;",
      "assign s_rdata_o    = rdata_r ^ (s_wvalid_i ? 32'h1 : 32'h0);", 1, ""),
    # AXI4-Lite: registered but functionally wrong
    A("p-axil-wready-while-issuing", "KL_mbx_axil.sv", "assign s_wready_o   = !w_full_r;",
      "assign s_wready_o   = !w_full_r || go_wr_w;", 1, ""),
    A("p-axil-b-on-read", "KL_mbx_axil.sv", "if (busy_r && host_ack_i && busy_we_r) bvalid_r <= 1'b1;",
      "if (busy_r && host_ack_i) bvalid_r <= 1'b1;", 1, ""),
    A("p-axil-write-drops-waiting-read", "KL_mbx_axil.sv",
      "end else if (go_rd_w) begin\n        ar_full_r <= 1'b0;",
      "end else if (go_rd_w || go_wr_w) begin\n        ar_full_r <= 1'b0;", 1, ""),
    # TX merge in commit order
    A("p-tx-scan-skips-served-channel", "KL_mbx_tx.sv",
      "int'(scan_k_r) <= int'(MBX_N_CH_C) && pend_w[scan_ch_w]",
      "int'(scan_k_r) < int'(MBX_N_CH_C) && pend_w[scan_ch_w]", 0, ""),
    A("p-tx-seq-read-from-word0", "KL_mbx_tx.sv",
      "rd_addr_o = MBX_RING_AW_C'((tail_r[scan_ch_w] + 16'd1) &",
      "rd_addr_o = MBX_RING_AW_C'((tail_r[scan_ch_w]) &", 0, ""),
    A("p-tx-stale-candidate", "KL_mbx_tx.sv",
      "          best_v_r <= 1'b0;\n          st_r     <= SCAN_S;",
      "          st_r     <= SCAN_S;", 0, ""),
    A("p-tx-ties-keep-last", "KL_mbx_tx.sv", "before_w  = !best_v_r || dseq_w[15];",
      "before_w  = !best_v_r || dseq_w[15] || dseq_w == 16'd0;", 0, ""),
    A("p-tx-rsvd-check-dropped", "KL_mbx_tx.sv",
      "if (w0_ok_w && (rd_data_i >> MBX_TXREC_W1_RSVD_LSB_C) == 32'd0) begin",
      "if (w0_ok_w) begin", 0, ""),
    # event-ring guard
    A("p-evt-guard-ahead-only", "KL_mbx_evt.sv",
      "free_w = (used_w > 16'(MBX_EVT_WORDS_C)) ? 16'd0 : 16'(MBX_EVT_WORDS_C) - used_w;",
      "free_w = 16'(MBX_EVT_WORDS_C) - used_w;", 0, ""),
)


def run(p):
    rc, log = mx.build_and_run(mx.plant(p, root), root / p.name, p.host)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    caught = rc == 1 and bool(fails)
    first = fails[0] if fails else (log.strip().splitlines() or ["no output"])[-1]
    return p, caught, rc, len(fails), first


def main() -> int:
    root.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(run, PROBES))
    for p, caught, rc, n, first in results:
        print(f"[{'caught' if caught else 'ESCAPED'}] {p.name} (host {p.host}, rc {rc}): {n} [FAIL]; first: {first}")
    print(f"reviewer RTL probes: {sum(r[1] for r in results)} of {len(results)} caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())

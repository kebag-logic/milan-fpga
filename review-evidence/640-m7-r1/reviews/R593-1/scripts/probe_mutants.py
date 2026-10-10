#!/usr/bin/env python3
"""Reviewer-owned defect probes for the gptp_tables lockstep (PR #713, R593-1).

Each probe edits ONE file of a disposable copy of the tree at the reviewed
head and states what the lockstep must say:
  expect=fail:<check prefix>  the named lockstep check must fail
  expect=pass                 an equivalent change; every check must stay green

Usage: probe_mutants.py <tree-root> <probe-name>    apply one probe
       probe_mutants.py --list                      list the probes
"""
import sys
from pathlib import Path

SHADOW = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
RET = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
TIMER = "gptp-processor/hdl/common/KL_gptp_timer.sv"

PROBES = {
    # TX decode off by one: lanes up to and including the count enabled
    "tx_decode_off_by_one": (SHADOW,
        "      txf_keep_w[i] = (CNT_W_C'(i) < txf_cnt_w);",
        "      txf_keep_w[i] = (CNT_W_C'(i) <= txf_cnt_w);",
        "fail:tx_fifo lockstep"),
    # RX lane field as popcount-1: equal to the highest lane for every
    # contiguous-from-0 tkeep, different only for a non-contiguous one
    "rx_top_popcount": (SHADOW,
        "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'(i);",
        "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'($countones(rx_tkeep_i) - 1);",
        "fail:rx_fifo lockstep"),
    # the conversion forgetting the unit change: DEPTH stays in octets, so
    # the tap FIFO is eight times deeper than before
    "rx_depth_octets": (SHADOW,
        "    .DEPTH               (RX_FIFO_BEATS_C),",
        "    .DEPTH               (RX_FIFO_BYTES_P),",
        "fail:rx_fifo lockstep"),
    # the ledger tag field written from the wrong source
    "ledger_tag_constant": (RET,
        "      led_tag_r [led_tail_w] <= alloc_tagged_i;",
        "      led_tag_r [led_tail_w] <= 1'b1;",
        "fail:ledger lockstep"),
    # result queue sequence copied from the ledger TAIL instead of its head
    "results_seq_from_tail": (RET,
        "      res_seq_r [res_tail_w] <= led_head_seq_w;",
        "      res_seq_r [res_tail_w] <= led_seq_r[led_tail_w];",
        "fail:results lockstep"),
    # equivalent: a disarm (delta 0) skips the deadline write; the sweep
    # never reads an unarmed slot, so nothing observable may change
    "timer_skip_disarm_write_equiv": (TIMER,
        "    if (rst_n && arm_we_i)\n      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
        "    if (rst_n && arm_we_i && (arm_delta_ms_i != 32'd0))\n      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
        "pass"),
    # NOT a defect: instrument the harness to print the cumulative coverage
    # counters at every phase boundary (stimulus unchanged: printing draws
    # no random numbers), so each phase's own share is visible
    "phase_coverage_print": ("tb/verilator/gptp_tables/sim_main.cpp",
        "  void traffic(uint64_t n, Mode mode) {\n",
        "  void phase_print(const char* what) {\n"
        "    std::printf(\"PHASE %s cyc=%llu prog=%u ledcmp=%u rescmp=%u tmrcmp=%u txframes=%u rxgood=%u evdrop=%u\\n\", what,\n"
        "      static_cast<unsigned long long>(cyc), dut->dbg_prog_run_o, dut->led_cmp_o, dut->res_cmp_o,\n"
        "      dut->tmr_cmp_o, dut->tx_frames_o, dut->rx_good_o, dut->dbg_ev_drop_o);\n"
        "  }\n"
        "  void traffic(uint64_t n, Mode mode) {\n"
        "    phase_print(\"begin\");\n",
        "pass"),
}


def main() -> int:
    if sys.argv[1:] == ["--list"]:
        for name, (path, _o, _n, expect) in PROBES.items():
            print(f"{name:32s} {path}  expect={expect}")
        return 0
    root, name = Path(sys.argv[1]), sys.argv[2]
    path, old, new, expect = PROBES[name]
    target = root / path
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        print(f"ANCHOR-MISSING {name} in {path}")
        return 2
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"APPLIED {name} to {path} expect={expect}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

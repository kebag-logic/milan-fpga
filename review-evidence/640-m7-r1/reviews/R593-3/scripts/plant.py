#!/usr/bin/env python3
"""Plant one reviewer probe in a disposable tree copy.

Usage: plant.py <tree> <probe-name>
Each probe replaces one anchor that must occur exactly once in its file.
Exit 0 = planted; 2 = anchor missing or ambiguous (the probe proves nothing).
"""
import sys
from pathlib import Path

SHADOW = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
RET = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
TIMER = "gptp-processor/hdl/common/KL_gptp_timer.sv"

#: name -> (file, old, new, what must catch it)
PROBES = {
    # results ok column written as 1: the one-valued list says gptp_shadow sees it
    "res_ok_stuck1": (RET,
        "      res_ok_r  [res_tail_w] <= res_ok_w;",
        "      res_ok_r  [res_tail_w] <= 1'b1;",
        "gptp_shadow fails"),
    # ledger tag written as 0: the list says gptp_tables sees it
    "led_tag_stuck0": (RET,
        "      led_tag_r [led_tail_w] <= alloc_tagged_i;",
        "      led_tag_r [led_tail_w] <= 1'b0;",
        "gptp_tables: ledger lockstep"),
    # ledger fields written at the head, not the tail
    "led_write_at_head": (RET,
        "      led_type_r[led_tail_w] <= alloc_type_i;\n"
        "      led_seq_r [led_tail_w] <= alloc_seq_i;",
        "      led_type_r[led_head_r] <= alloc_type_i;\n"
        "      led_seq_r [led_head_r] <= alloc_seq_i;",
        "gptp_tables: ledger lockstep"),
    # RX lane field holds the LOWEST enabled lane
    "rx_lowest_lane": (SHADOW,
        "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'(i);",
        "      if (rx_tkeep_i[i] && (fw_top_w == '0)) fw_top_w = LANE_W_C'(i);",
        "gptp_tables: rx_fifo lockstep"),
    # RX bad-frame mask widened over the lane bits
    "rx_bad_mask_wide": (SHADOW,
        "    .USER_BAD_FRAME_MASK ((LANE_W_C + 1)'(1)),",
        "    .USER_BAD_FRAME_MASK ((LANE_W_C + 1)'(15)),",
        "gptp_tables: rx_fifo lockstep"),
    # TX decode one lane long
    "tx_decode_le": (SHADOW,
        "      txf_keep_w[i] = (CNT_W_C'(i) < txf_cnt_w);",
        "      txf_keep_w[i] = (CNT_W_C'(i) <= txf_cnt_w);",
        "gptp_tables: tx_fifo decode / lockstep"),
    # timer deadline written at the neighbouring slot
    "tmr_write_alias": (TIMER,
        "      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
        "      deadline_r[arm_slot_i ^ 3'd1] <= ms_now_r + arm_delta_ms_i;",
        "gptp_tables: timer lockstep"),
    # result generation written as 0
    "res_gen_stuck0": (RET,
        "      res_gen_r [res_tail_w] <= gen_r;",
        "      res_gen_r [res_tail_w] <= '0;",
        "gptp_tables: results lockstep / values: gen"),
}


def main() -> int:
    tree, name = Path(sys.argv[1]), sys.argv[2]
    path, old, new, _ = PROBES[name]
    f = tree / path
    text = f.read_text(encoding="utf-8")
    if text.count(old) != 1:
        print(f"anchor for {name} occurs {text.count(old)} times in {path}")
        return 2
    f.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"planted {name} in {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

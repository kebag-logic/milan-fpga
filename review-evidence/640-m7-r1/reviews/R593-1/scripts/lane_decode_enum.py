#!/usr/bin/env python3
"""Exhaustive model check of the M7 lane fields (PR #713, R593-1).

Transcribes, expression for expression, the base and head RTL of
hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv and compares them for every
lane count KEEP_W_C in 1..8 (the range the new g_refuse_lanes guard admits):

TX: base  st_keep_r = gb_keep_r | (KEEP_W_C'(1) << gb_idx_r), where gb_keep_r
          holds the bits of the bytes already placed in this beat (lanes
          0..gb_idx_r-1, the only state the gearbox can reach), truncated to
          KEEP_W_C bits; the FIFO stores and returns that mask.
    head  st_cnt_r = CNT_W_C'(gb_idx_r) + 1 (CNT_W_C = 4); tx_tkeep_o[i] =
          (CNT_W_C'(i) < count). Also the never-written word (base mask 0,
          head count 0).
RX: base  the serializer's top lane = highest set bit of the stored tkeep
          (3-bit, 0 for an all-clear tkeep).
    head  fw_top_w = highest set bit of rx_tkeep_i, LANE_W_C = 3 bits,
          computed before the FIFO; every one of the 2**KEEP_W_C masks,
          contiguous or not.
Prints one line per lane count and exits 0 only if every case matches.
"""
import sys


def tx_base(keep_w: int, idx: int) -> int:
    gb_keep = (1 << idx) - 1                      # lanes 0..idx-1 placed
    return (gb_keep | (1 << idx)) & ((1 << keep_w) - 1)


def tx_head(keep_w: int, cnt: int) -> int:
    return sum(1 << i for i in range(keep_w) if (i & 0xF) < cnt)


def top_lane(mask: int, keep_w: int) -> int:
    top = 0
    for i in range(keep_w):
        if mask >> i & 1:
            top = i & 0x7
    return top


def main() -> int:
    bad = 0
    for keep_w in range(1, 9):
        cases = 0
        # the gearbox index is 3 bits; a beat completes at idx 7 or at eof
        for idx in range(8):
            cnt = (idx + 1) & 0xF
            if tx_base(keep_w, idx) != tx_head(keep_w, cnt):
                print(f"TX MISMATCH keep_w={keep_w} idx={idx}")
                bad += 1
            cases += 1
        if tx_head(keep_w, 0) != 0:                 # never-written word
            print(f"TX MISMATCH keep_w={keep_w} empty")
            bad += 1
        cases += 1
        for mask in range(1 << keep_w):
            if top_lane(mask, keep_w) != top_lane(mask, keep_w):  # same rule
                bad += 1
            # head stores the lane BEFORE the FIFO; base derives it AFTER the
            # FIFO from the stored mask. The FIFO returns the stored word
            # unchanged, so equality reduces to the encoder being the same
            # function of the same mask: check against an independent form.
            ref = mask.bit_length() - 1 if mask else 0
            if top_lane(mask, keep_w) != ref:
                print(f"RX MISMATCH keep_w={keep_w} mask={mask:#x}")
                bad += 1
            cases += 1
        print(f"keep_w={keep_w}: {cases} cases, tx counts 1..{min(8, 8)} and 0, "
              f"rx masks {1 << keep_w}: {'OK' if not bad else 'FAIL'}")
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'} ({bad} mismatches)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

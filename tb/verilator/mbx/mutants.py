#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""mutants.py - planted RTL defects the packet-mailbox suite must catch (#665 lane F0).

Each arm copies hdl/milan/mailbox to a scratch directory, writes ONE defect
into the copy (a substitution that must occur exactly once), builds the
suite's harness against the copy with the Makefile's own recipe (read through
`make print-vflags`, never restated here) through the adapter the arm names,
runs it, and requires the run to complete with exit 1 and a `[FAIL]` line
naming the arm's check. A positive control, the unmodified RTL through both
adapters, runs first. An arm that names two interfaces builds the contract's
two-interface variant, which the generator writes into the copy (as `make
run-if2` does into its build directory), so a defect only another interface
shows is graded there; that variant has its own positive controls. The tree
is never written: every build directory is under the scratch root.

Usage:
    python3 tb/verilator/mbx/mutants.py [--jobs N] [--keep DIR]
    python3 tb/verilator/mbx/mutants.py --quick   # the suite's default arm: one defect per leaf

--quick runs QUICK only and no controls: the default `make` runs it after
run-wb and run-axil, which are its positive controls.

Exit 0 = every arm caught by its named check and both controls green;
1 = an arm escaped or a control failed; 2 = a fixture did not apply.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE.parents[2] / "hdl" / "milan" / "mailbox"
GEN = HERE.parents[2] / "sw" / "mailbox" / "gen_mailbox.py"
CONTRACT_INC = HERE.parents[2] / "sw" / "firmware" / "ctrl" / "mbx"   # the Makefile's CONTRACT_INC
RTL_FILES = ("KL_mbx_pkg.sv", "KL_mbx_ring.sv", "KL_mbx_rx.sv", "KL_mbx_tx.sv", "KL_mbx_evt.sv", "KL_mbx.sv",
             "KL_mbx_wb.sv", "KL_mbx_axil.sv")


@dataclass(frozen=True)
class Arm:
    """One planted defect: file, substitution, the adapter build, the check that must fail."""

    name: str
    path: str
    old: str
    new: str
    host: int
    needle: str
    ifs: int = 1        # the contract's interface count the arm builds; 2 is the generator's variant


ARMS = (
    Arm("rx-msg-type-ignored", "KL_mbx_rx.sv", "if (MBX_TERM_MASK_TBL_C[j][{1'b0, msg_r}]) begin", "if (1'b1) begin",
        0, "F2 ENTITY_DISCOVER for another entity, and AVAILABLE or DEPARTING"),
    Arm("rx-eq-own-is-eq-zero", "KL_mbx_rx.sv", "MBX_TEST_EQ_OWN_C:        if (field_ok && eqown_r[j])",
        "MBX_TEST_EQ_OWN_C:        if (field_ok && eqzero_r[j])", 0, "F2 ENTITY_DISCOVER for this entity passes"),
    Arm("rx-field-length-unchecked", "KL_mbx_rx.sv", "MBX_TEST_EQ_ZERO_C:       if (field_ok && eqzero_r[j])",
        "MBX_TEST_EQ_ZERO_C:       if (eqzero_r[j])", 0, "F2 a DISCOVER truncated"),
    Arm("rx-writes-past-free-space", "KL_mbx_rx.sv", "+ 32'd2 < 32'(free_w))", "+ 32'd2 < 32'(free_w) + 32'd64)",
        0, "D0 every unread record survives"),
    Arm("rx-bucket-never-drains", "KL_mbx_rx.sv",
        "      if (commit_w && ch_r == MBX_CH_W_C'(c)) tokens = tokens - 9'd1;\n", "", 0,
        "T0 the frames past it count in RATE_DROP"),
    Arm("rx-lanes-big-endian", "KL_mbx_rx.sv", "(5'd8 * 5'(lane_r))", "(5'd8 * (5'd3 - 5'(lane_r)))", 0,
        "F1 frame byte k is ring word"),
    # lane FC: the classification is per match tuple now, so the subtype term is the tuple's
    # (round 2: read from `subtype`, byte 14 held for the decision at byte 15)
    Arm("rx-subtype-ignored", "KL_mbx_rx.sv",
        "(MBX_TUPLE_HAS_SUBTYPE_TBL_C[j] == 0 || subtype == 8'(MBX_TUPLE_SUBTYPE_TBL_C[j]))", "1'b1", 0,
        "C0 ACMP to this talker or this listener passes"),
    Arm("tx-reserved-word-unchecked", "KL_mbx_tx.sv",
        "if (w0_ok_w && (rd_data_i >> MBX_TXREC_W1_RSVD_LSB_C) == 32'd0) begin", "if (w0_ok_w) begin", 0,
        "X1 a malformed TX record counts once in TX_ERR"),
    Arm("tx-refusal-no-flush", "KL_mbx_tx.sv", "tail_r[ch_r] <= tx_head_words_i[16*ch_r +: 16];",
        "tail_r[ch_r] <= tail_r[ch_r];", 0, "X1 and flushes the ring to TX_HEAD"),
    # The merge before commit order: plain round-robin over the channels.
    Arm("tx-round-robin", "KL_mbx_tx.sv", "before_w  = !best_v_r || dseq_w[15];", "before_w  = !best_v_r;", 0,
        "X2 ACMP, ACMP, then AECP committed behind a stalled ACMP frame leave as 1, 1, 2"),
    Arm("tx-seq-wrap-unsigned", "KL_mbx_tx.sv", "before_w  = !best_v_r || dseq_w[15];",
        "before_w  = !best_v_r || seq_w < best_seq_r;", 0, "X2 SEQ 0xFFFF leaves before SEQ 0x0000"),
    Arm("tx-ties-fixed-priority", "KL_mbx_tx.sv", "sum       = int'(last_ch_r) + int'(scan_k_r);",
        "sum       = int'(scan_k_r) - 1;", 0, "X2 equal SEQs leave round-robin"),
    Arm("evt-rearm-keeps-tag", "KL_mbx_evt.sv", "          tag_r[SW_C'(tmr_slot_i)] <= tmr_tag_i;\n", "", 0,
        "M1 a re-armed slot expires once, with the second arm's tag"),
    Arm("evt-cancel-arms", "KL_mbx_evt.sv", "armed_r[SW_C'(tmr_slot_i)] <= (32'(tmr_op_i) == MBX_TMR_OP_ARM_C);",
        "armed_r[SW_C'(tmr_slot_i)] <= 1'b1;", 0, "M0 no event by +4 ms"),
    Arm("evt-tick-count-lost", "KL_mbx_evt.sv", "tick_cnt_r <= tick_cnt_r + 16'd1;", "tick_cnt_r <= 16'd1;", 0,
        "K1 carrying every tick"),
    Arm("top-tick-always-enabled", "KL_mbx.sv", ".tick_en_i         (tick_ctl_r[MBX_TICK_CTL_EN_LSB_C]),",
        ".tick_en_i         (1'b1),", 0, "K0 no TICK while TICK_CTL.EN is clear"),
    Arm("top-gm-hi-live", "KL_mbx.sv", "mbx_place_f(32'(gm_hi_snap_r[0]),",
        "mbx_place_f(32'(gm_id_i[64*0 + 32 +: 32]),",
        0, "G0 GM_HI reads the snapshot"),
    Arm("top-partial-strobe-accepted", "KL_mbx.sv",
        "assign wr_w      = host_req_i && host_we_i && (host_be_i == 4'hF);",
        "assign wr_w      = host_req_i && host_we_i;", 0, "R2 a write with a partial strobe leaves the register"),
    Arm("top-irq-ignores-enable", "KL_mbx.sv", ") & irq_enable_r);", ") & 32'hFFFF_FFFF);", 0,
        "R2 a cause that is not enabled leaves the line low"),
    Arm("rx-maap-empty-count-overlaps", "KL_mbx_rx.sv", "overlap  = (field_r[j][15:0] != 16'd0) && (maap_count_i",
        "overlap  = (maap_count_i", 0, "C2 MAAP PROBE/DEFEND/ANNOUNCE overlapping this range pass"),
    Arm("rx-drop-uncounted", "KL_mbx_rx.sv", "drop_r[c] != 16'hFFFF) drop_r[c] <= drop_r[c] + 16'd1;",
        "drop_r[c] != 16'hFFFF) drop_r[c] <= drop_r[c];", 0, "D0 a frame the free space cannot hold counts in RX_DROP"),
    Arm("rx-refill-slow", "KL_mbx_rx.sv", "+ 32'd1 >= MBX_CH_RATE_REFILL_MS_TBL_C[c]);",
        "+ 32'd1 >= 2 * MBX_CH_RATE_REFILL_MS_TBL_C[c]);", 0, "T1 one refill period buys exactly one more frame"),
    Arm("tx-lanes-reversed", "KL_mbx_tx.sv", "assign tx_data_o  = pw_r[8*lane_r +: 8];",
        "assign tx_data_o  = pw_r[8*(2'd3 - lane_r) +: 8];", 0, "X0 the first frame leaves byte for byte"),
    Arm("evt-link-never-posts", "KL_mbx_evt.sv", "if (!any_w && link_up_i[i] != posted_up_r[i]) begin",
        "if (1'b0) begin", 0, "E0 a link rise posts a LINK event"),
    Arm("evt-gm-domain-dropped", "KL_mbx_evt.sv",
        "w3_w = 32'(gptp_domain_i[8*src_if_w +: 8]) << MBX_EV_GM_W3_DOMAIN_LSB_C;", "w3_w = '0;", 0,
        "E1 GM DOMAIN"),
    Arm("evt-expires-late", "KL_mbx_evt.sv", "$signed(now_ms_i - dl_r[scan_r]) >= 0",
        "$signed(now_ms_i - dl_r[scan_r]) > 0",
        0, "M0 slot 3 expires at its deadline"),
    Arm("top-irq-enable-unmasked", "KL_mbx.sv",
        "if (wr_w && off_w == AW2_C'(MBX_REG_IRQ_ENABLE_C)) irq_enable_r <= host_wdata_i & (",
        "if (wr_w && off_w == AW2_C'(MBX_REG_IRQ_ENABLE_C)) irq_enable_r <= host_wdata_i | (", 0,
        "R1 IRQ_ENABLE keeps RX[7:0], EVT and ERR only"),
    Arm("rx-closed-channel-stores", "KL_mbx_rx.sv", "hit_r      <= cls_hit_w && open_i[cls_ch_w];",
        "hit_r      <= cls_hit_w;", 0, "F0 a closed channel stores nothing"),
    # lane FC: a channel's second EtherType is its second match tuple now (MVRP's)
    Arm("rx-second-ethertype-ignored", "KL_mbx_rx.sv",
        "for (int j = 0; j < int'(NM_C); j++) begin",
        "for (int j = 0; j < int'(NM_C); j += int'(MBX_MAX_TUPLES_C)) begin",
        0, "C3 every MSRP and MVRP PDU reaches the SRP ring"),
    # The three host-counter guards (R496-1 F4).
    Arm("rx-tail-unguarded", "KL_mbx_rx.sv",
        "free_w       = (used_w > ring_words_w) ? 16'd0 : ring_words_w - used_w;",
        "free_w       = ring_words_w - used_w;", 0, "H0 an RX_TAIL ahead of RX_HEAD stores nothing"),
    Arm("tx-head-unguarded", "KL_mbx_tx.sv", "&& occ_w <= ring_words_w && rec_words_w <= occ_w;",
        "&& rec_words_w <= occ_w;", 0, "H1 a TX_HEAD more than the ring ahead of TX_TAIL is refused"),
    Arm("evt-tail-unguarded", "KL_mbx_evt.sv",
        "free_w = (used_w > 16'(MBX_EVT_WORDS_C)) ? 16'd0 : 16'(MBX_EVT_WORDS_C) - used_w;",
        "free_w = 16'(MBX_EVT_WORDS_C) - used_w;", 0, "H2 an EVT_TAIL ahead of EVT_HEAD posts nothing"),
    Arm("evt-only-exact-deadline", "KL_mbx_evt.sv", "$signed(now_ms_i - dl_r[scan_r]) >= 0",
        "now_ms_i == dl_r[scan_r]", 0, "M2 a deadline already past expires at once"),
    Arm("wb-address-shifted", "KL_mbx_wb.sv", "assign host_addr_o  = wb_adr_i[MBX_ADDR_W_C-1:0];",
        "assign host_addr_o  = {wb_adr_i[MBX_ADDR_W_C-2:0], 1'b0};", 0, "R0 CAPS.N_CH"),
    Arm("axil-read-uses-write-address", "KL_mbx_axil.sv",
        "assign host_addr_o  = go_wr_w ? aw_addr_r : ar_addr_r;", "assign host_addr_o  = aw_addr_r;", 1,
        "R0 CAPS.N_CH"),
    # The two combinational READYs of the adapter this one replaced: AR
    # yielding to a write offered in the same cycle, and AW waiting for W.
    Arm("axil-arready-follows-awvalid", "KL_mbx_axil.sv", "assign s_arready_o  = !ar_full_r;",
        "assign s_arready_o  = !ar_full_r && !s_awvalid_i;", 1, "A0 no AXI4-Lite output followed"),
    Arm("axil-awready-waits-for-wvalid", "KL_mbx_axil.sv", "assign s_awready_o  = !aw_full_r;",
        "assign s_awready_o  = !aw_full_r && s_wvalid_i;", 1, "A0 no AXI4-Lite output followed"),
    Arm("axil-write-without-w", "KL_mbx_axil.sv", "assign wr_ok_w = aw_full_r && w_full_r && !bvalid_r && !busy_r;",
        "assign wr_ok_w = aw_full_r && !bvalid_r && !busy_r;", 1, "A1 and no B answers it before its W"),
    Arm("axil-write-ignores-b-slot", "KL_mbx_axil.sv",
        "assign wr_ok_w = aw_full_r && w_full_r && !bvalid_r && !busy_r;",
        "assign wr_ok_w = aw_full_r && w_full_r && !busy_r;", 1, "A4 each write is answered by exactly one B"),
    Arm("axil-b-dropped-without-bready", "KL_mbx_axil.sv", "else if (s_bready_i) bvalid_r <= 1'b0;",
        "else bvalid_r <= 1'b0;", 1, "A4 BVALID holds for 10 clocks"),
    Arm("axil-r-dropped-without-rready", "KL_mbx_axil.sv",
        "end else if (s_rready_i) begin\n        rvalid_r <= 1'b0;", "end else begin\n        rvalid_r <= 1'b0;", 1,
        "A5 RVALID holds for 10 clocks"),
    Arm("axil-rdata-follows-port", "KL_mbx_axil.sv", "assign s_rdata_o    = rdata_r;",
        "assign s_rdata_o    = host_rdata_i;", 1, "A5 RDATA and RRESP hold with it"),
    Arm("axil-read-before-write", "KL_mbx_axil.sv", "assign go_rd_w = rd_ok_w && !wr_ok_w;",
        "assign go_rd_w = rd_ok_w;", 1, "A3 the read answers its own address"),
    # A beat taken on the cycle its slot drains: the slot loads only when
    # empty, so the beat is lost and every later W pairs with the next AW.
    Arm("axil-wready-while-issuing", "KL_mbx_axil.sv", "assign s_wready_o   = !w_full_r;",
        "assign s_wready_o   = !w_full_r || go_wr_w;", 1, "A7 each write's data lands at its own address"),
    Arm("axil-awready-while-issuing", "KL_mbx_axil.sv", "assign s_awready_o  = !aw_full_r;",
        "assign s_awready_o  = !aw_full_r || go_wr_w;", 1, "A7 each write's data lands at its own address"),
    Arm("axil-reset-keeps-aw", "KL_mbx_axil.sv", "      aw_full_r <= 1'b0;\n      aw_addr_r <= '0;\n",
        "      aw_addr_r <= '0;\n", 1, "A6 an AW taken before a reset is forgotten"),
    # ---- lane FC: one defect per rule of the full-tuple filter ----
    # 1. tagged frames never reach a mailbox: a classifier that takes a C-tag's
    #    TPID for any tuple's EtherType, so a tagged MSRP or MVRP frame, whose
    #    tuples read no subtype, lands in the SRP ring
    Arm("rx-tpid-matches-a-tuple", "KL_mbx_rx.sv",
        "if (!cls_hit_w && dst_ok && ethertype == 16'(MBX_TUPLE_ETHERTYPE_TBL_C[j])",
        "if (!cls_hit_w && dst_ok && (ethertype == 16'(MBX_TUPLE_ETHERTYPE_TBL_C[j]) || ethertype == 16'h8100)", 0,
        "Q1 tagged, it (srp MSRP): no RX record"),
    # 2. each channel matches its exact tuple: destination, EtherType, subtype
    Arm("rx-dst-ignored", "KL_mbx_rx.sv",
        "dst_ok = (MBX_TUPLE_DST_TBL_C[j] == MBX_DST_MAC_C\n"
        "                && dst_r == {16'(MBX_TUPLE_DST_HI_TBL_C[j]), MBX_TUPLE_DST_LO_TBL_C[j]})\n"
        "               || (MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && own_if_w && dst_r == own_mac_w);",
        "dst_ok = MBX_TUPLE_DST_TBL_C[j] != MBX_DST_NONE_C;", 0, "Q2 to another destination MAC, it (adp)"),
    Arm("rx-multicast-dst-ignored", "KL_mbx_rx.sv",
        "                && dst_r == {16'(MBX_TUPLE_DST_HI_TBL_C[j]), MBX_TUPLE_DST_LO_TBL_C[j]})", ")", 0,
        "Q2 to another destination MAC, it (srp MSRP)"),
    Arm("rx-ethertype-ignored", "KL_mbx_rx.sv",
        "if (!cls_hit_w && dst_ok && ethertype == 16'(MBX_TUPLE_ETHERTYPE_TBL_C[j])",
        "if (!cls_hit_w && dst_ok", 0, "Q3 under another control EtherType, it (adp)"),
    # 3. own unicast is the arrival interface's MAC, never any unicast
    Arm("rx-own-any-unicast", "KL_mbx_rx.sv",
        "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && own_if_w && dst_r == own_mac_w)",
        "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && !dst_r[40])", 0,
        "Q2 to another destination MAC, it (aecp, command)"),
    Arm("rx-own-mac-of-interface-0", "KL_mbx_rx.sv", "if (int'(if_r) == i) begin\n        own_mac_w",
        "if (i == 0) begin\n        own_mac_w", 0,
        "Q8 another interface's own MAC, or one on an index with no interface, reaches no ring"),
    Arm("rx-own-mac-low-word-only", "KL_mbx_rx.sv", "&& own_if_w && dst_r == own_mac_w)",
        "&& own_if_w && dst_r[31:0] == own_mac_w[31:0])", 0, "Q8 a MAC differing from OWN_MAC in MAC[47:32] only"),
    Arm("top-own-mac-halves-swapped", "KL_mbx.sv", "own_mac_w[48*i +: 48] = {own_mac_hi_r[i], own_mac_lo_r[i]};",
        "own_mac_w[48*i +: 48] = {own_mac_lo_r[i][15:0], own_mac_lo_r[i][31:16], own_mac_hi_r[i]};", 0,
        "Q0 a valid frame reaches its channel (acmp, own unicast)"),
    Arm("top-own-mac-hi-read-from-lo", "KL_mbx.sv", "reg_rdata_w = 32'(own_mac_hi_r[0]);",
        "reg_rdata_w = 32'(own_mac_lo_r[0]);", 0, "R1 OWN_MAC_LO keeps every bit and OWN_MAC_HI keeps MAC[47:32] only"),
    # 4. AECP: (command AND target = own) OR (response AND controller = own),
    #    planted in the generated package the RTL reads its terms from
    Arm("pkg-aecp-command-only", "KL_mbx_pkg.sv", "MBX_CH_AECP_T1_TEST_C = 32'd2;", "MBX_CH_AECP_T1_TEST_C = 32'd0;", 0,
        "Q7 the CONTROLLER_AVAILABLE response for this controller reaches the AECP ring"),
    Arm("pkg-aecp-target-term-any-type", "KL_mbx_pkg.sv", "MBX_CH_AECP_T0_MSG_MASK_C = 32'h00005555;",
        "MBX_CH_AECP_T0_MSG_MASK_C = 32'h0000FFFF;", 0,
        "Q5 an AECP response for another controller, even to this target"),
    Arm("pkg-aecp-controller-term-any-type", "KL_mbx_pkg.sv", "MBX_CH_AECP_T1_MSG_MASK_C = 32'h0000AAAA;",
        "MBX_CH_AECP_T1_MSG_MASK_C = 32'h0000FFFF;", 0,
        "Q5 an AECP command for another target, even with this controller"),
    # 5. FILTER_MISMATCH: an untagged control frame failing its tuple, once;
    #    never a valid, tagged, identity-refused or short one; it sets ERR
    Arm("rx-mismatch-never-counted", "KL_mbx_rx.sv", "mis_r      <= ctrl_et_w && !cls_hit_w;", "mis_r      <= 1'b0;", 0,
        "Q2 to another destination MAC, it (adp): FILTER_MISMATCH counts it once"),
    Arm("rx-mismatch-counts-valid", "KL_mbx_rx.sv", "mis_r      <= ctrl_et_w && !cls_hit_w;",
        "mis_r      <= ctrl_et_w;",
        0, "Q0 a valid frame never counts in FILTER_MISMATCH (adp)"),
    Arm("rx-mismatch-counts-any-ethertype", "KL_mbx_rx.sv",
        "if (MBX_TUPLE_DST_TBL_C[j] != MBX_DST_NONE_C && ethertype == 16'(MBX_TUPLE_ETHERTYPE_TBL_C[j]))\n"
        "        ctrl_et_w = 1'b1;", "ctrl_et_w = 1'b1;", 0, "Q1 tagged, it (adp): FILTER_MISMATCH does not count it"),
    Arm("rx-mismatch-counts-identity-refusals", "KL_mbx_rx.sv", "assign mis_w       = fin_ready_w && mis_r;",
        "assign mis_w       = fin_ready_w && (mis_r || (hit_r && !rule_pass_w));", 0,
        "Q5 ENTITY_DISCOVER for another entity: FILTER_MISMATCH does not count it"),
    Arm("rx-mismatch-counted-twice", "KL_mbx_rx.sv", "mismatch_r <= mismatch_r + 16'd1;",
        "mismatch_r <= mismatch_r + 16'd2;", 0, "Q9 five tuple failures in a row count five"),
    Arm("rx-mismatch-needs-an-open-channel", "KL_mbx_rx.sv", "mis_r      <= ctrl_et_w && !cls_hit_w;",
        "mis_r      <= ctrl_et_w && !cls_hit_w && open_i != '0;", 0,
        "Q9 with every channel closed, an untagged AAF: FILTER_MISMATCH counts it once"),
    Arm("rx-short-frame-counted", "KL_mbx_rx.sv", "            cls_done_r <= 1'b1;\n            hit_r      <= 1'b0;\n",
        "            cls_done_r <= 1'b1;\n            hit_r      <= 1'b0;\n            mis_r      <= 1'b1;\n", 0,
        "Q9 valid, tagged and identity-refused frames, and one that ends before byte 14, leave it"),
    Arm("rx-mismatch-sets-no-err", "KL_mbx_rx.sv", "assign err_p_o     = drop_w || rate_w || mis_w;",
        "assign err_p_o     = drop_w || rate_w;", 0, "Q9 a mismatch sets IRQ_STATUS.ERR"),
    # the token buckets stay, apart from the filter: a refusal takes no token
    Arm("rx-refusal-takes-a-token", "KL_mbx_rx.sv", "if (commit_w && ch_r == MBX_CH_W_C'(c)) tokens = tokens - 9'd1;",
        "if ((commit_w || (fin_ready_w && hit_r && !rule_pass_w)) && ch_r == MBX_CH_W_C'(c)) tokens = tokens - 9'd1;",
        0, "Q10 refusals by the filter take no token"),
)


def _both(name: str, path: str, old: str, new: str, needle: str, ifs: int = 1) -> tuple[Arm, Arm]:
    """One defect planted through each bus adapter: `name` on Wishbone, `name-axil` on AXI4-Lite."""
    return Arm(name, path, old, new, 0, needle, ifs), Arm(f"{name}-axil", path, old, new, 1, needle, ifs)


#: ---- lane FC round 2: the MAAP DEFEND to own unicast (IEEE 1722-2016 B.2.1),
#: one defect per rule through both adapters (the model's twins are in
#: sw/firmware/ctrl/test/ctrl_mutants.py) ----
ARMS += (
    # a DEFEND to this interface's own MAC is delivered: the tuple dropped from
    # the contract, the message type read one byte early, the channel decided
    # at byte 14 before the message type arrives
    *_both("pkg-maap-defend-tuple-dropped", "KL_mbx_pkg.sv", "MBX_CH_MAAP_M1_DST_C = 32'd2;",
           "MBX_CH_MAAP_M1_DST_C = 32'd0;", "Q11 a DEFEND to this interface's own MAC reaches the MAAP ring"),
    *_both("rx-msg-type-off-by-one", "KL_mbx_rx.sv",
           "msg       = (cnt_r == 11'(MBX_MSG_TYPE_BYTE_C)) ? rx_data_i[3:0] : 4'd0;", "msg       = subtype[3:0];",
           "Q11 a DEFEND to this interface's own MAC reaches the MAAP ring"),
    *_both("rx-classified-before-msg-type", "KL_mbx_rx.sv",
           "assign cls_at_w = (cnt_r == 11'(MBX_MSG_TYPE_BYTE_C)) || (rx_last_i && cnt_r == 11'(MBX_SUBTYPE_BYTE_C));",
           "assign cls_at_w = (cnt_r == 11'(MBX_SUBTYPE_BYTE_C));",
           "Q11 a DEFEND to this interface's own MAC reaches the MAAP ring"),
    # a PROBE or ANNOUNCE to it is rejected and counted: the tuple's message
    # types ignored, a frame to the own MAC never counted
    *_both("rx-tuple-msg-type-ignored", "KL_mbx_rx.sv",
           "\n          && MBX_TUPLE_MSG_MASK_TBL_C[j][{1'b0, msg}]) begin", ") begin",
           "Q11 a PROBE to this interface's own MAC: no RX record"),
    *_both("rx-own-unicast-never-counted", "KL_mbx_rx.sv", "mis_r      <= ctrl_et_w && !cls_hit_w;",
           "mis_r      <= ctrl_et_w && !cls_hit_w && !(own_if_w && dst_r == own_mac_w);",
           "Q11 a PROBE to this interface's own MAC: FILTER_MISMATCH counts it once"),
    # a DEFEND to a foreign unicast is rejected: the DEFEND tuple takes any unicast
    *_both("rx-defend-any-unicast", "KL_mbx_rx.sv",
           "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && own_if_w && dst_r == own_mac_w)",
           "(MBX_TUPLE_DST_TBL_C[j] == MBX_DST_OWN_C && ((own_if_w && dst_r == own_mac_w)\n"
           "                   || (MBX_TUPLE_MSG_MASK_TBL_C[j] != 32'hFFFF && !dst_r[40])))",
           "Q11 a DEFEND to a unicast MAC no interface owns: no RX record"),
    # a frame that ends at byte 14, before its message type, is still decided:
    # without the last-byte decision it never is, and the receive path waits
    *_both("rx-short-frame-never-classified", "KL_mbx_rx.sv",
           " || (rx_last_i && cnt_r == 11'(MBX_SUBTYPE_BYTE_C));", ";",
           "Q11 a DEFEND to this interface's own MAC that ends at byte 14, before its message_type"),
)


#: ---- lane F3: the adp channel's bound talkers (#665, comment 6029368753),
#: one defect per rule through both adapters (the model's twins are in
#: sw/firmware/ctrl/test/ctrl_mutants.py). Round 3 holds the table in
#: distributed RAM and compares it byte by byte (comment 6032450078): the
#: round-2 rules are planted on the lines that now carry them ----
ARMS += (
    # an ENTITY_AVAILABLE or ENTITY_DEPARTING of a bound talker passes: the term
    # dropped from the contract, the identity's halves swapped into the compare
    *_both("pkg-adp-bound-term-dropped", "KL_mbx_pkg.sv", "MBX_CH_ADP_T2_TEST_C = 32'd5;",
           "MBX_CH_ADP_T2_TEST_C = 32'd0;", "Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring"),
    *_both("rx-bound-copy-halves-swapped", "KL_mbx_rx.sv", "RW_C'(2 * int'(cp_k_r) + int'(cp_b_r[2]))",
           "RW_C'(2 * int'(cp_k_r) + int'(!cp_b_r[2]))",
           "Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring"),
    # only those two message types, only the whole identity, only an enabled entry
    *_both("pkg-adp-bound-term-any-type", "KL_mbx_pkg.sv", "MBX_CH_ADP_T2_MSG_MASK_C = 32'h00000003;",
           "MBX_CH_ADP_T2_MSG_MASK_C = 32'h0000FFFF;",
           "Q12 no other message_type of a bound talker passes on its entity_id"),
    *_both("rx-bound-low-word-only", "KL_mbx_rx.sv", "(cnt_r == 11'(BO_C) || match_r[e])",
           "(cnt_r == 11'(BO_C + 4) || match_r[e])", "Q12 an entity_id differing from the entry in [63:32] only"),
    *_both("rx-bound-enable-ignored", "KL_mbx_rx.sv", "live_w[e] = fok_w && en_r[int'(fif_w) * int'(NB_C) + e] && ",
           "live_w[e] = fok_w && ", "Q12 an entry with BOUND_EN clear, its identity still written"),
    *_both("rx-bound-field-length-unchecked", "KL_mbx_rx.sv",
           "MBX_TEST_EQ_BOUND_C:      if (field_ok && bound_hit_w)", "MBX_TEST_EQ_BOUND_C:      if (bound_hit_w)",
           "Q12 an ENTITY_AVAILABLE of a bound talker that ends inside its entity_id"),
    # every entry takes part, and each is written and read at its own address
    *_both("rx-bound-first-entry-only", "KL_mbx_rx.sv", "assign bound_hit_w = |(match_r & live_w);",
           "assign bound_hit_w = match_r[0] && live_w[0];", "Q12 the last entry passes its talker"),
    *_both("rx-bound-entry-write-lands-in-entry-0", "KL_mbx_rx.sv",
           "assign rb_wa_w = RW_C'(2 * int'(hk_w) + int'(hhi_w));", "assign rb_wa_w = RW_C'(int'(hhi_w));",
           "R1 each bound-talker entry keeps"),
    *_both("top-bound-entry-decoded-as-0", "KL_mbx.sv", "bnd_entry_w = 5'(entry);", "bnd_entry_w = '0;",
           "R1 each bound-talker entry keeps"),
    *_both("top-bound-en-read-from-eid", "KL_mbx.sv",
           "reg_rdata_w = mbx_place_f(32'(bnd_en_w), MBX_BOUND_EN_EN_LSB_C, MBX_BOUND_EN_EN_WIDTH_C);",
           "reg_rdata_w = bnd_eid_w;", "R1 each bound-talker entry keeps"),
    # the table read is the arrival interface's: at one interface an index with
    # no interface behind it shows it, at two the other interface's table does
    *_both("rx-bound-table-of-interface-0", "KL_mbx_rx.sv",
           "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
           "assign {fok_w, fif_w} = {1'b1, MBX_IF_W_C'(0)};",
           "Q13 on another interface, or an index with no interface, it reaches no ring"),
    *_both("rx-bound-enable-of-interface-0", "KL_mbx_rx.sv", "en_r[int'(fif_w) * int'(NB_C) + e]", "en_r[e]",
           "Q13 a talker bound on interface i passes on interface i", 2),
    *_both("top-bound-write-ignores-interface", "KL_mbx.sv",
           "bnd_if_w    = MBX_IF_W_C'(rel >> $clog2(MBX_BND_STRIDE_C));", "bnd_if_w    = '0;",
           "Q13 a talker bound on interface i passes on interface i", 2),
    *_both("rx-bound-taps-of-interface-0", "KL_mbx_rx.sv",
           "eq_w[e]   = rx_data_i == c_tap_w[int'(fif_w) * int'(NB_C) + e];", "eq_w[e]   = rx_data_i == c_tap_w[e];",
           "Q13 a talker bound on interface i passes on interface i", 2),
    *_both("rx-bound-copy-into-interface-0", "KL_mbx_rx.sv", "c_sh_w[k] = cp_step_w && int'(cp_k_r) == k;",
           "c_sh_w[k] = cp_step_w && int'(cp_k_r) % int'(NB_C) == k;",
           "Q13 a talker bound on interface i passes on interface i", 2),
    # round 3: each identity byte against the same byte of every entry, as it
    # arrives: a wrong tap, the copier's bytes in the wrong lanes, a byte left out
    *_both("rx-bound-byte-index-off-by-one", "KL_mbx_rx.sv", "assign c_tap_w[k] = sr_r[cmp_b_w];",
           "assign c_tap_w[k] = sr_r[cmp_b_w + 3'd1];",
           "Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring"),
    *_both("rx-bound-copy-lanes-reversed", "KL_mbx_rx.sv", "rb_q_w[8 * int'(cp_b_r[1:0]) +: 8]",
           "rb_q_w[8 * (3 - int'(cp_b_r[1:0])) +: 8]",
           "Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring"),
    *_both("rx-bound-last-byte-uncompared", "KL_mbx_rx.sv", "(32'(cnt_r) - BO_C < 32'd8)",
           "(32'(cnt_r) - BO_C < 32'd7)",
           "Q15 an entity_id differing from the entry in one identity byte is refused"),
    # the match flag is the frame's own: never armed again, or the last
    # frame's carried into the first byte of the next
    *_both("rx-bound-flag-never-rearmed", "KL_mbx_rx.sv", "(cnt_r == 11'(BO_C) || match_r[e])", "match_r[e]",
           "Q14 the bound talker's right after it passes"),
    *_both("rx-bound-flag-carried-into-the-next-frame", "KL_mbx_rx.sv",
           "match_r[e] <= live_w[e] && eq_w[e] && (cnt_r == 11'(BO_C) || match_r[e]);",
           "match_r[e] <= live_w[e] && (eq_w[e] || (cnt_r == 11'(BO_C) && match_r[e])) "
           "&& (cnt_r == 11'(BO_C) || match_r[e]);",
           "Q14 right after that, one differing from it in the first identity byte only"),
    # an entry takes part from the first identity byte to the verdict only
    # while BOUND_EN is set and no copy of it is owed
    *_both("rx-bound-liveness-at-the-verdict-only", "KL_mbx_rx.sv", "else match_r[e] <= match_r[e] && live_w[e];",
           "else match_r[e] <= match_r[e];", "Q18 one stalled while BOUND_EN is cleared and set again"),
    *_both("rx-bound-live-while-owed", "KL_mbx_rx.sv", " && !owed_r[int'(fif_w) * int'(NB_C) + e];", ";",
           "Q19 one stalled while BOUND_EN is set again alone"),
    # round 4 (R530-2-F1): the verdict reads the table of the interface the frame
    # arrived on, not the one presented with the next frame, at one interface
    # and at two; and the owed copy gates each interface's own entries
    *_both("rx-bound-verdict-of-the-presented-interface", "KL_mbx_rx.sv",
           "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
           "assign {fok_w, fif_w} = (int'(rx_if_i) < int'(MBX_N_IF_C)) ? {1'b1, rx_if_i} : '0;",
           "Q22 a bound talker's ENTITY_AVAILABLE with the next frame, on another index, right behind it passes alone"),
    *_both("rx-bound-verdict-of-the-presented-interface-if2", "KL_mbx_rx.sv",
           "assign {fok_w, fif_w} = (int'(if_r) < int'(MBX_N_IF_C)) ? {1'b1, if_r} : '0;",
           "assign {fok_w, fif_w} = (int'(rx_if_i) < int'(MBX_N_IF_C)) ? {1'b1, rx_if_i} : '0;",
           "Q22 a bound talker's ENTITY_AVAILABLE with the next frame, on another index, right behind it passes alone",
           2),
    *_both("rx-bound-live-reads-interface-0-owed", "KL_mbx_rx.sv", " && !owed_r[int'(fif_w) * int'(NB_C) + e];",
           " && !owed_r[e];", "Q23 on each interface past the first, one stalled while BOUND_EN is set again alone", 2),
    # the copier: owed by BOUND_EN set and by a word written while it is, giving
    # way to the host's reads, starting over on a rewrite, reaching every entry
    *_both("rx-bound-copy-not-owed-on-enable", "KL_mbx_rx.sv",
           "(heid_w ? en_r[hk_w] : bnd_wdata_i[MBX_BOUND_EN_EN_LSB_C])", "(heid_w && en_r[hk_w])",
           "Q12 an ENTITY_AVAILABLE of a bound talker reaches the adp ring"),
    *_both("rx-bound-copy-not-owed-on-rewrite", "KL_mbx_rx.sv",
           "(heid_w ? en_r[hk_w] : bnd_wdata_i[MBX_BOUND_EN_EN_LSB_C])",
           "(!heid_w && bnd_wdata_i[MBX_BOUND_EN_EN_LSB_C])", "Q16 the new talker passes"),
    *_both("rx-bound-copy-ignores-the-host", "KL_mbx_rx.sv", "assign cp_step_w = cp_busy_r && !bnd_req_i;",
           "assign cp_step_w = cp_busy_r;", "Q20 the entry copied meanwhile passes its talker"),
    *_both("rx-bound-copy-not-restarted", "KL_mbx_rx.sv",
           "        if (cp_busy_r && hk_w == cp_k_r) cp_b_r <= '0;\n", "",
           "Q21 BOUND_EID_LO rewritten at each of 32 clocks"),
    *_both("rx-bound-scan-skips-the-last-entry", "KL_mbx_rx.sv", "(32'(cp_k_r) == NE_C - 1)",
           "(32'(cp_k_r) == NE_C - 2)",
           "Q12 the last entry passes its talker"),
    # distributed RAM keeps its contents through a reset: a word not written
    # since reads 0 and is copied as 0
    *_both("rx-bound-unwritten-word-copied-raw", "KL_mbx_rx.sv",
           "c_d_w = rb_vld_w ? rb_q_w[8 * int'(cp_b_r[1:0]) +: 8] : 8'd0;",
           "c_d_w = rb_q_w[8 * int'(cp_b_r[1:0]) +: 8];",
           "Q17 it holds talker 0, whose ENTITY_AVAILABLE passes"),
    *_both("top-bound-unwritten-word-read-raw", "KL_mbx.sv", " && bnd_eid_vld_w) reg_rdata_w = bnd_eid_w;",
           ") reg_rdata_w = bnd_eid_w;", "Q17 after a reset every entry of every interface's table reads 0 again"),
    *_both("rx-bound-valid-kept-through-reset", "KL_mbx_rx.sv", "      vlo_r     <= '0;\n", "",
           "Q17 after a reset every entry of every interface's table reads 0 again"),
)


#: ---- lane F-INT: the publication block (#665, comment 6088423771), one
#: defect per rule through both adapters (the model's twins are in
#: sw/firmware/ctrl/test/ctrl_mutants.py) ----
ARMS += (
    # the stream_id reaches the datapath only while SID_VALID is set, whole
    *_both("top-pub-sid-valid-held-high", "KL_mbx.sv",
           "pub_sid_valid_o[MBX_N_PUB_SINKS_C*i + k] = mbx_field_f(32'(pub_binding_r[i][k]), "
           "MBX_BINDING_SID_VALID_LSB_C, MBX_BINDING_SID_VALID_WIDTH_C) != 0;",
           "pub_sid_valid_o[MBX_N_PUB_SINKS_C*i + k] = 1'b1;",
           "P3 with SID_VALID clear the datapath reads the stream_id as 0"),
    *_both("top-pub-sid-halves-swapped", "KL_mbx.sv",
           "= {pub_sid_hi_r[i][k], pub_sid_lo_r[i][k]};", "= {pub_sid_lo_r[i][k], pub_sid_hi_r[i][k]};",
           "P3 with SID_VALID set the datapath reads SID_HI:SID_LO"),
    # every field on its own output
    *_both("top-pub-priority-from-vid", "KL_mbx.sv",
           "(mbx_field_f(32'(pub_sr_domain_r[i]), MBX_SR_DOMAIN_PRIORITY_LSB_C, MBX_SR_DOMAIN_PRIORITY_WIDTH_C));",
           "(mbx_field_f(32'(pub_sr_domain_r[i]), MBX_SR_DOMAIN_VID_LSB_C, MBX_SR_DOMAIN_PRIORITY_WIDTH_C));",
           "P2 every field reaches the datapath on its own output"),
    *_both("top-pub-bound-from-sid-valid", "KL_mbx.sv",
           "pub_bound_o[MBX_N_PUB_SINKS_C*i + k] = mbx_field_f(32'(pub_binding_r[i][k]), MBX_BINDING_BOUND_LSB_C,",
           "pub_bound_o[MBX_N_PUB_SINKS_C*i + k] = mbx_field_f(32'(pub_binding_r[i][k]), "
           "MBX_BINDING_SID_VALID_LSB_C,",
           "P3 and BOUND alone is on its output"),
    # each register keeps its own fields, at its own sink
    *_both("top-pub-domain-unmasked", "KL_mbx.sv", "pub_sr_domain_r[pub_if_w] <= 25'(host_wdata_i & (",
           "pub_sr_domain_r[pub_if_w] <= 25'(host_wdata_i | 32'd0 & (",
           "P1 DA_GATE keeps OPEN, LICENCE ACTIVE"),
    *_both("top-pub-sink-index-dropped", "KL_mbx.sv", "pub_binding_r[pub_if_w][pub_k_w] <= 2'(",
           "pub_binding_r[pub_if_w][0] <= 2'(",
           "P1 each interface's registers and each sink's entry read back what was written"),
    # nothing outside the registers takes a write: a hole aliasing a
    # register, and (two interfaces) an index past the build aliasing one
    *_both("top-pub-hole-aliases-a-register", "KL_mbx.sv",
           "pub_reg_w  = pub_sink_w ? (in_sinks & AW2_C'(MBX_PUB_SINK_STRIDE_C - 1)) : in_if;",
           "pub_reg_w  = pub_sink_w ? (in_sinks & AW2_C'(MBX_PUB_SINK_STRIDE_C - 1)) : (in_if & AW2_C'(32'hF));",
           "P4 every hole of every interface block"),
    *_both("top-pub-interface-unchecked", "KL_mbx.sv",
           "                 && (rel >> $clog2(MBX_PUB_STRIDE_C)) < AW2_C'(MBX_N_IF_C)\n", "",
           "P4 and none of those writes moved a register or an output", 2),
    *_both("top-pub-partial-strobe-accepted", "KL_mbx.sv", "end else if (wr_w && pub_at_w) begin",
           "end else if (host_req_i && host_we_i && pub_at_w) begin",
           "P4 a write with a partial strobe leaves the register and the output"),
    # a reset clears the whole block
    *_both("top-pub-licence-kept-through-reset", "KL_mbx.sv", "        pub_licence_r[i] <= '0;\n", "",
           "P5 a reset clears every publication register and every output"),
)


#: One defect per leaf and one in the skeleton, one in the filter's tuple and
#: one in the publication block: the arms the suite's default target runs.
QUICK = ("rx-lanes-big-endian", "tx-refusal-no-flush", "evt-tick-count-lost", "top-partial-strobe-accepted",
         "rx-dst-ignored", "top-pub-sid-valid-held-high")


def recipe() -> list[str]:
    """The Makefile's verilator command, one word per line."""
    res = subprocess.run(["make", "-s", "--no-print-directory", "print-vflags"], cwd=HERE, capture_output=True,
                         text=True, check=True)
    return [w for w in res.stdout.splitlines() if w]


def variant(copy: Path, ifs: int) -> None:
    """The contract's `ifs`-interface package, skeleton and header, written by
    the generator over the copy's (never the tree's)."""
    res = subprocess.run([sys.executable, "-B", str(GEN), "--variant-interfaces", str(ifs), "--out", str(copy)],
                         capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise ValueError(f"the {ifs}-interface variant was refused: {res.stdout}{res.stderr}")


def build_and_run(rtl_dir: Path, work: Path, host: int, ifs: int = 1) -> tuple[int, str]:
    """Build the suite against rtl_dir through one adapter and run it; a
    variant's C++ side includes the variant's header, which rtl_dir holds."""
    work.mkdir(parents=True, exist_ok=True)
    argv = recipe()
    if ifs != 1:
        include = f"-I{CONTRACT_INC}"
        if not any(include in w for w in argv):
            raise ValueError(f"the Makefile's recipe names no {include} to replace with the variant's header")
        argv = [w.replace(include, f"-I{rtl_dir}") for w in argv]
    argv += [f"-GHOST_P={host}", "--Mdir", str(work / "obj"), "-j", "4",
             *[str(rtl_dir / f) for f in RTL_FILES], "tb_mbx_top.sv", "sim_main.cpp", "-o", "Vmbx"]
    built = subprocess.run(argv, cwd=HERE, capture_output=True, text=True, check=False)
    if built.returncode != 0:
        return 2, built.stdout + built.stderr
    ran = subprocess.run([str(work / "obj" / "Vmbx"), str(host)], capture_output=True, text=True, check=False)
    return ran.returncode, ran.stdout + ran.stderr


def plant(arm: Arm, root: Path) -> Path:
    """A copy of the RTL with the arm's defect written into it."""
    copy = root / arm.name / "rtl"
    shutil.copytree(RTL, copy)
    if arm.ifs != 1:
        variant(copy, arm.ifs)
    target = copy / arm.path
    text = target.read_text(encoding="utf-8")
    if text.count(arm.old) != 1:
        raise ValueError(f"{arm.name}: fixture occurs {text.count(arm.old)} times in {arm.path}")
    target.write_text(text.replace(arm.old, arm.new), encoding="utf-8")
    return copy


def run_arm(arm: Arm, root: Path) -> tuple[Arm, bool, str]:
    """One arm's verdict and its first failing line."""
    rc, log = build_and_run(plant(arm, root), root / arm.name, arm.host, arm.ifs)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    caught = rc == 1 and any(arm.needle in ln for ln in fails)
    detail = fails[0] if fails else (log.strip().splitlines() or ["no output"])[-1]
    return arm, caught, f"{len(fails)} check(s) failed; first: {detail}"


def main(argv: list[str] | None = None) -> int:
    """Controls first, then every arm."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--jobs", type=int, default=4, help="arms built and run at once")
    ap.add_argument("--keep", type=Path, help="keep the scratch builds here")
    ap.add_argument("--quick", action="store_true", help="QUICK arms only, no controls (the default make)")
    args = ap.parse_args(argv)
    arms = tuple(a for a in ARMS if a.name in QUICK) if args.quick else ARMS
    with tempfile.TemporaryDirectory(prefix="mbx-mutants-") as tmp:
        root = args.keep.resolve() if args.keep else Path(tmp)
        bad = 0
        try:
            for ifs in () if args.quick else sorted({1} | {a.ifs for a in arms}):
                rtl = RTL
                if ifs != 1:
                    rtl = root / f"control-if{ifs}" / "rtl"
                    shutil.copytree(RTL, rtl)
                    variant(rtl, ifs)
                for host in (0, 1):
                    rc, log = build_and_run(rtl, root / f"control-if{ifs}-{host}", host, ifs)
                    tally = [ln for ln in log.splitlines() if "checks:" in ln]
                    verdict = tally[-1] if tally else log[-200:]
                    print(f"[{'ok' if rc == 0 else 'FAIL'}] positive control, {ifs} interface(s), host {host}: "
                          f"{verdict}")
                    bad += rc != 0
        except ValueError as exc:
            print(f"REFUSED: {exc}")
            return 2
        try:
            with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
                results = list(pool.map(lambda a: run_arm(a, root), arms))
        except ValueError as exc:
            print(f"REFUSED: {exc}")
            return 2
        for arm, caught, detail in results:
            print(f"[{'ok' if caught else 'ESCAPED'}] {arm.name}: {detail}")
            bad += not caught
        print(f"mbx mutants: {sum(c for _a, c, _d in results)} of {len(arms)} caught")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_rx_validator.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/03 §3)
//
//  Description : Shared RX front end — the filter/parser/validator of F03.1,
//                implementing the F03.2 validate/decode flow, the front-end
//                F03.6 rules, and the F03.4 common-header extraction:
//                  - DA gate {own unicast, 91-E0-F0-01-00-00, and the MAAP
//                    multicast 91-E0-F0-00-FF-00 of 1722-2016 Table B.10}
//                    (cnt rx_da)
//                  - V9: DA 01-80-C2-00-00-0E + EtherType 0x22EA (MSRP) and
//                    DA 01-80-C2-00-00-21 + 0x88F5 (MVRP) bypass the 1722.1
//                    pipeline byte-exactly onto mrp_*_o; LLDP/802.1X frames
//                    sharing those group DAs (wrong EtherType) are ignored
//                    with no count — DA alone is never sufficient
//                  - EtherType 0x22F0 gate (cnt rx_ethertype)
//                  - subtype FA/FB/FC/FE demux, DA-QUALIFIED (cnt
//                    rx_subtype): FA/FB/FC are only meaningful to the own
//                    unicast or the AVDECC multicast DA, FE (MAAP) only to
//                    the own unicast (a DEFEND answers the probe's SA,
//                    Annex B B.2.1) or the MAAP multicast DA — a subtype
//                    on a DA it is never sent to is an unknown subtype
//                    for that DA class and drops with one count
//                  - V8: h = 0 and version = 0 (cnt rx_version), and every
//                    malformed drop is drop + count, never fatal
//                  - V1/V2: total PDU = cdl + 12; padding excluded from cdl,
//                    so a frame >= cdl + 12 payload octets is accepted and
//                    exactly cdl + 12 octets are parsed/stored; a frame
//                    shorter than cdl + 12 drops (cnt rx_length)
//                Accepted PDUs stream into KL_pp_rx_slots through its exact
//                write-side ports: a one-cycle alloc after the EtherType
//                gate, wr_abort on any rule failing mid-frame, wr_commit +
//                one hdr_*_o parsed-header beat per accepted frame (fields
//                per F03.4 / F04.5 / F05.13 / F06.10 byte offsets; unread
//                tail fields report 0 — V3). V5/V6/V7 are engine/normalizer
//                rules and deliberately not here.
//
//                The one design decision that matters: the MRP route is an
//                elastic 64-byte FIFO plus a per-frame verdict queue, not a
//                fixed replay buffer — the V9 verdict lands at wire byte 13
//                while byte 0 must reach the SRP engine untouched, so bytes
//                wait in arrival order and drain one per cycle once their
//                frame's verdict exists (drain rate >= arrival rate bounds
//                occupancy near the 14-byte verdict latency); non-MRP frames
//                pop out discarded and the 1722.1 side taps the raw input
//                directly, two cycles ahead of the slot-pool write port.
//
//                Documented edge decisions (all V8: drop + count, one count
//                per frame, never fatal):
//                  - a frame ending before its DA completes counts rx_da
//                    (the first F03.2 gate was not passed);
//                  - a 1722.1-DA frame ending before EtherType completes
//                    counts rx_ethertype;
//                  - one passing the EtherType gate but ending before
//                    cdl + 12 payload octets counts rx_length, as does an
//                    inbound cdl + 12 beyond the slot capacity BYTES_P
//                    (inbound commands are <= 536 B per Milan §5.4.1);
//                  - the slot is allocated right after the EtherType gate
//                    (bytes must land somewhere before cdl is known), so a
//                    full pool counts rx_overrun in the pool even when the
//                    frame would also have failed a later rule; the refused
//                    frame is then sunk silently here so the front end still
//                    counts each frame exactly once.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_rx_validator
  import pp_pkg::*;
#(
    //! mirrors KL_pp_rx_slots SLOTS_P (P-RX-SLOTS, F01.5)
    parameter int unsigned SLOTS_P = 4,
    //! mirrors KL_pp_rx_slots BYTES_P (P-RX-SLOT-BYTES, F01.5)
    parameter int unsigned BYTES_P = 576,
    //! derived: slot index width (matches the pool's alloc_slot_o)
    localparam int unsigned SLOT_W_C = (SLOTS_P > 1) ? $clog2(SLOTS_P) : 1
) (
    input  wire                 clk_i,               //! core clock (P-CLK-HZ domain)
    input  wire                 rst_n,               //! synchronous active-low reset

    //! ---- MAC trunk in (byte stream; frames delimited by rx_last_i) ----
    input  wire                 rx_valid_i,          //! byte strobe from the RX async FIFO
    input  wire           [7:0] rx_data_i,           //! frame byte (byte 0 = first DA octet)
    input  wire                 rx_last_i,           //! final byte of the frame
    input  wire          [47:0] own_mac_i,           //! own unicast MAC ([47:40] = first wire octet)

    //! ---- V9 MRP pass-through (to the SRP engine's MRPDU queue) ----
    output logic                mrp_valid_o,         //! MRPDU byte strobe
    output logic          [7:0] mrp_data_o,          //! byte-exact frame byte (from DA byte 0)
    output logic                mrp_last_o,          //! final byte of the MRPDU frame

    //! ---- RX slot pool write side (KL_pp_rx_slots' exact ports) ----
    output logic                alloc_req_o,         //! one-cycle slot request after the EtherType gate
    input  wire                 alloc_gnt_i,         //! combinational grant (same cycle)
    input  wire  [SLOT_W_C-1:0] alloc_slot_i,        //! granted slot handle
    output logic                wr_valid_o,          //! PDU byte strobe into the granted slot
    output logic          [7:0] wr_data_o,           //! PDU byte (slot offset 0 = subtype)
    output logic                wr_last_o,           //! byte cdl+11 — closes the slot stream (V2)
    output logic                wr_abort_o,          //! a rule failed mid-frame: return the slot
    output logic                wr_commit_o,         //! frame accepted: latch length cdl+12

    //! ---- parsed-header beat (one per accepted frame, to the normalizer) ----
    output logic                hdr_valid_o,         //! fields + rx_slot valid (with wr_commit_o)
    output logic          [2:0] hdr_protocol_o,      //! pp_protocol_e: ADP/ACMP/AEM/MVU/AA/MAAP
    output logic          [3:0] hdr_msg_type_o,      //! header message_type (@1[3:0])
    output logic          [4:0] hdr_status_o,        //! status / valid_time / maap_version (@2[7:3])
    output logic         [10:0] hdr_cdl_o,           //! validated control_data_length (V1/V2)
    output logic         [47:0] hdr_src_mac_o,       //! Ethernet SA (response addressing)
    output logic         [63:0] hdr_controller_eid_o,//! controller_entity_id @12 (AECP/ACMP; 0 for ADP; MAAP: requested_start_address+requested_count @12..@19)
    output logic         [63:0] hdr_target_eid_o,    //! entity_id / stream_id / target_entity_id @4
    output logic         [15:0] hdr_sequence_id_o,   //! AECP @20 / ACMP @48 (0 for ADP/MAAP)
    output logic                hdr_u_o,             //! AECP u bit (@22 bit 7)
    output logic                hdr_cr_o,            //! AECP cr bit (@22 bit 6)
    output logic         [15:0] hdr_opcode_o,        //! AEM/MVU command_type; ACMP/ADP/MAAP message_type
    output pp_operands_t        hdr_operands_o,      //! desc_type/index (AECP), unique_id (ACMP), conflict_start+count (MAAP)
    output logic          [2:0] hdr_rx_slot_o,       //! committed slot handle (pp_pkg code space)

    //! ---- per-rule drop counters (F03.2 cnt names; 16-bit saturating) ----
    output logic         [15:0] rx_da_count_o,       //! DA gate drops
    output logic         [15:0] rx_ethertype_count_o,//! EtherType gate drops
    output logic         [15:0] rx_subtype_count_o,  //! unknown-subtype drops
    output logic         [15:0] rx_version_count_o,  //! h != 0 or version != 0 drops (V8)
    output logic         [15:0] rx_length_count_o    //! cdl + 12 > payload drops (V1)
);

  // ------------------------------------------------------------- constants
  localparam logic [47:0] DA_AVDECC_C = 48'h91_E0_F0_01_00_00;
  //! 1722-2016 Table B.10: the one reserved MAAP multicast address
  localparam logic [47:0] DA_MAAP_C   = 48'h91_E0_F0_00_FF_00;
  localparam logic [47:0] DA_MSRP_C   = 48'h01_80_C2_00_00_0E;
  localparam logic [47:0] DA_MVRP_C   = 48'h01_80_C2_00_00_21;
  localparam logic [15:0] ET_1722_C   = 16'h22F0;
  localparam logic [15:0] ET_MSRP_C   = 16'h22EA;
  localparam logic [15:0] ET_MVRP_C   = 16'h88F5;
  localparam logic [7:0]  SUB_ADP_C   = 8'hFA;
  localparam logic [7:0]  SUB_AECP_C  = 8'hFB;
  localparam logic [7:0]  SUB_ACMP_C  = 8'hFC;
  localparam logic [7:0]  SUB_MAAP_C  = 8'hFE;
  localparam logic [15:0] CNT_MAX_C   = 16'hFFFF;

  typedef enum logic [1:0] { FR_HDR, FR_PDU, FR_SINK } fr_st_e;

  //! wire octet i (0 = first transmitted) of a 48-bit MAC constant
  function automatic logic [7:0] mac_byte_f(input logic [47:0] m,
                                            input logic [10:0] i);
    int unsigned k;
    k = (i > 11'd5) ? 32'd0 : (32'd5 - 32'(i));
    return m[k * 8 +: 8];
  endfunction

  // ------------------------------------------------------ frame-cadence state
  fr_st_e              fr_st_r;
  logic [10:0]         idx_r;        // wire byte index, saturates at 2047
  logic                da_own_r, da_mcast_r, da_maap_r, da_msrp_r, da_mvrp_r;
  logic [7:0]          et_hi_r;      // EtherType high byte (@12)
  logic                vpushed_r;    // MRP verdict pushed for this frame
  logic                alloc_req_r;  // one-cycle alloc pulse
  logic                slot_held_r;
  logic [SLOT_W_C-1:0] slot_r;
  logic                cdl_known_r;  // PDU byte 3 captured

  // ------------------------------------------------------------ field capture
  logic [7:0]  subtype_r;
  logic [3:0]  msg_type_r;
  logic [4:0]  status_r;
  logic [10:0] cdl_r;
  logic [47:0] src_mac_r;
  logic [63:0] target_eid_r;
  logic [63:0] ctlr_eid_r;
  logic [15:0] seq_r, opcode_r, desc_type_r, desc_index_r, tuid_r, luid_r;
  logic        u_r, cr_r;

  // --------------------------------------------------------- outcome pipeline
  logic        end_pend_r;   // frame ended last cycle: latch hdr / reset captures
  logic        end_pass_r;   // ... and it passed V1 (commit path)
  logic        abort_pend_r; // assert wr_abort_o this cycle
  logic [1:0]  cp_r;         // commit shift: wr_commit_o/hdr_valid_o at t_end+3

  // write pipeline to the pool (2 stages: alloc grant precedes first strobe)
  logic        p1_en_r, p2_en_r;
  logic [7:0]  p1_d_r,  p2_d_r;
  logic        p1_l_r,  p2_l_r;

  // --------------------------------------------------------------- hdr output
  logic [2:0]   hdr_protocol_r;
  logic [3:0]   hdr_msg_type_r;
  logic [4:0]   hdr_status_r;
  logic [10:0]  hdr_cdl_r;
  logic [47:0]  hdr_src_mac_r;
  logic [63:0]  hdr_ctlr_eid_r, hdr_target_eid_r;
  logic [15:0]  hdr_seq_r, hdr_opcode_r;
  logic         hdr_u_r, hdr_cr_r;
  pp_operands_t hdr_operands_r;
  logic [2:0]   hdr_rx_slot_r;

  // ------------------------------------------------------------------ counters
  logic [15:0] cnt_da_r, cnt_et_r, cnt_sub_r, cnt_ver_r, cnt_len_r;

  // ------------------------------------------------------------- combinational
  logic        acc_w;
  logic        end_w;
  logic [10:0] pidx_w;
  logic        da_own_a_w, da_mcast_a_w, da_maap_a_w, da_msrp_a_w, da_mvrp_a_w;
  logic        da_1722_a_w, da_mrp_a_w;
  logic [15:0] et_w;
  logic        et_1722_ok_w, et_mrp_ok_w;
  logic        slot_now_w;
  logic [11:0] lim_w;
  logic        in_budget_w;
  logic        pdu_byte_w, sub_fail_w, ver_fail_w, fail_now_w;
  logic        wr_en_w, wlast_w;
  logic [11:0] pcnt_end_w;
  logic        v1_pass_w;
  logic        ev_da_w, ev_et_w, ev_len_w;

  assign acc_w  = rx_valid_i;
  assign end_w  = rx_valid_i && rx_last_i;
  assign pidx_w = idx_r - 11'd14;

  always_comb begin : da_fold
    da_own_a_w   = da_own_r;
    da_mcast_a_w = da_mcast_r;
    da_maap_a_w  = da_maap_r;
    da_msrp_a_w  = da_msrp_r;
    da_mvrp_a_w  = da_mvrp_r;
    if (acc_w && (fr_st_r == FR_HDR) && (idx_r <= 11'd5)) begin
      if (rx_data_i != mac_byte_f(own_mac_i,  idx_r)) da_own_a_w   = 1'b0;
      if (rx_data_i != mac_byte_f(DA_AVDECC_C, idx_r)) da_mcast_a_w = 1'b0;
      if (rx_data_i != mac_byte_f(DA_MAAP_C,  idx_r)) da_maap_a_w  = 1'b0;
      if (rx_data_i != mac_byte_f(DA_MSRP_C,  idx_r)) da_msrp_a_w  = 1'b0;
      if (rx_data_i != mac_byte_f(DA_MVRP_C,  idx_r)) da_mvrp_a_w  = 1'b0;
    end
  end

  assign da_1722_a_w = da_own_a_w | da_mcast_a_w | da_maap_a_w;
  assign da_mrp_a_w  = da_msrp_a_w | da_mvrp_a_w;

  assign et_w         = {et_hi_r, rx_data_i};              // valid at idx 13
  assign et_1722_ok_w = (et_w == ET_1722_C);
  assign et_mrp_ok_w  = (da_msrp_r && (et_w == ET_MSRP_C))
                      | (da_mvrp_r && (et_w == ET_MVRP_C));

  assign slot_now_w = slot_held_r | (alloc_req_r & alloc_gnt_i);
  assign lim_w      = {1'b0, cdl_r} + 12'd12;              // total PDU (V1)
  assign in_budget_w = cdl_known_r ? ({1'b0, pidx_w} < lim_w) : 1'b1;

  // per-byte 1722.1 rule checks — only with a secured slot (see banner)
  assign pdu_byte_w = acc_w && (fr_st_r == FR_PDU) && (idx_r >= 11'd14)
                      && slot_now_w;
  //! the subtype is DA-QUALIFIED (banner): 1722.1 subtypes belong to the
  //! own-unicast/AVDECC-multicast DA class, MAAP to the own-unicast (a
  //! unicast DEFEND, B.2.1) or the Table B.10 MAAP multicast DA class
  assign sub_fail_w = pdu_byte_w && (pidx_w == 11'd0)
                      && !(((rx_data_i == SUB_ADP_C)
                            || (rx_data_i == SUB_AECP_C)
                            || (rx_data_i == SUB_ACMP_C))
                           && (da_own_r | da_mcast_r))
                      && !((rx_data_i == SUB_MAAP_C)
                           && (da_own_r | da_maap_r));
  assign ver_fail_w = pdu_byte_w && (pidx_w == 11'd1)
                      && (rx_data_i[7:4] != 4'h0);         // h and version (V8)
  assign fail_now_w = sub_fail_w | ver_fail_w;

  assign wr_en_w = pdu_byte_w && in_budget_w && !fail_now_w;
  assign wlast_w = wr_en_w && cdl_known_r
                   && ({1'b0, pidx_w} == (lim_w - 12'd1));

  // V1 verdict at the last byte (cdl incomplete => pcnt_end < 12 fails anyway)
  assign pcnt_end_w = {1'b0, pidx_w} + 12'd1;
  assign v1_pass_w  = (fr_st_r == FR_PDU) && slot_now_w && !fail_now_w
                      && cdl_known_r
                      && (pcnt_end_w >= lim_w)
                      && (lim_w <= 12'(BYTES_P));

  // one counter event per dropped frame (V8)
  assign ev_da_w  = (acc_w && (fr_st_r == FR_HDR) && (idx_r == 11'd5)
                     && !(da_1722_a_w | da_mrp_a_w))
                  | (end_w && (fr_st_r == FR_HDR) && (idx_r < 11'd5));
  assign ev_et_w  = (fr_st_r == FR_HDR) && da_1722_a_w
                    && ((acc_w && (idx_r == 11'd13) && !et_1722_ok_w)
                        || (end_w && (idx_r >= 11'd5) && (idx_r < 11'd13)));
  assign ev_len_w = (acc_w && (fr_st_r == FR_HDR) && da_1722_a_w
                     && (idx_r == 11'd13) && et_1722_ok_w && rx_last_i)
                  | (end_w && (fr_st_r == FR_PDU) && slot_now_w
                     && !fail_now_w && !v1_pass_w);

  // ----------------------------------------------------------- main sequencer
  always_ff @(posedge clk_i) begin : validator_seq
    if (!rst_n) begin
      fr_st_r      <= FR_HDR;
      idx_r        <= '0;
      da_own_r     <= 1'b1;
      da_mcast_r   <= 1'b1;
      da_maap_r    <= 1'b1;
      da_msrp_r    <= 1'b1;
      da_mvrp_r    <= 1'b1;
      et_hi_r      <= '0;
      vpushed_r    <= 1'b0;
      alloc_req_r  <= 1'b0;
      slot_held_r  <= 1'b0;
      slot_r       <= '0;
      cdl_known_r  <= 1'b0;
      subtype_r    <= '0;
      msg_type_r   <= '0;
      status_r     <= '0;
      cdl_r        <= '0;
      src_mac_r    <= '0;
      target_eid_r <= '0;
      ctlr_eid_r   <= '0;
      seq_r        <= '0;
      opcode_r     <= '0;
      desc_type_r  <= '0;
      desc_index_r <= '0;
      tuid_r       <= '0;
      luid_r       <= '0;
      u_r          <= 1'b0;
      cr_r         <= 1'b0;
      end_pend_r   <= 1'b0;
      end_pass_r   <= 1'b0;
      abort_pend_r <= 1'b0;
      cp_r         <= '0;
      p1_en_r      <= 1'b0;
      p2_en_r      <= 1'b0;
      p1_d_r       <= '0;
      p2_d_r       <= '0;
      p1_l_r       <= 1'b0;
      p2_l_r       <= 1'b0;
      hdr_protocol_r   <= '0;
      hdr_msg_type_r   <= '0;
      hdr_status_r     <= '0;
      hdr_cdl_r        <= '0;
      hdr_src_mac_r    <= '0;
      hdr_ctlr_eid_r   <= '0;
      hdr_target_eid_r <= '0;
      hdr_seq_r        <= '0;
      hdr_opcode_r     <= '0;
      hdr_u_r          <= 1'b0;
      hdr_cr_r         <= 1'b0;
      hdr_operands_r   <= '0;
      hdr_rx_slot_r    <= PP_SLOT_NULL_C;
      cnt_da_r  <= '0;
      cnt_et_r  <= '0;
      cnt_sub_r <= '0;
      cnt_ver_r <= '0;
      cnt_len_r <= '0;
    end else begin
      // defaults: one-cycle pulses fall
      alloc_req_r  <= 1'b0;
      abort_pend_r <= 1'b0;
      end_pend_r   <= 1'b0;

      // ---- write pipeline (2 stages to the pool) ----
      p1_en_r <= wr_en_w;
      p1_d_r  <= rx_data_i;
      p1_l_r  <= wlast_w;
      p2_en_r <= p1_en_r;
      p2_d_r  <= p1_d_r;
      p2_l_r  <= p1_l_r;

      // ---- MRP verdict bookkeeping (push logic below; end reset wins) ----
      if (vd_push_w && !vq_full_w) vpushed_r <= 1'b1;

      // ---- alloc resolution (the cycle after arming) ----
      if (alloc_req_r) begin
        if (alloc_gnt_i) begin
          slot_held_r <= 1'b1;
          slot_r      <= alloc_slot_i;
        end else begin
          fr_st_r <= FR_SINK;   // pool refused: rx_overrun counted in the pool
        end
      end

      // ---- per-byte processing ----
      if (acc_w) begin
        idx_r <= end_w ? 11'd0
                       : ((idx_r == 11'h7FF) ? idx_r : (idx_r + 11'd1));

        if (fr_st_r == FR_HDR) begin
          if (idx_r <= 11'd5) begin
            da_own_r   <= da_own_a_w;
            da_mcast_r <= da_mcast_a_w;
            da_maap_r  <= da_maap_a_w;
            da_msrp_r  <= da_msrp_a_w;
            da_mvrp_r  <= da_mvrp_a_w;
            if ((idx_r == 11'd5) && !(da_1722_a_w | da_mrp_a_w))
              fr_st_r <= FR_SINK;                          // cnt rx_da
          end
          if ((idx_r >= 11'd6) && (idx_r <= 11'd11))
            src_mac_r[(32'd11 - 32'(idx_r)) * 8 +: 8] <= rx_data_i;
          if (idx_r == 11'd12) et_hi_r <= rx_data_i;
          if (idx_r == 11'd13) begin
            if (da_1722_a_w) begin
              if (et_1722_ok_w && !rx_last_i) begin
                fr_st_r     <= FR_PDU;
                alloc_req_r <= 1'b1;                       // one-cycle alloc
              end else begin
                fr_st_r <= FR_SINK;      // cnt rx_ethertype / rx_length below
              end
            end else begin
              fr_st_r <= FR_SINK;        // MRP verdict handled by the FIFO path
            end
          end
        end else if (fr_st_r == FR_PDU) begin
          if (pdu_byte_w && in_budget_w) begin : field_cap
            // F03.4 common header
            if (pidx_w == 11'd0) subtype_r <= rx_data_i;
            if (pidx_w == 11'd1) msg_type_r <= rx_data_i[3:0];
            if (pidx_w == 11'd2) begin
              status_r    <= rx_data_i[7:3];
              cdl_r[10:8] <= rx_data_i[2:0];
            end
            if (pidx_w == 11'd3) begin
              cdl_r[7:0]  <= rx_data_i;
              cdl_known_r <= 1'b1;
            end
            if ((pidx_w >= 11'd4) && (pidx_w <= 11'd11))
              target_eid_r[(32'd11 - 32'(pidx_w)) * 8 +: 8] <= rx_data_i;
            // F05.13 / F06.10 (AECP and ACMP share @12..@19)
            if ((subtype_r != SUB_ADP_C)
                && (pidx_w >= 11'd12) && (pidx_w <= 11'd19))
              ctlr_eid_r[(32'd19 - 32'(pidx_w)) * 8 +: 8] <= rx_data_i;
            if (subtype_r == SUB_AECP_C) begin
              if (pidx_w == 11'd20) seq_r[15:8] <= rx_data_i;
              if (pidx_w == 11'd21) seq_r[7:0]  <= rx_data_i;
              if (pidx_w == 11'd22) begin
                u_r            <= rx_data_i[7];
                cr_r           <= rx_data_i[6];
                opcode_r[15:8] <= {2'b00, rx_data_i[5:0]};
              end
              if (pidx_w == 11'd23) opcode_r[7:0]     <= rx_data_i;
              if (pidx_w == 11'd24) desc_type_r[15:8] <= rx_data_i;
              if (pidx_w == 11'd25) desc_type_r[7:0]  <= rx_data_i;
              if (pidx_w == 11'd26) desc_index_r[15:8] <= rx_data_i;
              if (pidx_w == 11'd27) desc_index_r[7:0]  <= rx_data_i;
            end
            if (subtype_r == SUB_ACMP_C) begin
              if (pidx_w == 11'd36) tuid_r[15:8] <= rx_data_i;
              if (pidx_w == 11'd37) tuid_r[7:0]  <= rx_data_i;
              if (pidx_w == 11'd38) luid_r[15:8] <= rx_data_i;
              if (pidx_w == 11'd39) luid_r[7:0]  <= rx_data_i;
              if (pidx_w == 11'd48) seq_r[15:8]  <= rx_data_i;
              if (pidx_w == 11'd49) seq_r[7:0]   <= rx_data_i;
            end
            //! MAAP (Figure B.1): requested_start+count @12..@19 already ride
            //! the shared @12..@19 capture above (the record's controller_eid
            //! lane); conflict_start (@20..@25) + conflict_count (@26..@27)
            //! land in the four operand halves, so the whole PDU rides the
            //! record and the MAAP engine never reads the payload slot
            if (subtype_r == SUB_MAAP_C) begin
              if (pidx_w == 11'd20) desc_type_r[15:8]  <= rx_data_i;
              if (pidx_w == 11'd21) desc_type_r[7:0]   <= rx_data_i;
              if (pidx_w == 11'd22) desc_index_r[15:8] <= rx_data_i;
              if (pidx_w == 11'd23) desc_index_r[7:0]  <= rx_data_i;
              if (pidx_w == 11'd24) tuid_r[15:8]       <= rx_data_i;
              if (pidx_w == 11'd25) tuid_r[7:0]        <= rx_data_i;
              if (pidx_w == 11'd26) luid_r[15:8]       <= rx_data_i;
              if (pidx_w == 11'd27) luid_r[7:0]        <= rx_data_i;
            end
          end
          if (fail_now_w) fr_st_r <= FR_SINK;   // cnt rx_subtype / rx_version
        end

        // ---- frame end: verdict + frame-cadence reset ----
        if (end_w) begin
          end_pend_r <= 1'b1;
          end_pass_r <= v1_pass_w;
          fr_st_r    <= FR_HDR;
          da_own_r   <= 1'b1;
          da_mcast_r <= 1'b1;
          da_maap_r  <= 1'b1;
          da_msrp_r  <= 1'b1;
          da_mvrp_r  <= 1'b1;
          vpushed_r  <= 1'b0;
        end
      end

      // ---- abort: any failed rule / V1 miss with a slot secured ----
      if ((fail_now_w && slot_now_w)
          || (end_w && (fr_st_r == FR_PDU) && slot_now_w
              && !fail_now_w && !v1_pass_w)) begin
        abort_pend_r <= 1'b1;
      end
      if (abort_pend_r) slot_held_r <= 1'b0;

      // ---- accepted frame: hdr latch at t_end+1, commit at t_end+3 ----
      cp_r <= {cp_r[0], end_pend_r & end_pass_r};
      if (end_pend_r) begin
        if (end_pass_r) begin : hdr_latch
          hdr_msg_type_r   <= msg_type_r;
          hdr_status_r     <= status_r;
          hdr_cdl_r        <= cdl_r;
          hdr_src_mac_r    <= src_mac_r;
          hdr_target_eid_r <= target_eid_r;
          hdr_ctlr_eid_r   <= (subtype_r == SUB_ADP_C) ? 64'd0 : ctlr_eid_r;
          hdr_seq_r        <= seq_r;
          hdr_u_r          <= u_r;
          hdr_cr_r         <= cr_r;
          hdr_rx_slot_r    <= 3'(slot_r);
          if (subtype_r == SUB_ADP_C) begin
            hdr_protocol_r <= 3'(PP_PROTO_ADP);
            hdr_opcode_r   <= {12'd0, msg_type_r};
            hdr_operands_r <= '0;
          end else if (subtype_r == SUB_MAAP_C) begin
            //! Annex B record: controller_eid = requested_start(48)+count(16)
            //! (the shared @12..@19 capture), operands = conflict_start(48)
            //! folded over {desc_type, desc_index, config_index} + count in
            //! unique_id; status_in already carries maap_version (@2[7:3])
            hdr_protocol_r <= 3'(PP_PROTO_MAAP);
            hdr_opcode_r   <= {12'd0, msg_type_r};
            hdr_operands_r <= '{desc_type: desc_type_r,
                                desc_index: desc_index_r,
                                config_index: tuid_r, unique_id: luid_r};
          end else if (subtype_r == SUB_ACMP_C) begin
            hdr_protocol_r <= 3'(PP_PROTO_ACMP);
            hdr_opcode_r   <= {12'd0, msg_type_r};
            //! the operand carries the unique_id of the engine that will
            //! CONSUME the record: the talker for its command set {0,2,4,12}
            //! (mirroring the top's ACMP pop steer term for term), the
            //! LISTENER for everything else - including the TX-family
            //! RESPONSES the listener itself originated (PROBE_TX_RESPONSE
            //! above all: Milan's listener probes and consumes the answer,
            //! and its record is addressed by listener_unique_id @38).
            //! CAVEAT for a future originator: messages 5/13 (GET_TX_STATE /
            //! GET_TX_CONNECTION responses) get the listener uid here, which
            //! a CONTROLLER consumer would not want - inert today because
            //! nothing originates either command and both are silently
            //! consumed; revisit this arm if KL_pp_originator ever grows a
            //! GET_TX_* command. The
            //! old arm keyed responses on talker_unique_id @36, which held
            //! only while every bind used tuid == luid: a probe answer with
            //! tuid >= the sink count was silently consumed as
            //! out-of-range, and one with a small distinct tuid would have
            //! walked the WRONG sink's record.
            hdr_operands_r <= '{desc_type: 16'd0, desc_index: 16'd0,
                                config_index: 16'd0,
                                unique_id: ((msg_type_r == 4'd0)
                                            || (msg_type_r == 4'd2)
                                            || (msg_type_r == 4'd4)
                                            || (msg_type_r == 4'd12))
                                           ? tuid_r : luid_r};
          end else begin                                    // 0xFB AECP
            hdr_protocol_r <=
                ((msg_type_r == 4'd6) || (msg_type_r == 4'd7))
                  ? 3'(PP_PROTO_MVU)
                  : (((msg_type_r == 4'd2) || (msg_type_r == 4'd3))
                       ? 3'(PP_PROTO_AA) : 3'(PP_PROTO_AEM));
            hdr_opcode_r   <= opcode_r;
            hdr_operands_r <= '{desc_type: desc_type_r,
                                desc_index: desc_index_r,
                                config_index: 16'd0, unique_id: 16'd0};
          end
        end
        // capture reset (V3: unread tail fields report 0 next frame)
        cdl_known_r  <= 1'b0;
        subtype_r    <= '0;
        msg_type_r   <= '0;
        status_r     <= '0;
        cdl_r        <= '0;
        src_mac_r    <= '0;
        target_eid_r <= '0;
        ctlr_eid_r   <= '0;
        seq_r        <= '0;
        opcode_r     <= '0;
        desc_type_r  <= '0;
        desc_index_r <= '0;
        tuid_r       <= '0;
        luid_r       <= '0;
        u_r          <= 1'b0;
        cr_r         <= 1'b0;
      end
      if (cp_r[1]) slot_held_r <= 1'b0;         // slot ownership passed on

      // ---- saturating drop counters (one event per frame) ----
      if (ev_da_w   && (cnt_da_r  != CNT_MAX_C)) cnt_da_r  <= cnt_da_r  + 16'd1;
      if (ev_et_w   && (cnt_et_r  != CNT_MAX_C)) cnt_et_r  <= cnt_et_r  + 16'd1;
      if (sub_fail_w && (cnt_sub_r != CNT_MAX_C)) cnt_sub_r <= cnt_sub_r + 16'd1;
      if (ver_fail_w && (cnt_ver_r != CNT_MAX_C)) cnt_ver_r <= cnt_ver_r + 16'd1;
      if (ev_len_w  && (cnt_len_r != CNT_MAX_C)) cnt_len_r <= cnt_len_r + 16'd1;
    end
  end

  // ======================================================== V9 MRP route
  // Elastic FIFO (64 x {last, data}) + 16-deep per-frame verdict queue.
  // Verdict points: byte 5 (DA not an MRP group DA -> discard), byte 13
  // (MRP DA: EtherType pair decides), or the last byte of a frame ending
  // before its verdict point (discard). Pops stall until the head frame's
  // verdict exists, then drain one byte per cycle (one bubble per frame at
  // the verdict retire); occupancy stays near the 14-byte verdict latency
  // for legal (>= 64 B) frames, so the 64-deep FIFO never fills.
  logic [8:0] mrp_mem_r [0:63];
  logic [6:0] wptr_r, rptr_r;
  logic       vq_r [0:15];
  logic [4:0] vwptr_r, vrptr_r;
  logic       od_last_r;
  logic [7:0] od_data_r;
  logic       out_valid_r, out_emit_r;

  logic       fifo_ne_w, fifo_full_w, vq_ne_w, vq_full_w;
  logic       vq_head_w;
  logic       push_w, vd_push_w, vd_val_w, rd_fire_w, retire_w;

  assign fifo_ne_w   = (wptr_r != rptr_r);
  assign fifo_full_w = (wptr_r == (rptr_r ^ 7'h40));
  assign vq_ne_w     = (vwptr_r != vrptr_r);
  assign vq_full_w   = (vwptr_r == (vrptr_r ^ 5'h10));
  assign vq_head_w   = vq_r[vrptr_r[3:0]];

  assign push_w = acc_w && !fifo_full_w;

  always_comb begin : verdict_point
    vd_push_w = 1'b0;
    vd_val_w  = 1'b0;
    if (acc_w && (fr_st_r == FR_HDR) && !vpushed_r) begin
      if ((idx_r == 11'd5) && !da_mrp_a_w) begin
        vd_push_w = 1'b1;                        // 1722.1 or foreign DA
      end else if ((idx_r == 11'd13) && da_mrp_a_w) begin
        vd_push_w = 1'b1;
        vd_val_w  = et_mrp_ok_w;                 // V9 pair; LLDP/802.1X -> 0
      end
    end
    if (end_w && !vpushed_r && !vd_push_w) vd_push_w = 1'b1;  // early end
  end

  assign retire_w  = out_valid_r && od_last_r;   // head frame fully popped
  assign rd_fire_w = fifo_ne_w && vq_ne_w && !retire_w;

  always_ff @(posedge clk_i) begin : mrp_ctrl
    if (!rst_n) begin
      wptr_r      <= '0;
      rptr_r      <= '0;
      vwptr_r     <= '0;
      vrptr_r     <= '0;
      out_valid_r <= 1'b0;
      out_emit_r  <= 1'b0;
      for (int unsigned i = 0; i < 16; i++) vq_r[i] <= 1'b0;
    end else begin
      if (push_w) wptr_r <= wptr_r + 7'd1;
      if (vd_push_w && !vq_full_w) begin
        vq_r[vwptr_r[3:0]] <= vd_val_w;
        vwptr_r            <= vwptr_r + 5'd1;
      end
      if (rd_fire_w) begin
        rptr_r      <= rptr_r + 7'd1;
        out_valid_r <= 1'b1;
        out_emit_r  <= vq_head_w;
      end else begin
        out_valid_r <= 1'b0;
      end
      if (retire_w) vrptr_r <= vrptr_r + 5'd1;
    end
  end

  // No reset on the array or its read register — BRAM/LUTRAM inference
  // (the justified exception to the sync-reset rule, as in KL_pp_rx_slots).
  always_ff @(posedge clk_i) begin : mrp_mem_wr
    if (push_w) mrp_mem_r[wptr_r[5:0]] <= {rx_last_i, rx_data_i};
  end
  always_ff @(posedge clk_i) begin : mrp_mem_rd
    if (rd_fire_w) {od_last_r, od_data_r} <= mrp_mem_r[rptr_r[5:0]];
  end

  // ------------------------------------------------------------------ outputs
  assign mrp_valid_o = out_valid_r && out_emit_r;
  assign mrp_data_o  = od_data_r;
  assign mrp_last_o  = out_valid_r && out_emit_r && od_last_r;

  assign alloc_req_o = alloc_req_r;
  assign wr_valid_o  = p2_en_r;
  assign wr_data_o   = p2_d_r;
  assign wr_last_o   = p2_l_r;
  assign wr_abort_o  = abort_pend_r;
  assign wr_commit_o = cp_r[1];

  assign hdr_valid_o          = cp_r[1];
  assign hdr_protocol_o       = hdr_protocol_r;
  assign hdr_msg_type_o       = hdr_msg_type_r;
  assign hdr_status_o         = hdr_status_r;
  assign hdr_cdl_o            = hdr_cdl_r;
  assign hdr_src_mac_o        = hdr_src_mac_r;
  assign hdr_controller_eid_o = hdr_ctlr_eid_r;
  assign hdr_target_eid_o     = hdr_target_eid_r;
  assign hdr_sequence_id_o    = hdr_seq_r;
  assign hdr_u_o              = hdr_u_r;
  assign hdr_cr_o             = hdr_cr_r;
  assign hdr_opcode_o         = hdr_opcode_r;
  assign hdr_operands_o       = hdr_operands_r;
  assign hdr_rx_slot_o        = hdr_rx_slot_r;

  assign rx_da_count_o        = cnt_da_r;
  assign rx_ethertype_count_o = cnt_et_r;
  assign rx_subtype_count_o   = cnt_sub_r;
  assign rx_version_count_o   = cnt_ver_r;
  assign rx_length_count_o    = cnt_len_r;

endmodule

`default_nettype wire

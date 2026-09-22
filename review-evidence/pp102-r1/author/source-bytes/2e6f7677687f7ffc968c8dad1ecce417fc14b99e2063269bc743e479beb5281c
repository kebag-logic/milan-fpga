/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_decoder.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/10 §3)
//
//  Description : SRP MRPDU vector decoder — walks the validator's rule-V9
//                MRP pass-through byte stream (MSRP 0x22EA / MVRP 0x88F5)
//                through the F10.6 skeleton: ProtocolVersion, per-message
//                AttributeType + AttributeLength (validated against the
//                F10.8 FirstValue lengths), the MSRP AttributeListLength
//                (COUNTED and flagged when it lies — never trusted for
//                framing), VectorHeader {LeaveAllEvent, NumberOfValues},
//                FirstValue by type (F10.7 offsets), three-packed and
//                Listener four-packed event extraction, and the dual
//                EndMark (AttributeList EndMark then MRPDU EndMark, 802.1Q
//                §10.8.1.2 BNF) which IS the framing truth — a PDU that
//                ends after a single EndMark is malformed.
//
//                The one decision that matters: events are emitted PER
//                VECTOR VALUE with the k-th reconstruction applied in place
//                (the 10 §3 vector-value-k rule). Talker/Listener values
//                increment {unique_id, DA} together, Domain values
//                increment {SRclassID, SRclassPriority} together (VID
//                unchanged; class A is surfaced wherever it sits via
//                evt_class_a_o — 802.1Q §35.2.2.9's own worked example puts
//                class A at value 1 of FirstValue {5, 2, VID}), MVRP values
//                increment the VID. FirstValue alone never leaves this
//                module, so a downstream matcher CANNOT equality-match it —
//                the wire defect the contract warns about is
//                unrepresentable here.
//
//                Tolerance (Milan §4.2.7.1.2/.1.3, tested per F09.4): a
//                malformed vector attribute (bad AttributeType or
//                AttributeLength, an out-of-alphabet three-packed digit,
//                truncation mid-anything) is processed up to the bad field,
//                then the REST of that attribute list and ALL subsequent
//                messages of the PDU are discarded, and the PDU summary
//                reports malformed. LeaveAll is strobed PER APPLICATION
//                (MSRP vs MVRP — the corrected §6.5 rule): one merged pulse
//                would let a bridge's MVRP maintenance cycle age a healthy
//                MSRP Listener Ready and flap the stream licence.
//
//                Listener pairing storage is a sync-read byte RAM (the
//                three-packed bytes precede the four-packed bytes on the
//                wire, §35.2.2.7 — the k-th {event, declaration} pair only
//                exists after buffering). The decoder paces the stream with
//                mrp_ready_o (one event strobe per cycle while draining
//                packed bytes); the F10.1 MRPDU RX queue absorbs the stall.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_decoder
  import srp_pkg::*;
#(
    //! listener three-packed buffer depth in bytes: ceil(NumberOfValues/3)
    //! for the largest Listener vector a legal frame can carry
    parameter int unsigned TP_DEPTH_P = 1024
) (
    input  wire         clk_i,        //! core clock (P-CLK-HZ)
    input  wire         rst_n,        //! synchronous active-low reset

    // ---- validator MRP pass-through in (03 §5 rule V9 demux) -------------
    input  wire         mrp_valid_i,  //! byte valid (MRPDU RX queue not empty)
    input  wire  [7:0]  mrp_data_i,   //! MRPDU byte, wire order
    input  wire         mrp_last_i,   //! last byte of this MRPDU
    input  wire         mrp_msrp_i,   //! 1 = MSRP (0x22EA), 0 = MVRP (0x88F5); sampled with the first byte
    output logic        mrp_ready_o,  //! decoder pop — low only while draining packed values

    // ---- per-value match-query event out (class-C strobe + payload) ------
    output logic        evt_valid_o,               //! one strobe per vector value k
    output logic        evt_msrp_o,                //! application: 1 = MSRP, 0 = MVRP
    output logic [7:0]  evt_attr_type_o,           //! F10.8 AttributeType within the application
    output logic [63:0] evt_stream_id_o,           //! reconstructed k-th stream_id (unique_id + k)
    output logic [47:0] evt_da_o,                  //! reconstructed k-th destination_address (+ k); 0 for Listener/Domain/VID
    output logic [15:0] evt_vid_o,                 //! talker vlan_id / Domain SRclassVID / reconstructed k-th MVRP VID
    output logic [2:0]  evt_mrp_event_o,           //! k-th three-packed event (srp_event_e)
    output logic [1:0]  evt_fourpacked_o,          //! k-th Listener declaration (srp_decl_e); 0 otherwise
    output logic [15:0] evt_max_frame_size_o,      //! talker TSpec MaxFrameSize (F10.7)
    output logic [15:0] evt_max_interval_frames_o, //! talker TSpec MaxIntervalFrames (F10.7)
    output logic [7:0]  evt_priority_o,            //! talker {5'b0, PCP} / reconstructed k-th Domain SRclassPriority
    output logic        evt_rank_o,                //! talker rank bit (F10.7 byte 20 bit 4)
    output logic [31:0] evt_acc_latency_o,         //! talker accumulated_latency (802.1Q §35.2.2.8.6)
    output logic [63:0] evt_failure_system_id_o,   //! Talker Failed FailureInformation system id (§35.2.2.8.7)
    output logic [7:0]  evt_failure_code_o,        //! Talker Failed failure code
    output logic [7:0]  evt_class_id_o,            //! reconstructed k-th Domain SRclassID
    output logic        evt_class_a_o,             //! Domain value k IS class A (SRclassID == 6) — the value-k rule

    // ---- LeaveAll, PER APPLICATION (corrected §6.5 rule) ------------------
    output logic        la_msrp_o,    //! MSRP LeaveAllEvent decoded (never fires on an MVRP PDU)
    output logic        la_mvrp_o,    //! MVRP LeaveAllEvent decoded (never fires on an MSRP PDU)

    // ---- PDU summary ------------------------------------------------------
    output logic        pdu_done_o,       //! one strobe per PDU: walk finished
    output logic        pdu_ok_o,         //! with pdu_done_o: dual EndMark seen, nothing malformed
    output logic        pdu_malformed_o,  //! with pdu_done_o: tolerance discard happened (prefix events stand)
    output logic        listlen_bad_o,    //! strobe at an MSRP AttributeList close whose COUNTED octets != declared
    output logic [15:0] dbg_listlen_cnt_o //! counted AttributeList octets at the last list close
);

  localparam int unsigned PTR_W_C = $clog2(TP_DEPTH_P);

  // ------------------------------------------------------------ FSM states
  typedef enum logic [3:0] {
    S_IDLE,      // await ProtocolVersion (first byte latches the application)
    S_MSGTYPE,   // AttributeType, or 0x00 opening the MRPDU EndMark
    S_END2,      // second MRPDU EndMark byte
    S_ALEN,      // AttributeLength (validated against F10.8)
    S_LL1,       // MSRP AttributeListLength high byte
    S_LL2,       // MSRP AttributeListLength low byte
    S_VHDR1,     // VectorHeader byte 1, or 0x00 opening the list EndMark
    S_VHDR2,     // VectorHeader byte 2 / list EndMark close
    S_FV,        // FirstValue bytes (F10.7 offsets)
    S_TP,        // next three-packed byte (non-Listener)
    S_TPDRAIN,   // emit up to 3 values from the held three-packed byte
    S_TPSTORE,   // Listener: buffer three-packed bytes into the RAM
    S_FP,        // Listener: next four-packed byte
    S_FPDRAIN,   // Listener: emit up to 4 paired values
    S_PAD,       // PDU complete — ignore padding until last
    S_DISCARD    // tolerance discard — consume to end of PDU
  } state_e;

  state_e       state_r;
  logic         app_msrp_r;      // application of the current PDU
  logic  [7:0]  attr_type_r;
  logic  [7:0]  attr_len_r;
  logic  [15:0] listlen_decl_r;  // declared MSRP AttributeListLength
  logic  [15:0] listlen_cnt_r;   // counted AttributeList octets
  logic  [7:0]  vhdr1_r;         // VectorHeader byte 1 held for byte 2
  logic  [12:0] values_left_r;   // vector values not yet emitted
  logic  [5:0]  fv_idx_r;        // FirstValue byte offset
  logic         last_seen_r;     // the byte feeding the current drain carried last

  // FirstValue field registers (captured at their F10.7 offsets, then
  // incremented IN PLACE per emitted value — the value-k reconstruction)
  logic  [63:0] sid_r;
  logic  [47:0] da_r;
  logic  [15:0] vid_r;
  logic  [15:0] mfs_r;
  logic  [15:0] mif_r;
  logic  [7:0]  pr_r;            // priority(3) rank(1) reserved(4)
  logic  [31:0] lat_r;
  logic  [63:0] sysid_r;
  logic  [7:0]  fcode_r;
  logic  [7:0]  dcid_r;          // Domain SRclassID
  logic  [7:0]  dprio_r;         // Domain SRclassPriority

  // packed-byte drain bookkeeping
  logic  [7:0]  pend_byte_r;     // held three-packed byte (non-Listener)
  logic  [7:0]  fp_byte_r;       // held four-packed byte (Listener)
  logic  [1:0]  idx_r;           // digit / declaration position within the byte
  logic  [2:0]  slot_left_r;     // values remaining in the held byte
  logic  [12:0] store_left_r;    // values still to be covered by buffered bytes

  // Listener three-packed buffer: RAM-shaped, sync read
  logic [7:0]        tp_ram [TP_DEPTH_P];
  logic [PTR_W_C:0]  tp_wptr_r;
  logic [PTR_W_C-1:0] tp_rd_byte_r;
  logic [1:0]        tp_rd_dig_r;
  logic [7:0]        tp_rdata_r;
  logic [PTR_W_C-1:0] tp_raddr_w;
  logic              tp_we_w;

  // ------------------------------------------------------------ handshakes
  logic accept_w;
  assign accept_w = mrp_valid_i && mrp_ready_o;

  always_comb begin : ready_map
    mrp_ready_o = !((state_r == S_TPDRAIN) || (state_r == S_FPDRAIN));
  end

  // AttributeLength validation against the F10.8 table (framing truth)
  logic len_ok_w;
  always_comb begin : alen_check
    if (app_msrp_r) begin
      unique case (attr_type_r)
        SRP_MSRP_ATTR_TALKER_ADV_C:    len_ok_w = (mrp_data_i == SRP_FV_LEN_TALKER_ADV_C);
        SRP_MSRP_ATTR_TALKER_FAILED_C: len_ok_w = (mrp_data_i == SRP_FV_LEN_TALKER_FAILED_C);
        SRP_MSRP_ATTR_LISTENER_C:      len_ok_w = (mrp_data_i == SRP_FV_LEN_LISTENER_C);
        SRP_MSRP_ATTR_DOMAIN_C:        len_ok_w = (mrp_data_i == SRP_FV_LEN_DOMAIN_C);
        default:                       len_ok_w = 1'b0;
      endcase
    end else begin
      len_ok_w = (attr_type_r == SRP_MVRP_ATTR_VID_C) && (mrp_data_i == SRP_FV_LEN_VID_C);
    end
  end

  logic is_listener_w, is_domain_w;
  assign is_listener_w = app_msrp_r && (attr_type_r == SRP_MSRP_ATTR_LISTENER_C);
  assign is_domain_w   = app_msrp_r && (attr_type_r == SRP_MSRP_ATTR_DOMAIN_C);

  // list-scope octet counting (MSRP AttributeListLength is counted, F10.6)
  logic in_list_w;
  assign in_list_w = (state_r == S_VHDR1) || (state_r == S_VHDR2)
                  || (state_r == S_FV)    || (state_r == S_TP)
                  || (state_r == S_TPSTORE) || (state_r == S_FP);

  // current-value digit / declaration extraction
  logic [2:0] tpd_digit_w, fpd_digit_w, cur_digit_w;
  logic [1:0] fp_code_w;
  assign tpd_digit_w = srp_tp_digit(pend_byte_r, idx_r);
  assign fpd_digit_w = srp_tp_digit(tp_rdata_r, tp_rd_dig_r);
  assign cur_digit_w = (state_r == S_FPDRAIN) ? fpd_digit_w : tpd_digit_w;

  always_comb begin : fp_code_sel
    unique case (idx_r)
      2'd0:    fp_code_w = fp_byte_r[7:6];
      2'd1:    fp_code_w = fp_byte_r[5:4];
      2'd2:    fp_code_w = fp_byte_r[3:2];
      default: fp_code_w = fp_byte_r[1:0];
    endcase
  end

  // ------------------------------------------------------------ TP buffer
  // sync-read RAM; while draining, the read address tracks the NEXT value's
  // byte so tp_rdata_r is always one value ahead of the emit
  assign tp_we_w = accept_w && (state_r == S_TPSTORE)
                && (tp_wptr_r < (PTR_W_C + 1)'(TP_DEPTH_P));
  assign tp_raddr_w = ((state_r == S_FPDRAIN) && (tp_rd_dig_r == 2'd2))
                    ? (tp_rd_byte_r + PTR_W_C'(1))
                    : tp_rd_byte_r;

  always_ff @(posedge clk_i) begin : tp_buffer
    if (tp_we_w) begin
      tp_ram[tp_wptr_r[PTR_W_C-1:0]] <= mrp_data_i;
    end
    tp_rdata_r <= tp_ram[tp_raddr_w];
  end

  // ------------------------------------------------------------ decode walk
  //! close a PDU as malformed: tolerance discard finished or truncation —
  //! prefix events already emitted stand (Milan §4.2.7.1.2)
  task pdu_fail_t();
    pdu_done_o      <= 1'b1;
    pdu_ok_o        <= 1'b0;
    pdu_malformed_o <= 1'b1;
    last_seen_r     <= 1'b0;
    state_r         <= S_IDLE;
  endtask

  always_ff @(posedge clk_i) begin : decode_walk
    if (!rst_n) begin
      state_r         <= S_IDLE;
      app_msrp_r      <= 1'b0;
      attr_type_r     <= 8'd0;
      attr_len_r      <= 8'd0;
      listlen_decl_r  <= 16'd0;
      listlen_cnt_r   <= 16'd0;
      vhdr1_r         <= 8'd0;
      values_left_r   <= 13'd0;
      fv_idx_r        <= 6'd0;
      last_seen_r     <= 1'b0;
      sid_r           <= 64'd0;
      da_r            <= 48'd0;
      vid_r           <= 16'd0;
      mfs_r           <= 16'd0;
      mif_r           <= 16'd0;
      pr_r            <= 8'd0;
      lat_r           <= 32'd0;
      sysid_r         <= 64'd0;
      fcode_r         <= 8'd0;
      dcid_r          <= 8'd0;
      dprio_r         <= 8'd0;
      pend_byte_r     <= 8'd0;
      fp_byte_r       <= 8'd0;
      idx_r           <= 2'd0;
      slot_left_r     <= 3'd0;
      store_left_r    <= 13'd0;
      tp_wptr_r       <= '0;
      tp_rd_byte_r    <= '0;
      tp_rd_dig_r     <= 2'd0;
      evt_valid_o     <= 1'b0;
      evt_msrp_o      <= 1'b0;
      evt_attr_type_o <= 8'd0;
      evt_stream_id_o <= 64'd0;
      evt_da_o        <= 48'd0;
      evt_vid_o       <= 16'd0;
      evt_mrp_event_o <= 3'd0;
      evt_fourpacked_o <= 2'd0;
      evt_max_frame_size_o <= 16'd0;
      evt_max_interval_frames_o <= 16'd0;
      evt_priority_o  <= 8'd0;
      evt_rank_o      <= 1'b0;
      evt_acc_latency_o <= 32'd0;
      evt_failure_system_id_o <= 64'd0;
      evt_failure_code_o <= 8'd0;
      evt_class_id_o  <= 8'd0;
      evt_class_a_o   <= 1'b0;
      la_msrp_o       <= 1'b0;
      la_mvrp_o       <= 1'b0;
      pdu_done_o      <= 1'b0;
      pdu_ok_o        <= 1'b0;
      pdu_malformed_o <= 1'b0;
      listlen_bad_o   <= 1'b0;
      dbg_listlen_cnt_o <= 16'd0;
    end else begin
      // strobes are one-cycle
      evt_valid_o   <= 1'b0;
      la_msrp_o     <= 1'b0;
      la_mvrp_o     <= 1'b0;
      pdu_done_o    <= 1'b0;
      listlen_bad_o <= 1'b0;

      // ---------------------------------------------------- byte consumed
      if (accept_w) begin
        if (in_list_w) begin
          listlen_cnt_r <= listlen_cnt_r + 16'd1;
        end
        unique case (state_r)
          S_IDLE: begin
            // ProtocolVersion — accepted at any value (MRP forward compat)
            app_msrp_r <= mrp_msrp_i;
            if (mrp_last_i) pdu_fail_t();
            else            state_r <= S_MSGTYPE;
          end
          S_MSGTYPE: begin
            if (mrp_data_i == 8'h00) begin
              // 0x00 is no AttributeType — this opens the MRPDU EndMark
              if (mrp_last_i) pdu_fail_t();  // half an EndMark
              else            state_r <= S_END2;
            end else begin
              attr_type_r <= mrp_data_i;
              if (mrp_last_i) pdu_fail_t();
              else            state_r <= S_ALEN;
            end
          end
          S_END2: begin
            if (mrp_data_i == 8'h00) begin
              // dual EndMark closed — the PDU is complete
              pdu_done_o      <= 1'b1;
              pdu_ok_o        <= 1'b1;
              pdu_malformed_o <= 1'b0;
              state_r         <= mrp_last_i ? S_IDLE : S_PAD;
            end else if (mrp_last_i) begin
              pdu_fail_t();
            end else begin
              state_r <= S_DISCARD;
            end
          end
          S_ALEN: begin
            attr_len_r <= mrp_data_i;
            if (!len_ok_w) begin
              // bad AttributeType/AttributeLength = malformed vector
              // attribute: discard the rest of the PDU (F09.4)
              if (mrp_last_i) pdu_fail_t();
              else            state_r <= S_DISCARD;
            end else if (mrp_last_i) begin
              pdu_fail_t();
            end else begin
              state_r <= app_msrp_r ? S_LL1 : S_VHDR1;
            end
          end
          S_LL1: begin
            listlen_decl_r[15:8] <= mrp_data_i;
            if (mrp_last_i) pdu_fail_t();
            else            state_r <= S_LL2;
          end
          S_LL2: begin
            listlen_decl_r[7:0] <= mrp_data_i;
            listlen_cnt_r       <= 16'd0;
            if (mrp_last_i) pdu_fail_t();
            else            state_r <= S_VHDR1;
          end
          S_VHDR1: begin
            vhdr1_r <= mrp_data_i;
            if (mrp_last_i) pdu_fail_t();
            else            state_r <= S_VHDR2;
          end
          S_VHDR2: begin
            if ((vhdr1_r == 8'h00) && (mrp_data_i == 8'h00)) begin
              // AttributeList EndMark — counted, and the COUNT is compared
              // against the declared AttributeListLength (never vice versa)
              dbg_listlen_cnt_o <= listlen_cnt_r + 16'd1;
              if (app_msrp_r && ((listlen_cnt_r + 16'd1) != listlen_decl_r)) begin
                listlen_bad_o <= 1'b1;
              end
              if (mrp_last_i) pdu_fail_t();  // single-EndMark PDU
              else            state_r <= S_MSGTYPE;
            end else begin
              // VectorHeader {LeaveAllEvent[2:0], NumberOfValues[12:0]}
              if (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) begin
                la_msrp_o <= app_msrp_r;    // per-application, never merged
                la_mvrp_o <= ~app_msrp_r;
              end
              values_left_r <= {vhdr1_r[4:0], mrp_data_i};
              fv_idx_r      <= 6'd0;
              sid_r   <= 64'd0;
              da_r    <= 48'd0;
              vid_r   <= 16'd0;
              mfs_r   <= 16'd0;
              mif_r   <= 16'd0;
              pr_r    <= 8'd0;
              lat_r   <= 32'd0;
              sysid_r <= 64'd0;
              fcode_r <= 8'd0;
              dcid_r  <= 8'd0;
              dprio_r <= 8'd0;
              if (mrp_last_i) pdu_fail_t();
              else            state_r <= S_FV;
            end
          end
          S_FV: begin
            // FirstValue capture at the F10.7 / F10.8 offsets
            if (app_msrp_r) begin
              unique case (attr_type_r)
                SRP_MSRP_ATTR_TALKER_ADV_C,
                SRP_MSRP_ATTR_TALKER_FAILED_C: begin
                  if      (fv_idx_r < 6'd8)   sid_r   <= {sid_r[55:0], mrp_data_i};
                  else if (fv_idx_r < 6'd14)  da_r    <= {da_r[39:0], mrp_data_i};
                  else if (fv_idx_r < 6'd16)  vid_r   <= {vid_r[7:0], mrp_data_i};
                  else if (fv_idx_r < 6'd18)  mfs_r   <= {mfs_r[7:0], mrp_data_i};
                  else if (fv_idx_r < 6'd20)  mif_r   <= {mif_r[7:0], mrp_data_i};
                  else if (fv_idx_r == 6'd20) pr_r    <= mrp_data_i;
                  else if (fv_idx_r < 6'd25)  lat_r   <= {lat_r[23:0], mrp_data_i};
                  else if (fv_idx_r < 6'd33)  sysid_r <= {sysid_r[55:0], mrp_data_i};
                  else                        fcode_r <= mrp_data_i;
                end
                SRP_MSRP_ATTR_LISTENER_C: begin
                  sid_r <= {sid_r[55:0], mrp_data_i};
                end
                default: begin  // SRP_MSRP_ATTR_DOMAIN_C
                  if      (fv_idx_r == 6'd0) dcid_r  <= mrp_data_i;
                  else if (fv_idx_r == 6'd1) dprio_r <= mrp_data_i;
                  else                       vid_r   <= {vid_r[7:0], mrp_data_i};
                end
              endcase
            end else begin
              vid_r <= {vid_r[7:0], mrp_data_i};  // MVRP VID, 2 octets
            end
            fv_idx_r <= fv_idx_r + 6'd1;
            if (fv_idx_r == (attr_len_r[5:0] - 6'd1)) begin
              // FirstValue complete
              if (mrp_last_i) begin
                pdu_fail_t();  // vector bytes / EndMarks can no longer arrive
              end else if (values_left_r == 13'd0) begin
                state_r <= S_VHDR1;  // NumberOfValues 0: header+FirstValue only
              end else if (is_listener_w) begin
                store_left_r <= values_left_r;
                tp_wptr_r    <= '0;
                tp_rd_byte_r <= '0;
                tp_rd_dig_r  <= 2'd0;
                state_r      <= S_TPSTORE;
              end else begin
                state_r <= S_TP;
              end
            end else if (mrp_last_i) begin
              pdu_fail_t();  // truncation mid-FirstValue
            end
          end
          S_TP: begin
            pend_byte_r <= mrp_data_i;
            idx_r       <= 2'd0;
            slot_left_r <= (values_left_r > 13'd3) ? 3'd3 : values_left_r[2:0];
            last_seen_r <= mrp_last_i;
            state_r     <= S_TPDRAIN;
          end
          S_TPSTORE: begin
            if (tp_wptr_r >= (PTR_W_C + 1)'(TP_DEPTH_P)) begin
              // vector larger than any legal frame — malformed
              if (mrp_last_i) pdu_fail_t();
              else            state_r <= S_DISCARD;
            end else begin
              tp_wptr_r <= tp_wptr_r + (PTR_W_C + 1)'(1);
              if (store_left_r <= 13'd3) begin
                // last three-packed byte buffered; four-packed must follow
                if (mrp_last_i) pdu_fail_t();
                else            state_r <= S_FP;
              end else begin
                store_left_r <= store_left_r - 13'd3;
                if (mrp_last_i) pdu_fail_t();  // truncation mid-vector
              end
            end
          end
          S_FP: begin
            fp_byte_r   <= mrp_data_i;
            idx_r       <= 2'd0;
            slot_left_r <= (values_left_r > 13'd4) ? 3'd4 : values_left_r[2:0];
            last_seen_r <= mrp_last_i;
            state_r     <= S_FPDRAIN;
          end
          S_PAD: begin
            if (mrp_last_i) state_r <= S_IDLE;  // padding after the dual EndMark
          end
          S_DISCARD: begin
            if (mrp_last_i) pdu_fail_t();  // discard ran to end of PDU
          end
          default: state_r <= S_IDLE;
        endcase
      end

      // ---------------------------------------------- packed-value drain
      // (mrp_ready_o is low here — no byte is consumed in the same cycle)
      if ((state_r == S_TPDRAIN) || (state_r == S_FPDRAIN)) begin
        if (cur_digit_w > 3'd5) begin
          // out-of-alphabet three-packed digit: malformed vector attribute
          // — the values already emitted are the processed prefix
          if (last_seen_r) pdu_fail_t();
          else             state_r <= S_DISCARD;
        end else begin
          // emit vector value k, then apply the +k increments in place
          evt_valid_o     <= 1'b1;
          evt_msrp_o      <= app_msrp_r;
          evt_attr_type_o <= attr_type_r;
          evt_stream_id_o <= sid_r;
          evt_da_o        <= da_r;
          evt_vid_o       <= vid_r;
          evt_mrp_event_o <= cur_digit_w;
          evt_fourpacked_o <= (state_r == S_FPDRAIN) ? fp_code_w : 2'd0;
          evt_max_frame_size_o      <= mfs_r;
          evt_max_interval_frames_o <= mif_r;
          evt_priority_o  <= is_domain_w ? dprio_r : {5'd0, pr_r[7:5]};
          evt_rank_o      <= pr_r[4];
          evt_acc_latency_o       <= lat_r;
          evt_failure_system_id_o <= sysid_r;
          evt_failure_code_o      <= fcode_r;
          evt_class_id_o  <= dcid_r;
          evt_class_a_o   <= is_domain_w && (dcid_r == SRP_CLASS_A_ID_C);
          if (is_domain_w) begin
            dcid_r  <= dcid_r + 8'd1;   // SRclassID and SRclassPriority
            dprio_r <= dprio_r + 8'd1;  // step TOGETHER (802.1Q §35.2.2.9)
          end else if (app_msrp_r) begin
            sid_r[15:0] <= sid_r[15:0] + 16'd1;  // unique_id and DA step
            da_r        <= da_r + 48'd1;         // together (§35.2.2.8)
          end else begin
            vid_r <= vid_r + 16'd1;              // MVRP VID (§11.2.3.1.6)
          end
          values_left_r <= values_left_r - 13'd1;
          idx_r         <= idx_r + 2'd1;
          slot_left_r   <= slot_left_r - 3'd1;
          if (state_r == S_FPDRAIN) begin
            if (tp_rd_dig_r == 2'd2) begin
              tp_rd_dig_r  <= 2'd0;
              tp_rd_byte_r <= tp_rd_byte_r + PTR_W_C'(1);
            end else begin
              tp_rd_dig_r <= tp_rd_dig_r + 2'd1;
            end
          end
          if (slot_left_r == 3'd1) begin
            // held byte exhausted
            if (values_left_r == 13'd1) begin
              // vector complete
              if (last_seen_r) pdu_fail_t();  // EndMarks can no longer arrive
              else             state_r <= S_VHDR1;
              last_seen_r <= 1'b0;
            end else if (last_seen_r) begin
              pdu_fail_t();  // truncation mid-vector
            end else begin
              state_r <= (state_r == S_TPDRAIN) ? S_TP : S_FP;
            end
          end
        end
      end
    end
  end

endmodule

`default_nettype wire

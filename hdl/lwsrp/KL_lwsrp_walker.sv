/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_walker.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : STREAMING MRPDU vector parser — constant state, any PDU
//                length, no frame buffer (docs/LWSRP_FPGA_ARCHITECTURE.md §3).
//                Consumes the ingress FIFO byte-serially (~1 byte/cycle; the
//                FIFO absorbs the rate mismatch) and emits event pulses for
//                exactly what gates us:
//
//                  leaveall_p_o    any vector header with LeaveAllEvent != 0
//                                  (once per PDU — the reference treats any
//                                  nonzero lva field as LeaveAll)
//                  domain_p_o      MSRP Domain FirstValue + its event
//                  listener_p_o    MSRP Listener vector COVERING our StreamID
//                                  + the three-packed event + the four-packed
//                                  declaration for our exact value index
//                  tadv_p_o        bridge re-declares TalkerAdvertise for our
//                                  StreamID (clears a sticky failure)
//                  tfail_p_o       TalkerFailed covering our StreamID
//                                  + failure code
//
//                Framing follows the reference RX behaviour exactly: messages
//                and vector lists terminate on 0x0000 EndMarks; the MSRP
//                AttributeListLength is consumed but NEVER trusted (mrp.c
//                parses purely by endmarks). Unknown attribute types are
//                skipped generically (FourPacked assumed only for Listener,
//                like the reference's has_params).
//
//                The +k vector trap: value k of a vector is FirstValue
//                incremented k times, so our StreamID is RANGE-matched
//                (base <= our_sid < base+NumberOfValues) — the reference
//                only ever emits NumberOfValues=1 and skips this; bridges
//                aggregate, so we must not. The packed-byte position of the
//                matched value is found with incremental 3-per-byte /
//                4-per-byte windows — no dividers. Domain vectors are taken
//                at value 0 (bridges declare one Domain per SR class).
//
//                Malformed input (bad version, zero attribute length,
//                truncated PDU) aborts the frame silently; MRP re-declares
//                every JoinTime so nothing needs recovering.
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_walker (
    input  wire         clk_i,
    input  wire         rst_n,

    // ---- MRPDU stream from KL_lwsrp_ingress (little lane) --------------
    input  wire [63:0]  s_tdata,
    input  wire [7:0]   s_tkeep,
    input  wire         s_tvalid,
    input  wire         s_tlast,
    input  wire         s_tuser,          //! 0 = MSRP, 1 = MVRP
    output wire         s_tready,

    // ---- our identity (for the range match) ----------------------------
    input  wire [47:0]  station_mac_i,    //! [47:40] = first wire byte
    input  wire [15:0]  unique_id_i,

    // ---- listener-side bound stream (second match context) --------------
    input  wire [63:0]  lsid_i,           //! bound stream_id (ACMP listener)
    input  wire         lsid_en_i,        //! binding valid

    // ---- event pulses (data valid with the pulse) -----------------------
    output reg          leaveall_p_o,
    output reg          domain_p_o,
    output reg  [7:0]   domain_class_o,
    output reg  [7:0]   domain_prio_o,
    output reg  [15:0]  domain_vid_o,
    output reg  [2:0]   domain_evt_o,
    output reg          listener_p_o,
    output reg  [2:0]   listener_evt_o,
    output reg  [1:0]   listener_decl_o,
    output reg          tadv_p_o,
    output reg          tfail_p_o,
    output reg  [7:0]   tfail_code_o,

    //! listener-side events: TalkerAdvertise/Failed vectors covering lsid
    output reg          l_tadv_p_o,
    output reg          l_tfail_p_o,
    output reg  [2:0]   l_evt_o,          //! MRP event of the matched value
    output reg  [7:0]   l_tfail_code_o,

    output reg  [15:0]  pdu_cnt_o         //! cleanly parsed PDUs
);

  wire [63:0] our_sid_w = {station_mac_i, unique_id_i};

  // -----------------------------------------------------------------------
  // Byte-serial front end: one beat register, one byte per cycle
  // -----------------------------------------------------------------------
  reg        cur_v_r, cur_l_r, cur_u_r;
  reg [63:0] cur_d_r;
  reg [7:0]  cur_k_r;
  reg [2:0]  lane_r;

  assign s_tready = !cur_v_r;

  wire [7:0] byte_w      = cur_d_r[{lane_r, 3'b000} +: 8];
  wire       lane_last_w = (lane_r == 3'd7) || !cur_k_r[3'(lane_r + 3'd1)];
  wire       byte_v_w    = cur_v_r && cur_k_r[lane_r];
  wire       frame_end_w = byte_v_w && lane_last_w && cur_l_r;

  // -----------------------------------------------------------------------
  // Parser state
  // -----------------------------------------------------------------------
  typedef enum logic [3:0] {
    W_HDR_S, W_VER_S, W_MTYPE_S, W_MLEN_S, W_ALLH_S, W_ALLL_S,
    W_VECH_S, W_VECL_S, W_FV_S, W_EVT_S, W_PAR_S, W_SKIP_S
  } wst_t;
  wst_t st_r;

  reg [3:0] hdr_idx_r;   //! Ethernet header skip counter (frames arrive whole)

  reg        kind_r;          //! frame kind latched at first byte
  reg        lva_seen_r;      //! LeaveAll already pulsed for this PDU
  reg [7:0]  attr_type_r, attr_len_r;
  reg [7:0]  vech_hi_r;
  reg [12:0] nv_r;            //! NumberOfValues
  reg [7:0]  fv_idx_r;        //! FirstValue byte index
  reg [63:0] fv_r;            //! first 8 FirstValue bytes (shift-in)
  reg [7:0]  tfail_code_r;    //! TalkerFailed byte 33
  reg [7:0]  d_class_r, d_prio_r;
  reg [15:0] d_vid_r;

  //! value-index match (resolved when FirstValue completes)
  reg        val_match_r;
  reg [12:0] k_r;             //! matched value index
  //! listener-side (lsid) match context
  reg        lval_match_r;
  reg [12:0] lk_r;
  reg [2:0]  lcap_evt_r;
  //! incremental packed-byte windows
  reg [13:0] vbase_r;         //! first value index of the current packed byte
  reg [2:0]  cap_evt_r;       //! captured three-packed event for k
  reg [1:0]  cap_par_r;       //! captured four-packed declaration for k
  reg [12:0] pack_idx_r;      //! packed byte counter
  reg [12:0] pack_n_r;        //! packed bytes total for this phase

  //! three-packed extraction: {e0,e1,e2} = {b/36, (b%36)/6, b%6}
  function automatic [2:0] unpack3(input [7:0] b, input [1:0] pos);
    logic [7:0] r36;
    begin
      r36 = b % 8'd36;
      unique case (pos)
        2'd0: unpack3 = 3'((b / 8'd36) % 8'd6);
        2'd1: unpack3 = 3'(r36 / 8'd6);
        default: unpack3 = 3'(r36 % 8'd6);
      endcase
    end
  endfunction

  //! four-packed extraction: p_pos = (b >> ((3-pos)*2)) & 3
  function automatic [1:0] unpack4(input [7:0] b, input [1:0] pos);
    unpack4 = 2'(b >> ({2'd3 - pos, 1'b0}));
  endfunction

  wire is_msrp_w     = (kind_r == 1'b0);
  wire is_listener_w = is_msrp_w && (attr_type_r == MSRP_ATTR_LISTENER_C);
  wire is_domain_w   = is_msrp_w && (attr_type_r == MSRP_ATTR_DOMAIN_C);
  wire is_tadv_w     = is_msrp_w && (attr_type_r == MSRP_ATTR_TALKER_ADV_C);
  wire is_tfail_w    = is_msrp_w && (attr_type_r == MSRP_ATTR_TALKER_FAILED_C);
  wire is_stream_w   = is_tadv_w || is_tfail_w || is_listener_w;

  //! FirstValue as seen INCLUDING the byte being consumed this cycle — the
  //! Listener FirstValue is exactly 8 B, so on its completion cycle the 8th
  //! byte is still in flight and fv_r alone would be one byte short.
  wire [63:0] fv_eff_w = (fv_idx_r < 8'd8) ? {fv_r[55:0], byte_w} : fv_r;

  //! range match: base <= our_sid < base + nv
  wire [63:0] sid_diff_w = our_sid_w - fv_eff_w;
  wire        sid_hit_w  = (our_sid_w >= fv_eff_w) &&
                           (sid_diff_w[63:13] == '0) &&
                           (sid_diff_w[12:0] < nv_r);

  //! second context: the ACMP listener's bound stream_id
  wire [63:0] lsid_diff_w = lsid_i - fv_eff_w;
  wire        lsid_hit_w  = lsid_en_i && (lsid_i >= fv_eff_w) &&
                            (lsid_diff_w[63:13] == '0) &&
                            (lsid_diff_w[12:0] < nv_r);

  //! event bytes = ceil(nv/3), param bytes = ceil(nv/4)
  wire [12:0] n_evt_bytes_w = 13'((nv_r + 13'd2) / 13'd3);
  wire [12:0] n_par_bytes_w = 13'((nv_r + 13'd3) / 13'd4);

  // -----------------------------------------------------------------------
  // FSM. Captured event/declaration values are passed THROUGH the emit
  // helper on the final packed byte's cycle — reading the capture registers
  // there would be one cycle stale when the matched byte is also the last.
  // -----------------------------------------------------------------------
  task automatic vector_done(input [2:0] evt, input [1:0] par,
                             input [2:0] levt, output wst_t nxt);
    begin
      if (is_domain_w) begin
        domain_p_o     <= 1'b1;
        domain_class_o <= d_class_r;
        domain_prio_o  <= d_prio_r;
        domain_vid_o   <= d_vid_r;
        domain_evt_o   <= evt;
      end else if (val_match_r && is_listener_w) begin
        listener_p_o    <= 1'b1;
        listener_evt_o  <= evt;
        listener_decl_o <= par;
      end else if (val_match_r && is_tadv_w) begin
        tadv_p_o <= 1'b1;
      end else if (val_match_r && is_tfail_w) begin
        tfail_p_o    <= 1'b1;
        tfail_code_o <= tfail_code_r;
      end
      // listener-side context is independent (both can hit one vector)
      if (lval_match_r && is_tadv_w) begin
        l_tadv_p_o <= 1'b1;
        l_evt_o    <= levt;
      end else if (lval_match_r && is_tfail_w) begin
        l_tfail_p_o     <= 1'b1;
        l_evt_o         <= levt;
        l_tfail_code_o  <= tfail_code_r;
      end
      nxt = W_VECH_S;
    end
  endtask

  always_ff @(posedge clk_i or negedge rst_n) begin
    wst_t nxt;
    logic [2:0] evt_v;
    logic [1:0] par_v;
    logic [2:0] levt_v;
    if (!rst_n) begin
      cur_v_r <= 1'b0; cur_l_r <= 1'b0; cur_u_r <= 1'b0;
      cur_d_r <= '0; cur_k_r <= '0; lane_r <= '0;
      st_r <= W_HDR_S; hdr_idx_r <= '0; kind_r <= 1'b0; lva_seen_r <= 1'b0;
      attr_type_r <= '0; attr_len_r <= '0; vech_hi_r <= '0; nv_r <= '0;
      fv_idx_r <= '0; fv_r <= '0; tfail_code_r <= '0;
      d_class_r <= '0; d_prio_r <= '0; d_vid_r <= '0;
      val_match_r <= 1'b0; k_r <= '0; vbase_r <= '0;
      lval_match_r <= 1'b0; lk_r <= '0; lcap_evt_r <= '0;
      cap_evt_r <= '0; cap_par_r <= '0; pack_idx_r <= '0; pack_n_r <= '0;
      leaveall_p_o <= 1'b0;
      domain_p_o <= 1'b0; domain_class_o <= '0; domain_prio_o <= '0;
      domain_vid_o <= '0; domain_evt_o <= '0;
      listener_p_o <= 1'b0; listener_evt_o <= '0; listener_decl_o <= '0;
      tadv_p_o <= 1'b0; tfail_p_o <= 1'b0; tfail_code_o <= '0;
      l_tadv_p_o <= 1'b0; l_tfail_p_o <= 1'b0;
      l_evt_o <= '0; l_tfail_code_o <= '0;
      pdu_cnt_o <= '0;
    end else begin
      // pulses are one-cycle
      leaveall_p_o <= 1'b0; domain_p_o <= 1'b0; listener_p_o <= 1'b0;
      tadv_p_o <= 1'b0; tfail_p_o <= 1'b0;
      l_tadv_p_o <= 1'b0; l_tfail_p_o <= 1'b0;

      // beat intake
      if (!cur_v_r && s_tvalid) begin
        cur_v_r <= 1'b1; cur_l_r <= s_tlast; cur_u_r <= s_tuser;
        cur_d_r <= s_tdata; cur_k_r <= s_tkeep; lane_r <= 3'd0;
      end

      if (byte_v_w) begin
        nxt = st_r;
        case (st_r)
          // ---- Ethernet header (14 B, already matched by the ingress) ---
          W_HDR_S: begin
            hdr_idx_r <= hdr_idx_r + 4'd1;
            nxt = (hdr_idx_r == 4'd13) ? W_VER_S : W_HDR_S;
          end

          // ---- MRPDU header --------------------------------------------
          W_VER_S: begin
            kind_r     <= cur_u_r;
            lva_seen_r <= 1'b0;
            nxt = (byte_w == MRP_PROTO_VER_C) ? W_MTYPE_S : W_SKIP_S;
          end

          // ---- message header ------------------------------------------
          W_MTYPE_S: begin
            attr_type_r <= byte_w;
            nxt = W_MLEN_S;
          end
          W_MLEN_S: begin
            attr_len_r <= byte_w;
            if (attr_type_r == 8'h00 && byte_w == 8'h00) begin
              // message-list EndMark: clean PDU end
              pdu_cnt_o <= pdu_cnt_o + 16'd1;
              nxt = W_SKIP_S;   // trailing bytes = padding
            end else if (attr_type_r == 8'h00 || byte_w == 8'h00) begin
              nxt = W_SKIP_S;   // malformed
            end else begin
              nxt = (cur_u_r == 1'b0) ? W_ALLH_S : W_VECH_S;
            end
          end
          //! MSRP AttributeListLength: consumed, never trusted for framing
          W_ALLH_S: nxt = W_ALLL_S;
          W_ALLL_S: nxt = W_VECH_S;

          // ---- vector header --------------------------------------------
          W_VECH_S: begin
            vech_hi_r <= byte_w;
            nxt = W_VECL_S;
          end
          W_VECL_S: begin
            if (vech_hi_r == 8'h00 && byte_w == 8'h00) begin
              // vector-list EndMark: next message
              nxt = W_MTYPE_S;
            end else begin
              if (vech_hi_r[7:5] != 3'b000 && !lva_seen_r) begin
                leaveall_p_o <= 1'b1;    // any nonzero LeaveAllEvent
                lva_seen_r   <= 1'b1;
              end
              nv_r        <= {vech_hi_r[4:0], byte_w};
              fv_idx_r    <= 8'd0;
              fv_r        <= '0;
              val_match_r <= 1'b0;
              lval_match_r<= 1'b0;
              cap_evt_r   <= MRP_EVT_MT_C;   // default: no news
              lcap_evt_r  <= MRP_EVT_MT_C;
              cap_par_r   <= LSTN_DECL_IGNORE_C;
              nxt = W_FV_S;
            end
          end

          // ---- FirstValue ------------------------------------------------
          W_FV_S: begin
            if (fv_idx_r < 8'd8) fv_r <= {fv_r[55:0], byte_w};
            // domain fields (FirstValue bytes 0-3)
            if (is_domain_w) begin
              unique case (fv_idx_r)
                8'd0: d_class_r      <= byte_w;
                8'd1: d_prio_r       <= byte_w;
                8'd2: d_vid_r[15:8]  <= byte_w;
                8'd3: d_vid_r[7:0]   <= byte_w;
                default: ;
              endcase
            end
            // TalkerFailed failure code (FirstValue byte 33)
            if (is_tfail_w && fv_idx_r == 8'd33) tfail_code_r <= byte_w;

            if (fv_idx_r == attr_len_r - 8'd1) begin
              // FirstValue complete: resolve the value-index matches
              if (is_stream_w && attr_len_r >= 8'd8 && sid_hit_w) begin
                val_match_r <= 1'b1;
                k_r         <= sid_diff_w[12:0];
              end
              if ((is_tadv_w || is_tfail_w) && attr_len_r >= 8'd8 && lsid_hit_w) begin
                lval_match_r <= 1'b1;
                lk_r         <= lsid_diff_w[12:0];
              end
              pack_n_r   <= n_evt_bytes_w;
              pack_idx_r <= '0;
              vbase_r    <= '0;
              // nv==0 <=> n_evt_bytes==0, and nv_r is a plain register:
              // branching on nv_r keeps the ceil(nv/3) carry chain OFF the
              // FSM next-state arc (the AX 100 MHz critical path, WNS -0.285
              // on the milanv12b sweep — 11 CARRY4 levels into st_r).
              if (nv_r == '0) begin
                // nv==0 (pure-LeaveAll vector): no packed bytes follow.
                // A stream/listener match cannot exist with nv==0, so only
                // a Domain pulse (with the MT default event) can emit here.
                vector_done(MRP_EVT_MT_C, LSTN_DECL_IGNORE_C, MRP_EVT_MT_C, nxt);
              end else begin
                nxt = W_EVT_S;
              end
            end
            fv_idx_r <= fv_idx_r + 8'd1;
          end

          // ---- ThreePackedEvents -----------------------------------------
          W_EVT_S: begin
            evt_v  = cap_evt_r;
            levt_v = lcap_evt_r;
            if (val_match_r &&
                ({1'b0, k_r} >= vbase_r) && ({1'b0, k_r} < vbase_r + 14'd3))
              evt_v = unpack3(byte_w, 2'(14'({1'b0, k_r}) - vbase_r));
            if (lval_match_r &&
                ({1'b0, lk_r} >= vbase_r) && ({1'b0, lk_r} < vbase_r + 14'd3))
              levt_v = unpack3(byte_w, 2'(14'({1'b0, lk_r}) - vbase_r));
            if (is_domain_w && pack_idx_r == '0)
              evt_v = unpack3(byte_w, 2'd0);   // domain: value 0 only
            cap_evt_r  <= evt_v;
            lcap_evt_r <= levt_v;
            vbase_r    <= vbase_r + 14'd3;
            pack_idx_r <= pack_idx_r + 13'd1;
            if (pack_idx_r == pack_n_r - 13'd1) begin
              if (is_listener_w) begin
                pack_n_r   <= n_par_bytes_w;
                pack_idx_r <= '0;
                vbase_r    <= '0;
                nxt = W_PAR_S;
              end else begin
                vector_done(evt_v, cap_par_r, levt_v, nxt);
              end
            end
          end

          // ---- FourPackedEvents (Listener only) --------------------------
          W_PAR_S: begin
            par_v = cap_par_r;
            if (val_match_r &&
                ({1'b0, k_r} >= vbase_r) && ({1'b0, k_r} < vbase_r + 14'd4))
              par_v = unpack4(byte_w, 2'(14'({1'b0, k_r}) - vbase_r));
            cap_par_r  <= par_v;
            vbase_r    <= vbase_r + 14'd4;
            pack_idx_r <= pack_idx_r + 13'd1;
            if (pack_idx_r == pack_n_r - 13'd1) begin
              vector_done(cap_evt_r, par_v, lcap_evt_r, nxt);
            end
          end

          // ---- discard until frame end -----------------------------------
          W_SKIP_S: nxt = W_SKIP_S;

          default: nxt = W_SKIP_S;
        endcase

        // frame boundary overrides everything: a PDU that ends mid-structure
        // is dropped; the next frame starts clean.
        st_r <= frame_end_w ? W_HDR_S : nxt;
        if (frame_end_w) hdr_idx_r <= '0;

        // lane advance / beat release
        if (lane_last_w) begin
          cur_v_r <= 1'b0;
        end else begin
          lane_r <= lane_r + 3'd1;
        end
      end
    end
  end

endmodule

`default_nettype wire

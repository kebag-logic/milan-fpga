/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_ingress.sv
  Description : RX front-end for the AECP subsystem.

                Non-intrusive MONITOR of the MAC RX AXIS stream (Forencich
                little lane order, tdata[7:0] = first wire byte): it reads
                tvalid/tdata/tkeep/tlast and drives NOTHING back, so it can
                never backpressure or disturb the NIC RX path it taps.

                AREA NOTE (2026-07-15 rewrite): the original store-and-forward
                kept the frame in a 128-byte REGISTER array with unaligned
                byte indexing on both ports — 8.2K LUTs of write decoders and
                replay muxes, the single biggest control-plane block and the
                cone that pushed both boards past placement. This version is
                the KL_lwsrp_ingress recipe instead: frames ride a BRAM
                axis_fifo (FRAME_FIFO), classification happens at ALIGNED
                beat/lane positions on the way in, and the 12-byte strip on
                the way out is a FIXED 4-byte rotation across FIFO words —
                no variable byte muxes anywhere.

                Write side (per tapped frame, beats counted from 0):
                  beat 0: dst MAC (lanes 0-5, == our station MAC?),
                          src MAC hi (lanes 6-7)
                  beat 1: src MAC lo (lanes 0-3), EtherType (4-5, 0x22F0?),
                          subtype (6: 0xFB AECP / 0xFA ADP), msg_type (7)
                  beat 2/3: target_entity_id (bytes 18..25) for the ADP
                          ENTITY_DISCOVER check
                Frames that are not an AECP command for us are terminated
                into the FIFO immediately after beat 1 with tlast+tuser=1
                (DROP_BAD_FRAME reclaims them atomically, max 2 words spent);
                matching frames stream through whole, marked bad only when
                shorter than the 28-byte ACMP/AECP minimum. ADP DISCOVER for
                us (subtype 0xFA, msg_type 2, target 0 or us) never enters
                the replay path — it pulses adp_discover_o at frame end.

                THE TARGET TEST IS IEEE Std 1722.1-2021 6.2.7 Figure 6-5
                (Discovery Interface State Machine), verbatim: from RECEIVED
                DISCOVER, "entity_id == 0 || entity_id ==
                entityInfo.entity_id" reaches the DISCOVER state which sets
                needsAdvertise = TRUE, while "entity_id != 0 && entity_id !=
                entityInfo.entity_id" returns to WAITING and advertises
                NOTHING. adp_discover_o is that qualified edge and nothing
                else. adp_disc_seen_o is the UNQUALIFIED witness of the same
                frames (any ADP ENTITY_DISCOVER on the wire, target ignored,
                enable ignored): counted at A_ADP_DIAG2[23:16] it separates
                "no controller is discovering at all" from "discovers arrive
                but name another entity" - a distinction no register could
                make before 2026-07-30, when proving the first case took a
                peer-side wire capture.

                Read side: pops one GOOD frame at a time (gated on the
                requester-MAC slot being free), extracts the controller's
                source MAC from the two header words while discarding them,
                then replays the frame from the EtherType onward in BIG lane
                order (tdata[63:56] = first byte — the KL_aecp_* parser
                convention). Stripped byte 12+8k+j lives at FIFO word k+1
                lane 4+j (j<4) / word k+2 lane j-4 (j>=4): a constant
                rotation, streamed with a 4-byte hold register.

  Spec refs   : IEEE Std 1722.1-2021 §6 (ADP), §9 (AECP)
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;
import adp_pkg::*;

module KL_aecp_ingress #(
  //! Frame FIFO capacity in bytes. AECP commands in scope top out around a
  //! 98-byte SET_NAME; 512 holds several while the builder is busy. Larger
  //! frames drop atomically (DROP_OVERSIZE_FRAME; controllers retry).
  parameter int unsigned FIFO_DEPTH_BYTES = 512
) (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire          enable_i,

  // ---- identity ------------------------------------------------------
  input  wire [47:0]   station_mac_i,   //! [47:40] = first wire byte
  input  wire [63:0]   entity_id_i,

  // ---- RX monitor tap (little lane order; inputs only) ---------------
  input  wire          rx_tvalid_i,
  input  wire [63:0]   rx_tdata_i,
  input  wire [7:0]    rx_tkeep_i,
  input  wire          rx_tlast_i,

  // ---- replayed command stream to KL_aecp_packet_validator -----------
  output logic         m_axis_tvalid,
  input  wire          m_axis_tready,
  output logic [63:0]  m_axis_tdata,
  output logic [7:0]   m_axis_tkeep,
  output logic         m_axis_tlast,

  // ---- captured requester MAC (for the response builder) -------------
  output logic [47:0]  req_src_mac_o,
  output logic         req_valid_o,
  input  wire          req_pop_i,

  // ---- ADP discover-response trigger ---------------------------------
  output logic         adp_discover_o,   //! 1-cycle: an ENTITY_DISCOVER FOR US (6.2.7 target test passed)
  output logic         adp_disc_seen_o,  //! 1-cycle DIAG: any ENTITY_DISCOVER on the wire, target/enable ignored

  // ---- gh #59 CONTROLLER_AVAILABLE reply witness (Milan §5.4.5.3) -----
  //! A controller answering OUR probe replies with an AEM_RESPONSE, and the
  //! packet validator drops every response-typed AECP frame — so nothing
  //! downstream can ever see it. This witness is the adp_pend_r pattern
  //! applied one beat later: classify at aligned lanes on the way IN, pulse
  //! at frame end, and let the frame drain to the validator's drop path
  //! exactly as before. 1722.1-2021 9.3.6 matches a response on
  //! controller_entity_id == myEntityID; the ANSWERING controller is then
  //! the frame's target_entity_id (our probe named it there).
  output logic         ca_reply_p_o,     //! 1-cycle: a CONTROLLER_AVAILABLE response for us
  output logic [63:0]  ca_reply_eid_o    //! ...the answering controller's Entity ID
);

  // ------------------------------------------------------------------ //
  // Input pipeline register on the tapped RX bus (transparent: monitor). //
  // ------------------------------------------------------------------ //
  logic        rxv_r, rxl_r;
  logic [63:0] rxd_r;
  logic [7:0]  rxk_r;
  always_ff @(posedge clk_i) begin
    rxv_r <= rx_tvalid_i;
    rxd_r <= rx_tdata_i;
    rxk_r <= rx_tkeep_i;
    rxl_r <= rx_tlast_i;
  end

  // ------------------------------------------------------------------ //
  // Write side: aligned-lane classification + frame push                 //
  // ------------------------------------------------------------------ //
  logic [2:0] wbeat_r;        //! beat index, saturating at 4 (= "4 or more")
  logic       pushing_r;      //! frame started while enabled (beat 0 seen)
  logic       drop_rest_r;    //! mismatch decided: swallow until tlast
  logic       kill_pend_r;    //! emit the fabricated bad-tlast word
  logic       dst_ok_r;
  logic [7:0]  subtype_r;
  logic [3:0]  msgtype_r;
  logic       is_avtp_r;
  logic [47:0] tgt_hi_r;      //! target_entity_id bytes 18..23
  logic       adp_pend_r;     //! ADP DISCOVER for us: pulse at frame end
  logic       adp_seen_r;     //! ADP DISCOVER seen (any target): pulse at frame end
  //! gh #59 witness state. beat 4 carries controller_entity_id bytes 32-33
  //! and command_type bytes 36-37, so the verdict settles one beat later
  //! than the ADP one; ca_b4_r is the single-shot enable that keeps the
  //! saturated wbeat_r == 4 from re-classifying beats 5, 6, ...
  logic        ca_rsp_r;      //! beat 1: AEM_RESPONSE, AECP subtype, for our MAC
  logic [63:0] ca_tgt_r;      //! ...the frame's target_entity_id (who answered)
  logic [47:0] ca_ctl_hi_r;   //! controller_entity_id bytes 26..31
  logic        ca_b4_r;       //! beat 4 is the NEXT beat (one-shot)
  logic        ca_pend_r;     //! verdict latched: pulse at frame end

  //! beat-1 verdict, computed on the registered beat as it is pushed
  wire w_b1_full   = rxv_r && (wbeat_r == 3'd1) && (rxk_r == 8'hFF);
  wire w_b1_avtp   = w_b1_full && ({rxd_r[39:32], rxd_r[47:40]} == AVTP_ETYPE_C);
  wire w_b1_aecp   = w_b1_avtp && (rxd_r[55:48] == AECP_SUBTYPE_C) && dst_ok_r;

  //! >= 28 wire bytes at the tlast beat: 4+ full beats before it, or
  //! exactly 3 full beats and at least 4 tail bytes
  wire w_len_ok = (wbeat_r == 3'd4) || (wbeat_r == 3'd3 && rxk_r[3]);

  //! FIFO write channel
  logic        fw_valid, fw_last, fw_user;
  logic [63:0] fw_data;
  logic [7:0]  fw_keep;
  wire         fw_ready;   //! FRAME_FIFO + DROP_WHEN_FULL: never stalls

  wire w_push = rxv_r && !drop_rest_r &&
                ((wbeat_r == 3'd0) ? enable_i : pushing_r);

  always_comb begin
    fw_valid = 1'b0;
    fw_data  = rxd_r;
    fw_keep  = rxk_r;
    fw_last  = rxl_r;
    fw_user  = 1'b0;
    if (kill_pend_r) begin
      // fabricated terminator for a frame decided-against at beat 1
      fw_valid = 1'b1;
      fw_keep  = 8'h01;
      fw_last  = 1'b1;
      fw_user  = 1'b1;   // bad -> DROP_BAD_FRAME reclaims it
    end else if (w_push) begin
      fw_valid = 1'b1;
      if (rxl_r) fw_user = !w_len_ok;   // runt AECP command -> drop
    end
  end

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      wbeat_r <= 3'd0; pushing_r <= 1'b0;
      drop_rest_r <= 1'b0; kill_pend_r <= 1'b0;
      dst_ok_r <= 1'b0;
      subtype_r <= '0; msgtype_r <= '0; is_avtp_r <= 1'b0;
      tgt_hi_r <= '0; adp_pend_r <= 1'b0; adp_seen_r <= 1'b0;
      adp_discover_o <= 1'b0; adp_disc_seen_o <= 1'b0;
      ca_rsp_r <= 1'b0; ca_tgt_r <= '0; ca_ctl_hi_r <= '0;
      ca_b4_r <= 1'b0; ca_pend_r <= 1'b0;
      ca_reply_p_o <= 1'b0; ca_reply_eid_o <= '0;
    end else begin
      adp_discover_o  <= 1'b0;
      adp_disc_seen_o <= 1'b0;
      ca_reply_p_o    <= 1'b0;
      if (kill_pend_r) kill_pend_r <= 1'b0;

      if (rxv_r) begin
        unique case (wbeat_r)
          3'd0: begin
            pushing_r <= enable_i;
            dst_ok_r <= ({rxd_r[7:0],   rxd_r[15:8],  rxd_r[23:16],
                          rxd_r[31:24], rxd_r[39:32], rxd_r[47:40]}
                         == station_mac_i);
            adp_pend_r <= 1'b0;
            adp_seen_r <= 1'b0;
            ca_rsp_r   <= 1'b0;
            ca_pend_r  <= 1'b0;
            ca_b4_r    <= 1'b0;
          end
          3'd1: begin
            is_avtp_r <= w_b1_avtp;
            subtype_r <= rxd_r[55:48];
            msgtype_r <= rxd_r[59:56];
            //! DIAG witness: subtype + message_type are complete at beat 1, so
            //! an ENTITY_DISCOVER is recognisable HERE, before the target id
            //! exists. Deliberately NOT gated by enable_i or by dst_ok_r: it
            //! reports what is on the wire, which is the whole point of it.
            //! A frame whose tlast lands on beat 1 (a 16-byte runt, never a
            //! valid 82-byte ADPDU) is not counted - the tlast arm below
            //! clears the flag in the same cycle and reads its old value.
            adp_seen_r <= w_b1_avtp && (rxd_r[55:48] == 8'hFA) &&
                          (rxd_r[59:56] == 4'd2);
            //! gh #59: an AECP AEM_RESPONSE addressed to our station MAC.
            //! w_b1_aecp tests subtype + dst only (never message_type), so
            //! this frame is NOT killed here: it streams whole into the FIFO
            //! and the validator drops it downstream, unchanged.
            ca_rsp_r   <= w_b1_aecp && (rxd_r[59:56] == MSG_AEM_RESPONSE);
            // not an AECP command for us: terminate it into the FIFO now
            // (ADP frames included — they never replay)
            if (!rxl_r && pushing_r && !w_b1_aecp) begin
              drop_rest_r <= 1'b1;
              kill_pend_r <= 1'b1;
            end
          end
          3'd2: begin
            // target_entity_id bytes 18..23 = lanes 2..7
            tgt_hi_r <= {rxd_r[23:16], rxd_r[31:24], rxd_r[39:32],
                         rxd_r[47:40], rxd_r[55:48], rxd_r[63:56]};
          end
          3'd3: begin
            // lanes 0..1 complete the target id (bytes 24..25). Discover
            // frames are full 82-byte ADPDUs, so this beat is never tlast
            // and the pend settles before the frame-end pulse below.
            if (is_avtp_r && subtype_r == 8'hFA && msgtype_r == 4'd2 &&
                rxk_r[1])
              adp_pend_r <=
                ({tgt_hi_r, rxd_r[7:0], rxd_r[15:8]} == 64'd0) ||
                ({tgt_hi_r, rxd_r[7:0], rxd_r[15:8]} == entity_id_i);
            //! gh #59: lanes 0..1 also complete the AECP target_entity_id
            //! (the answering controller); lanes 2..7 are controller_entity_id
            //! bytes 26..31, whose last two bytes arrive on beat 4.
            ca_tgt_r    <= {tgt_hi_r, rxd_r[7:0], rxd_r[15:8]};
            ca_ctl_hi_r <= {rxd_r[23:16], rxd_r[31:24], rxd_r[39:32],
                            rxd_r[47:40], rxd_r[55:48], rxd_r[63:56]};
            ca_b4_r     <= 1'b1;
          end
          default: begin
            //! beat 4 (wbeat_r saturates here, so ca_b4_r makes it one-shot):
            //! controller_entity_id completes at lanes 0..1 and command_type
            //! sits at lanes 4..5. A CONTROLLER_AVAILABLE response carries
            //! command_type 0x0003 with the u bit clear (byte 36 bit 7).
            //! Same standing assumption as the ADP witness above: a 38-octet
            //! AECPDU is padded to the 60-octet Ethernet minimum, so tlast
            //! lands on beat 7 and this verdict is always registered before
            //! the frame-end arm reads it. A sub-46-byte frame could not
            //! reach a MAC in the first place.
            if (ca_b4_r) begin
              ca_b4_r <= 1'b0;
              if (ca_rsp_r && rxk_r[5] &&
                  ({ca_ctl_hi_r, rxd_r[7:0], rxd_r[15:8]} == entity_id_i) &&
                  ({rxd_r[38:32], rxd_r[47:40]} == CMD_CONTROLLER_AVAILABLE))
                ca_pend_r <= 1'b1;
            end
          end
        endcase
        wbeat_r <= (wbeat_r == 3'd4) ? 3'd4 : wbeat_r + 3'd1;

        if (rxl_r) begin
          if (enable_i && adp_pend_r) adp_discover_o  <= 1'b1;
          if (adp_seen_r)             adp_disc_seen_o <= 1'b1;
          if (enable_i && ca_pend_r) begin
            ca_reply_p_o   <= 1'b1;
            ca_reply_eid_o <= ca_tgt_r;
          end
          wbeat_r     <= 3'd0;
          pushing_r   <= 1'b0;
          drop_rest_r <= 1'b0;
          adp_pend_r  <= 1'b0;
          adp_seen_r  <= 1'b0;
          ca_pend_r   <= 1'b0;
          ca_rsp_r    <= 1'b0;
          ca_b4_r     <= 1'b0;
        end
      end
    end
  end

  // ------------------------------------------------------------------ //
  // Frame FIFO (BRAM; whole good AECP frames, wire order)                //
  // ------------------------------------------------------------------ //
  logic        ff_valid, ff_last, ff_ready;
  logic [63:0] ff_data;
  logic [7:0]  ff_keep;

  axis_fifo #(
    .DEPTH(FIFO_DEPTH_BYTES),
    .DATA_WIDTH(64),
    .KEEP_ENABLE(1),
    .KEEP_WIDTH(8),
    .LAST_ENABLE(1),
    .ID_ENABLE(0),
    .DEST_ENABLE(0),
    .USER_ENABLE(1),
    .USER_WIDTH(1),
    .FRAME_FIFO(1),
    .USER_BAD_FRAME_VALUE(1'b1),
    .USER_BAD_FRAME_MASK(1'b1),
    .DROP_BAD_FRAME(1),
    .DROP_OVERSIZE_FRAME(1),
    .DROP_WHEN_FULL(1)
  ) frame_fifo (
    .clk(clk_i),
    .rst(~rst_n),
    .s_axis_tdata (fw_data),
    .s_axis_tkeep (fw_keep),
    .s_axis_tvalid(fw_valid),
    .s_axis_tready(fw_ready),
    .s_axis_tlast (fw_last),
    .s_axis_tid   ('0),
    .s_axis_tdest ('0),
    .s_axis_tuser (fw_user),
    .m_axis_tdata (ff_data),
    .m_axis_tkeep (ff_keep),
    .m_axis_tvalid(ff_valid),
    .m_axis_tready(ff_ready),
    .m_axis_tlast (ff_last),
    .m_axis_tid   (),
    .m_axis_tdest (),
    .m_axis_tuser (),
    .status_overflow(),
    .status_bad_frame(),
    .status_good_frame(),
    .status_depth(),
    .status_depth_commit(),
    .pause_req(1'b0),
    .pause_ack()
  );

  // ------------------------------------------------------------------ //
  // Read side: strip 12 bytes, little -> big lane, capture src MAC       //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] { R_W0_S, R_W1_S, R_STREAM_S, R_HOLD_S } rst_t;
  rst_t rstate_r;

  logic [31:0] hold_r;        //! word k lanes 4..7 (next beat's first 4 bytes)
  logic [2:0]  hold_cnt_r;    //! valid bytes in hold (0..4)
  logic        hold_last_r;   //! hold came from the frame's LAST word
  logic [47:0] src_mac_r;

  //! current output beat: hold (bytes 0..3) + ff word lanes 0..3 (4..7),
  //! emitted in BIG lane order. Keeps are contiguous low-aligned:
  //! lo = lanes 0..3 count (capped 4), hi = lanes 4..7 count.
  wire [2:0] w_lo_cnt  = ff_valid ? (ff_keep[3] ? 3'd4
                                    : ff_keep[2] ? 3'd3
                                    : ff_keep[1] ? 3'd2
                                    : ff_keep[0] ? 3'd1 : 3'd0) : 3'd0;
  wire [2:0] w_hi_cnt  = ff_valid ? (ff_keep[7] ? 3'd4
                                    : ff_keep[6] ? 3'd3
                                    : ff_keep[5] ? 3'd2
                                    : ff_keep[4] ? 3'd1 : 3'd0) : 3'd0;

  //! this output beat ends the frame: hold is the tail, or the incoming
  //! last word contributes nothing past lane 3
  wire w_tail_only = hold_last_r;                       // no more words
  wire w_word_tail = ff_valid && ff_last && (w_hi_cnt == 3'd0);

  wire [3:0] w_out_cnt = w_tail_only ? {1'b0, hold_cnt_r}
                       : {1'b0, hold_cnt_r} + {1'b0, w_lo_cnt};

  logic [63:0] w_out;
  always_comb begin
    w_out = 64'd0;
    // hold bytes j -> big lanes 7-j
    for (int j = 0; j < 4; j++)
      if (j < hold_cnt_r) w_out[8*(7-j) +: 8] = hold_r[8*j +: 8];
    // word lanes 0..3 -> big lanes 3..0 offset by hold_cnt (hold_cnt is
    // always 4 mid-frame; short holds only occur on the tail where the
    // word half is empty)
    if (!w_tail_only)
      for (int j = 0; j < 4; j++)
        if (j < w_lo_cnt) w_out[8*(3-j) +: 8] = ff_data[8*j +: 8];
  end

  assign m_axis_tvalid = (rstate_r == R_STREAM_S) &&
                         (w_tail_only || ff_valid);
  assign m_axis_tdata  = w_out;
  assign m_axis_tlast  = (rstate_r == R_STREAM_S) &&
                         (w_tail_only || w_word_tail);
  always_comb begin
    m_axis_tkeep = 8'h00;
    for (int j = 0; j < 8; j++)
      if (4'(j) < w_out_cnt) m_axis_tkeep[7-j] = 1'b1;
  end

  //! pop the FIFO word when its lanes are consumed into an accepted beat
  assign ff_ready = (rstate_r == R_W0_S && !req_valid_o) ||
                    (rstate_r == R_W1_S) ||
                    (rstate_r == R_STREAM_S && !w_tail_only &&
                     m_axis_tready);

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      rstate_r    <= R_W0_S;
      hold_r      <= '0;
      hold_cnt_r  <= '0;
      hold_last_r <= 1'b0;
      src_mac_r   <= '0;
      req_src_mac_o <= 48'd0;
      req_valid_o   <= 1'b0;
    end else begin
      if (req_pop_i) req_valid_o <= 1'b0;

      unique case (rstate_r)
        // word 0: dst(0-5) + src hi(6-7) — discard, capture src hi
        R_W0_S: begin
          if (ff_valid && !req_valid_o) begin
            src_mac_r[47:32] <= {ff_data[55:48], ff_data[63:56]};
            rstate_r <= R_W1_S;
          end
        end
        // word 1: src lo(0-3) + ethertype/subtype/msg (4-7): the 4..7
        // lanes seed the hold (stripped bytes 12..15)
        R_W1_S: begin
          if (ff_valid) begin
            src_mac_r[31:0] <= {ff_data[7:0],   ff_data[15:8],
                                ff_data[23:16], ff_data[31:24]};
            hold_r      <= ff_data[63:32];
            hold_cnt_r  <= w_hi_cnt;   // 4 (good frames are >= 28 B)
            hold_last_r <= ff_last;    // defensive; never for good frames
            rstate_r    <= R_STREAM_S;
          end
        end
        // stream: emit {hold, word lanes 0..3}, reload hold from 4..7
        R_STREAM_S: begin
          if (m_axis_tvalid && m_axis_tready) begin
            if (m_axis_tlast) begin
              req_src_mac_o <= src_mac_r;
              req_valid_o   <= 1'b1;
              hold_cnt_r    <= 3'd0;
              hold_last_r   <= 1'b0;
              rstate_r      <= R_W0_S;
            end else begin
              hold_r      <= ff_data[63:32];
              hold_cnt_r  <= w_hi_cnt;
              hold_last_r <= ff_last;
            end
          end
        end
        default: rstate_r <= R_W0_S;
      endcase
    end
  end

  // verilator lint_off UNUSED
  wire unused_ok = &{1'b0, fw_ready, ff_keep};
  // verilator lint_on  UNUSED

endmodule

`default_nettype wire

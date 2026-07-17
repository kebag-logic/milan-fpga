/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_aaf_rx_depacketizer.sv
  Author      : Kebag Logic

  Date        : 2026-07-17
  Description : AAF RX payload extractor for the bound listener sink — the
                media half of the Milan listener (task-12 lineage,
                ARCHITECTURE_HW_SW_SPLIT "DMA PCM ring from Linux first").

                Taps the RX AXI-Stream (never backpressures the datapath),
                buffers every frame through a drop-capable frame FIFO, and
                emits ONLY the AAF sample payload (bytes O+24 .. O+24+
                data_len-1, wire byte order = S32BE interleaved PCM as
                PipeWire consumes it) as one AXIS frame per PDU toward the
                DRAM PCM ring writer.

                The accept/kill verdict is NOT re-derived here: the paired
                KL_avtp_rx_monitor pulses pdu_accept_p for every PDU it
                counts in FRAMES_RX (bound + stream_id match + current-format
                match), and that pulse lands at parse-complete (frame byte 48)
                — always before tlast of any real AAF PDU (>= 230 B). Frames
                without the pulse are dropped at FIFO commit, so the ring
                receives exactly the PDUs FRAMES_RX counts.

                Payload realignment: payload starts at frame byte 38
                (untagged, rotate 2) or 42 (C-VLAN, rotate 6); the read side
                re-parses the buffered header (VLAN flag from bytes 12..13,
                data_len from O+20..21) and rotates through a hold register.
                Output beats are always FULL 8-byte words (the DRAM ring
                writer consumes whole words): Milan base-format payloads are
                8-byte multiples (48k: 192 B, 96k: 384 B, 192k: 768 B); a
                non-multiple data_len is zero-padded in the final beat and
                the ring advances by the padded length.

  Company     : Kebag Logic
  Project     : Milan AVTP

  Notes       :
    - The write side marks frames bad by default; the monitor's accept pulse
      (arriving mid-frame) clears the mark before commit.
    - FIFO overflow (downstream ring stalled) drops WHOLE frames and counts
      them in drops_o — the tap itself never stalls the RX datapath.
------------------------------------------------------------------------------
*/

//! AAF RX payload extractor (listener media path): taps the RX AXI-Stream
//! without ever backpressuring it, buffers frames through a drop-capable
//! frame FIFO, and emits only the AAF sample payload (wire byte order =
//! S32BE interleaved PCM) as one AXIS frame per PDU toward the DRAM PCM
//! ring writer. The commit verdict comes from `KL_avtp_rx_monitor`'s
//! `pdu_accept_p` pulse (bound + stream_id + current-format match), so the
//! ring receives exactly the PDUs FRAMES_RX counts. Payload realignment
//! strips 38 (untagged) or 42 (C-VLAN) header bytes via a hold-register
//! rotation; output beats are always full 8-byte words (Milan base-format
//! payloads are 8-byte multiples), zero-padded on a non-multiple tail.

`default_nettype none

module KL_aaf_rx_depacketizer #(
  parameter int FIFO_DEPTH_BYTES = 2048   //! frame FIFO depth (BRAM)
)(
  input  wire         clk_i,              //! Global clock
  input  wire         rst_n,              //! Active-low synchronous reset

  //! --- monitored RX AXI-Stream (observed, never driven) ------------------
  input  wire [63:0]  s_tdata_i,
  input  wire [7:0]   s_tkeep_i,
  input  wire         s_tvalid_i,
  input  wire         s_tready_i,
  input  wire         s_tlast_i,

  //! --- accept verdict from KL_avtp_rx_monitor ----------------------------
  input  wire         pdu_accept_p_i,     //! pulse: current in-flight PDU is
                                          //! bound + sid + format valid

  //! --- PCM payload out (full 8-byte beats, wire byte order = S32BE) ------
  output logic [63:0] m_axis_tdata,
  output logic [7:0]  m_axis_tkeep,
  output logic        m_axis_tvalid,
  output logic        m_axis_tlast,       //! one AXIS frame per AAF PDU
  input  wire         m_axis_tready,

  //! --- observability ------------------------------------------------------
  output logic [15:0] pdus_o,             //! payloads emitted to the ring
  output logic [15:0] drops_o             //! whole frames lost to FIFO overflow
);

  // ------------------------------------------------------------------ //
  // Write side: tap passthrough, bad-by-default, accept pulse clears     //
  // ------------------------------------------------------------------ //
  wire in_acc = s_tvalid_i && s_tready_i;

  logic good_r;                           //! monitor accepted this frame
  logic in_frame_r;                       //! a frame is in flight on the tap

  //! the verdict pulse is honored only while ITS frame is in flight: a PDU
  //! truncated right at parse-complete pulses one cycle AFTER its tlast, and
  //! an unguarded pulse would pre-approve the NEXT frame regardless of its
  //! own verdict (found by the coverage drive)
  always_ff @(posedge clk_i) begin : write_verdict
    if (!rst_n) begin
      good_r     <= 1'b0;
      in_frame_r <= 1'b0;
    end
    else begin
      if (in_acc) in_frame_r <= !s_tlast_i;
      if (in_acc && s_tlast_i) good_r <= 1'b0;
      else if (pdu_accept_p_i && (in_frame_r || in_acc)) good_r <= 1'b1;
    end
  end : write_verdict

  //! frame is committed good only if the accept pulse arrived; the pulse can
  //! land on the tlast-beat cycle itself, so the marker looks at both
  wire fw_user = !(good_r || pdu_accept_p_i);

  logic        ff_valid, ff_last, ff_ready;
  logic [63:0] ff_data;
  logic [7:0]  ff_keep;
  logic        ff_overflow;

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
    .s_axis_tdata (s_tdata_i),
    .s_axis_tkeep (s_tkeep_i),
    .s_axis_tvalid(in_acc),
    .s_axis_tready(),
    .s_axis_tlast (s_tlast_i),
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
    .status_overflow(ff_overflow),
    .status_bad_frame(),
    .status_good_frame(),
    .status_depth(),
    .status_depth_commit(),
    .pause_req(1'b0),
    .pause_ack()
  );

  // ------------------------------------------------------------------ //
  // Read side: re-parse the buffered header, strip 38/42 bytes via a     //
  // hold-register rotation, emit exactly ceil(data_len/8) payload beats  //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] {
    R_HDR_S,      //! beats 0..4/5: VLAN flag, data_len, prime the hold
    R_PAY_S,      //! rotate + emit payload beats
    R_FLUSH_S     //! swallow padding/tail beats to the frame's tlast
  } rstate_t;

  rstate_t rstate_r;

  logic [2:0]  rbeat_r;       //! header beat index (saturates at 7)
  logic        vlan_r;        //! frame carries a C-VLAN tag
  logic [15:0] remain_r;      //! payload bytes still to emit
  logic [47:0] hold_r;        //! carried tail bytes (2 untagged / 6 tagged)

  //! rotation k: hold contributes bytes 0..k-1 of every output beat
  wire [2:0] k_w = vlan_r ? 3'd6 : 3'd2;

  //! byte accessor into the little-lane FIFO word
  function automatic [7:0] fbyte(input [63:0] w, input [2:0] j);
    fbyte = w[8*j +: 8];
  endfunction

  //! final beat needs no FIFO word when the tail fits inside the hold
  wire hold_only_w = (rstate_r == R_PAY_S) && (remain_r <= 16'(k_w));
  wire emit_w      = (rstate_r == R_PAY_S) && (hold_only_w || ff_valid);
  wire last_beat_w = (remain_r <= 16'd8);

  //! assemble the output beat: hold bytes then FIFO lanes, zero-padded
  //! past the payload tail
  always_comb begin : out_assemble
    for (int j = 0; j < 8; j++) begin
      logic [7:0] b;
      if (3'(j) < k_w) b = hold_r[8*j +: 8];
      else             b = fbyte(ff_data, 3'(j) - k_w);
      m_axis_tdata[8*j +: 8] = (16'(j) < remain_r) ? b : 8'h00;
    end
  end : out_assemble

  assign m_axis_tvalid = emit_w;
  assign m_axis_tkeep  = 8'hFF;
  assign m_axis_tlast  = emit_w && last_beat_w;

  //! pop the FIFO word once its lanes are consumed (header beats always;
  //! payload beats when the emit is accepted; flush beats always)
  assign ff_ready = (rstate_r == R_HDR_S) ||
                    (rstate_r == R_FLUSH_S) ||
                    (rstate_r == R_PAY_S && !hold_only_w && m_axis_tready);

  wire pop_w = ff_valid && ff_ready;

  always_ff @(posedge clk_i) begin : read_fsm
    if (!rst_n) begin
      rstate_r <= R_HDR_S;
      rbeat_r  <= '0;
      vlan_r   <= 1'b0;
      remain_r <= '0;
      hold_r   <= '0;
      pdus_o   <= '0;
      drops_o  <= '0;
    end
    else begin
      if (ff_overflow) drops_o <= drops_o + 16'd1;

      case (rstate_r)
        R_HDR_S : begin
          if (pop_w) begin
            rbeat_r <= (rbeat_r == 3'd7) ? 3'd7 : rbeat_r + 3'd1;
            if (rbeat_r == 3'd1)
              vlan_r <= (fbyte(ff_data, 3'd4) == 8'h81) &&
                        (fbyte(ff_data, 3'd5) == 8'h00);
            if (rbeat_r == 3'd4) begin
              if (!vlan_r) begin
                //! untagged: data_len at bytes 34..35, payload from byte 38
                remain_r <= {fbyte(ff_data, 3'd2), fbyte(ff_data, 3'd3)};
                hold_r   <= {32'h0, fbyte(ff_data, 3'd7),
                                    fbyte(ff_data, 3'd6)};
                rstate_r <= R_PAY_S;
              end
              else begin
                //! tagged: data_len at bytes 38..39, payload from byte 42
                remain_r <= {fbyte(ff_data, 3'd6), fbyte(ff_data, 3'd7)};
              end
            end
            if (rbeat_r == 3'd5 && vlan_r) begin
              hold_r   <= {fbyte(ff_data, 3'd7), fbyte(ff_data, 3'd6),
                           fbyte(ff_data, 3'd5), fbyte(ff_data, 3'd4),
                           fbyte(ff_data, 3'd3), fbyte(ff_data, 3'd2)};
              rstate_r <= R_PAY_S;
            end
            //! runt safety: a committed frame cannot end inside its header
            //! (commit needs the parse-complete pulse at frame byte 48),
            //! so this arm is defensive-only
            // verilator coverage_off
            if (ff_last) begin
              rstate_r <= R_HDR_S;
              rbeat_r  <= '0;
            end
            // verilator coverage_on
          end
        end

        R_PAY_S : begin
          if (emit_w && m_axis_tready) begin
            //! carry the beat's tail lanes: hold byte j = lane j + (8-k)
            if (!hold_only_w)
              hold_r <= vlan_r
                ? {fbyte(ff_data, 3'd7), fbyte(ff_data, 3'd6),
                   fbyte(ff_data, 3'd5), fbyte(ff_data, 3'd4),
                   fbyte(ff_data, 3'd3), fbyte(ff_data, 3'd2)}
                : {32'h0, fbyte(ff_data, 3'd7), fbyte(ff_data, 3'd6)};
            if (last_beat_w) begin
              pdus_o   <= pdus_o + 16'd1;
              remain_r <= '0;
              rbeat_r  <= '0;
              //! the beat that completed the payload may also close the
              //! frame; otherwise swallow padding/FCS-strip tail beats
              if (hold_only_w || !pop_w || !ff_last) begin
                if (hold_only_w || !ff_last) rstate_r <= R_FLUSH_S;
                // verilator coverage_off
                else                         rstate_r <= R_HDR_S;
                // verilator coverage_on
              end
              else rstate_r <= R_HDR_S;
            end
            else begin
              remain_r <= remain_r - 16'd8;
            end
          end
          //! truncated frame (never for committed AAF PDUs): resync
          if (pop_w && ff_last && !(emit_w && m_axis_tready && last_beat_w)) begin
            rstate_r <= R_HDR_S;
            rbeat_r  <= '0;
            remain_r <= '0;
          end
        end

        R_FLUSH_S : begin
          if (pop_w && ff_last) begin
            rstate_r <= R_HDR_S;
            rbeat_r  <= '0;
          end
        end

        // verilator coverage_off
        default : begin
          rstate_r <= R_HDR_S;
        end
        // verilator coverage_on
      endcase
    end
  end : read_fsm

endmodule

`default_nettype wire

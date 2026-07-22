/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_lwsrp_ingress.sv
//  Project     : Milan lwSRP  (IEEE 802.1Q MSRP/MVRP, AVnu Milan v1.2 §5.6)
//
//  Description : lwSRP RX ingress — a non-intrusive MONITOR tap on the
//                post-filter RX stream (inputs only, never drives tready;
//                registered once on entry, the KL_aecp_ingress recipe).
//                Frames whose destination MAC + EtherType match MSRP
//                (01:80:C2:00:00:0E / 0x22EA) or MVRP (01:80:C2:00:00:21 /
//                0x88F5) are copied whole into a packet FIFO; everything
//                else is ignored at zero datapath cost.
//
//                The FIFO (Forencich axis_fifo, FRAME_FIFO + DROP_WHEN_FULL)
//                decouples the 8-byte/cycle tap from the byte-serial walker:
//                bridge MRPDUs can be ~1500 B and the walker consumes ~1
//                byte/cycle, so bursts park here. A PDU that does not fit is
//                dropped ATOMICALLY and counted — MRP heals dropped PDUs at
//                the next Join refresh, so counted loss is benign; a torn
//                PDU would be a parser hazard.
//
//                tuser carries the frame kind to the walker: 0 MSRP, 1 MVRP.
//
//                Dest-MAC match is done here (not in the TCAM): the two
//                link-local groups must also be admitted to rx_axis_to_dma
//                by the TCAM default-pass / an explicit entry so this tap
//                sees them (docs/LWSRP_FPGA_ARCHITECTURE.md §4).
//---------------------------------------------------------------------------//

`default_nettype none

import lwsrp_pkg::*;

module KL_lwsrp_ingress #(
  //! FIFO depth in BYTES (axis_fifo semantics with KEEP_ENABLE)
  parameter int FIFO_DEPTH_BYTES_P = 2048
)(
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         enable_i,        //! lwSRP engine enable (CSR)

    // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) --------
    input  wire         rx_tvalid_i,
    input  wire [63:0]  rx_tdata_i,
    input  wire [7:0]   rx_tkeep_i,
    input  wire         rx_tlast_i,

    // ---- MRPDU stream to the walker (little lane) ----------------------
    output wire [63:0]  m_tdata,
    output wire [7:0]   m_tkeep,
    output wire         m_tvalid,
    output wire         m_tlast,
    output wire         m_tuser,         //! 0 = MSRP, 1 = MVRP
    input  wire         m_tready,

    // ---- status ---------------------------------------------------------
    output reg  [15:0]  rx_pdus_o,       //! matched MRPDU frames accepted
    output reg  [7:0]   rx_drops_o       //! matched frames dropped (FIFO full)
);

  // -----------------------------------------------------------------------
  // Registered tap (zero combinational load on datapath nets)
  // -----------------------------------------------------------------------
  reg        rxv_r, rxl_r;
  reg [63:0] rxd_r;
  reg [7:0]  rxk_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      rxv_r <= 1'b0; rxl_r <= 1'b0; rxd_r <= '0; rxk_r <= '0;
    end else begin
      rxv_r <= rx_tvalid_i; rxl_r <= rx_tlast_i;
      rxd_r <= rx_tdata_i;  rxk_r <= rx_tkeep_i;
    end
  end

  // -----------------------------------------------------------------------
  // 1-beat delay line + match at beat 1 (dst MAC in beat 0 lanes 0-5,
  // EtherType in beat 1 lanes 4-5). The held beat is pushed once the frame
  // is known to match; the last beat flushes one cycle after tlast.
  // -----------------------------------------------------------------------
  reg        hold_v_r, hold_l_r;
  reg [63:0] hold_d_r;
  reg [7:0]  hold_k_r;

  reg [1:0]  beat_idx_r;    //! 0 = expecting beat0, 1 = expecting beat1, 2 = body
  reg        active_r;      //! frame matched, streaming into the FIFO
  reg        skip_r;        //! frame rejected, discard until tlast
  reg        kind_r;        //! 0 MSRP / 1 MVRP

  wire [47:0] hold_dst_w = {hold_d_r[7:0],   hold_d_r[15:8],
                            hold_d_r[23:16], hold_d_r[31:24],
                            hold_d_r[39:32], hold_d_r[47:40]};
  wire [15:0] et_w       = {rxd_r[39:32], rxd_r[47:40]};   //! bytes 12,13

  wire match_msrp_w = (hold_dst_w == MSRP_MCAST_MAC_C) && (et_w == MSRP_ETHERTYPE_C);
  wire match_mvrp_w = (hold_dst_w == MVRP_MCAST_MAC_C) && (et_w == MVRP_ETHERTYPE_C);
  wire match_w      = enable_i && (match_msrp_w || match_mvrp_w);

  // FIFO write port (never backpressured: DROP_WHEN_FULL)
  logic        fw_valid;
  logic [63:0] fw_data;
  logic [7:0]  fw_keep;
  logic        fw_last;
  logic        fw_user;
  wire         fw_ready;    //! stays high with DROP_WHEN_FULL (unused)
  wire         fifo_overflow_w;   //! pulses when a frame is dropped

  always_comb begin
    fw_valid = 1'b0;
    fw_data  = hold_d_r;
    fw_keep  = hold_k_r;
    fw_last  = 1'b0;
    fw_user  = kind_r;
    if (hold_v_r && hold_l_r) begin
      // flush of a completed frame's final beat
      fw_valid = 1'b1;
      fw_last  = 1'b1;
    end else if (rxv_r && hold_v_r) begin
      if (beat_idx_r == 2'd1) begin
        // beat 1 arriving: push beat 0 only if the frame matches
        fw_valid = match_w;
        fw_user  = match_mvrp_w;   // kind decided this very cycle
      end else if (active_r) begin
        fw_valid = 1'b1;
      end
    end
  end

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      hold_v_r <= 1'b0; hold_l_r <= 1'b0; hold_d_r <= '0; hold_k_r <= '0;
      beat_idx_r <= 2'd0; active_r <= 1'b0; skip_r <= 1'b0; kind_r <= 1'b0;
      rx_pdus_o <= 16'd0; rx_drops_o <= 8'd0;
    end else begin
      if (fifo_overflow_w) rx_drops_o <= rx_drops_o + 8'd1;
      // a flushed final beat empties the hold register
      if (hold_v_r && hold_l_r) begin
        hold_v_r <= 1'b0; hold_l_r <= 1'b0;
        active_r <= 1'b0;
      end

      if (rxv_r) begin
        if (skip_r) begin
          if (rxl_r) begin
            skip_r <= 1'b0; beat_idx_r <= 2'd0;
          end
        end else begin
          case (beat_idx_r)
            2'd0: begin
              if (rxl_r) begin
                // runt (<= 8 B): nothing to match, drop silently
                beat_idx_r <= 2'd0;
              end else begin
                hold_d_r <= rxd_r; hold_k_r <= rxk_r; hold_l_r <= 1'b0;
                hold_v_r <= 1'b1;
                beat_idx_r <= 2'd1;
              end
            end
            2'd1: begin
              if (match_w) begin
                active_r <= 1'b1;
                kind_r   <= match_mvrp_w;
                rx_pdus_o <= rx_pdus_o + 16'd1;
                hold_d_r <= rxd_r; hold_k_r <= rxk_r; hold_l_r <= rxl_r;
                hold_v_r <= 1'b1;
                beat_idx_r <= rxl_r ? 2'd0 : 2'd2;
              end else begin
                hold_v_r <= 1'b0;
                if (rxl_r) beat_idx_r <= 2'd0;
                else begin skip_r <= 1'b1; beat_idx_r <= 2'd0; end
              end
            end
            default: begin
              hold_d_r <= rxd_r; hold_k_r <= rxk_r; hold_l_r <= rxl_r;
              hold_v_r <= 1'b1;
              if (rxl_r) beat_idx_r <= 2'd0;
            end
          endcase
        end
      end
    end
  end

  // -----------------------------------------------------------------------
  // Packet FIFO (atomic frames, drop-when-full)
  // -----------------------------------------------------------------------
  axis_fifo #(
    .DEPTH(FIFO_DEPTH_BYTES_P),
    .DATA_WIDTH(64),
    .KEEP_ENABLE(1),
    .KEEP_WIDTH(8),
    .LAST_ENABLE(1),
    .ID_ENABLE(0),
    .DEST_ENABLE(0),
    .USER_ENABLE(1),
    .USER_WIDTH(1),
    .FRAME_FIFO(1),
    .DROP_OVERSIZE_FRAME(1),
    .DROP_WHEN_FULL(1)
  ) mrpdu_fifo (
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
    .m_axis_tdata (m_tdata),
    .m_axis_tkeep (m_tkeep),
    .m_axis_tvalid(m_tvalid),
    .m_axis_tready(m_tready),
    .m_axis_tlast (m_tlast),
    .m_axis_tid   (),
    .m_axis_tdest (),
    .m_axis_tuser (m_tuser),
    .pause_req(1'b0),
    .pause_ack(),
    .status_depth(),
    .status_depth_commit(),
    .status_overflow(fifo_overflow_w),
    .status_bad_frame(),
    .status_good_frame()
  );

endmodule

`default_nettype wire

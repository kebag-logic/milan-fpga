/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_ctrl_split.sv
  Description : The split placement's control frames, in the datapath clock
                (#665). With CTRL_SPLIT_P = 1, milan_datapath
                builds no KL_pp_shadow, and this block carries what the
                wrapper's two frame faces carried, between the fabric and the
                mailbox's byte streams (docs/design/MAILBOX_SPLIT.md):

                  ingress  the fabric's receive tap, every beat qualified on
                           tvalid && tready, classified at beat 1, buffered
                           a whole frame at a time, and handed out a byte a
                           cycle while the consumer is ready
                  egress   the mailbox's transmit bytes packed into the
                           control lane's beats, little lane order

                THE ONE DESIGN DECISION: the tap keeps the wrapper's own
                buffer and drain. Its FIFO holds RX_FIFO_BYTES_P (4,096, the
                wrapper's), stores whole frames and drops a frame it cannot
                take; the serializer drains one byte a cycle. So the split
                tolerates exactly the control bursts the all-fabric build
                does. It accepts a superset of the mailbox filter's tuples
                (sw/mailbox/mailbox.yaml, its channels): EtherType 0x22F0
                with the subtype of ADP (0xFA), AECP (0xFB) or ACMP (0xFC),
                which IEEE 1722.1-2021 assigns, or of MAAP (0xFE, IEEE
                1722-2016 Annex B), and MSRP and MVRP at their group
                addresses, as the wrapper's tap accepts them. The wrapper
                also passed the media subtypes; here they never reach the
                mailbox, which would refuse them.

                THE COUNTERS are the wrapper's three, at the same CSR words
                (PP rx/tx frames and drops): a frame handed out and a frame
                sent, each wrapping at 16 bits, and a control frame lost to
                a full FIFO, saturating at 255 (PP_DIAG[15:8]). A FIFO that
                drops when full never lowers tready, so the loss is read
                from the FIFO's own overflow indication, not the handshake.
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_ctrl_split #(
    parameter int unsigned TDATA_WIDTH_P   = 64,
    //! the tap's FIFO, in bytes: the wrapper's own (KL_pp_shadow)
    parameter int unsigned RX_FIFO_BYTES_P = 4096
) (
    input  wire                        clk_i,        //! the datapath's clock
    input  wire                        rst_n,        //! synchronous active-low reset
    //! ---- the fabric's receive tap (input only, qualified on the handshake)
    input  wire [TDATA_WIDTH_P-1:0]    rx_tdata_i,
    input  wire [TDATA_WIDTH_P/8-1:0]  rx_tkeep_i,
    input  wire                        rx_tvalid_i,
    input  wire                        rx_tready_i,
    input  wire                        rx_tlast_i,
    //! ---- the control frames' bytes, to the mailbox's ingress
    output logic                       rx_valid_o,   //! a byte is offered
    output logic [7:0]                 rx_data_o,    //! the byte, wire order
    output logic                       rx_last_o,    //! the frame's last byte
    input  wire                        rx_ready_i,   //! the byte is taken
    //! ---- the mailbox's egress bytes
    input  wire                        tx_valid_i,   //! a byte is offered
    input  wire  [7:0]                 tx_data_i,    //! the byte, wire order
    input  wire                        tx_last_i,    //! the frame's last byte
    output logic                       tx_ready_o,   //! the byte is taken
    //! ---- the control lane's beats (ctl_tx_mux's s_data leg)
    output logic [TDATA_WIDTH_P-1:0]   m_axis_tx_tdata,  //! little lane order
    output logic [TDATA_WIDTH_P/8-1:0] m_axis_tx_tkeep,  //! contiguous from lane 0
    output logic                       m_axis_tx_tvalid, //! a beat is offered
    output logic                       m_axis_tx_tlast,  //! the frame's last beat
    input  wire                        m_axis_tx_tready, //! the lane takes the beat
    //! ---- the wrapper's three counters
    output logic [15:0]                rx_frames_o,  //! control frames handed out, wrapping
    output logic [7:0]                 rx_drops_o,   //! control frames a full FIFO lost, saturating
    output logic [15:0]                tx_frames_o   //! control frames sent, wrapping
);

  localparam int unsigned KEEP_W_C = TDATA_WIDTH_P / 8;
  //! the lane arithmetic below holds eight lanes, as the wrapper's does
  if (TDATA_WIDTH_P != 64) begin : g_width_check
    $error("KL_ctrl_split: TDATA_WIDTH_P must be 64, got %0d", TDATA_WIDTH_P);
  end

  localparam logic [47:0] DA_MSRP_C = 48'h01_80_C2_00_00_0E;
  localparam logic [47:0] DA_MVRP_C = 48'h01_80_C2_00_00_21;
  localparam logic [15:0] ET_1722_C = 16'h22F0;
  localparam logic [15:0] ET_MSRP_C = 16'h22EA;
  localparam logic [15:0] ET_MVRP_C = 16'h88F5;
  //! the AVTP control subtypes the mailbox has a channel for
  localparam logic [7:0]  ST_ADP_C  = 8'hFA;
  localparam logic [7:0]  ST_AECP_C = 8'hFB;
  localparam logic [7:0]  ST_ACMP_C = 8'hFC;
  localparam logic [7:0]  ST_MAAP_C = 8'hFE;

  // ======================================================================= //
  //  Ingress: classify at beat 1, then buffer whole frames                  //
  // ======================================================================= //
  logic beat_w;
  assign beat_w = rx_tvalid_i & rx_tready_i;

  //! beat 0 carries the destination in lanes 0-5; beat 1 the EtherType in
  //! lanes 4-5 (wire bytes 12 and 13) and the subtype in lane 6 (byte 14)
  logic [47:0] da_num_w;
  logic [15:0] etype_w;
  logic [7:0]  subtype_w;
  assign da_num_w  = {rx_tdata_i[7:0],   rx_tdata_i[15:8],
                      rx_tdata_i[23:16], rx_tdata_i[31:24],
                      rx_tdata_i[39:32], rx_tdata_i[47:40]};
  assign etype_w   = {rx_tdata_i[39:32], rx_tdata_i[47:40]};
  assign subtype_w = rx_tdata_i[55:48];

  typedef enum logic [1:0] {TAP_HEAD0_S, TAP_HEAD1_S, TAP_BODY_S, TAP_SKIP_S} tap_state_e;
  tap_state_e tap_r;
  logic [47:0] da_r;

  logic accept_w;
  assign accept_w = ((etype_w == ET_1722_C)
                     && ((subtype_w == ST_ADP_C) || (subtype_w == ST_AECP_C)
                         || (subtype_w == ST_ACMP_C) || (subtype_w == ST_MAAP_C)))
                 || ((da_r == DA_MSRP_C) && (etype_w == ET_MSRP_C))
                 || ((da_r == DA_MVRP_C) && (etype_w == ET_MVRP_C));

  logic                     fw_valid_w, fw_last_w, fw_user_w, fw_ready_w;
  logic [TDATA_WIDTH_P-1:0] fw_data_w;
  logic [KEEP_W_C-1:0]      fw_keep_w;

  always_comb begin : tap_forward
    fw_valid_w = 1'b0;
    fw_data_w  = rx_tdata_i;
    fw_keep_w  = rx_tkeep_i;
    fw_last_w  = rx_tlast_i;
    fw_user_w  = 1'b0;
    unique case (tap_r)
      TAP_HEAD0_S: begin
        //! beat 0 is written before the verdict; a frame ending here is a
        //! runt and is dropped
        fw_valid_w = beat_w;
        fw_user_w  = rx_tlast_i;
      end
      TAP_HEAD1_S: begin
        //! a refused frame ends here, marked bad, so the FIFO reclaims it
        fw_valid_w = beat_w;
        if (!accept_w) begin
          fw_last_w = 1'b1;
          fw_user_w = 1'b1;
        end
      end
      TAP_BODY_S: fw_valid_w = beat_w;
      default:    fw_valid_w = 1'b0;   // the rest of a refused frame
    endcase
  end : tap_forward

  always_ff @(posedge clk_i) begin : tap_state
    if (!rst_n) begin
      tap_r <= TAP_HEAD0_S;
      da_r  <= 48'd0;
    end else if (beat_w) begin
      unique case (tap_r)
        TAP_HEAD0_S: begin
          da_r  <= da_num_w;
          tap_r <= rx_tlast_i ? TAP_HEAD0_S : TAP_HEAD1_S;
        end
        TAP_HEAD1_S: tap_r <= rx_tlast_i ? TAP_HEAD0_S
                                         : (accept_w ? TAP_BODY_S : TAP_SKIP_S);
        default:     if (rx_tlast_i) tap_r <= TAP_HEAD0_S;
      endcase
    end
  end : tap_state

  //! A frame the tap kept, lost to a full FIFO (#665). With FRAME_FIFO and
  //! DROP_WHEN_FULL the FIFO holds tready high and drops a frame it has no
  //! room for by itself, raising status_overflow for the cycle after that
  //! frame's last beat (verilog-axis axis_fifo). A runt or a refused frame
  //! ends marked bad and is reclaimed either way, so its overflow loses no
  //! control frame: the count takes an overflow only after the last beat of
  //! a frame the tap kept, as that beat records it.
  logic drop_p_w, ff_overflow_w, last_kept_r;
  always_ff @(posedge clk_i) begin : drop_track
    if (!rst_n) begin
      last_kept_r <= 1'b0;
    end else if (fw_valid_w && fw_ready_w && fw_last_w) begin
      last_kept_r <= (tap_r == TAP_BODY_S) || ((tap_r == TAP_HEAD1_S) && accept_w);
    end
  end : drop_track
  assign drop_p_w = ff_overflow_w & last_kept_r;

  logic [TDATA_WIDTH_P-1:0] ff_data_w;
  logic [KEEP_W_C-1:0]      ff_keep_w;
  logic                     ff_valid_w, ff_last_w, ff_ready_w;

  axis_fifo #(
    .DEPTH               (RX_FIFO_BYTES_P),
    .DATA_WIDTH          (TDATA_WIDTH_P),
    .KEEP_ENABLE         (1),
    .KEEP_WIDTH          (KEEP_W_C),
    .LAST_ENABLE         (1),
    .ID_ENABLE           (0),
    .DEST_ENABLE         (0),
    .USER_ENABLE         (1),
    .USER_WIDTH          (1),
    .FRAME_FIFO          (1),
    .USER_BAD_FRAME_VALUE(1'b1),
    .USER_BAD_FRAME_MASK (1'b1),
    .DROP_BAD_FRAME      (1),
    .DROP_OVERSIZE_FRAME (1),
    .DROP_WHEN_FULL      (1)
  ) rx_fifo (
    .clk                (clk_i),
    .rst                (~rst_n),
    .s_axis_tdata       (fw_data_w),
    .s_axis_tkeep       (fw_keep_w),
    .s_axis_tvalid      (fw_valid_w),
    .s_axis_tready      (fw_ready_w),
    .s_axis_tlast       (fw_last_w),
    .s_axis_tid         ('0),
    .s_axis_tdest       ('0),
    .s_axis_tuser       (fw_user_w),
    .m_axis_tdata       (ff_data_w),
    .m_axis_tkeep       (ff_keep_w),
    .m_axis_tvalid      (ff_valid_w),
    .m_axis_tready      (ff_ready_w),
    .m_axis_tlast       (ff_last_w),
    .m_axis_tid         (),
    .m_axis_tdest       (),
    .m_axis_tuser       (),
    .status_overflow    (ff_overflow_w),
    .status_bad_frame   (),
    .status_good_frame  (),
    .status_depth       (),
    .status_depth_commit(),
    .pause_req          (1'b0),
    .pause_ack          ()
  );

  // ======================================================================= //
  //  Ingress serializer: one word held, its bytes out while ready           //
  // ======================================================================= //
  logic [TDATA_WIDTH_P-1:0] ser_data_r;
  logic [KEEP_W_C-1:0]      ser_keep_r;
  logic                     ser_last_r, ser_busy_r;
  logic [2:0]               ser_idx_r;

  //! the held word's last valid lane (keep is contiguous from lane 0)
  logic [2:0] ser_top_w;
  always_comb begin : ser_top
    ser_top_w = 3'd0;
    for (int unsigned i = 0; i < KEEP_W_C; i++) begin
      if (ser_keep_r[i]) ser_top_w = 3'(i);
    end
  end : ser_top

  assign ff_ready_w = ~ser_busy_r;
  assign rx_valid_o = ser_busy_r;
  assign rx_data_o  = ser_data_r[8*ser_idx_r +: 8];
  assign rx_last_o  = ser_busy_r & ser_last_r & (ser_idx_r == ser_top_w);

  always_ff @(posedge clk_i) begin : ser_step
    if (!rst_n) begin
      ser_busy_r <= 1'b0;
      ser_idx_r  <= 3'd0;
      ser_data_r <= '0;
      ser_keep_r <= '0;
      ser_last_r <= 1'b0;
    end else if (!ser_busy_r) begin
      if (ff_valid_w) begin
        ser_data_r <= ff_data_w;
        ser_keep_r <= ff_keep_w;
        ser_last_r <= ff_last_w;
        ser_idx_r  <= 3'd0;
        ser_busy_r <= 1'b1;
      end
    end else if (rx_ready_i) begin
      if (ser_idx_r == ser_top_w) ser_busy_r <= 1'b0;
      else                        ser_idx_r  <= ser_idx_r + 3'd1;
    end
  end : ser_step

  // ======================================================================= //
  //  Egress packer: bytes into beats, one completed beat held at a time     //
  // ======================================================================= //
  //! The mailbox offers at most one byte a cycle and a beat holds eight, so
  //! the beat register stalls the bytes only while a completed beat waits
  //! for the lane, as the wrapper's packer does.
  logic [TDATA_WIDTH_P-1:0] txp_data_r;
  logic [KEEP_W_C-1:0]      txp_keep_r;
  logic                     txp_valid_r, txp_last_r;
  logic [2:0]               txp_idx_r;
  logic                     txp_take_w;

  assign txp_take_w = txp_valid_r & m_axis_tx_tready;
  assign tx_ready_o = ~txp_valid_r;

  always_ff @(posedge clk_i) begin : txp_step
    if (!rst_n) begin
      txp_data_r  <= '0;
      txp_keep_r  <= '0;
      txp_valid_r <= 1'b0;
      txp_last_r  <= 1'b0;
      txp_idx_r   <= 3'd0;
    end else begin
      if (txp_take_w) begin
        txp_valid_r <= 1'b0;
        txp_keep_r  <= '0;
        txp_data_r  <= '0;
      end
      if (tx_valid_i & tx_ready_o) begin
        txp_data_r[8*txp_idx_r +: 8] <= tx_data_i;
        txp_keep_r[txp_idx_r]        <= 1'b1;
        //! a beat closes on its eighth byte or at the frame's end
        if (tx_last_i || (txp_idx_r == 3'd7)) begin
          txp_valid_r <= 1'b1;
          txp_last_r  <= tx_last_i;
          txp_idx_r   <= 3'd0;
        end else begin
          txp_idx_r <= txp_idx_r + 3'd1;
        end
      end
    end
  end : txp_step

  assign m_axis_tx_tdata  = txp_data_r;
  assign m_axis_tx_tkeep  = txp_keep_r;
  assign m_axis_tx_tvalid = txp_valid_r;
  assign m_axis_tx_tlast  = txp_last_r;

  // ======================================================================= //
  //  The wrapper's counters                                                 //
  // ======================================================================= //
  always_ff @(posedge clk_i) begin : frame_counters
    if (!rst_n) begin
      rx_frames_o <= 16'd0;
      rx_drops_o  <= 8'd0;
      tx_frames_o <= 16'd0;
    end else begin
      if (rx_valid_o & rx_ready_i & rx_last_o) rx_frames_o <= rx_frames_o + 16'd1;
      if (drop_p_w & (rx_drops_o != 8'hFF))    rx_drops_o  <= rx_drops_o + 8'd1;
      if (tx_valid_i & tx_ready_o & tx_last_i) tx_frames_o <= tx_frames_o + 16'd1;
    end
  end : frame_counters

endmodule

`default_nettype wire

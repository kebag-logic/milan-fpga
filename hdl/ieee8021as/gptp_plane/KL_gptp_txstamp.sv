/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_gptp_txstamp.sv
//  Project     : Milan AVB end-station -- the fabric gPTP plane (issue #110)
//
//  Description : Observer-pure egress stamper for the gPTP plane's own
//                frames at the MAC boundary. The control lane does not
//                traverse ptp_ts_top's TX stamper (only the shaped data
//                path does), so the plane's Sync/Pdelay egress timestamps
//                are captured HERE: on the final merged TX stream, an
//                EtherType 0x88F7 frame latches the PHC at its first beat
//                and reports {ts, sequenceId, msgType} once the sequence
//                lanes pass -- the engine matches by its pending exchange.
//
//                ARMED counting keeps this the PLANE'S stamper: the plane
//                pulses armed_i as each of its frames enters the merge
//                chain, and only that many 0x88F7 boundary frames are
//                stamped. Frames arbitrated between the plane's lane and
//                the boundary cannot reorder (the merge chain locks per
//                frame downstream of the lane), so the count pairs frames
//                exactly while the plane is the only gPTP transmitter.
//                Running a second gPTP stack (ptp4l) on the same port
//                while the plane transmits is itself invalid -- the A/B
//                bring-up comparison keeps exactly one of them talking.
//
//                PURE OBSERVER: this module drives nothing on the stream
//                it watches (check_tap_purity holds).
//---------------------------------------------------------------------------//
`default_nettype none

module KL_gptp_txstamp #(
    parameter int unsigned TDATA_WIDTH_P = 64
) (
    input  wire clk_i,
    input  wire rst_n,

    //! the final merged MAC TX stream, observed only
    input  wire [TDATA_WIDTH_P-1:0] tx_tdata_i,
    input  wire                     tx_tvalid_i,
    input  wire                     tx_tready_i,
    input  wire                     tx_tlast_i,

    //! the live PHC value
    input  wire [63:0] phc_ns_i,

    //! one pulse per plane frame that entered the merge chain
    input  wire armed_i,

    //! the stamp, seq-matched by the engine
    output logic        ts_valid_o,
    output logic [63:0] ts_ns_o,
    output logic [15:0] ts_seq_o
);

  localparam logic [15:0] ET_GPTP_C = 16'h88F7;

  logic beat_w;
  assign beat_w = tx_tvalid_i & tx_tready_i;

  //! plane frames in flight between the lane and the boundary
  logic [3:0] armed_r;

  //! wire bytes 12,13 = beat-1 lanes 4,5; sequenceId = wire bytes 44,45 =
  //! beat-5 lanes 4,5 (byte b = beat b/8, lane b%8)
  logic [2:0]  bcnt_r;                  //! beats 0..5 tracked, saturates
  logic        is_gptp_r, take_r;
  logic [63:0] ts_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      armed_r    <= 4'd0;
      bcnt_r     <= 3'd0;
      is_gptp_r  <= 1'b0;
      take_r     <= 1'b0;
      ts_r       <= 64'd0;
      ts_valid_o <= 1'b0;
      ts_ns_o    <= 64'd0;
      ts_seq_o   <= 16'd0;
    end else begin
      ts_valid_o <= 1'b0;

      //! arm and consume can coincide; the counter nets them
      unique case ({armed_i, take_r & beat_w & (bcnt_r == 3'd5)
                             & is_gptp_r})
        2'b10:   armed_r <= armed_r + 4'd1;
        2'b01:   armed_r <= armed_r - 4'd1;
        default: ;
      endcase

      if (beat_w) begin
        if (bcnt_r == 3'd0) begin
          ts_r      <= phc_ns_i;        //! first-beat boundary stamp
          is_gptp_r <= 1'b0;
          take_r    <= (armed_r != 4'd0) | armed_i;
        end
        if (bcnt_r == 3'd1)
          is_gptp_r <= ({tx_tdata_i[39:32], tx_tdata_i[47:40]} == ET_GPTP_C);
        if ((bcnt_r == 3'd5) && is_gptp_r && take_r) begin
          ts_valid_o <= 1'b1;
          ts_ns_o    <= ts_r;
          ts_seq_o   <= {tx_tdata_i[39:32], tx_tdata_i[47:40]};
        end
        if (tx_tlast_i)          bcnt_r <= 3'd0;
        else if (bcnt_r != 3'd7) bcnt_r <= bcnt_r + 3'd1;
      end
    end
  end

  //! an observer reads only the lanes it needs
  logic unused_w;
  assign unused_w = ^{tx_tdata_i[63:48], tx_tdata_i[31:0]};

endmodule : KL_gptp_txstamp
`default_nettype wire

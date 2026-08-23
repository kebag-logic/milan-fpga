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
//                lanes pass. Both tags travel because neither alone
//                identifies the transmitter: a Pdelay_Req carries our own
//                request counter while a Pdelay_Resp echoes the peer's, so
//                two legs can hold the same 16-bit sequenceId at once, and
//                on a link where both ends run this plane the two counters
//                start equal at boot and stay equal at 1 Hz. Two frames of
//                the SAME messageType cannot be outstanding together, so
//                {sequenceId, msgType} separates every pair the engine has
//                to tell apart (milan-fpga #214, Mister-M-alt/FPGA-gPTP#28).
//
//                ARMED counting keeps this the PLANE'S stamper: the plane
//                pulses armed_i as each of its frames enters the merge
//                chain, and only that many 0x88F7 boundary frames are
//                stamped. What that counting guarantees, exactly: the
//                plane's own frames cannot reorder against each other,
//                because they leave on ONE AXI-Stream lane and every
//                arbiter in the merge chain locks a frame from tlast to
//                tlast rather than interleaving beats (proved for
//                adp_tx_arbiter by tb/verilator/adp_tx, "frame not
//                interleaved (single tag)"). What it does NOT guarantee is
//                exclusivity: a foreign 0x88F7 frame from another stack on
//                the same port would be counted as ours, which is why
//                running ptp4l beside the plane is invalid -- the A/B
//                bring-up comparison keeps exactly one of them talking.
//                The order premise is not load-bearing any more either:
//                the engine matches the returning stamp by its {sequenceId,
//                msgType} tag, not by position. No bench proves the merge
//                chain end to end for THIS module; tb/verilator/gptp_shadow
//                watches the lane with no arbiter between (it proves the
//                stamper pairs back-to-back frames in order, one stamp
//                each, tagged with their own header fields), and a full
//                proof would need tb/verilator/milan_dp to run the gPTP
//                lane against a contending source and check the pairing
//                survives (milan-fpga #214).
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

    //! the stamp, matched by the engine on {sequenceId, msgType}
    output logic        ts_valid_o,
    output logic [63:0] ts_ns_o,
    output logic [15:0] ts_seq_o,
    output logic [3:0]  ts_type_o    //! messageType of the stamped frame
);

  localparam logic [15:0] ET_GPTP_C = 16'h88F7;

  logic beat_w;
  assign beat_w = tx_tvalid_i & tx_tready_i;

  //! plane frames in flight between the lane and the boundary
  logic [3:0] armed_r;

  //! wire bytes 12,13 = beat-1 lanes 4,5; messageType = the low nibble of
  //! wire byte 14 = beat-1 lane 6 (802.1AS-2011 11.4.2.1, the high nibble
  //! is transportSpecific); sequenceId = wire bytes 44,45 = beat-5 lanes
  //! 4,5 (byte b = beat b/8, lane b%8)
  logic [2:0]  bcnt_r;                  //! beats 0..5 tracked, saturates
  logic        is_gptp_r, take_r;
  logic [3:0]  mtype_r;                 //! latched with the EtherType
  logic [63:0] ts_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      armed_r    <= 4'd0;
      bcnt_r     <= 3'd0;
      is_gptp_r  <= 1'b0;
      take_r     <= 1'b0;
      mtype_r    <= 4'd0;
      ts_r       <= 64'd0;
      ts_valid_o <= 1'b0;
      ts_ns_o    <= 64'd0;
      ts_seq_o   <= 16'd0;
      ts_type_o  <= 4'd0;
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
        if (bcnt_r == 3'd1) begin
          is_gptp_r <= ({tx_tdata_i[39:32], tx_tdata_i[47:40]} == ET_GPTP_C);
          mtype_r   <= tx_tdata_i[51:48];   //! byte 14 low nibble
        end
        if ((bcnt_r == 3'd5) && is_gptp_r && take_r) begin
          ts_valid_o <= 1'b1;
          ts_ns_o    <= ts_r;
          ts_seq_o   <= {tx_tdata_i[39:32], tx_tdata_i[47:40]};
          ts_type_o  <= mtype_r;
        end
        if (tx_tlast_i)          bcnt_r <= 3'd0;
        else if (bcnt_r != 3'd7) bcnt_r <= bcnt_r + 3'd1;
      end
    end
  end

  //! an observer reads only the lanes it needs: lane 6's low nibble is the
  //! messageType above, its high nibble (transportSpecific) is not read
  logic unused_w;
  assign unused_w = ^{tx_tdata_i[63:52], tx_tdata_i[31:0]};

endmodule : KL_gptp_txstamp
`default_nettype wire

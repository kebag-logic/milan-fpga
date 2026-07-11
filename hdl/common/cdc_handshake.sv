/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : cdc_handshake.sv
//  Description : Open, FPGA-independent **multi-bit value** clock-domain crossing
//                via a 4-phase req/ack handshake. The data bus is held stable by
//                the source until the acknowledge returns, so it is sampled by the
//                destination only after the request has synchronised — no per-bit
//                synchroniser needed. Replaces Xilinx `xpm_cdc_handshake`
//                (docs/integration/OPEN_SOURCE_MIGRATION.md Track 1.4).
//
//  Protocol    : source asserts `src_send` (level) with `src_in` valid; when the
//                transfer completes `src_rcv` pulses (source may drop `src_send`).
//                Destination gets `dest_out` + a 1-cycle `dest_req`.
//
//  Synthesis   : put a false-path / max-delay on `data_hold` and the two toggles.
//---------------------------------------------------------------------------//
`default_nettype none

module cdc_handshake #(
    parameter int WIDTH        = 64,
    parameter int DEST_SYNC_FF = 2,
    parameter int SRC_SYNC_FF  = 2
)(
    input  wire             src_clk,
    input  wire             src_rst_n,
    input  wire [WIDTH-1:0] src_in,
    input  wire             src_send,   //! assert (level) to send; hold until src_rcv
    output wire             src_rcv,     //! 1-cycle: destination captured the value
    input  wire             dest_clk,
    input  wire             dest_rst_n,
    output wire [WIDTH-1:0] dest_out,
    output wire             dest_req      //! 1-cycle: dest_out valid
);

  // ---- declarations (both domains) --------------------------------------
  reg             src_send_d, req_tog;
  reg [WIDTH-1:0] data_hold;
  (* ASYNC_REG = "TRUE" *) reg [SRC_SYNC_FF:0]  ack_sync;
  (* ASYNC_REG = "TRUE" *) reg [DEST_SYNC_FF:0] req_sync;
  reg [WIDTH-1:0] dest_out_r;
  reg             dest_req_r, ack_tog;

  // ---- source: on rising edge of src_send, latch data + toggle request ---
  always_ff @(posedge src_clk) begin
    if (!src_rst_n) begin
      src_send_d <= 1'b0; req_tog <= 1'b0; data_hold <= '0;
    end else begin
      src_send_d <= src_send;
      if (src_send && !src_send_d) begin
        data_hold <= src_in;
        req_tog   <= ~req_tog;
      end
    end
  end

  // ack toggle synchronised back into the source domain -> src_rcv pulse
  always_ff @(posedge src_clk)
    if (!src_rst_n) ack_sync <= '0;
    else            ack_sync <= {ack_sync[SRC_SYNC_FF-1:0], ack_tog};
  assign src_rcv = ack_sync[SRC_SYNC_FF] ^ ack_sync[SRC_SYNC_FF-1];

  // ---- destination: sync request, capture data on its edge, toggle ack ---
  always_ff @(posedge dest_clk)
    if (!dest_rst_n) req_sync <= '0;
    else             req_sync <= {req_sync[DEST_SYNC_FF-1:0], req_tog};
  wire req_edge = req_sync[DEST_SYNC_FF] ^ req_sync[DEST_SYNC_FF-1];

  always_ff @(posedge dest_clk) begin
    if (!dest_rst_n) begin
      dest_out_r <= '0; dest_req_r <= 1'b0; ack_tog <= 1'b0;
    end else begin
      dest_req_r <= req_edge;
      if (req_edge) begin
        dest_out_r <= data_hold;   //! stable: source holds it until ack returns
        ack_tog    <= ~ack_tog;
      end
    end
  end

  assign dest_out = dest_out_r;
  assign dest_req = dest_req_r;

endmodule

`default_nettype wire

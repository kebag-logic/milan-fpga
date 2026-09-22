/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_trace_ring.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/02 §7
//                window 0x40000, 07 §5.5 side-port map, 01 F01.5
//                P-TRACE-RING)
//
//  Description : Debug trace ring — the backing store of the RO side-port
//                window 0x40000. Shape is P-TRACE-RING (F01.5): 256 records
//                × 128 b. One record arrives per event on wr_valid_i (the
//                record content is the class-A framed event its producer
//                emits, 02 §1 — opaque bits here); the ring overwrites
//                oldest-first and NEVER back-pressures a producer: tracing
//                may lose history, it must never stall the plane. The
//                monotonic 16-bit write counter (mod 2^16) is the only
//                progress state — its low bits are the write pointer, and
//                the host reads it through the side-port window to locate
//                the ring head and detect wrap.
//
//                Read side is the side-port window path: record index
//                rd_addr_i plus 32-bit lane select rd_lane_i, lane 0 =
//                record bits [127:96] (MSB-first, the class-A word order
//                of 02 §3).
//
//                The one design decision that matters: ONE 256 × 128 b
//                1W1R sync-read RAM with the 4:1 lane mux placed AFTER the
//                128-bit read register — sync read so the array infers
//                block RAM, never a flop mirror with a wide asynchronous
//                read mux (the +894-LUT failure mode). Same-address
//                read-during-write returns the OLD record (read-first), so
//                a host walk during live tracing is always
//                record-consistent.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_trace_ring #(
    //! P-TRACE-RING records (F01.5 default 256)
    parameter int unsigned RECORDS_P = 256,
    //! P-TRACE-RING record width in bits (F01.5 default 128; multiple of 32)
    parameter int unsigned RECORD_W_P = 128,
    //! derived: record index width
    localparam int unsigned ADDR_W_C = $clog2(RECORDS_P),
    //! derived: 32-bit lanes per record
    localparam int unsigned LANES_C = RECORD_W_P / 32,
    //! derived: lane select width
    localparam int unsigned LANE_W_C = $clog2(LANES_C)
) (
    input  wire                   clk_i,       //! core clock (P-CLK-HZ domain)
    input  wire                   rst_n,       //! synchronous active-low reset

    //! ---- write side (event producers; never back-pressured) ----
    input  wire                   wr_valid_i,  //! one trace record this cycle
    input  wire  [RECORD_W_P-1:0] wr_data_i,   //! the record (class-A framed event)
    output logic           [15:0] wr_count_o,  //! monotonic write count, mod 2^16

    //! ---- read side (side-port window 0x40000, RO) ----
    input  wire                   rd_en_i,     //! sync read enable
    input  wire    [ADDR_W_C-1:0] rd_addr_i,   //! record index
    input  wire    [LANE_W_C-1:0] rd_lane_i,   //! 32-bit lane, 0 = bits [127:96]
    output logic           [31:0] rd_data_o    //! lane data, one cycle after rd_en_i
);

  // ------------------------------------------------- monotonic write count
  logic            [15:0] wr_count_r;
  logic  [ADDR_W_C-1:0]   wr_ptr_w;

  assign wr_ptr_w   = wr_count_r[ADDR_W_C-1:0];
  assign wr_count_o = wr_count_r;

  always_ff @(posedge clk_i) begin : count_ff
    if (!rst_n) begin
      wr_count_r <= 16'h0;
    end else if (wr_valid_i) begin
      wr_count_r <= wr_count_r + 16'd1;
    end
  end

  // ---------------------------------------------------------- the ring RAM
  // RECORDS_P × RECORD_W_P bits, 1W1R, sync read. Deliberately NO reset on
  // the array or the read registers — a reset here breaks block-RAM
  // inference (the justified exception to the sync-reset rule, as in
  // KL_pp_rx_slots). Stale pre-wrap records are qualified by wr_count_o.
  logic [RECORD_W_P-1:0] mem_r [0:RECORDS_P-1];
  logic [RECORD_W_P-1:0] rd_word_r;
  logic [LANE_W_C-1:0]   rd_lane_r;

  always_ff @(posedge clk_i) begin : ring_wr
    if (wr_valid_i) mem_r[wr_ptr_w] <= wr_data_i;
  end

  always_ff @(posedge clk_i) begin : ring_rd
    if (rd_en_i) begin
      rd_word_r <= mem_r[rd_addr_i];
      rd_lane_r <= rd_lane_i;
    end
  end

  // lane mux AFTER the read register (MSB-first: lane 0 = top 32 bits)
  always_comb begin : lane_mux
    rd_data_o = 32'h0;
    for (int unsigned l = 0; l < LANES_C; l++) begin
      if (rd_lane_r == LANE_W_C'(l)) begin
        rd_data_o = rd_word_r[(LANES_C-1-l)*32 +: 32];
      end
    end
  end

endmodule

`default_nettype wire

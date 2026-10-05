/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_ring.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665 lane F0)
//
//  Description : One mailbox ring's storage: WORDS_P x 32 bits of simple
//                dual-port block RAM, one write port and one registered
//                read port. A ring has exactly one producer and one
//                consumer, so it never needs a second write port: an RX ring
//                and the event ring are written by the fabric and read by
//                the host, a TX ring is written by the host and read by the
//                fabric. The head and tail counters that give the words
//                their meaning live with their owners in KL_mbx, never here.
//
//                The one decision that matters: the storage has no reset.
//                Block RAM cannot be cleared in one cycle, and nothing reads
//                a word the producer has not written since its counter last
//                passed it, so a reset would cost a clear sequence and buy
//                nothing. The read register is reset like every register.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mbx_ring #(
  parameter int unsigned WORDS_P = 256   //! ring size in 32-bit words, a power of two
) (
  input  wire                         clk_i,      //! the mailbox clock
  input  wire                         rst_n,      //! synchronous active-low reset (read register only)

  input  wire                         wr_en_i,    //! write one word this cycle
  input  wire  [$clog2(WORDS_P)-1:0]  wr_addr_i,  //! word index written
  input  wire  [31:0]                 wr_data_i,  //! word written

  input  wire                         rd_en_i,    //! read one word; it appears on rd_data_o next cycle
  input  wire  [$clog2(WORDS_P)-1:0]  rd_addr_i,  //! word index read
  output logic [31:0]                 rd_data_o   //! word read, one cycle after rd_en_i
);

  // An elaboration contract: the ring counters wrap modulo the size, which is
  // only an index when the size is a power of two, and a one-word ring cannot
  // hold a record header.
  if (WORDS_P < 2 || (WORDS_P & (WORDS_P - 1)) != 0) begin : g_bad_words
    $error("KL_mbx_ring: WORDS_P=%0d is not a power of two of at least 2", WORDS_P);
  end : g_bad_words

  logic [31:0] mem_r [WORDS_P];

  always_ff @(posedge clk_i) begin : write_port
    if (wr_en_i) mem_r[wr_addr_i] <= wr_data_i;
  end : write_port

  always_ff @(posedge clk_i) begin : read_port
    if (!rst_n) rd_data_o <= '0;
    else if (rd_en_i) rd_data_o <= mem_r[rd_addr_i];
  end : read_port

endmodule : KL_mbx_ring

`default_nettype wire

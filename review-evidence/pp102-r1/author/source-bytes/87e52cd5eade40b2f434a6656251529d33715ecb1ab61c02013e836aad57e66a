/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : tx_arbiter_harness.sv
//  Project     : IEEE 1722.1 protocol processor — tx_arbiter suite harness
//                (docs/architecture/03 §7 + §8 wired together)
//
//  Description : KL_pp_tx_arbiter wired to the REAL KL_pp_tx_slots pool at
//                the F01.5 shape (4 x 576 + 1600). The C++ harness plays
//                the response builders (alloc/write/commit) and the six
//                F03.5 requesters; the merged tx_* stream and the grant
//                pulses/counters are observed. The ser_* port match
//                between arbiter and pool is proven by this elaboration.
//
//  Decision    : the harness adds NOTHING between the two DUTs — every
//                wire of the ser_* contract is a direct connection, so a
//                suite pass is evidence about the real pair, not about
//                harness glue.
//---------------------------------------------------------------------------//
`default_nettype none

module tx_arbiter_harness (
    input  wire         clk_i,        //! core clock
    input  wire         rst_n,        //! synchronous active-low reset
    input  wire         tick_ms_i,    //! compressed ms tick (aging)

    // ---- builder side of the pool (TB = response builders) ---------------
    input  wire         alloc_req_i,  //! slot request
    input  wire         oversize_i,   //! request the Δ8 oversize slot
    output logic        alloc_gnt_o,  //! one-cycle grant pulse
    output logic [2:0]  alloc_slot_o, //! granted slot index
    input  wire  [2:0]  wr_slot_i,    //! slot being written / committed
    input  wire  [10:0] wr_addr_i,    //! byte offset within the slot
    input  wire         wr_valid_i,   //! byte-write strobe
    input  wire  [7:0]  wr_data_i,    //! byte to write
    input  wire         wr_commit_i,  //! ALLOC -> READY
    input  wire  [10:0] wr_len_i,     //! committed frame length

    // ---- the six requesters (TB = engines) --------------------------------
    input  wire  [5:0]       req_valid_i,  //! request pending per lane
    input  wire  [5:0][2:0]  tx_slot_i,    //! committed slot per lane
    input  wire              start_abort_i, //! withdraw selected request before pool start
    output logic [5:0]       gnt_o,        //! grant pulse per lane
    output logic [5:0][15:0] gnt_count_o,  //! grant counters per lane

    // ---- merged stream (02 §2 class A) ------------------------------------
    output logic        tx_valid_o,   //! merged stream byte valid
    output logic        tx_sof_o,     //! first byte of each frame
    output logic [7:0]  tx_data_o,    //! merged stream byte
    output logic        tx_eof_o,     //! final byte of each frame
    input  wire         tx_ready_i,   //! downstream consumes the byte

    // ---- pool status (observability) --------------------------------------
    output logic [4:0]  slots_ready_o, //! per-slot committed-unserviced
    output logic [2:0]  slots_free_o   //! number of FREE slots
);

  // the ser_* contract under test: direct wires, nothing added
  logic       ser_req_w;
  logic [2:0] ser_slot_w;
  logic       ser_valid_w;
  logic [7:0] ser_data_w;
  logic       ser_last_w;
  logic       ser_ready_w;

  KL_pp_tx_slots u_pool (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .alloc_req_i   (alloc_req_i),
      .oversize_i    (oversize_i),
      .alloc_gnt_o   (alloc_gnt_o),
      .alloc_slot_o  (alloc_slot_o),
      .wr_slot_i     (wr_slot_i),
      .wr_addr_i     (wr_addr_i),
      .wr_valid_i    (wr_valid_i),
      .wr_data_i     (wr_data_i),
      .wr_commit_i   (wr_commit_i),
      .wr_len_i      (wr_len_i),
      .hold_valid_i  (1'b0),
      .hold_slot_i   ('0),
      .release_valid_i(1'b0),
      .release_slot_i('0),
      .ser_req_i     (ser_req_w),
      .ser_slot_i    (ser_slot_w),
      .ser_valid_o   (ser_valid_w),
      .ser_data_o    (ser_data_w),
      .ser_last_o    (ser_last_w),
      .ser_ready_i   (ser_ready_w),
      .slots_ready_o (slots_ready_o),
      .slots_free_o  (slots_free_o)
  );

  KL_pp_tx_arbiter u_arb (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .tick_ms_i   (tick_ms_i),
      .req_valid_i (req_valid_i),
      .tx_slot_i   (tx_slot_i),
      .start_abort_i(start_abort_i),
      .gnt_o       (gnt_o),
      .gnt_count_o (gnt_count_o),
      .ser_req_o   (ser_req_w),
      .ser_slot_o  (ser_slot_w),
      .ser_valid_i (ser_valid_w),
      .ser_data_i  (ser_data_w),
      .ser_last_i  (ser_last_w),
      .ser_ready_o (ser_ready_w),
      .tx_valid_o  (tx_valid_o),
      .tx_sof_o    (tx_sof_o),
      .tx_data_o   (tx_data_o),
      .tx_eof_o    (tx_eof_o),
      .tx_ready_i  (tx_ready_i)
  );

endmodule : tx_arbiter_harness
`default_nettype wire

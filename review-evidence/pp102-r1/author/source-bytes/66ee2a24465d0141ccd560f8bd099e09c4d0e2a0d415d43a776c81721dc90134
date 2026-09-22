/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_tx_slots.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/03 §7 response buffers, §8 TX path)
//
//  Description : TX slot pool between the response builders and the TX
//                arbiter: P-TX-STD-SLOTS (4) standard 576 B response slots
//                (indices 0..3, covering every <= 524-cdl PDU) plus ONE
//                P-TX-OVERSIZE-BYTES (1600 B) full-frame slot (index 4)
//                reserved for the Milan §5.4.1 Δ8 oversize command set
//                (READ_DESCRIPTOR, GET_AVB_INFO, GET_AS_PATH,
//                GET_AUDIO_MAP, ADD/REMOVE_AUDIO_MAPPINGS) — F01.5
//                "P-TX 4x576 + 1600". The oversize slot is granted only to
//                an allocation carrying oversize_i, and an oversize
//                allocation waits for slot 4 even while 0..3 sit free; a
//                plain allocation never receives index 4.
//
//                Slot lifecycle: FREE -> ALLOC (random-access byte writes,
//                headers legal after payloads) -> READY (wr_commit_i +
//                length) -> STREAM (one byte per ser_ready_i cycle to the
//                arbiter) -> FREE again on the cycle the last byte is
//                consumed (auto-free: the TX_QUEUED -> RETIRED arc of
//                03 §4). alloc_gnt_o is a one-cycle pulse the cycle after
//                each sampled request; ser_req_i is sampled while the
//                serializer is idle.
//
//  Decision    : the design decision that matters — the pool is ONE flat
//                3,904-byte sync-read memory (1W + 1R, BRAM-shaped, never
//                flops) with per-slot base offsets, and the serializer
//                gates the read-enable with (!valid || ready) so the BRAM
//                output register itself is the backpressure skid: a
//                dropped ser_ready_i holds the byte, it can never skip.
//                Out-of-slot writes and over-capacity commit lengths are
//                clamped so no builder can corrupt a neighbouring frame.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_tx_slots #(
    //! P-TX-STD-SLOTS (F01.5): standard 576 B response slots
    parameter int unsigned TX_STD_SLOTS_P      = 4,
    //! standard slot capacity in bytes (03 §7: every <= 524-cdl PDU fits)
    parameter int unsigned TX_STD_BYTES_P      = 576,
    //! P-TX-OVERSIZE-BYTES (F01.5): the one full-frame Δ8 slot
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600
) (
    input  wire  clk_i,                          //! core clock (P-CLK-HZ domain)
    input  wire  rst_n,                          //! synchronous active-low reset

    // ---- allocation (response builders / originator) ---------------------
    input  wire                                     alloc_req_i,   //! slot request, sampled every cycle
    input  wire                                     oversize_i,    //! request targets THE oversize slot (Δ8 path)
    output logic                                    alloc_gnt_o,   //! one-cycle grant pulse (cycle after the request)
    output logic [$clog2(TX_STD_SLOTS_P+1)-1:0]     alloc_slot_o,  //! granted index: 0..3 std, 4 oversize

    // ---- random-access byte writes (builders write headers after payloads)
    input  wire  [$clog2(TX_STD_SLOTS_P+1)-1:0]     wr_slot_i,     //! slot being written / committed
    input  wire  [$clog2(TX_OVERSIZE_BYTES_P+1)-1:0] wr_addr_i,    //! byte offset within the slot
    input  wire                                     wr_valid_i,    //! byte-write strobe
    input  wire  [7:0]                              wr_data_i,     //! byte to write
    input  wire                                     wr_commit_i,   //! ALLOC -> READY: mark ready-to-send
    input  wire  [$clog2(TX_OVERSIZE_BYTES_P+1)-1:0] wr_len_i,     //! committed frame length in bytes

    // ---- originator pin/release -------------------------------------------
    input  wire                                     hold_valid_i,  //! keep slot READY after serialization
    input  wire  [$clog2(TX_STD_SLOTS_P+1)-1:0]     hold_slot_i,   //! slot to pin for an exact retry
    input  wire                                     release_valid_i, //! exchange complete, free pinned slot
    input  wire  [$clog2(TX_STD_SLOTS_P+1)-1:0]     release_slot_i, //! pinned slot to release

    // ---- serialize port (TX arbiter) --------------------------------------
    input  wire                                     ser_req_i,     //! start streaming ser_slot_i (sampled when idle)
    input  wire  [$clog2(TX_STD_SLOTS_P+1)-1:0]     ser_slot_i,    //! slot to stream — must be READY
    output logic                                    ser_valid_o,   //! stream byte valid
    output logic [7:0]                              ser_data_o,    //! stream byte, offsets 0..len-1 in order
    output logic                                    ser_last_o,    //! high with the final byte of the frame
    input  wire                                     ser_ready_i,   //! arbiter consumes the byte this cycle

    // ---- status ------------------------------------------------------------
    output logic [TX_STD_SLOTS_P:0]                 slots_ready_o, //! per-slot: committed, not yet serviced
    output logic [$clog2(TX_STD_SLOTS_P+2)-1:0]     slots_free_o   //! number of FREE slots (0..5)
);

  // ------------------------------------------------------------- geometry
  localparam int unsigned N_SLOTS_C     = TX_STD_SLOTS_P + 1;              // 5
  localparam int unsigned OVERSIZE_IX_C = TX_STD_SLOTS_P;                  // 4
  localparam int unsigned MEM_BYTES_C   =
      TX_STD_SLOTS_P * TX_STD_BYTES_P + TX_OVERSIZE_BYTES_P;               // 3,904
  localparam int unsigned SLOT_W_C = $clog2(N_SLOTS_C);                    // 3
  localparam int unsigned LEN_W_C  = $clog2(TX_OVERSIZE_BYTES_P + 1);      // 11
  localparam int unsigned ADDR_W_C = $clog2(MEM_BYTES_C);                  // 12
  localparam int unsigned FREE_W_C = $clog2(N_SLOTS_C + 1);                // 3

  //! slot 4 base = 4 x 576 = 2,304: the oversize base is the uniform product
  function automatic logic [ADDR_W_C-1:0] slot_base_f(
      input logic [SLOT_W_C-1:0] s);
    return ADDR_W_C'(32'(s) * TX_STD_BYTES_P);
  endfunction

  //! per-slot byte capacity — the write/commit clamp line
  function automatic logic [LEN_W_C-1:0] slot_cap_f(
      input logic [SLOT_W_C-1:0] s);
    return (32'(s) == OVERSIZE_IX_C) ? LEN_W_C'(TX_OVERSIZE_BYTES_P)
                                     : LEN_W_C'(TX_STD_BYTES_P);
  endfunction

  // ----------------------------------------------------------- slot state
  typedef enum logic [1:0] {
    SLOT_FREE   = 2'd0,   // allocatable
    SLOT_ALLOC  = 2'd1,   // owned by a builder, accepting writes
    SLOT_READY  = 2'd2,   // committed, unserviced
    SLOT_STREAM = 2'd3    // being serialized to the arbiter
  } slot_st_e;

  // state + committed length, sized to the full index space so a rogue
  // slot index (5..7) reads a hard FREE and can never alias a live slot
  slot_st_e           st_r  [0:(1 << SLOT_W_C) - 1];
  logic [LEN_W_C-1:0] len_r [0:(1 << SLOT_W_C) - 1];
  logic [(1 << SLOT_W_C)-1:0] held_r, release_pend_r;

  logic                alloc_gnt_r;
  logic [SLOT_W_C-1:0] alloc_slot_r;

  // ------------------------------------------------------ serializer regs
  logic                run_r;         // a frame is being streamed
  logic                out_valid_r;   // BRAM output register holds a live byte
  logic                out_last_r;    // ... and it is the final byte
  logic [SLOT_W_C-1:0] cur_slot_r;    // slot being streamed
  logic [LEN_W_C-1:0]  fetch_idx_r;   // next byte offset to fetch

  // ---------------------------------------------------- allocation picker
  logic                pick_ok_w;
  logic [SLOT_W_C-1:0] pick_w;

  always_comb begin : alloc_pick
    pick_ok_w = 1'b0;
    pick_w    = '0;
    if (oversize_i) begin
      // the Δ8 path: only ever slot 4, and it waits for slot 4
      pick_ok_w = (st_r[OVERSIZE_IX_C] == SLOT_FREE);
      pick_w    = SLOT_W_C'(OVERSIZE_IX_C);
    end else begin
      // lowest free standard index; a plain alloc never returns 4
      for (int i = int'(TX_STD_SLOTS_P) - 1; i >= 0; i--) begin
        if (st_r[i] == SLOT_FREE) begin
          pick_ok_w = 1'b1;
          pick_w    = SLOT_W_C'(i);
        end
      end
    end
  end

  // ------------------------------------------------------- event strobes
  logic grant_w, commit_w, ser_start_w, ser_zero_w, consume_w, done_w, rd_en_w;
  logic [LEN_W_C-1:0] cur_len_w;

  assign grant_w     = alloc_req_i && pick_ok_w;
  assign commit_w    = wr_commit_i && (st_r[wr_slot_i] == SLOT_ALLOC);
  assign cur_len_w   = len_r[cur_slot_r];
  assign consume_w   = out_valid_r && ser_ready_i;
  assign done_w      = consume_w && out_last_r;
  assign ser_start_w = !run_r && ser_req_i
                       && (st_r[ser_slot_i] == SLOT_READY)
                       && (len_r[ser_slot_i] != '0)
                       && !(release_valid_i
                            && (release_slot_i == ser_slot_i));
  // a zero-length commit has nothing to stream: freed on service request
  assign ser_zero_w  = !run_r && ser_req_i
                       && (st_r[ser_slot_i] == SLOT_READY)
                       && (len_r[ser_slot_i] == '0)
                       && !(release_valid_i
                            && (release_slot_i == ser_slot_i));
  // the backpressure line: refill the BRAM output register only when it is
  // empty or its byte is being consumed this cycle — stall, never skip
  assign rd_en_w     = run_r && (fetch_idx_r < cur_len_w)
                       && (!out_valid_r || ser_ready_i);

  // ------------------------------------------------- slot lifecycle + len
  // the four writers (grant/commit/start/free) target mutually exclusive
  // states, so one ordered block is conflict-free by construction
  always_ff @(posedge clk_i) begin : slot_state
    if (!rst_n) begin
      for (int i = 0; i < (1 << SLOT_W_C); i++) begin
        st_r[i]  <= SLOT_FREE;
        len_r[i] <= '0;
      end
      alloc_gnt_r  <= 1'b0;
      alloc_slot_r <= '0;
      held_r         <= '0;
      release_pend_r <= '0;
    end else begin
      alloc_gnt_r <= grant_w;
      if (grant_w) begin
        alloc_slot_r <= pick_w;
        st_r[pick_w] <= SLOT_ALLOC;
      end
      if (commit_w) begin
        st_r[wr_slot_i]  <= SLOT_READY;
        len_r[wr_slot_i] <= (wr_len_i > slot_cap_f(wr_slot_i))
                            ? slot_cap_f(wr_slot_i) : wr_len_i;
      end
      if (hold_valid_i && (32'(hold_slot_i) < N_SLOTS_C)) begin
        held_r[hold_slot_i] <= 1'b1;
      end
      if (release_valid_i && (32'(release_slot_i) < N_SLOTS_C)) begin
        held_r[release_slot_i] <= 1'b0;
        if (st_r[release_slot_i] == SLOT_STREAM)
          release_pend_r[release_slot_i] <= 1'b1;
        else if ((st_r[release_slot_i] == SLOT_READY)
                 || (st_r[release_slot_i] == SLOT_ALLOC)) begin
          st_r[release_slot_i] <= SLOT_FREE;
          release_pend_r[release_slot_i] <= 1'b0;
        end
      end
      if (ser_start_w) st_r[ser_slot_i] <= SLOT_STREAM;
      if (ser_zero_w)  st_r[ser_slot_i] <= SLOT_FREE;
      if (done_w) begin
        if (held_r[cur_slot_r] && !release_pend_r[cur_slot_r]
            && !(release_valid_i && (release_slot_i == cur_slot_r)))
          st_r[cur_slot_r] <= SLOT_READY;
        else begin
          st_r[cur_slot_r] <= SLOT_FREE;
          held_r[cur_slot_r] <= 1'b0;
          release_pend_r[cur_slot_r] <= 1'b0;
        end
      end
    end
  end

  // ------------------------------------------------------ serializer FSM
  always_ff @(posedge clk_i) begin : serializer
    if (!rst_n) begin
      run_r       <= 1'b0;
      out_valid_r <= 1'b0;
      out_last_r  <= 1'b0;
      cur_slot_r  <= '0;
      fetch_idx_r <= '0;
    end else begin
      if (ser_start_w) begin
        run_r       <= 1'b1;
        cur_slot_r  <= ser_slot_i;
        fetch_idx_r <= '0;
      end else if (run_r) begin
        if (rd_en_w) begin
          fetch_idx_r <= fetch_idx_r + LEN_W_C'(1);
          out_valid_r <= 1'b1;
          out_last_r  <= (fetch_idx_r == cur_len_w - LEN_W_C'(1));
        end else if (consume_w) begin
          out_valid_r <= 1'b0;
          if (out_last_r) begin
            out_last_r <= 1'b0;
            run_r      <= 1'b0;
          end
        end
      end
    end
  end

  // ----------------------------------------------------------- the store
  // ONE flat sync-read byte memory, 1W + 1R — BRAM-shaped, never flops
  logic [7:0] mem_r [0:MEM_BYTES_C-1];
  logic [7:0] rd_q_r;

  logic                wr_en_w;
  logic [ADDR_W_C-1:0] wr_madr_w;
  logic [ADDR_W_C-1:0] rd_madr_w;

  // writes land only in an ALLOC slot and inside its capacity — a stray
  // builder write can neither clobber a queued frame nor a neighbour slot
  assign wr_en_w   = wr_valid_i && (st_r[wr_slot_i] == SLOT_ALLOC)
                     && (wr_addr_i < slot_cap_f(wr_slot_i));
  assign wr_madr_w = slot_base_f(wr_slot_i) + ADDR_W_C'(wr_addr_i);
  assign rd_madr_w = slot_base_f(cur_slot_r) + ADDR_W_C'(fetch_idx_r);

  always_ff @(posedge clk_i) begin : mem_write
    if (wr_en_w) mem_r[wr_madr_w] <= wr_data_i;
  end

  always_ff @(posedge clk_i) begin : mem_read
    if (rd_en_w) rd_q_r <= mem_r[rd_madr_w];
  end

  // -------------------------------------------------------------- outputs
  assign alloc_gnt_o  = alloc_gnt_r;
  assign alloc_slot_o = alloc_slot_r;
  assign ser_valid_o  = out_valid_r;
  assign ser_data_o   = rd_q_r;
  assign ser_last_o   = out_last_r;

  always_comb begin : status
    slots_free_o = '0;
    for (int i = 0; i < int'(N_SLOTS_C); i++) begin
      slots_ready_o[i] = (st_r[i] == SLOT_READY);
      if (st_r[i] == SLOT_FREE) slots_free_o = slots_free_o + FREE_W_C'(1);
    end
  end

endmodule : KL_pp_tx_slots
`default_nettype wire

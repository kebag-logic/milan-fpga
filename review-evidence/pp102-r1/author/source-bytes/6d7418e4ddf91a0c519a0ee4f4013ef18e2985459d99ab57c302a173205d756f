/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_rx_slots.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/03 §2/§3)
//
//  Description : RX slot pool — the "RX slot RAM" row of F03.1 and the
//                slot-free gate of F03.2 (drop6, counter rx_overrun, rule
//                V8: never fatal, drop + count). `P-RX-SLOTS` slots of
//                `P-RX-SLOT-BYTES` (F01.5: 4 × 576, slot ≥ 536 = max
//                command PDU) hold validated frames as zero-copy payload
//                handles for the three engines. One writer class (the RX
//                validator, 07 §2), one reader side (the engines), and this
//                pool is the LAST drop gate: an alloc request with no free
//                slot is refused and counted in rx_overrun_count_o — the
//                frame dies upstream, no state changes (V8).
//
//                The one design decision that matters: PACKED slot
//                addressing (slot × BYTES_P + offset) into a single 1W1R
//                sync-read byte array — 4 × 576 B = 18,432 bits, exactly
//                one RAMB18 on the reference part. Power-of-two slot
//                padding (4 × 1024 B) would spill into a RAMB36, and an
//                async read would drop the pool into LUTRAM/flops; the
//                read side therefore pays one cycle of latency, always.
//
//                Write protocol (frame-atomic, single validator): alloc is
//                a combinational grant of the lowest-index free slot,
//                refused while a write is in flight (the validator is
//                frame-serial; a refusal with free slots present is NOT an
//                overrun and is not counted). Bytes stream in with
//                wr_valid_i; wr_last_i closes the stream (later bytes are
//                ignored); wr_commit_i latches the accepted-byte count as
//                the slot length and marks the slot occupied; wr_abort_i
//                returns the slot to the pool. Writes beyond BYTES_P are
//                dropped and the length clamps at BYTES_P. free_i returns
//                an occupied slot; freeing a non-occupied slot is a no-op.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_rx_slots #(
    //! P-RX-SLOTS (F01.5) — slots in the pool
    parameter int unsigned SLOTS_P = 4,
    //! P-RX-SLOT-BYTES (F01.5) — bytes per slot, ≥ 536 (max command PDU)
    parameter int unsigned BYTES_P = 576,
    //! derived: slot index width
    localparam int unsigned SLOT_W_C = (SLOTS_P > 1) ? $clog2(SLOTS_P) : 1,
    //! derived: byte address width within a slot
    localparam int unsigned ADDR_W_C = $clog2(BYTES_P),
    //! derived: length width (0..BYTES_P inclusive)
    localparam int unsigned LEN_W_C  = $clog2(BYTES_P + 1),
    //! derived: free-count width (0..SLOTS_P inclusive)
    localparam int unsigned FREE_W_C = $clog2(SLOTS_P + 1)
) (
    input  wire                 clk_i,               //! core clock (P-CLK-HZ domain)
    input  wire                 rst_n,               //! synchronous active-low reset

    //! ---- alloc side (RX validator) ----
    input  wire                 alloc_req_i,         //! request a slot for an incoming frame
    output logic                alloc_gnt_o,         //! combinational grant (same cycle)
    output logic [SLOT_W_C-1:0] alloc_slot_o,        //! granted slot handle (valid with gnt)

    //! ---- byte stream into the granted slot ----
    input  wire                 wr_valid_i,          //! byte strobe
    input  wire           [7:0] wr_data_i,           //! frame byte
    input  wire                 wr_last_i,           //! final byte of the frame (closes the stream)
    input  wire                 wr_abort_i,          //! validator: frame bad mid-write, return the slot
    input  wire                 wr_commit_i,         //! frame good: latch length, mark occupied-complete

    //! ---- read side (the engines) ----
    input  wire  [SLOT_W_C-1:0] rd_slot_i,           //! slot handle to read
    input  wire  [ADDR_W_C-1:0] rd_addr_i,           //! byte address within the slot
    input  wire                 rd_en_i,             //! read enable (sync read)
    output logic          [7:0] rd_data_o,           //! read byte, one cycle after rd_en_i
    output logic  [LEN_W_C-1:0] slot_len_o,          //! committed length of rd_slot_i (valid when occupied)

    //! ---- slot return ----
    input  wire                 free_i,              //! return an occupied slot to the pool
    input  wire  [SLOT_W_C-1:0] free_slot_i,         //! which slot to return

    //! ---- occupancy / status ----
    output logic [FREE_W_C-1:0] slots_free_o,        //! free slots right now
    output logic         [15:0] rx_overrun_count_o   //! alloc requests refused while full (drop6; saturates)
);

  localparam int unsigned MADDR_W_C = $clog2(SLOTS_P * BYTES_P);
  localparam logic [15:0] OVR_MAX_C = 16'hFFFF;

  // ------------------------------------------------------------ slot state
  logic [SLOTS_P-1:0] writing_r;    // allocated, stream in progress
  logic [SLOTS_P-1:0] occupied_r;   // committed, owned by an engine
  logic [SLOTS_P-1:0] free_mask_w;

  logic [SLOT_W_C-1:0] cur_slot_r;  // slot of the in-flight write
  logic                wr_active_r; // a write is in flight
  logic                wr_closed_r; // wr_last_i seen — ignore further bytes
  logic [LEN_W_C-1:0]  wr_ptr_r;    // accepted-byte count of the in-flight write

  logic [LEN_W_C-1:0]  len_r [0:SLOTS_P-1];
  logic [15:0]         ovr_cnt_r;

  assign free_mask_w        = ~(writing_r | occupied_r);
  assign rx_overrun_count_o = ovr_cnt_r;

  // ------------------------------------------------- lowest-free encoder
  logic                ff_valid_w;
  logic [SLOT_W_C-1:0] ff_slot_w;

  always_comb begin : first_free_enc
    ff_valid_w = 1'b0;
    ff_slot_w  = '0;
    for (int unsigned i = 0; i < SLOTS_P; i++) begin
      if (!ff_valid_w && free_mask_w[i]) begin
        ff_valid_w = 1'b1;
        ff_slot_w  = SLOT_W_C'(i);
      end
    end
  end

  assign alloc_gnt_o  = alloc_req_i && ff_valid_w && !wr_active_r;
  assign alloc_slot_o = ff_slot_w;

  always_comb begin : free_count
    slots_free_o = '0;
    for (int unsigned i = 0; i < SLOTS_P; i++) begin
      if (free_mask_w[i]) slots_free_o = slots_free_o + FREE_W_C'(1);
    end
  end

  // ------------------------------------------------------- write datapath
  logic               byte_acc_w;   // this cycle's byte is accepted
  logic [LEN_W_C-1:0] wr_len_now_w; // length as of this cycle (incl. same-cycle byte)

  assign byte_acc_w   = wr_active_r && wr_valid_i && !wr_closed_r
                        && (wr_ptr_r < LEN_W_C'(BYTES_P));
  assign wr_len_now_w = byte_acc_w ? (wr_ptr_r + LEN_W_C'(1)) : wr_ptr_r;

  always_ff @(posedge clk_i) begin : slot_ctrl
    if (!rst_n) begin
      writing_r   <= '0;
      occupied_r  <= '0;
      cur_slot_r  <= '0;
      wr_active_r <= 1'b0;
      wr_closed_r <= 1'b0;
      wr_ptr_r    <= '0;
      ovr_cnt_r   <= '0;
      for (int unsigned i = 0; i < SLOTS_P; i++) len_r[i] <= '0;
    end else begin
      // alloc accept — grant is combinational, state binds on the edge
      if (alloc_gnt_o) begin
        cur_slot_r           <= ff_slot_w;
        writing_r[ff_slot_w] <= 1'b1;
        wr_active_r          <= 1'b1;
        wr_closed_r          <= 1'b0;
        wr_ptr_r             <= '0;
      end

      // the LAST drop gate: refused-while-full is counted, saturating (V8)
      if (alloc_req_i && !ff_valid_w && (ovr_cnt_r != OVR_MAX_C)) begin
        ovr_cnt_r <= ovr_cnt_r + 16'd1;
      end

      // byte accept
      if (byte_acc_w) begin
        wr_ptr_r <= wr_ptr_r + LEN_W_C'(1);
        if (wr_last_i) wr_closed_r <= 1'b1;
      end

      // abort wins over commit if both are asserted (validator error path)
      if (wr_active_r && wr_abort_i) begin
        writing_r[cur_slot_r] <= 1'b0;  // abort returns the slot
        wr_active_r           <= 1'b0;
      end else if (wr_active_r && wr_commit_i) begin
        writing_r[cur_slot_r]  <= 1'b0;
        occupied_r[cur_slot_r] <= 1'b1;
        len_r[cur_slot_r]      <= wr_len_now_w;
        wr_active_r            <= 1'b0;
      end

      // slot return — only an occupied slot; anything else is a no-op
      if (free_i && occupied_r[free_slot_i]) begin
        occupied_r[free_slot_i] <= 1'b0;
      end
    end
  end

  // -------------------------------------------------------- the slot RAM
  // SLOTS_P × BYTES_P bytes, packed (slot × BYTES_P + offset): 18,432 bits
  // at the F01.5 defaults = one RAMB18. 1W1R, sync read. Deliberately NO
  // reset in these two blocks — a reset on the array or the read register
  // breaks BRAM inference (the justified exception to the sync-reset rule).
  logic [7:0] mem_r [0:SLOTS_P*BYTES_P-1];

  logic [MADDR_W_C-1:0] wr_maddr_w;
  logic [MADDR_W_C-1:0] rd_maddr_w;

  assign wr_maddr_w = (MADDR_W_C'(cur_slot_r) * MADDR_W_C'(BYTES_P))
                      + MADDR_W_C'(wr_ptr_r);
  assign rd_maddr_w = (MADDR_W_C'(rd_slot_i) * MADDR_W_C'(BYTES_P))
                      + MADDR_W_C'(rd_addr_i);

  always_ff @(posedge clk_i) begin : slot_mem_wr
    if (byte_acc_w) mem_r[wr_maddr_w] <= wr_data_i;
  end

  always_ff @(posedge clk_i) begin : slot_mem_rd
    if (rd_en_i) rd_data_o <= mem_r[rd_maddr_w];
  end

  // engines read lengths of committed slots only (see header)
  assign slot_len_o = len_r[rd_slot_i];

endmodule

`default_nettype wire

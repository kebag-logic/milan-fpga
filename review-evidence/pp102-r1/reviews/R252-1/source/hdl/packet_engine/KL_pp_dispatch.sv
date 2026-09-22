/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_dispatch.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/03 §2 "per-engine dispatch FIFOs",
//                 03 §5 four producers -> per-engine queues, F03.3
//                 DECODED->DISPATCHED arc)
//
//  Description : Per-engine dispatch queues — four independent FIFOs
//                (ADP / ACMP / AECP / MAAP) of 03 §4 records, fed by the
//                single normalized stream from KL_pp_normalizer (the
//                producer merge and its fixed RX > TIMER > SELF > MGMT
//                priority live there). Routing is by the record's protocol
//                field: ADP -> ADP queue, ACMP -> ACMP queue, MAAP -> MAAP
//                queue, AEM/MVU/AA (and, defensively, any unknown code) ->
//                AECP queue. Each engine pops its queue over a valid/ready
//                port; the presented head record holds bit-stable through
//                a stall. The MAAP queue is SHALLOWER by default (2 + the
//                head): Annex B traffic is a handful of frames per claim
//                walk and its engine drains a record in tens of cycles, so
//                depth buys nothing but distributed RAM.
//
//                Full policy: producers STALL, never drop — F03.3 has no
//                drop arc after the RX-slot gate (F03.2 drop6 is the LAST
//                drop gate) and 03 §6 (e) forbids silent drops, so a full
//                queue deasserts enq_ready_o and the record waits upstream
//                (03 §4 pool sizing bounds in-flight work by P-RX-SLOTS +
//                queue depths). The per-queue "overflow" counters are
//                therefore STALL-CYCLE counters (16-bit, saturating): one
//                count per cycle a record is presented against a full
//                queue. Nothing is ever lost; the counters are the
//                trace-visible evidence of backpressure.
//
//                The one design decision that matters: each queue is a
//                sync-read RAM FIFO (1W1R, no reset on array or read
//                register, BRAM/LUTRAM-inferable) whose output register IS
//                the head-of-queue skid — refilled only when empty or
//                popped, exactly the KL_pp_tx_slots backpressure trick —
//                never a flop file behind a wide read mux (the +894-LUT
//                failure mode). Observable capacity per queue is DEPTH + 1
//                (RAM + the presented head).
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_dispatch
  import pp_pkg::*;
#(
    //! ADP queue depth (RAM entries; +1 presented head)
    parameter int unsigned ADP_DEPTH_P  = 4,
    //! ACMP queue depth (RAM entries; +1 presented head)
    parameter int unsigned ACMP_DEPTH_P = 4,
    //! AECP queue depth (RAM entries; +1 presented head)
    parameter int unsigned AECP_DEPTH_P = 4,
    //! MAAP queue depth (RAM entries; +1 presented head)
    parameter int unsigned MAAP_DEPTH_P = 2
) (
    input  wire                    clk_i,             //! core clock (P-CLK-HZ domain)
    input  wire                    rst_n,             //! synchronous active-low reset

    //! ---- enqueue side (from KL_pp_normalizer) ----
    input  wire                    enq_valid_i,       //! record presented (held through a stall)
    input  wire  [PP_TXN_W_C-1:0]  enq_txn_i,         //! the 03 §4 record
    output logic                   enq_ready_o,       //! target queue accepts this cycle

    //! ---- ADP engine pop port ----
    output logic                   adp_txn_valid_o,   //! head record valid
    output logic [PP_TXN_W_C-1:0]  adp_txn_o,         //! head record (stable through a stall)
    input  wire                    adp_txn_ready_i,   //! engine consumes the head this cycle

    //! ---- ACMP engine pop port ----
    output logic                   acmp_txn_valid_o,  //! head record valid
    output logic [PP_TXN_W_C-1:0]  acmp_txn_o,        //! head record (stable through a stall)
    input  wire                    acmp_txn_ready_i,  //! engine consumes the head this cycle

    //! ---- AECP engine pop port ----
    output logic                   aecp_txn_valid_o,  //! head record valid
    output logic [PP_TXN_W_C-1:0]  aecp_txn_o,        //! head record (stable through a stall)
    input  wire                    aecp_txn_ready_i,  //! engine consumes the head this cycle

    //! ---- MAAP engine pop port ----
    output logic                   maap_txn_valid_o,  //! head record valid
    output logic [PP_TXN_W_C-1:0]  maap_txn_o,        //! head record (stable through a stall)
    input  wire                    maap_txn_ready_i,  //! engine consumes the head this cycle

    //! ---- observability ----
    output logic [7:0]             adp_level_o,       //! ADP records in flight (RAM + head)
    output logic [7:0]             acmp_level_o,      //! ACMP records in flight (RAM + head)
    output logic [7:0]             aecp_level_o,      //! AECP records in flight (RAM + head)
    output logic [7:0]             maap_level_o,      //! MAAP records in flight (RAM + head)
    output logic [15:0]            adp_stall_count_o, //! cycles a record stalled on full ADP (saturates)
    output logic [15:0]            acmp_stall_count_o,//! cycles a record stalled on full ACMP (saturates)
    output logic [15:0]            aecp_stall_count_o,//! cycles a record stalled on full AECP (saturates)
    output logic [15:0]            maap_stall_count_o //! cycles a record stalled on full MAAP (saturates)
);

  localparam logic [15:0] STALL_MAX_C = 16'hFFFF;

  // ------------------------------------------------------------- routing
  pp_txn_t enq_txn_w;
  logic    sel_adp_w, sel_acmp_w, sel_maap_w, sel_aecp_w;

  assign enq_txn_w  = pp_txn_t'(enq_txn_i);
  assign sel_adp_w  = (enq_txn_w.protocol == PP_PROTO_ADP);
  assign sel_acmp_w = (enq_txn_w.protocol == PP_PROTO_ACMP);
  assign sel_maap_w = (enq_txn_w.protocol == PP_PROTO_MAAP);
  assign sel_aecp_w = !sel_adp_w && !sel_acmp_w
                    && !sel_maap_w;               // AEM / MVU / AA + unknown

  logic adp_full_w, acmp_full_w, aecp_full_w, maap_full_w;

  assign enq_ready_o = (sel_adp_w  && !adp_full_w)
                     || (sel_acmp_w && !acmp_full_w)
                     || (sel_maap_w && !maap_full_w)
                     || (sel_aecp_w && !aecp_full_w);

  // ------------------------------------------------------- the three FIFOs
  KL_pp_dispatch_fifo #(
      .DEPTH_P (ADP_DEPTH_P)
  ) u_adp_q (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .push_i      (enq_valid_i && sel_adp_w),
      .wdata_i     (enq_txn_i),
      .full_o      (adp_full_w),
      .pop_valid_o (adp_txn_valid_o),
      .pop_data_o  (adp_txn_o),
      .pop_ready_i (adp_txn_ready_i),
      .level_o     (adp_level_o)
  );

  KL_pp_dispatch_fifo #(
      .DEPTH_P (ACMP_DEPTH_P)
  ) u_acmp_q (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .push_i      (enq_valid_i && sel_acmp_w),
      .wdata_i     (enq_txn_i),
      .full_o      (acmp_full_w),
      .pop_valid_o (acmp_txn_valid_o),
      .pop_data_o  (acmp_txn_o),
      .pop_ready_i (acmp_txn_ready_i),
      .level_o     (acmp_level_o)
  );

  KL_pp_dispatch_fifo #(
      .DEPTH_P (AECP_DEPTH_P)
  ) u_aecp_q (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .push_i      (enq_valid_i && sel_aecp_w),
      .wdata_i     (enq_txn_i),
      .full_o      (aecp_full_w),
      .pop_valid_o (aecp_txn_valid_o),
      .pop_data_o  (aecp_txn_o),
      .pop_ready_i (aecp_txn_ready_i),
      .level_o     (aecp_level_o)
  );

  KL_pp_dispatch_fifo #(
      .DEPTH_P (MAAP_DEPTH_P)
  ) u_maap_q (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .push_i      (enq_valid_i && sel_maap_w),
      .wdata_i     (enq_txn_i),
      .full_o      (maap_full_w),
      .pop_valid_o (maap_txn_valid_o),
      .pop_data_o  (maap_txn_o),
      .pop_ready_i (maap_txn_ready_i),
      .level_o     (maap_level_o)
  );

  // ------------------------------------------- stall-cycle counters (V8-
  // style trace evidence: a stall is counted, a record is never dropped)
  logic [15:0] adp_stall_r, acmp_stall_r, aecp_stall_r, maap_stall_r;

  always_ff @(posedge clk_i) begin : stall_counters
    if (!rst_n) begin
      adp_stall_r  <= '0;
      acmp_stall_r <= '0;
      aecp_stall_r <= '0;
      maap_stall_r <= '0;
    end else begin
      if (enq_valid_i && sel_adp_w && adp_full_w
          && (adp_stall_r != STALL_MAX_C)) begin
        adp_stall_r <= adp_stall_r + 16'd1;
      end
      if (enq_valid_i && sel_acmp_w && acmp_full_w
          && (acmp_stall_r != STALL_MAX_C)) begin
        acmp_stall_r <= acmp_stall_r + 16'd1;
      end
      if (enq_valid_i && sel_aecp_w && aecp_full_w
          && (aecp_stall_r != STALL_MAX_C)) begin
        aecp_stall_r <= aecp_stall_r + 16'd1;
      end
      if (enq_valid_i && sel_maap_w && maap_full_w
          && (maap_stall_r != STALL_MAX_C)) begin
        maap_stall_r <= maap_stall_r + 16'd1;
      end
    end
  end

  assign adp_stall_count_o  = adp_stall_r;
  assign acmp_stall_count_o = acmp_stall_r;
  assign aecp_stall_count_o = aecp_stall_r;
  assign maap_stall_count_o = maap_stall_r;

endmodule : KL_pp_dispatch

//---------------------------------------------------------------------------//
//  KL_pp_dispatch_fifo — one dispatch queue (same file: it exists only as
//  the plural of KL_pp_dispatch and is not a public block of F03.1).
//  Sync-read RAM FIFO, 1W1R: cnt_r counts RAM entries; the output register
//  is the presented head, refilled only when it is empty or being consumed
//  (stall, never skip — the KL_pp_tx_slots trick). push into a full RAM is
//  refused here (full_o) and counted upstream. rd never collides with wr:
//  rd requires cnt_r != 0 and push requires !full_o, so the pointers can
//  only be equal when the RAM is empty or full — never both active on one
//  address.
//---------------------------------------------------------------------------//
module KL_pp_dispatch_fifo
  import pp_pkg::*;
#(
    //! RAM entries (observable capacity = DEPTH_P + 1 with the head)
    parameter int unsigned DEPTH_P = 4,
    //! derived: pointer width
    localparam int unsigned PTR_W_C = (DEPTH_P > 1) ? $clog2(DEPTH_P) : 1,
    //! derived: RAM occupancy width (0..DEPTH_P inclusive)
    localparam int unsigned CNT_W_C = $clog2(DEPTH_P + 1)
) (
    input  wire                    clk_i,        //! core clock
    input  wire                    rst_n,        //! synchronous active-low reset

    input  wire                    push_i,       //! enqueue request (ignored while full)
    input  wire  [PP_TXN_W_C-1:0]  wdata_i,      //! the 03 §4 record
    output logic                   full_o,       //! RAM full — upstream must stall

    output logic                   pop_valid_o,  //! head record valid
    output logic [PP_TXN_W_C-1:0]  pop_data_o,   //! head record (stable through a stall)
    input  wire                    pop_ready_i,  //! consume the head this cycle

    output logic [7:0]             level_o       //! records in flight (RAM + head)
);

  logic [PTR_W_C-1:0] wr_ptr_r, rd_ptr_r;
  logic [CNT_W_C-1:0] cnt_r;        // entries in the RAM (head excluded)
  logic               out_valid_r;  // the head register holds a live record

  logic push_w, rd_en_w;

  assign full_o = (cnt_r == CNT_W_C'(DEPTH_P));
  assign push_w = push_i && !full_o;
  // refill the head only when it is empty or its record is consumed now
  assign rd_en_w = (cnt_r != '0) && (!out_valid_r || pop_ready_i);

  always_ff @(posedge clk_i) begin : fifo_ctrl
    if (!rst_n) begin
      wr_ptr_r    <= '0;
      rd_ptr_r    <= '0;
      cnt_r       <= '0;
      out_valid_r <= 1'b0;
    end else begin
      if (push_w) begin
        wr_ptr_r <= (wr_ptr_r == PTR_W_C'(DEPTH_P - 1)) ? '0
                    : wr_ptr_r + PTR_W_C'(1);
      end
      if (rd_en_w) begin
        rd_ptr_r    <= (rd_ptr_r == PTR_W_C'(DEPTH_P - 1)) ? '0
                       : rd_ptr_r + PTR_W_C'(1);
        out_valid_r <= 1'b1;
      end else if (out_valid_r && pop_ready_i) begin
        out_valid_r <= 1'b0;
      end
      case ({push_w, rd_en_w})
        2'b10:   cnt_r <= cnt_r + CNT_W_C'(1);
        2'b01:   cnt_r <= cnt_r - CNT_W_C'(1);
        default: ;  // 00 or 11: occupancy unchanged
      endcase
    end
  end

  // ----------------------------------------------------------- the queue RAM
  // sync read, 1W1R; deliberately NO reset on the array or the read
  // register — a reset here breaks RAM inference (the justified exception
  // to the sync-reset rule, same as KL_pp_rx_slots / KL_pp_tx_slots).
  //
  // DISTRIBUTED, NOT BLOCK. This array is WIDE and SHALLOW — DEPTH_P (4) x
  // PP_TXN_W_C (393) = 1,572 bits, and it is the WIDTH that decides the
  // mapping: a synthesiser handed a 393-bit port bands enough block-RAM tiles
  // side by side to reach it and leaves 99 % of each tile empty. Measured on
  // the reference part (xc7a100t, Vivado 2026.1, post-synthesis
  // out-of-context, 1-stream shape) the three queues of KL_pp_dispatch took
  // 14 RAMB36 + 3 RAMB18 between them — 42 % of this processor's whole
  // block-RAM budget for 4,716 bits of data, on a die that had none left. The
  // hint costs LUTs, which this design has, and returns the tiles, which it
  // does not. It is a synthesis attribute, not a primitive: a tool that does
  // not know it ignores it (hdl/README rule 1), and KL_aecp_ucpu's operand
  // file already carries the same one.
  (* ram_style = "distributed" *)
  logic [PP_TXN_W_C-1:0] mem_r [0:DEPTH_P-1];
  logic [PP_TXN_W_C-1:0] out_data_r;

  always_ff @(posedge clk_i) begin : fifo_mem_wr
    if (push_w) mem_r[wr_ptr_r] <= wdata_i;
  end

  always_ff @(posedge clk_i) begin : fifo_mem_rd
    if (rd_en_w) out_data_r <= mem_r[rd_ptr_r];
  end

  assign pop_valid_o = out_valid_r;
  assign pop_data_o  = out_data_r;
  assign level_o     = 8'(cnt_r) + {7'h0, out_valid_r};

endmodule : KL_pp_dispatch_fifo
`default_nettype wire

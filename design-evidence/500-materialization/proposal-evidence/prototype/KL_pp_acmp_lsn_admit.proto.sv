/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_acmp_lsn_admit.proto.sv   (PROTOTYPE, design evidence)
//  Project     : milan-fpga #500, saved-state scope D3, seam S4
//                (docs/design/SAVED_STATE_MATERIALIZATION.md section 5.1)
//
//  Description : BOOT-OWNED LISTENER ADMISSION, in front of the UNCHANGED
//                pinned KL_pp_acmp_listener. The listener serves one work
//                item at a time and ranks a START/STOP holder, a dispatch
//                transaction, a pending timer expiry and a talker event above
//                the binding restore's preload: pre_ready_o is low while any
//                of them is present. Any of them can therefore hold the
//                binding walk's preload phase for as long as it keeps coming.
//                Every walk it runs also ends in a record write-back that the
//                binding manager takes as a live change, so during the
//                restore even a read-only GET_RX_STATE withdraws a sink's
//                restored binding and flushes the unbound record.
//
//                This gate owns the listener's four work faces from the HARD
//                reset to the binding walk's DRAINED terminal and admits
//                nothing but the preload meanwhile:
//                - a transaction, a talker event and a START/STOP request are
//                  HELD at their producers. Valid is masked towards the
//                  listener and ready towards the producer, so nothing is
//                  consumed that the listener did not see. The START/STOP
//                  face's ready is a completion that cannot fire without a
//                  captured request, so only its valid needs the mask.
//                - an expiry is not admitted. The listener arms its timers
//                  only in the walks this gate holds off and the timer
//                  service's armed bits reset to 0, so no expiry of a
//                  listener owner can be legitimate while the gate owns the
//                  faces; each one that arrives is counted, never queued.
//                With nothing else admitted, the listener's reachable states
//                from reset are X_INIT, X_IDLE and X_PRELOAD, so pre_ready_o
//                is 1 in every X_IDLE cycle and a preload is taken in the
//                cycle it is presented.
//
//                RELEASE is one-way until the next hard reset. It needs the
//                binding manager's walk at its terminal (done, failed or not)
//                with no preload presented, the listener idle and its last
//                preload's discovery-arm strobe gone. The binding manager
//                never walks again before a reset, so nothing needs the gate
//                afterwards. released_o is the binding walk's drained
//                terminal: the D3 walk starts on it, and the restore done
//                that releases the entity enable takes it.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_acmp_lsn_admit #(
    //! P-N-STREAM-IN: the listener's sinks, its timer owner range
    parameter int unsigned N_SINKS_P        = 8,
    //! the listener's TMR_OWNER_BASE_P: its owners are BASE .. BASE+N-1
    parameter int unsigned TMR_OWNER_BASE_P = 32,
    //! the timer service's owner tag width (pp_pkg PP_TIMER_OWNER_W_C)
    parameter int unsigned OWNER_W_P        = 8
) (
    input  wire                 clk_i,
    input  wire                 rst_n,           //! the HARD reset only

    //! ---- release: the binding walk's drained terminal --------------------
    input  wire                 walk_done_i,     //! KL_acmp_nvm_shadow restore_done_o
    input  wire                 pre_valid_i,     //! its preload request
    input  wire                 lsn_busy_i,      //! the listener is not in X_IDLE
    input  wire                 lsn_arm_i,       //! the listener's A4 discovery-arm strobe
    output logic                own_o,           //! the gate owns the listener's faces
    output logic                released_o,      //! the binding walk's drained terminal

    //! ---- the dispatch transaction face ------------------------------------
    input  wire                 p_txn_valid_i,   //! the producer's head
    output logic                p_txn_ready_o,   //! the producer's pop
    output logic                l_txn_valid_o,   //! to the listener's txn_valid_i
    input  wire                 l_txn_ready_i,   //! the listener's txn_ready_o

    //! ---- the talker event face (the event router) ---------------------------
    input  wire                 p_tk_valid_i,
    output logic                p_tk_ready_o,
    output logic                l_tk_valid_o,
    input  wire                 l_tk_ready_i,

    //! ---- the START/STOP face (the AECP engine holds its request) ------------
    input  wire                 p_strm_valid_i,
    output logic                l_strm_valid_o,

    //! ---- the timer expiry bus ------------------------------------------------
    input  wire                 p_exp_valid_i,
    input  wire [OWNER_W_P-1:0] p_exp_owner_i,
    output logic                l_exp_valid_o,

    //! expiries of a listener owner that arrived while the gate owned the
    //! faces (saturating): only an arm the listener never issued makes one
    output logic [15:0]         dbg_exp_drop_o
);

  logic        own_r;
  logic        drained_w;
  logic        lsn_exp_w;
  logic [15:0] drop_r;

  assign drained_w = walk_done_i && !pre_valid_i && !lsn_busy_i && !lsn_arm_i;

  always_ff @(posedge clk_i) begin : own_ff
    if (!rst_n) begin
      own_r <= 1'b1;
    end else if (drained_w) begin
      own_r <= 1'b0;
    end
  end

  assign own_o      = own_r;
  assign released_o = !own_r;

  //! held at the producer: masked both ways
  assign l_txn_valid_o  = p_txn_valid_i  && !own_r;
  assign p_txn_ready_o  = l_txn_ready_i  && !own_r;
  assign l_tk_valid_o   = p_tk_valid_i   && !own_r;
  assign p_tk_ready_o   = l_tk_ready_i   && !own_r;
  assign l_strm_valid_o = p_strm_valid_i && !own_r;

  //! the expiry bus reaches the listener only once it is released
  assign l_exp_valid_o = p_exp_valid_i && !own_r;
  assign lsn_exp_w     = p_exp_valid_i
                         && (32'(p_exp_owner_i) >= TMR_OWNER_BASE_P)
                         && (32'(p_exp_owner_i) <  TMR_OWNER_BASE_P + N_SINKS_P);

  always_ff @(posedge clk_i) begin : drop_ff
    if (!rst_n) begin
      drop_r <= 16'd0;
    end else if (own_r && lsn_exp_w && (drop_r != 16'hFFFF)) begin
      drop_r <= drop_r + 16'd1;
    end
  end

  assign dbg_exp_drop_o = drop_r;

endmodule

`default_nettype wire

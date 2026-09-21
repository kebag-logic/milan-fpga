/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_nvm_mgr_arb.proto.sv   (PROTOTYPE, design evidence)
//  Project     : milan-fpga #500, saved-state scope D3
//                (docs/design/SAVED_STATE_MATERIALIZATION.md section 5)
//
//  Description : Two record managers, ONE port. KL_pp_nvm_port has one
//                manager face and serves one operation at a time; this block
//                puts the binding manager (KL_acmp_nvm_shadow, manager 0)
//                and the D3 record writer (manager 1) in front of it, so the
//                device face keeps exactly ONE sequential initiator (the
//                port) and the backend sees nothing new.
//
//                OWNERSHIP IS PER OPERATION. The manager whose request the
//                port accepted owns every data phase and the done or err
//                pulse that ends it; the other manager sees none of them.
//
//                THE ONE RULE THAT MATTERS. Manager 0 raises a one-cycle
//                REGISTERED request after it reads the port idle (its own
//                contract), so the request lands one cycle after the sample.
//                The busy it reads must therefore cover every cycle in which
//                a request landing next cycle could not be issued: while
//                manager 1 owns the port AND in the cycle manager 1 is
//                granted. With that, a manager-0 request only ever meets an
//                idle port and is issued at once; nothing is held here. The
//                grant-cycle term is load-bearing: without it a request that
//                lands on manager 1's grant cycle is lost and the binding
//                manager waits for its data phase for ever (mutant A01,
//                case K15). Manager 1 holds its request until m1_gnt_o. On a
//                tie at an idle port manager 0 wins.
//
//                AN ABANDONED READ IS DRAINED, NEVER HANDED ON (page section
//                8.8). The port answers untagged: its bytes and its done or
//                err name no operation. So when manager 1 abandons a READ the
//                port is serving (m1_abort_i, the restore watchdog), this
//                block keeps that operation as its OWN: it holds rready so the
//                port can move every late byte, discards the bytes, swallows
//                the done or err that ends it, and keeps both managers off the
//                port until then. A late response can therefore only ever end
//                the operation it belongs to. A device that never answers
//                keeps the port drained for ever: every later change reads
//                pending, never durable, and processor issue 15 is what would
//                bound it. Only reads are abandoned; a write stream is never
//                cut here.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_nvm_mgr_arb (
    input  wire        clk_i,
    input  wire        rst_n,
    //! ---- manager 0: the binding manager (one-cycle request) ----
    input  wire        m0_req_i,
    input  wire        m0_we_i,
    input  wire [7:0]  m0_rid_i,
    input  wire        m0_wvalid_i,
    input  wire [7:0]  m0_wdata_i,
    input  wire        m0_rready_i,
    output logic       m0_wready_o,
    output logic       m0_rvalid_o,
    output logic [7:0] m0_rdata_o,
    output logic       m0_busy_o,
    output logic       m0_done_o,
    output logic       m0_err_o,
    //! ---- manager 1: the D3 record writer (request held until granted) ----
    input  wire        m1_req_i,
    input  wire        m1_we_i,
    input  wire [7:0]  m1_rid_i,
    input  wire        m1_wvalid_i,
    input  wire [7:0]  m1_wdata_i,
    input  wire        m1_rready_i,
    output logic       m1_gnt_o,
    output logic       m1_wready_o,
    output logic       m1_rvalid_o,
    output logic [7:0] m1_rdata_o,
    output logic       m1_done_o,
    output logic       m1_err_o,
    //! manager 1 abandons the READ it was granted: drain it
    input  wire        m1_abort_i,
    //! ---- the port's manager face ----
    output logic       p_req_o,
    output logic       p_we_o,
    output logic [7:0] p_rid_o,
    output logic       p_wvalid_o,
    output logic [7:0] p_wdata_o,
    output logic       p_rready_o,
    input  wire        p_wready_i,
    input  wire        p_rvalid_i,
    input  wire [7:0]  p_rdata_i,
    input  wire        p_busy_i,
    input  wire        p_done_i,
    input  wire        p_err_i
);

  typedef enum logic [1:0] { O_NONE, O_M0, O_M1 } own_e;
  own_e       own_r;
  logic       idle_w, iss0_w, iss1_w, end_w;
  //! manager 1's operation, abandoned and being drained
  logic       drain_r;

  //! the port can take a request only in S_IDLE, which follows its done or
  //! err pulse by one cycle; ownership retires on that pulse
  assign idle_w  = (own_r == O_NONE) && !p_busy_i && !p_done_i && !p_err_i;
  assign iss0_w  = idle_w && m0_req_i;
  assign iss1_w  = idle_w && !m0_req_i && m1_req_i;
  assign end_w   = (own_r != O_NONE) && (p_done_i || p_err_i);

  always_ff @(posedge clk_i) begin
    if (!rst_n)      own_r <= O_NONE;
    else if (iss0_w) own_r <= O_M0;
    else if (iss1_w) own_r <= O_M1;
    else if (end_w)  own_r <= O_NONE;
  end

  //! the drain starts on the abort of a manager-1 operation still open and
  //! ends with that operation's own done or err, never on time
  always_ff @(posedge clk_i) begin
    if (!rst_n)                                  drain_r <= 1'b0;
    else if (end_w)                              drain_r <= 1'b0;
    else if (m1_abort_i && (own_r == O_M1))      drain_r <= 1'b1;
  end

  assign p_req_o    = iss0_w || iss1_w;
  assign p_we_o     = iss0_w ? m0_we_i : m1_we_i;
  assign p_rid_o    = iss0_w ? m0_rid_i : m1_rid_i;
  assign p_wvalid_o = (own_r == O_M0) ? m0_wvalid_i : (own_r == O_M1) ? m1_wvalid_i : 1'b0;
  assign p_wdata_o  = (own_r == O_M1) ? m1_wdata_i : m0_wdata_i;
  assign p_rready_o = (own_r == O_M0) ? m0_rready_i
                    : (own_r == O_M1) ? (drain_r || m1_rready_i) : 1'b0;

  assign m0_wready_o = (own_r == O_M0) && p_wready_i;
  assign m0_rvalid_o = (own_r == O_M0) && p_rvalid_i;
  assign m0_rdata_o  = p_rdata_i;
  //! manager 0 strobes only when it reads idle; any other owner reads busy,
  //! and so does the cycle manager 1 is granted (the banner's one rule)
  assign m0_busy_o   = p_busy_i || (own_r == O_M1) || iss1_w;
  assign m0_done_o   = (own_r == O_M0) && p_done_i;
  assign m0_err_o    = (own_r == O_M0) && p_err_i;

  //! a drained operation's bytes and ending reach no manager
  assign m1_gnt_o    = iss1_w;
  assign m1_wready_o = (own_r == O_M1) && !drain_r && p_wready_i;
  assign m1_rvalid_o = (own_r == O_M1) && !drain_r && p_rvalid_i;
  assign m1_rdata_o  = p_rdata_i;
  assign m1_done_o   = (own_r == O_M1) && !drain_r && p_done_i;
  assign m1_err_o    = (own_r == O_M1) && !drain_r && p_err_i;

endmodule

`default_nettype wire

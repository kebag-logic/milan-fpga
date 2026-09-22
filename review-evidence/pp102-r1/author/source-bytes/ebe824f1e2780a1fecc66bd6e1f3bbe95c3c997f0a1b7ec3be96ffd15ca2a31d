/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_pp_side_port.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/02 §7
//                class E "mgmt", 07 §5.5 side-port address map, 07 §2
//                access-rights rule)
//
//  Description : Management side-port — the class-E single-master port of
//                F02.7 (psel/pwrite/paddr/pwdata/prdata/pready mapped 1:1
//                onto req_valid/we/addr/wdata/rdata/rvalid; wait states
//                allowed) decoding the six 07 §5.5 windows of the 20-bit
//                word-address space:
//
//                  0x00000  image + identity load   W pre-enable only, R
//                  0x10000  overlay/name debug view RO
//                  0x20000  registry + counters snapshot RO
//                  0x30000..0x300FF control/status  RW
//                  0x40000  trace ring (P-TRACE-RING backing) RO
//                  0x50000  firmware mailbox RW — only if P-EN-FIRMWARE-ASSIST
//
//                Refused accesses — a write to an RO window, an image-load
//                write after entity_enable (07 §2: "read-only everywhere
//                after entity_enable except the control window"), or any
//                unmapped address (0x30100..0x3FFFF, window 5 when the
//                parameter is off, windows 6..15) — answer rvalid_o+err_o
//                one cycle later and are NEVER forwarded. The enforcement
//                lives here, not with the host.
//
//                The one design decision that matters: this is a thin
//                ADDRESS MUX in front of six per-window backend master
//                ports — it owns no storage and no shadow registers, never
//                a second register file over existing state (the
//                +385-slice failure mode). Backend rdata/rvalid pass
//                through combinationally; the only flops are the 2-bit
//                response FSM and the 3-bit window select.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_pp_side_port #(
    //! P-EN-FIRMWARE-ASSIST (F01.5 default 0) — window 0x50000 exists only when set
    parameter bit EN_FW_ASSIST_P = 1'b0
) (
    input  wire         clk_i,            //! core or mgmt-bridged clock (02 §2 rule 3)
    input  wire         rst_n,            //! synchronous active-low reset

    //! ---- access gate (07 §2 access-rights rule) ----
    input  wire         entity_enable_i,  //! 1 = image window is write-locked

    //! ---- host request/response (class E, F02.7 mapped 1:1) ----
    input  wire         req_valid_i,      //! psel: request present (hold until rvalid_o)
    input  wire         we_i,             //! pwrite: 1 = write
    input  wire  [19:0] addr_i,           //! paddr: 20-bit WORD address
    input  wire  [31:0] wdata_i,          //! pwdata
    output logic [31:0] rdata_o,          //! prdata (0 on error responses)
    output logic        rvalid_o,         //! pready: completion strobe, exactly one per request
    output logic        err_o,            //! with rvalid_o: access refused, nothing forwarded

    //! ---- window 0x00000: image + identity load (W pre-enable, R) ----
    output logic        img_req_o,        //! forwarded request pulse (one cycle)
    output logic        img_we_o,         //! write strobe (only while !entity_enable_i)
    output logic [15:0] img_addr_o,       //! window word offset (valid with req)
    output logic [31:0] img_wdata_o,      //! write data (valid with req)
    input  wire  [31:0] img_rdata_i,      //! backend read data (valid with rvalid)
    input  wire         img_rvalid_i,     //! backend completion (read data / write ack)

    //! ---- window 0x10000: dynamic-overlay + name debug view (RO) ----
    output logic        dbg_req_o,        //! forwarded read pulse
    output logic [15:0] dbg_addr_o,       //! window word offset
    input  wire  [31:0] dbg_rdata_i,      //! backend read data
    input  wire         dbg_rvalid_i,     //! backend completion

    //! ---- window 0x20000: registry + counters snapshot (RO) ----
    output logic        snap_req_o,       //! forwarded read pulse
    output logic [15:0] snap_addr_o,      //! window word offset
    input  wire  [31:0] snap_rdata_i,     //! backend read data
    input  wire         snap_rvalid_i,    //! backend completion

    //! ---- window 0x30000..0x300FF: control/status (RW) ----
    output logic        ctrl_req_o,       //! forwarded request pulse
    output logic        ctrl_we_o,        //! write strobe
    output logic  [7:0] ctrl_addr_o,      //! window word offset (256-word window)
    output logic [31:0] ctrl_wdata_o,     //! write data
    input  wire  [31:0] ctrl_rdata_i,     //! backend read data
    input  wire         ctrl_rvalid_i,    //! backend completion

    //! ---- window 0x40000: trace ring, P-TRACE-RING backing (RO) ----
    output logic        trace_req_o,      //! forwarded read pulse
    output logic [15:0] trace_addr_o,     //! window word offset
    input  wire  [31:0] trace_rdata_i,    //! backend read data
    input  wire         trace_rvalid_i,   //! backend completion

    //! ---- window 0x50000: firmware mailbox (RW, P-EN-FIRMWARE-ASSIST) ----
    output logic        fw_req_o,         //! forwarded request pulse
    output logic        fw_we_o,          //! write strobe
    output logic [15:0] fw_addr_o,        //! window word offset
    output logic [31:0] fw_wdata_o,       //! write data
    input  wire  [31:0] fw_rdata_i,       //! backend read data
    input  wire         fw_rvalid_i       //! backend completion
);

  // ---------------------------------- window indices (addr_i[19:16], 07 §5.5)
  localparam logic [3:0] WIN_IMG_C   = 4'h0;
  localparam logic [3:0] WIN_DBG_C   = 4'h1;
  localparam logic [3:0] WIN_SNAP_C  = 4'h2;
  localparam logic [3:0] WIN_CTRL_C  = 4'h3;
  localparam logic [3:0] WIN_TRACE_C = 4'h4;
  localparam logic [3:0] WIN_FW_C    = 4'h5;

  typedef enum logic [1:0] {
    SP_IDLE = 2'd0,   // no request in flight
    SP_WAIT = 2'd1,   // forwarded; passing the backend response through
    SP_ERR  = 2'd2    // refused; single-cycle error response
  } sp_state_e;

  sp_state_e   state_r;
  logic  [2:0] sel_r;         // window of the in-flight forward

  logic  [3:0] win_w;
  logic        fwd_ok_w;      // decode verdict: forward vs refuse
  logic        accept_w;
  logic        sel_rvalid_w;
  logic [31:0] sel_rdata_w;

  assign win_w    = addr_i[19:16];
  assign accept_w = req_valid_i && (state_r == SP_IDLE);

  // --------------------------------------------- window decode (07 §5.5 map)
  always_comb begin : win_decode
    case (win_w)
      WIN_IMG_C:   fwd_ok_w = we_i ? !entity_enable_i : 1'b1;  // W pre-enable, R
      WIN_DBG_C:   fwd_ok_w = !we_i;                           // RO
      WIN_SNAP_C:  fwd_ok_w = !we_i;                           // RO
      WIN_CTRL_C:  fwd_ok_w = (addr_i[15:8] == 8'h00);         // RW, 0x300FF top
      WIN_TRACE_C: fwd_ok_w = !we_i;                           // RO
      WIN_FW_C:    fwd_ok_w = (EN_FW_ASSIST_P != 1'b0);        // RW when fitted
      default:     fwd_ok_w = 1'b0;                            // unmapped
    endcase
  end

  // ------------------------------------- forward pulses (the thin address mux)
  assign img_req_o   = accept_w && fwd_ok_w && (win_w == WIN_IMG_C);
  assign img_we_o    = img_req_o && we_i;
  assign img_addr_o  = addr_i[15:0];
  assign img_wdata_o = wdata_i;

  assign dbg_req_o   = accept_w && fwd_ok_w && (win_w == WIN_DBG_C);
  assign dbg_addr_o  = addr_i[15:0];

  assign snap_req_o  = accept_w && fwd_ok_w && (win_w == WIN_SNAP_C);
  assign snap_addr_o = addr_i[15:0];

  assign ctrl_req_o   = accept_w && fwd_ok_w && (win_w == WIN_CTRL_C);
  assign ctrl_we_o    = ctrl_req_o && we_i;
  assign ctrl_addr_o  = addr_i[7:0];
  assign ctrl_wdata_o = wdata_i;

  assign trace_req_o  = accept_w && fwd_ok_w && (win_w == WIN_TRACE_C);
  assign trace_addr_o = addr_i[15:0];

  assign fw_req_o   = accept_w && fwd_ok_w && (win_w == WIN_FW_C);
  assign fw_we_o    = fw_req_o && we_i;
  assign fw_addr_o  = addr_i[15:0];
  assign fw_wdata_o = wdata_i;

  // -------------------------------------------- response mux (pass-through)
  always_comb begin : rsp_mux
    case (sel_r)
      3'd0:    begin sel_rvalid_w = img_rvalid_i;   sel_rdata_w = img_rdata_i;   end
      3'd1:    begin sel_rvalid_w = dbg_rvalid_i;   sel_rdata_w = dbg_rdata_i;   end
      3'd2:    begin sel_rvalid_w = snap_rvalid_i;  sel_rdata_w = snap_rdata_i;  end
      3'd3:    begin sel_rvalid_w = ctrl_rvalid_i;  sel_rdata_w = ctrl_rdata_i;  end
      3'd4:    begin sel_rvalid_w = trace_rvalid_i; sel_rdata_w = trace_rdata_i; end
      3'd5:    begin sel_rvalid_w = fw_rvalid_i;    sel_rdata_w = fw_rdata_i;    end
      default: begin sel_rvalid_w = 1'b0;           sel_rdata_w = 32'h0;         end
    endcase
  end

  always_comb begin : rsp_drive
    rvalid_o = 1'b0;
    err_o    = 1'b0;
    rdata_o  = 32'h0;
    case (state_r)
      SP_WAIT: begin
        rvalid_o = sel_rvalid_w;
        rdata_o  = sel_rvalid_w ? sel_rdata_w : 32'h0;
      end
      SP_ERR: begin
        rvalid_o = 1'b1;
        err_o    = 1'b1;
      end
      default: ;  // SP_IDLE: bus quiet
    endcase
  end

  always_ff @(posedge clk_i) begin : sp_fsm
    if (!rst_n) begin
      state_r <= SP_IDLE;
      sel_r   <= 3'd0;
    end else begin
      case (state_r)
        SP_IDLE: begin
          if (accept_w) begin
            state_r <= fwd_ok_w ? SP_WAIT : SP_ERR;
            sel_r   <= win_w[2:0];
          end
        end
        SP_WAIT: begin
          if (sel_rvalid_w) state_r <= SP_IDLE;
        end
        default: begin  // SP_ERR is a single-cycle response
          state_r <= SP_IDLE;
        end
      endcase
    end
  end

endmodule

`default_nettype wire

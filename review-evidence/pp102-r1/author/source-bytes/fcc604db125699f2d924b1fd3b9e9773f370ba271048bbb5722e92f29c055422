/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_srp_encoder.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/10 §3 PDU wire rules + §7 join
//                 aggregation, 03 §7/§8 TX slot pool + arbiter requester,
//                 08 §2 T-MRP-JOIN / T-MRP-LEAVEALL cadences)
//
//  Description : MSRP/MVRP MRPDU vector encoder. Declaration events (New /
//                JoinIn / Lv ...) from the Domain, VLAN and stream FSMs
//                accumulate in two per-application pending tables and are
//                drained into ONE MRPDU per application on that
//                application's T-MRP-JOIN tick (10 §7: one frame carries
//                many attributes — never one frame per event). The drain
//                walks the table in push order and detects sorted runs
//                whose value is the +1 successor of the previous entry
//                under the attribute's own increment rule (802.1Q
//                §35.2.2.8/.9: Talker/Listener step {stream_id, DA}
//                together, Domain steps {SRclassID, SRclassPriority} with
//                the VID pinned, MVRP steps the VID), folding each run into
//                one VectorAttribute with NumberOfValues > 1, ThreePacked
//                (radix-6) event coding and, for Listener attributes, the
//                FourPacked (radix-4) declaration parameters.
//                AttributeListLength counts the VectorAttributes PLUS the
//                AttributeList EndMark (802.1Q §35.2.2.6, MSRP only — MVRP
//                has no such field); the AttributeList EndMark and the
//                MRPDU EndMark are both always written, so the EndMark is
//                explicit ahead of any MAC padding (Milan §4.2.7.1.3). A
//                pending LeaveAll (per application, 802.1Q §10.7.1 keeps
//                the two participants separate) rides the first
//                VectorHeader of that application's next MRPDU. The
//                finished frame — Ethernet header included, per the 03 §8
//                destination-addressing row — lands in a KL_pp_tx_slots
//                slot; the committed handle is offered to the (not yet
//                landed) TX arbiter as txreq_valid_o/txreq_slot_o.
//
//  Decision    : the design decision that matters — runs are COLLECTED
//                FIRST and emitted only after they break, so
//                NumberOfValues and both packed-event field sizes are
//                known before their bytes stream out and no vector field
//                ever needs a second pass; the ONE field that cannot be
//                known in advance, AttributeListLength, is back-patched
//                through the slot pool's random-access write port (03 §7:
//                headers are legal after payloads). The pending stores are
//                1W1R sync-read RAMs (push is the only writer, the drain
//                walk the only reader) — never a flop mirror behind a wide
//                read mux.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_srp_encoder #(
    //! pending-event table depth per application; sized so a full drain of
    //! worst-case singles (Talker Failed, 37 B each) still fits a standard
    //! 576 B slot — see the elaboration check below
    parameter int unsigned DEPTH_P             = 12,
    //! standard slot capacity of the attached KL_pp_tx_slots (F01.5)
    parameter int unsigned TX_STD_BYTES_P      = 576,
    //! oversize slot capacity of the pool — sizes the write-address lanes
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600
) (
    input  wire          clk_i,          //! core clock (P-CLK-HZ domain)
    input  wire          rst_n,          //! synchronous active-low reset

    // ---- declaration-event push (Domain / VLAN / stream FSMs) -------------
    input  wire          ev_valid_i,     //! event offered, held until ready
    output logic         ev_ready_o,     //! accept: full or drain-side busy on ev_app_i deasserts
    input  wire          ev_app_i,       //! 0 = MSRP participant, 1 = MVRP
    input  wire  [7:0]   ev_attr_type_i, //! F10.8 AttributeType (MSRP 1..4, MVRP 1)
    input  wire  [2:0]   ev_event_i,     //! attribute event 0 New .. 5 Lv (10 §3)
    input  wire  [1:0]   ev_fourpack_i,  //! Listener declaration parameter (FourPacked lane)
    input  wire  [271:0] ev_value_i,     //! FirstValue, wire byte 0 at [271:264]; unused low bytes zero
    output logic         ev_drop_o,      //! strobe: accepted event had an unknown type and was dropped

    // ---- cadence strobes (timer expiries routed by the event router) ------
    input  wire  [1:0]   join_tick_i,    //! T-MRP-JOIN per participant: bit 0 MSRP, bit 1 MVRP
    input  wire  [1:0]   leaveall_i,     //! LeaveAllEvent injection request per participant

    // ---- addressing -------------------------------------------------------
    input  wire  [47:0]  own_mac_i,      //! station MAC — Ethernet source address

    // ---- KL_pp_tx_slots allocation face (exact port match) ----------------
    output logic         alloc_req_o,    //! slot request (deasserts on grant)
    output logic         oversize_o,     //! never set: an MRPDU drain fits a standard slot
    input  wire  [$bits(pp_pkg::PP_SLOT_NULL_C)-1:0] alloc_slot_i, //! granted slot index
    input  wire          alloc_gnt_i,    //! one-cycle grant pulse from the pool

    // ---- KL_pp_tx_slots write face (exact port match) ---------------------
    output logic [$bits(pp_pkg::PP_SLOT_NULL_C)-1:0]   wr_slot_o,   //! slot being written / committed
    output logic [$clog2(TX_OVERSIZE_BYTES_P+1)-1:0]   wr_addr_o,   //! byte offset inside the slot
    output logic                                       wr_valid_o,  //! byte-write strobe
    output logic [7:0]                                 wr_data_o,   //! frame byte
    output logic                                       wr_commit_o, //! one-cycle commit with wr_len_o
    output logic [$clog2(TX_OVERSIZE_BYTES_P+1)-1:0]   wr_len_o,    //! committed frame length in bytes

    // ---- TX request face (arbiter not yet landed: 03 §8 requester) --------
    output logic         txreq_valid_o,  //! committed frame ready, held until accepted
    output logic [$bits(pp_pkg::PP_SLOT_NULL_C)-1:0] txreq_slot_o, //! committed KL_pp_tx_slots handle
    input  wire          txreq_ready_i,  //! arbiter accepts the request

    // ---- observability ----------------------------------------------------
    output logic [$clog2(DEPTH_P+1)-1:0] dbg_cnt_msrp_o, //! pending MSRP events
    output logic [$clog2(DEPTH_P+1)-1:0] dbg_cnt_mvrp_o  //! pending MVRP events
);

  // ------------------------------------------------------------- geometry
  localparam int unsigned SLOT_W_C = $bits(pp_pkg::PP_SLOT_NULL_C);      // 3
  localparam int unsigned ADDR_W_C = $clog2(TX_OVERSIZE_BYTES_P + 1);    // 11
  localparam int unsigned CNT_W_C  = $clog2(DEPTH_P + 1);                // 4
  localparam int unsigned IDX_W_C  = (DEPTH_P > 1) ? $clog2(DEPTH_P) : 1;

  // worst-case drained MSRP frame: eth+version 15, four message shells
  // (type + length + list-length + list EndMark = 6 B each), every entry a
  // lone Talker Failed vector (2 + 34 + 1 = 37 B), MRPDU EndMark 2
  localparam int unsigned WORST_BYTES_C = 15 + (4 * 6) + (DEPTH_P * 37) + 2;
  if (WORST_BYTES_C > TX_STD_BYTES_P) begin : g_depth_check
    $error("DEPTH_P drain cannot fit a standard TX slot");
  end

  // ---- applications and attribute types (10 §2 / F10.8 constants) --------
  localparam logic        APP_MSRP_C        = 1'b0;
  localparam logic        APP_MVRP_C        = 1'b1;
  localparam logic [47:0] MSRP_DA_C         = 48'h0180_C200_000E;
  localparam logic [47:0] MVRP_DA_C         = 48'h0180_C200_0021;
  localparam logic [15:0] MSRP_ETYPE_C      = 16'h22EA;
  localparam logic [15:0] MVRP_ETYPE_C      = 16'h88F5;
  localparam logic [7:0]  ATTR_TALKER_ADV_C  = 8'd1;
  localparam logic [7:0]  ATTR_TALKER_FAIL_C = 8'd2;
  localparam logic [7:0]  ATTR_LISTENER_C    = 8'd3;
  localparam logic [7:0]  ATTR_DOMAIN_C      = 8'd4;
  localparam logic [7:0]  ATTR_MVRP_VID_C    = 8'd1;

  //! FirstValue length in bytes by application/type (F10.8)
  function automatic logic [5:0] attr_len_f(input logic app,
                                            input logic [7:0] t);
    if (app == APP_MVRP_C) return 6'd2;
    case (t)
      ATTR_TALKER_ADV_C:  return 6'd25;
      ATTR_TALKER_FAIL_C: return 6'd34;
      ATTR_LISTENER_C:    return 6'd8;
      ATTR_DOMAIN_C:      return 6'd4;
      default:            return 6'd0;
    endcase
  endfunction

  //! +1 successor test under the attribute's own increment rule (10 §3)
  function automatic logic succ_f(input logic app, input logic [7:0] t,
                                  input logic [271:0] prev,
                                  input logic [271:0] nxt);
    logic [63:0] sid_w;
    logic [47:0] da_w;
    logic [7:0]  cid_w;
    logic [7:0]  pri_w;
    logic [15:0] vid_w;
    sid_w = prev[271:208] + 64'd1;
    da_w  = prev[207:160] + 48'd1;
    cid_w = prev[271:264] + 8'd1;
    pri_w = prev[263:256] + 8'd1;
    vid_w = prev[271:256] + 16'd1;
    if (app == APP_MVRP_C) begin
      return (nxt[271:256] == vid_w) && (nxt[255:0] == prev[255:0]);
    end
    case (t)
      ATTR_TALKER_ADV_C, ATTR_TALKER_FAIL_C:
        return (nxt[271:208] == sid_w) && (nxt[207:160] == da_w)
            && (nxt[159:0] == prev[159:0]);
      ATTR_LISTENER_C:
        return (nxt[271:208] == sid_w) && (nxt[207:0] == prev[207:0]);
      ATTR_DOMAIN_C:
        return (nxt[271:264] == cid_w) && (nxt[263:256] == pri_w)
            && (nxt[255:0] == prev[255:0]);
      default: return 1'b0;
    endcase
  endfunction

  //! big-endian byte i of the 34-byte FirstValue lane
  function automatic logic [7:0] fv_byte_f(input logic [271:0] v,
                                           input logic [5:0] i);
    return v[271 - 8 * int'(i) -: 8];
  endfunction

  //! big-endian byte i of a 48-bit MAC lane
  function automatic logic [7:0] mac_byte_f(input logic [47:0] v,
                                            input logic [5:0] i);
    return v[47 - 8 * int'(i) -: 8];
  endfunction

  //! ThreePackedEvents byte: (((e1 * 6) + e2) * 6) + e3 (802.1Q §10.8.2.7)
  function automatic logic [7:0] pack3_f(input logic [2:0] a,
                                         input logic [2:0] b,
                                         input logic [2:0] c);
    return 8'(a) * 8'd36 + 8'(b) * 8'd6 + 8'(c);
  endfunction

  //! FourPackedEvents byte (802.1Q §35.2.2.7.1, radix 4)
  function automatic logic [7:0] pack4_f(input logic [1:0] a,
                                         input logic [1:0] b,
                                         input logic [1:0] c,
                                         input logic [1:0] d);
    return 8'(a) * 8'd64 + 8'(b) * 8'd16 + 8'(c) * 8'd4 + 8'(d);
  endfunction

  // -------------------------------------------------- pending tables (RAM)
  // entry = {type[7:0], event[2:0], fourpack[1:0], value[271:0]} = 285 b
  localparam int unsigned MSRP_EW_C = 285;
  localparam int unsigned MVRP_EW_C = 19;   // {event[2:0], vid[15:0]}

  // DISTRIBUTED, NOT BLOCK — the same wide-and-shallow trap KL_pp_dispatch
  // documents: DEPTH_P (12) x 285 bits is 3,420 bits of data, but the 285-bit
  // port made the synthesiser band 4 RAMB36 together and leave 97 % of them
  // empty. Measured on the reference part (xc7a100t, Vivado 2026.1,
  // post-synthesis out-of-context, 1-stream shape). A synthesis attribute,
  // not a primitive: a tool that does not know it ignores it.
  (* ram_style = "distributed" *)
  logic [MSRP_EW_C-1:0] msrp_ram_r [0:DEPTH_P-1];
  logic [MVRP_EW_C-1:0] mvrp_ram_r [0:DEPTH_P-1];
  logic [MSRP_EW_C-1:0] msrp_q_r;
  logic [MVRP_EW_C-1:0] mvrp_q_r;

  logic [CNT_W_C-1:0] cnt_msrp_r;
  logic [CNT_W_C-1:0] cnt_mvrp_r;
  logic [CNT_W_C-1:0] rd_idx_r;

  // ------------------------------------------------------------ FSM state
  typedef enum logic [3:0] {
    E_IDLE     = 4'd0,   // wait for a join tick with pending events
    E_ALLOC    = 4'd1,   // request a standard TX slot
    E_HDR      = 4'd2,   // Ethernet header + ProtocolVersion (15 B)
    E_RD       = 4'd3,   // issue pending-table read
    E_CAP      = 4'd4,   // capture entry: open / extend / break the run
    E_BOUND    = 4'd5,   // message-boundary dispatch for a final run
    E_MSGHDR   = 4'd6,   // AttributeType/-Length (+ list-length placeholder)
    E_VHDR     = 4'd7,   // VectorHeader {LeaveAllEvent, NumberOfValues}
    E_VFV      = 4'd8,   // FirstValue bytes
    E_V3PK     = 4'd9,   // ThreePackedEvents bytes
    E_V4PK     = 4'd10,  // FourPackedEvents bytes (Listener only)
    E_MSGCLOSE = 4'd11,  // AttributeList EndMark
    E_PATCH    = 4'd12,  // back-patch AttributeListLength (MSRP only)
    E_PDUEND   = 4'd13,  // MRPDU EndMark
    E_COMMIT   = 4'd14,  // commit the slot with the final length
    E_TXREQ    = 4'd15   // offer the handle to the TX arbiter
  } enc_st_e;

  enc_st_e             st_r;
  logic                cur_app_r;      // application being drained
  logic [CNT_W_C-1:0]  drain_n_r;      // snapshot of the pending count
  logic [SLOT_W_C-1:0] slot_r;         // granted TX slot
  logic [ADDR_W_C-1:0] waddr_r;        // next sequential byte offset
  logic [5:0]          bidx_r;         // byte index inside the region
  logic [ADDR_W_C-1:0] ll_addr_r;      // AttributeListLength patch address
  logic                msg_open_r;     // a message shell is open
  logic [7:0]          msg_type_r;     // its AttributeType
  logic                first_vec_r;    // next vector is the PDU's first
  logic                close_for_pdu_r;// message close leads to the PDU EndMark

  // collected run
  logic                run_open_r;
  logic [7:0]          run_type_r;
  logic [271:0]        run_first_r;
  logic [271:0]        run_last_r;
  logic [CNT_W_C-1:0]  run_len_r;
  logic [DEPTH_P-1:0][2:0] run_ev_r;   // packed: read inside functions (sv2v)
  logic [DEPTH_P-1:0][1:0] run_fp_r;   // packed: read inside functions (sv2v)

  // entry that broke the run, promoted to the next run after the emit
  logic                hold_valid_r;
  logic [7:0]          hold_type_r;
  logic [2:0]          hold_ev_r;
  logic [1:0]          hold_fp_r;
  logic [271:0]        hold_val_r;

  // deferred cadence requests
  logic [1:0]          join_pend_r;
  logic [1:0]          la_pend_r;

  // --------------------------------------------------------- push plumbing
  logic valid_type_w, ev_accept_w, push_msrp_w, push_mvrp_w;
  logic go0_w, go1_w, start0_w, start1_w, busy_app_w, tgt_full_w, start_tgt_w;

  assign valid_type_w = (ev_app_i == APP_MVRP_C)
                      ? (ev_attr_type_i == ATTR_MVRP_VID_C)
                      : ((ev_attr_type_i >= ATTR_TALKER_ADV_C)
                         && (ev_attr_type_i <= ATTR_DOMAIN_C));
  assign ev_accept_w  = ev_valid_i && ev_ready_o;
  assign push_msrp_w  = ev_accept_w && valid_type_w && (ev_app_i == APP_MSRP_C);
  assign push_mvrp_w  = ev_accept_w && valid_type_w && (ev_app_i == APP_MVRP_C);
  assign ev_drop_o    = ev_accept_w && !valid_type_w;

  assign go0_w    = join_tick_i[0] || join_pend_r[0];
  assign go1_w    = join_tick_i[1] || join_pend_r[1];
  assign start0_w = (st_r == E_IDLE) && go0_w && (cnt_msrp_r != '0);
  assign start1_w = (st_r == E_IDLE) && !start0_w && go1_w && (cnt_mvrp_r != '0);

  // the drain owns its application's table: pushes to it wait
  assign busy_app_w  = (st_r != E_IDLE) && (cur_app_r == ev_app_i);
  assign tgt_full_w  = (ev_app_i == APP_MSRP_C)
                     ? (cnt_msrp_r == CNT_W_C'(DEPTH_P))
                     : (cnt_mvrp_r == CNT_W_C'(DEPTH_P));
  assign start_tgt_w = (ev_app_i == APP_MSRP_C) ? start0_w : start1_w;
  assign ev_ready_o  = !tgt_full_w && !busy_app_w && !start_tgt_w;

  always_ff @(posedge clk_i) begin : pend_write
    if (push_msrp_w) begin
      msrp_ram_r[cnt_msrp_r[IDX_W_C-1:0]]
        <= {ev_attr_type_i, ev_event_i, ev_fourpack_i, ev_value_i};
    end
    if (push_mvrp_w) begin
      mvrp_ram_r[cnt_mvrp_r[IDX_W_C-1:0]]
        <= {ev_event_i, ev_value_i[271:256]};
    end
  end

  always_ff @(posedge clk_i) begin : pend_read
    msrp_q_r <= msrp_ram_r[rd_idx_r[IDX_W_C-1:0]];
    mvrp_q_r <= mvrp_ram_r[rd_idx_r[IDX_W_C-1:0]];
  end

  // ---------------------------------------------------- captured-entry view
  logic [7:0]   cap_type_w;
  logic [2:0]   cap_ev_w;
  logic [1:0]   cap_fp_w;
  logic [271:0] cap_val_w;
  logic         open_w, ext_w, more_w;

  always_comb begin : cap_unpack
    if (cur_app_r == APP_MSRP_C) begin
      cap_type_w = msrp_q_r[284:277];
      cap_ev_w   = msrp_q_r[276:274];
      cap_fp_w   = msrp_q_r[273:272];
      cap_val_w  = msrp_q_r[271:0];
    end else begin
      cap_type_w = ATTR_MVRP_VID_C;
      cap_ev_w   = mvrp_q_r[18:16];
      cap_fp_w   = 2'd0;
      cap_val_w  = {mvrp_q_r[15:0], 256'd0};
    end
  end

  assign open_w = !run_open_r;
  assign ext_w  = run_open_r && (cap_type_w == run_type_r)
               && succ_f(cur_app_r, run_type_r, run_last_r, cap_val_w)
               && (run_len_r < CNT_W_C'(DEPTH_P));
  assign more_w = ((rd_idx_r + CNT_W_C'(1)) < drain_n_r);

  // --------------------------------------------------------- byte emission
  //! packed-event lane j of the collected run (0 beyond NumberOfValues)
  function automatic logic [2:0] run_ev_at_f(input logic [5:0] j);
    if (32'(j) >= 32'(run_len_r)) return 3'd0;
    return run_ev_r[j[IDX_W_C-1:0]];
  endfunction

  //! FourPacked lane j of the collected run (0 beyond NumberOfValues)
  function automatic logic [1:0] run_fp_at_f(input logic [5:0] j);
    if (32'(j) >= 32'(run_len_r)) return 2'd0;
    return run_fp_r[j[IDX_W_C-1:0]];
  endfunction

  logic        wr_valid_w;
  logic [7:0]  wr_data_w;
  logic [5:0]  nbytes_w;
  logic        last_byte_w;
  logic [47:0] da_sel_w;
  logic [15:0] et_sel_w;
  logic [5:0]  alen_w;
  logic [2:0]  la3_w;
  logic [12:0] nov_w;
  logic [ADDR_W_C-1:0] ll_val_w;
  logic [5:0]  j3_w;
  logic [5:0]  j4_w;

  assign da_sel_w = (cur_app_r == APP_MVRP_C) ? MVRP_DA_C : MSRP_DA_C;
  assign et_sel_w = (cur_app_r == APP_MVRP_C) ? MVRP_ETYPE_C : MSRP_ETYPE_C;
  assign alen_w   = attr_len_f(cur_app_r, run_type_r);
  assign la3_w    = (first_vec_r && la_pend_r[cur_app_r]) ? 3'd1 : 3'd0;
  assign nov_w    = 13'(run_len_r);
  // AttributeListLength: everything after its own field, EndMark INCLUDED
  assign ll_val_w = waddr_r - ll_addr_r - ADDR_W_C'(2);
  assign j3_w     = 6'd3 * bidx_r;
  assign j4_w     = 6'd4 * bidx_r;

  always_comb begin : emit_byte
    wr_valid_w = 1'b0;
    wr_data_w  = 8'h00;
    nbytes_w   = 6'd1;
    unique case (st_r)
      E_HDR: begin
        wr_valid_w = 1'b1;
        nbytes_w   = 6'd15;
        if (bidx_r < 6'd6)        wr_data_w = mac_byte_f(da_sel_w, bidx_r);
        else if (bidx_r < 6'd12)  wr_data_w = mac_byte_f(own_mac_i, bidx_r - 6'd6);
        else if (bidx_r == 6'd12) wr_data_w = et_sel_w[15:8];
        else if (bidx_r == 6'd13) wr_data_w = et_sel_w[7:0];
        else                      wr_data_w = 8'h00;   // ProtocolVersion = 0
      end
      E_MSGHDR: begin
        wr_valid_w = 1'b1;
        nbytes_w   = (cur_app_r == APP_MSRP_C) ? 6'd4 : 6'd2;
        if (bidx_r == 6'd0)      wr_data_w = run_type_r;
        else if (bidx_r == 6'd1) wr_data_w = {2'd0, alen_w};
        else                     wr_data_w = 8'h00;    // list-length placeholder
      end
      E_VHDR: begin
        wr_valid_w = 1'b1;
        nbytes_w   = 6'd2;
        wr_data_w  = (bidx_r == 6'd0) ? {la3_w, nov_w[12:8]} : nov_w[7:0];
      end
      E_VFV: begin
        wr_valid_w = 1'b1;
        nbytes_w   = alen_w;
        wr_data_w  = fv_byte_f(run_first_r, bidx_r);
      end
      E_V3PK: begin
        wr_valid_w = 1'b1;
        nbytes_w   = (6'(run_len_r) + 6'd2) / 6'd3;
        wr_data_w  = pack3_f(run_ev_at_f(j3_w),
                             run_ev_at_f(j3_w + 6'd1),
                             run_ev_at_f(j3_w + 6'd2));
      end
      E_V4PK: begin
        wr_valid_w = 1'b1;
        nbytes_w   = (6'(run_len_r) + 6'd3) / 6'd4;
        wr_data_w  = pack4_f(run_fp_at_f(j4_w),
                             run_fp_at_f(j4_w + 6'd1),
                             run_fp_at_f(j4_w + 6'd2),
                             run_fp_at_f(j4_w + 6'd3));
      end
      E_MSGCLOSE, E_PDUEND: begin
        wr_valid_w = 1'b1;      // both EndMarks always explicit (Milan §4.2.7.1.3)
        nbytes_w   = 6'd2;
        wr_data_w  = 8'h00;
      end
      E_PATCH: begin
        wr_valid_w = 1'b1;
        nbytes_w   = 6'd2;
        wr_data_w  = (bidx_r == 6'd0) ? {5'd0, ll_val_w[10:8]} : ll_val_w[7:0];
      end
      default: begin
        wr_valid_w = 1'b0;
      end
    endcase
  end

  assign last_byte_w = wr_valid_w && (bidx_r == nbytes_w - 6'd1);

  // ------------------------------------------------------------- main FSM
  always_ff @(posedge clk_i) begin : enc_fsm
    if (!rst_n) begin
      st_r            <= E_IDLE;
      cur_app_r       <= APP_MSRP_C;
      drain_n_r       <= '0;
      slot_r          <= '0;
      waddr_r         <= '0;
      bidx_r          <= '0;
      ll_addr_r       <= '0;
      msg_open_r      <= 1'b0;
      msg_type_r      <= 8'd0;
      first_vec_r     <= 1'b0;
      close_for_pdu_r <= 1'b0;
      run_open_r      <= 1'b0;
      run_type_r      <= 8'd0;
      run_first_r     <= '0;
      run_last_r      <= '0;
      run_len_r       <= '0;
      hold_valid_r    <= 1'b0;
      hold_type_r     <= 8'd0;
      hold_ev_r       <= 3'd0;
      hold_fp_r       <= 2'd0;
      hold_val_r      <= '0;
      cnt_msrp_r      <= '0;
      cnt_mvrp_r      <= '0;
      rd_idx_r        <= '0;
      join_pend_r     <= 2'b00;
      la_pend_r       <= 2'b00;
    end else begin
      // ---- pending-table push side --------------------------------------
      if (push_msrp_w) cnt_msrp_r <= cnt_msrp_r + CNT_W_C'(1);
      if (push_mvrp_w) cnt_mvrp_r <= cnt_mvrp_r + CNT_W_C'(1);

      // ---- generic byte advance -----------------------------------------
      if (wr_valid_w) begin
        if (st_r != E_PATCH) waddr_r <= waddr_r + ADDR_W_C'(1);
        bidx_r <= last_byte_w ? 6'd0 : bidx_r + 6'd1;
      end

      // ---- per-state transitions ----------------------------------------
      unique case (st_r)
        E_IDLE: begin
          if (start0_w || start1_w) begin
            cur_app_r   <= start0_w ? APP_MSRP_C : APP_MVRP_C;
            drain_n_r   <= start0_w ? cnt_msrp_r : cnt_mvrp_r;
            if (start0_w) join_pend_r[0] <= 1'b0;
            else          join_pend_r[1] <= 1'b0;
            rd_idx_r    <= '0;
            waddr_r     <= '0;
            bidx_r      <= '0;
            msg_open_r  <= 1'b0;
            first_vec_r <= 1'b1;
            run_open_r  <= 1'b0;
            hold_valid_r <= 1'b0;
            st_r        <= E_ALLOC;
          end else begin
            // a deferred tick with nothing pending expires quietly
            if (join_pend_r[0] && (cnt_msrp_r == '0)) join_pend_r[0] <= 1'b0;
            if (join_pend_r[1] && (cnt_mvrp_r == '0)) join_pend_r[1] <= 1'b0;
          end
        end
        E_ALLOC: begin
          if (alloc_gnt_i) begin
            slot_r <= alloc_slot_i;
            bidx_r <= '0;
            st_r   <= E_HDR;
          end
        end
        E_HDR: begin
          if (last_byte_w) st_r <= E_RD;
        end
        E_RD: begin
          st_r <= E_CAP;    // sync read lands next cycle
        end
        E_CAP: begin
          rd_idx_r <= rd_idx_r + CNT_W_C'(1);
          if (open_w || ext_w) begin
            if (open_w) begin
              run_open_r  <= 1'b1;
              run_type_r  <= cap_type_w;
              run_first_r <= cap_val_w;
              run_last_r  <= cap_val_w;
              run_ev_r[0] <= cap_ev_w;
              run_fp_r[0] <= cap_fp_w;
              run_len_r   <= CNT_W_C'(1);
            end else begin
              run_last_r  <= cap_val_w;
              run_ev_r[run_len_r[IDX_W_C-1:0]] <= cap_ev_w;
              run_fp_r[run_len_r[IDX_W_C-1:0]] <= cap_fp_w;
              run_len_r   <= run_len_r + CNT_W_C'(1);
            end
            st_r <= more_w ? E_RD : E_BOUND;
          end else begin
            hold_type_r  <= cap_type_w;
            hold_ev_r    <= cap_ev_w;
            hold_fp_r    <= cap_fp_w;
            hold_val_r   <= cap_val_w;
            hold_valid_r <= 1'b1;
            st_r         <= E_BOUND;
          end
        end
        E_BOUND: begin
          if (!msg_open_r) begin
            st_r <= E_MSGHDR;
          end else if (msg_type_r != run_type_r) begin
            close_for_pdu_r <= 1'b0;
            st_r <= E_MSGCLOSE;
          end else begin
            st_r <= E_VHDR;
          end
        end
        E_MSGHDR: begin
          if (bidx_r == 6'd2) ll_addr_r <= waddr_r;   // placeholder high byte
          if (last_byte_w) begin
            msg_open_r <= 1'b1;
            msg_type_r <= run_type_r;
            st_r       <= E_VHDR;
          end
        end
        E_VHDR: begin
          if (last_byte_w) begin
            first_vec_r <= 1'b0;
            st_r        <= E_VFV;
          end
        end
        E_VFV: begin
          if (last_byte_w) st_r <= E_V3PK;
        end
        E_V3PK: begin
          if (last_byte_w) begin
            if ((cur_app_r == APP_MSRP_C) && (run_type_r == ATTR_LISTENER_C)) begin
              st_r <= E_V4PK;
            end else if (hold_valid_r) begin
              hold_valid_r <= 1'b0;
              run_type_r   <= hold_type_r;
              run_first_r  <= hold_val_r;
              run_last_r   <= hold_val_r;
              run_ev_r[0]  <= hold_ev_r;
              run_fp_r[0]  <= hold_fp_r;
              run_len_r    <= CNT_W_C'(1);
              st_r         <= (rd_idx_r < drain_n_r) ? E_RD : E_BOUND;
            end else begin
              run_open_r      <= 1'b0;
              close_for_pdu_r <= 1'b1;
              st_r            <= E_MSGCLOSE;
            end
          end
        end
        E_V4PK: begin
          if (last_byte_w) begin
            if (hold_valid_r) begin
              hold_valid_r <= 1'b0;
              run_type_r   <= hold_type_r;
              run_first_r  <= hold_val_r;
              run_last_r   <= hold_val_r;
              run_ev_r[0]  <= hold_ev_r;
              run_fp_r[0]  <= hold_fp_r;
              run_len_r    <= CNT_W_C'(1);
              st_r         <= (rd_idx_r < drain_n_r) ? E_RD : E_BOUND;
            end else begin
              run_open_r      <= 1'b0;
              close_for_pdu_r <= 1'b1;
              st_r            <= E_MSGCLOSE;
            end
          end
        end
        E_MSGCLOSE: begin
          if (last_byte_w) begin
            msg_open_r <= 1'b0;
            if (cur_app_r == APP_MSRP_C)  st_r <= E_PATCH;
            else if (close_for_pdu_r)     st_r <= E_PDUEND;
            else                          st_r <= E_MSGHDR;
          end
        end
        E_PATCH: begin
          if (last_byte_w) st_r <= close_for_pdu_r ? E_PDUEND : E_MSGHDR;
        end
        E_PDUEND: begin
          if (last_byte_w) st_r <= E_COMMIT;
        end
        E_COMMIT: begin
          if (cur_app_r == APP_MSRP_C) cnt_msrp_r <= '0;
          else                         cnt_mvrp_r <= '0;
          la_pend_r[cur_app_r] <= 1'b0;
          st_r <= E_TXREQ;
        end
        E_TXREQ: begin
          if (txreq_ready_i) st_r <= E_IDLE;
        end
        default: st_r <= E_IDLE;
      endcase

      // ---- cadence latches (after the case: a tick landing on the same
      // cycle as a pend-clear or LeaveAll-consume must survive it) ---------
      if (join_tick_i[0] && !start0_w) join_pend_r[0] <= 1'b1;
      if (join_tick_i[1] && !start1_w) join_pend_r[1] <= 1'b1;
      if (leaveall_i[0]) la_pend_r[0] <= 1'b1;
      if (leaveall_i[1]) la_pend_r[1] <= 1'b1;
    end
  end

  // -------------------------------------------------------------- outputs
  assign alloc_req_o   = (st_r == E_ALLOC) && !alloc_gnt_i;
  assign oversize_o    = 1'b0;
  assign wr_slot_o     = slot_r;
  assign wr_addr_o     = (st_r == E_PATCH) ? (ll_addr_r + ADDR_W_C'(bidx_r))
                                           : waddr_r;
  assign wr_valid_o    = wr_valid_w;
  assign wr_data_o     = wr_data_w;
  assign wr_commit_o   = (st_r == E_COMMIT);
  assign wr_len_o      = waddr_r;
  assign txreq_valid_o = (st_r == E_TXREQ);
  assign txreq_slot_o  = slot_r;
  assign dbg_cnt_msrp_o = cnt_msrp_r;
  assign dbg_cnt_mvrp_o = cnt_mvrp_r;

endmodule : KL_srp_encoder
`default_nettype wire

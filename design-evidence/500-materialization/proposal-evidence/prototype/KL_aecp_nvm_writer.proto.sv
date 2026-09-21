/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_nvm_writer.proto.sv   (PROTOTYPE, design evidence)
//  Project     : milan-fpga #500, saved-state scope D3
//                (docs/design/SAVED_STATE_MATERIALIZATION.md)
//
//  Description : THE D3 RECORD WRITER, candidate (b) of the design page: ONE
//                processor-side manager for every non-binding persisted
//                group -- configuration index, sampling rate, clock source,
//                stream formats in and out, presentation time offset,
//                channel maps in and out, user names -- beside the binding
//                manager KL_acmp_nvm_shadow and sharing KL_pp_nvm_port with it
//                through KL_pp_nvm_mgr_arb. Records are F07.8 frames at the
//                section 4.2 ids of the saved-state page.
//
//                NO SHADOW. It keeps no copy of the state it persists: one
//                dirty bit per record, and at flush time it LATCHES the live
//                value from its owner (the dynamic-state store and the name
//                table over the uCPU state bus, the channel maps over the
//                GET_AUDIO_MAP read face), in ONE quiescent window: no AECP
//                program is running and none is dispatched until the latch
//                is complete (own_o). What reaches a record is therefore
//                always a value some completed command left.
//
//                THE CLEAR RULE (page section 6). A record's dirty bit is SET
//                by a change to it and CLEARED only by the done of the whole
//                record commit that carries a value latched AFTER the last
//                change: a change that lands after the latch taints the
//                commit, and a tainted commit clears nothing. A change on
//                the done edge wins. The OR of the bits is unflushed_o, the
//                parent's pend_i term, so until the record is in the window
//                the pending bit says so, and from the record's close on the
//                backend's dirty_live does. A map set with more mappings
//                than its record has entries is neither written nor
//                forgotten: it stays dirty (pending) and is skipped by the
//                flush scan until the next change to that port.
//
//                RESTORE (page section 8), after the binding walk and before
//                the entity is enabled, in two passes over the port: the
//                first only proves that no record stream is torn (a torn one
//                aborts the walk before anything is applied), the second
//                reads every record again and checks it (framing, crc16,
//                then its VALUE against the image by the rule the matching
//                SET program applies); only a value that passes is written
//                back. Formats are
//                judged on "supported" alone and applied before the maps;
//                the maps of a port then REPLACE its image-default set and
//                are judged against the restored formats; a refused set puts
//                the defaults back, reverting any restored format they would
//                orphan; a final pass reverts a restored format that orphans
//                a mapping. Names follow, once the descriptor store holds a
//                validated image. A restore write is not a change.
//
//  Model faces : the map EDIT face (mr_*) and the format JUDGE face (fj_*)
//                are simplified stand-ins for the processor's
//                ADD/REMOVE_AUDIO_MAPPINGS transaction face and the GSI(15)
//                gather (bit 0 supported, bit 1 no mapped channel orphaned).
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_nvm_writer #(
    parameter int unsigned N_STREAM_IN_P  = 8,
    parameter int unsigned N_STREAM_OUT_P = 8,
    parameter int unsigned N_SPORT_IN_P   = 8,
    parameter int unsigned N_SPORT_OUT_P  = 8,
    parameter int unsigned N_AUDIO_UNIT_P = 1,
    parameter int unsigned N_CLK_DOM_P    = 1,
    parameter int unsigned N_NAME_P       = 99,
    //! clusters per stream port, 8 bits each, port k at [8k +: 8]; a map
    //! record carries 8 bytes per cluster (saved-state page section 8.3)
    parameter logic [8*N_SPORT_IN_P-1:0]  MAPI_CLS_P = '0,
    parameter logic [8*N_SPORT_OUT_P-1:0] MAPO_CLS_P = '0,
    //! the largest cluster count of any port: the map buffer depth in entries
    parameter int unsigned MAP_ENT_MAX_P  = 17,
    //! F07.8 layout_version: one value per container, so it MUST be the
    //! binding manager's LAYOUT_VER_P (the integrator passes the same one)
    parameter logic [7:0]  LAYOUT_VER_P   = 8'h02,
    //! T-NVM-DEBOUNCE in tick_i units, the binding manager's meaning
    parameter int unsigned DEB_TICKS_P    = 500,
    parameter int unsigned RETRY_MAX_P    = 2
) (
    input  wire         clk_i,
    input  wire         rst_n,
    input  wire         tick_i,

    //! ---- change sources: the uCPU side of the state bus, and the marks ----
    input  wire         u_dyn_ack_i,   //! the dynamic-state store took a uCPU write
    input  wire         u_name_ack_i,  //! the descriptor store took a uCPU name write
    input  wire  [19:0] u_addr_i,      //! that access's address
    input  wire  [15:0] u_didx_i,      //! that access's descriptor index
    //! the map edit face's commit-one-record beat (amap_edit_req_o with
    //! amap_edit_phase_o 5): the live map write itself, which the class-6
    //! commit mark follows only after the rest of the program
    input  wire         me_stb_i,
    input  wire  [15:0] me_type_i,     //! the edited port's descriptor type
    input  wire  [15:0] me_idx_i,      //! ... and descriptor index

    //! ---- quiescence ----
    input  wire         prog_busy_i,   //! a uCPU program is running, marks included
    output logic        own_o,         //! the writer owns the state bus and map faces

    //! ---- uCPU state-bus master (valid while own_o) ----
    output logic        sb_req_o,
    output logic        sb_we_o,
    output logic        sb_name_o,
    output logic [19:0] sb_addr_o,
    output logic [63:0] sb_wdata_o,
    output logic [7:0]  sb_wstrb_o,
    output logic [15:0] sb_didx_o,
    input  wire         sb_ready_i,
    input  wire         sb_rvalid_i,
    input  wire  [63:0] sb_rdata_i,
    input  wire         sb_err_i,
    input  wire         desc_img_valid_i, //! the descriptor store validated its image

    //! ---- GET_AUDIO_MAP read face master (valid while own_o) ----
    output logic        am_req_o,
    output logic [15:0] am_type_o,
    output logic [15:0] am_idx_o,
    output logic [15:0] am_map_o,
    output logic [1:0]  am_sel_o,
    output logic [7:0]  am_rec_o,
    input  wire  [63:0] am_data_i,
    input  wire         am_wait_i,     //! a HOLD: 0 means the answer is on am_data_i

    //! ---- map edit face (restore only; model of ADD/REMOVE_AUDIO_MAPPINGS) --
    output logic        mr_req_o,
    output logic        mr_add_o,      //! 1 ADD the set, 0 REMOVE it
    output logic [15:0] mr_type_o,
    output logic [15:0] mr_idx_o,
    output logic [7:0]  mr_cnt_o,
    output logic        mr_ent_v_o,
    output logic [63:0] mr_ent_o,
    input  wire         mr_ent_rdy_i,
    input  wire         mr_done_i,     //! one cycle: the staged set was judged
    input  wire         mr_ok_i,       //! ... and applied whole (else nothing)

    //! ---- format judge face (restore only; model of the GSI(15) gather) ----
    output logic        fj_req_o,
    output logic        fj_out_o,      //! 0 STREAM_INPUT, 1 STREAM_OUTPUT
    output logic [15:0] fj_idx_o,
    output logic [63:0] fj_fmt_o,
    input  wire         fj_wait_i,     //! a HOLD
    input  wire  [1:0]  fj_data_i,     //! bit 0 supported, bit 1 no mapped channel orphaned

    //! ---- the port, through KL_pp_nvm_mgr_arb (manager 1) ----
    output logic        m_req_o,       //! held until m_gnt_i
    output logic        m_we_o,
    output logic [7:0]  m_rid_o,
    input  wire         m_gnt_i,
    output logic        m_wvalid_o,
    output logic [7:0]  m_wdata_o,
    input  wire         m_wready_i,
    input  wire         m_rvalid_i,
    input  wire  [7:0]  m_rdata_i,
    output logic        m_rready_o,
    input  wire         m_done_i,
    input  wire         m_err_i,

    //! ---- restore sequencing ----
    input  wire         restore_go_i,  //! level: the binding walk has completed
    output logic        restore_busy_o,
    output logic        restore_done_o,
    output logic        restore_fail_o, //! a torn read-back, or image defaults refused
    output logic        restore_blank_o, //! done, and no D3 record passed framing and crc
    output logic [7:0]  rs_applied_o,
    output logic [7:0]  rs_refused_o,
    output logic [7:0]  rs_blank_o,
    output logic [7:0]  rs_reverted_o,

    //! ---- published ----
    output logic        unflushed_o,   //! a change no record in the window carries yet
    output logic        alarm_o,       //! sticky: a record given up after RETRY_MAX_P errors
    output logic [15:0] writes_o,      //! whole-record commits completed
    output logic [15:0] dbg_slot_o,    //! observation: the slot in hand
    output logic        dbg_taint_o,
    output logic [N_AUDIO_UNIT_P + N_CLK_DOM_P + N_STREAM_IN_P + 2*N_STREAM_OUT_P
                  + N_SPORT_IN_P + N_SPORT_OUT_P + N_NAME_P:0] dbg_dirty_o
);

  // ---- the record slots, ascending record id (saved-state page 4.2) -------
  localparam int unsigned G_CFG = 0, G_RATE = 1, G_CLKS = 2, G_FMTI = 3,
                          G_FMTO = 4, G_PTOF = 5, G_MAPI = 6, G_MAPO = 7,
                          G_NAME = 8;
  localparam int unsigned S_CFG_C  = 0;
  localparam int unsigned S_RATE_C = 1;
  localparam int unsigned S_CLKS_C = S_RATE_C + N_AUDIO_UNIT_P;
  localparam int unsigned S_FMTI_C = S_CLKS_C + N_CLK_DOM_P;
  localparam int unsigned S_FMTO_C = S_FMTI_C + N_STREAM_IN_P;
  localparam int unsigned S_PTOF_C = S_FMTO_C + N_STREAM_OUT_P;
  localparam int unsigned S_MAPI_C = S_PTOF_C + N_STREAM_OUT_P;
  localparam int unsigned S_MAPO_C = S_MAPI_C + N_SPORT_IN_P;
  localparam int unsigned S_NAME_C = S_MAPO_C + N_SPORT_OUT_P;
  localparam int unsigned N_REC_C  = S_NAME_C + N_NAME_P;
  localparam int unsigned SW_C     = $clog2(N_REC_C + 1);
  localparam int unsigned MAPB_C   = 8 * MAP_ENT_MAX_P;
  localparam int unsigned PAY_C    = (MAPB_C > 64) ? MAPB_C : 64;
  localparam int unsigned PW_C     = $clog2(PAY_C + 1);
  localparam int unsigned AW_C     = $clog2(MAPB_C + 1);
  localparam int unsigned FW_C     = $clog2(N_STREAM_IN_P + N_STREAM_OUT_P);

  localparam logic [15:0] T_AU_C  = 16'h0002, T_SI_C = 16'h0005, T_SO_C = 16'h0006,
                          T_SPI_C = 16'h000E, T_SPO_C = 16'h000F, T_CD_C = 16'h0024;
  localparam logic [3:0]  RG_DATA_C = 4'h0, RG_DYN_C = 4'h1, RG_NCFG_C = 4'hD,
                          RG_LOC_C = 4'hF;
  //! the SET programs' own constants (protocol-processor gen_ucode.py)
  localparam logic [15:0] AU_RATE_OFF_C  = 16'd136, SSR_LIST_OFF_C = 16'd144,
                          CD_SRCCNT_OFF_C = 16'd74, SI_CURFMT_OFF_C = 16'd74;
  localparam int unsigned SSR_WALK_MAX_C = 8;

  function automatic logic [3:0] grp_f(input logic [SW_C-1:0] s);
    if (32'(s) < S_RATE_C)      return 4'(G_CFG);
    else if (32'(s) < S_CLKS_C) return 4'(G_RATE);
    else if (32'(s) < S_FMTI_C) return 4'(G_CLKS);
    else if (32'(s) < S_FMTO_C) return 4'(G_FMTI);
    else if (32'(s) < S_PTOF_C) return 4'(G_FMTO);
    else if (32'(s) < S_MAPI_C) return 4'(G_PTOF);
    else if (32'(s) < S_MAPO_C) return 4'(G_MAPI);
    else if (32'(s) < S_NAME_C) return 4'(G_MAPO);
    else                        return 4'(G_NAME);
  endfunction

  function automatic logic [15:0] base_f(input logic [3:0] g);
    case (g)
      4'(G_CFG):  return 16'(S_CFG_C);
      4'(G_RATE): return 16'(S_RATE_C);
      4'(G_CLKS): return 16'(S_CLKS_C);
      4'(G_FMTI): return 16'(S_FMTI_C);
      4'(G_FMTO): return 16'(S_FMTO_C);
      4'(G_PTOF): return 16'(S_PTOF_C);
      4'(G_MAPI): return 16'(S_MAPI_C);
      4'(G_MAPO): return 16'(S_MAPO_C);
      default:    return 16'(S_NAME_C);
    endcase
  endfunction

  function automatic logic [7:0] ridbase_f(input logic [3:0] g);
    case (g)
      4'(G_CFG):  return 8'h00;
      4'(G_RATE): return 8'h02;
      4'(G_CLKS): return 8'h0A;
      4'(G_FMTI): return 8'h30;
      4'(G_FMTO): return 8'h40;
      4'(G_PTOF): return 8'h50;
      4'(G_MAPI): return 8'h60;
      4'(G_MAPO): return 8'h70;
      default:    return 8'h80;
    endcase
  endfunction

  //! the dynamic-state selector of a scalar group (KL_aecp_dyn_state SEL_*)
  function automatic logic [12:0] sel_f(input logic [3:0] g);
    case (g)
      4'(G_CFG):  return 13'd0;
      4'(G_RATE): return 13'd1;
      4'(G_CLKS): return 13'd2;
      4'(G_FMTI): return 13'd3;
      4'(G_FMTO): return 13'd4;
      default:    return 13'd5;
    endcase
  endfunction

  function automatic logic [7:0] cls_f(input logic [3:0] g, input logic [7:0] i);
    if (g == 4'(G_MAPI)) return MAPI_CLS_P[8 * i +: 8];
    else                 return MAPO_CLS_P[8 * i +: 8];
  endfunction

  function automatic logic [15:0] plen_f(input logic [3:0] g, input logic [7:0] i);
    case (g)
      4'(G_CFG), 4'(G_CLKS):   return 16'd2;
      4'(G_RATE), 4'(G_PTOF):  return 16'd4;
      4'(G_FMTI), 4'(G_FMTO):  return 16'd8;
      4'(G_MAPI), 4'(G_MAPO):  return {5'd0, cls_f(g, i), 3'd0};
      default:                 return 16'd64;
    endcase
  endfunction

  function automatic logic [15:0] crc16_f(input logic [15:0] c, input logic [7:0] d);
    logic [15:0] x;
    x = c ^ {d, 8'h00};
    for (int unsigned k = 0; k < 8; k++) x = x[15] ? ((x << 1) ^ 16'h1021) : (x << 1);
    return x;
  endfunction

  // ---- change events, decoded straight onto the record bits ------------------
  //! each source names its record by group and index; the bits are set by
  //! per-group decoders, with no slot arithmetic on the path
  logic [12:0]        u_sel_w;
  logic               dyn_w, name_w, map_w;
  logic [N_REC_C-1:0] set_w, clr_w;
  assign u_sel_w = u_addr_i[15:3];
  assign dyn_w   = u_dyn_ack_i && (u_addr_i[19:16] == RG_DYN_C);
  assign name_w  = u_name_ack_i;
  assign map_w   = me_stb_i;

  //! selector 7, IDENTIFY, is volatile by Milan 5.3.12 and never a change
  //! here; selector 6 is retired; an index past the shape is none
  assign set_w[S_CFG_C] = dyn_w && (u_sel_w == 13'd0) && (u_didx_i == 16'd0);
  for (genvar gi = 0; gi < N_AUDIO_UNIT_P; gi++) begin : g_ev_rate
    assign set_w[S_RATE_C + gi] = dyn_w && (u_sel_w == 13'd1) && (u_didx_i == 16'(gi));
  end
  for (genvar gi = 0; gi < N_CLK_DOM_P; gi++) begin : g_ev_clks
    assign set_w[S_CLKS_C + gi] = dyn_w && (u_sel_w == 13'd2) && (u_didx_i == 16'(gi));
  end
  for (genvar gi = 0; gi < N_STREAM_IN_P; gi++) begin : g_ev_fmti
    assign set_w[S_FMTI_C + gi] = dyn_w && (u_sel_w == 13'd3) && (u_didx_i == 16'(gi));
  end
  for (genvar gi = 0; gi < N_STREAM_OUT_P; gi++) begin : g_ev_fmto
    assign set_w[S_FMTO_C + gi] = dyn_w && (u_sel_w == 13'd4) && (u_didx_i == 16'(gi));
    assign set_w[S_PTOF_C + gi] = dyn_w && (u_sel_w == 13'd5) && (u_didx_i == 16'(gi));
  end
  for (genvar gi = 0; gi < N_SPORT_IN_P; gi++) begin : g_ev_mapi
    assign set_w[S_MAPI_C + gi] = map_w && (me_type_i == T_SPI_C) && (me_idx_i == 16'(gi));
  end
  for (genvar gi = 0; gi < N_SPORT_OUT_P; gi++) begin : g_ev_mapo
    assign set_w[S_MAPO_C + gi] = map_w && (me_type_i == T_SPO_C) && (me_idx_i == 16'(gi));
  end
  for (genvar gi = 0; gi < N_NAME_P; gi++) begin : g_ev_name
    assign set_w[S_NAME_C + gi] = name_w && (u_addr_i[15:6] == 10'(gi));
  end

  logic ev_any_w;
  assign ev_any_w = |set_w;

  // ---- the main machine ------------------------------------------------------
  typedef enum logic [6:0] {
    W_INIT, W_WAITGO,
    // restore
    R_ACQ, R_IMG, R_IMGW, R_NEXT, R_RD, R_RS, R_VAL, R_AUX, R_APPLY, R_NAMEW,
    R_MA, R_MR, R_MS, R_MV, R_MVW, R_MD, R_CHK, R_CHKJ, R_ADV, R_FIN,
    // steady state and flush
    F_RUN, F_ACQ, F_LAT, F_LATN, F_MAPW, F_PAD, F_REL, F_CRC, F_REQ, F_STR, F_WAIT,
    // shared sub-sequences
    X_BUS, X_BUSG, X_AM, X_MRH, X_MRE, X_MRW, X_FJ
  } st_e;

  st_e             st_r, ret_r, ret2_r;
  logic [N_REC_C-1:0] dirty_r;
  logic [SW_C-1:0] cur_r, scan_r;
  logic [3:0]      cg_r;
  logic [15:0]     ci_r, cplen_r;
  logic [7:0]      crid_r;
  logic            taint_r, own_r, alarm_r, deb_open_r, fl_arm_r;
  logic [31:0]     deb_cnt_r;
  logic [7:0]      retry_r;
  logic [15:0]     writes_r;

  // the latched payload and, for a map restore, the port's default set
  logic [7:0]      bufs_r [0:PAY_C-1];
  logic [7:0]      bufa_r [0:MAPB_C-1];
  logic            bs_we_w, ba_we_w;
  logic [PW_C-1:0] bs_wa_w, bs_ra_w;
  logic [AW_C-1:0] ba_wa_w, ba_ra_w;
  logic [7:0]      bs_wd_w, ba_wd_w, bs_rd_w, ba_rd_w;

  always_ff @(posedge clk_i) begin
    if (bs_we_w) bufs_r[bs_wa_w] <= bs_wd_w;
    if (ba_we_w) bufa_r[ba_wa_w] <= ba_wd_w;
  end
  assign bs_rd_w = bufs_r[bs_ra_w];
  assign ba_rd_w = bufa_r[ba_ra_w];

  // generic cursors
  logic [PW_C-1:0] ptr_r;       // payload byte cursor
  logic [16:0]     bcnt_r;      // bytes seen on the port
  logic [15:0]     crc_r, rcrc_r;
  logic [7:0]      rver_r, rrid_r;
  logic [15:0]     rplen_r;
  logic [63:0]     val_r;       // scalar value / lane / entry assembly
  logic [63:0]     aux_r;       // descriptor field, count, format
  logic [7:0]      k_r, n_r;    // loop counters (entries, lanes, pages)
  logic [7:0]      na_r, ns_r;  // default and saved map entry counts
  logic [15:0]     pg_r, npg_r;
  logic            img_bad_r, rs_fail_r, rs_done_r, chk_done_r;
  //! the restore walks the records TWICE, reading them through the port both
  //! times: pass 0 only proves that no stream is torn, pass 1 judges and
  //! applies. A torn stream therefore aborts the walk before anything is
  //! applied (the binding manager's "fail whole" rule), with no copy kept.
  logic            rpass_r, any_rec_r;
  logic [7:0]      rs_app_r, rs_ref_r, rs_blank_r, rs_rev_r;
  logic [N_STREAM_IN_P+N_STREAM_OUT_P-1:0] frest_r; // formats this restore applied

  // bus sub-sequence registers
  logic        sb_req_r, sb_we_r, sb_name_r;
  logic [19:0] sb_addr_r;
  logic [63:0] sb_wdata_r;
  logic [15:0] sb_didx_r;
  logic        sb_errq_r;
  logic        am_req_r;
  logic [1:0]  am_sel_r;
  logic        mr_req_r, mr_add_r, mr_from_a_r, mr_okq_r;
  logic        fj_req_r;
  logic [63:0] fj_fmt_r;
  logic [3:0]  sub_r;          // step inside a validation or apply sequence
  logic [15:0] fld_off_r;      // descriptor field offset in hand

  assign own_o          = own_r;
  assign sb_req_o       = sb_req_r;
  assign sb_we_o        = sb_we_r;
  assign sb_name_o      = sb_name_r;
  assign sb_addr_o      = sb_addr_r;
  assign sb_wdata_o     = sb_wdata_r;
  assign sb_wstrb_o     = 8'hFF;
  assign sb_didx_o      = sb_didx_r;
  assign am_req_o       = am_req_r;
  assign am_type_o      = (cg_r == 4'(G_MAPI)) ? T_SPI_C : T_SPO_C;
  assign am_idx_o       = ci_r;
  assign am_map_o       = pg_r;
  assign am_sel_o       = am_sel_r;
  assign am_rec_o       = k_r;
  assign mr_req_o       = mr_req_r;
  assign mr_add_o       = mr_add_r;
  assign mr_type_o      = am_type_o;
  assign mr_idx_o       = ci_r;
  assign mr_cnt_o       = mr_from_a_r ? na_r : ns_r;
  assign fj_req_o       = fj_req_r;
  assign fj_fmt_o       = fj_fmt_r;
  assign alarm_o        = alarm_r;
  assign writes_o       = writes_r;
  assign unflushed_o    = |dirty_r;
  assign dbg_slot_o     = 16'(cur_r);
  assign dbg_taint_o    = taint_r;
  assign restore_busy_o = (st_r != W_INIT) && (st_r != W_WAITGO) && !rs_done_r;
  assign restore_done_o = rs_done_r;
  assign restore_fail_o = rs_fail_r;
  assign restore_blank_o = rs_done_r && !any_rec_r;
  assign rs_applied_o   = rs_app_r;
  assign rs_refused_o   = rs_ref_r;
  assign rs_blank_o     = rs_blank_r;
  assign rs_reverted_o  = rs_rev_r;

  //! observation only: the record bits, zero-extended to a fixed width
  assign dbg_dirty_o = dirty_r;

  // the stream index a mapping entry names: bytes 0..1 of the 8-byte entry
  logic        is_scalar_w, fmt_out_w;
  assign is_scalar_w = (cg_r <= 4'(G_PTOF));
  assign fmt_out_w   = (cg_r == 4'(G_FMTO)) || (cg_r == 4'(G_MAPO));

  // the port face
  logic        m_req_r, m_we_r;
  logic [4:0]  hdr_i_r;
  assign m_req_o    = m_req_r;
  assign m_we_o     = m_we_r;
  assign m_rid_o    = crid_r;
  assign m_rready_o = (st_r == R_RS);
  logic [7:0]  hdr_byte_w;
  always_comb begin
    unique case (hdr_i_r[2:0])
      3'd0: hdr_byte_w = 8'h17;
      3'd1: hdr_byte_w = 8'h22;
      3'd2: hdr_byte_w = LAYOUT_VER_P;
      3'd3: hdr_byte_w = crid_r;
      3'd4: hdr_byte_w = cplen_r[15:8];
      3'd5: hdr_byte_w = cplen_r[7:0];
      3'd6: hdr_byte_w = crc_r[15:8];
      default: hdr_byte_w = crc_r[7:0];
    endcase
  end
  assign m_wvalid_o = (st_r == F_STR);
  assign m_wdata_o  = hdr_i_r[3] ? bs_rd_w : hdr_byte_w;

  // the value of a scalar payload, right-justified, from the latched bytes
  // (assembled one byte per cycle in val_r)

  // buffer ports, driven by the machine below
  always_comb begin
    bs_we_w = 1'b0; bs_wa_w = ptr_r; bs_wd_w = 8'd0; bs_ra_w = ptr_r;
    ba_we_w = 1'b0; ba_wa_w = AW_C'(ptr_r); ba_wd_w = 8'd0; ba_ra_w = AW_C'(ptr_r);
    unique case (st_r)
      R_RS: begin
        //! payload bytes of the record under restore land in the buffer
        bs_we_w = m_rvalid_i && (bcnt_r >= 17'd8) && (32'(bcnt_r) - 8 < PAY_C);
        bs_wa_w = PW_C'(bcnt_r - 17'd8);
        bs_wd_w = m_rdata_i;
      end
      F_LAT, F_LATN: begin
        bs_we_w = (sub_r == 4'd1);
        bs_wa_w = ptr_r;
        bs_wd_w = val_r[63:56];
      end
      F_PAD: begin
        bs_we_w = (32'(ptr_r) < 32'(cplen_r));
        bs_wd_w = 8'hFF;
      end
      R_MA: begin
        //! the port's default set, captured before it is removed
        ba_we_w = (sub_r == 4'd5) && (eb_r != 4'd0) && (eb_r != 4'd9);
        ba_wa_w = AW_C'(ptr_r);
        ba_wd_w = val_r[63:56];
      end
      F_MAPW: begin
        bs_we_w = (sub_r == 4'd6);
        bs_wa_w = ptr_r;
        bs_wd_w = val_r[63:56];
      end
      F_STR: bs_ra_w = ptr_r;
      default: ;
    endcase
  end

  // map edit entry stream: 8 bytes per entry from buffer A (defaults) or S
  logic [3:0]  eb_r;
  logic [63:0] ent_acc_r;
  assign mr_ent_o   = ent_acc_r;
  assign mr_ent_v_o = (st_r == X_MRE) && (eb_r == 4'd8);

  // the descriptor field reader: value of `len` bytes at `fld_off_r` from
  // the lanes the store returns, assembled by the machine into aux_r

  logic fl_done_ok_w, fl_giveup_w, fl_err_w, fl_ovf_w, map_ovf_w;
  assign fl_err_w     = ((st_r == F_STR) || (st_r == F_WAIT)) && m_err_i;
  //! the live map set has more mappings than its record has entries (an
  //! output port fans one cluster out to several stream channels): the set
  //! cannot be represented, so it is NOT written and NOT forgotten
  assign map_ovf_w    = (32'(ns_r) >= 32'(cplen_r[15:3]));
  assign fl_ovf_w     = (st_r == F_MAPW) && (sub_r == 4'd4) && (k_r < n_r) && map_ovf_w;
  assign fl_giveup_w  = fl_err_w && (32'(retry_r) >= RETRY_MAX_P);
  assign fl_done_ok_w = (st_r == F_WAIT) && m_done_i && !taint_r;

  // ---- the dirty vector: set wins, cleared only by an untainted done --------
  logic clr_en_w, cur_ev_w;
  assign clr_en_w = fl_done_ok_w || fl_giveup_w;
  for (genvar gs = 0; gs < N_REC_C; gs++) begin : g_dirty
    assign clr_w[gs] = clr_en_w && (cg_r == grp_f(SW_C'(gs)))
                     && (ci_r[7:0] == 8'(gs - base_f(grp_f(SW_C'(gs)))));
    always_ff @(posedge clk_i) begin
      if (!rst_n)         dirty_r[gs] <= 1'b0;
      else if (set_w[gs]) dirty_r[gs] <= 1'b1;
      else if (clr_w[gs]) dirty_r[gs] <= 1'b0;
    end
  end
  //! a change to the record in hand (the taint source)
  assign cur_ev_w = set_w[cur_r];

  // ---- unrepresentable map sets: pending, and skipped until changed ---------
  //! One bit per MAP record. An overflowing set keeps its dirty bit (so the
  //! pending bit keeps saying "accepted and not durable") and is skipped by
  //! the flush scan until the next change to that port re-arms it; a change
  //! on the overflow edge wins, exactly as for the dirty bit.
  logic [N_REC_C-1:0] skip_w, elig_w;
  for (genvar gs = 0; gs < N_REC_C; gs++) begin : g_skip
    if ((gs >= S_MAPI_C) && (gs < S_NAME_C)) begin : g_map
      logic skip_r;
      always_ff @(posedge clk_i) begin
        if (!rst_n)                             skip_r <= 1'b0;
        else if (set_w[gs])                     skip_r <= 1'b0;
        else if (fl_ovf_w && (32'(cur_r) == gs)) skip_r <= 1'b1;
      end
      assign skip_w[gs] = skip_r;
    end else begin : g_none
      assign skip_w[gs] = 1'b0;
    end
  end
  assign elig_w = dirty_r & ~skip_w;

  // ---- debounce (T-NVM-DEBOUNCE, the binding manager's coalescing) ---------
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      deb_open_r <= 1'b0;
      deb_cnt_r  <= 32'd0;
      fl_arm_r   <= 1'b0;
    end else begin
      if (ev_any_w && !deb_open_r) begin
        deb_open_r <= 1'b1;
        deb_cnt_r  <= 32'(DEB_TICKS_P);
      end else if (deb_open_r && tick_i) begin
        if (deb_cnt_r <= 32'd1) begin
          deb_open_r <= 1'b0;
          fl_arm_r   <= 1'b1;
        end else begin
          deb_cnt_r <= deb_cnt_r - 32'd1;
        end
      end
      if ((st_r == F_RUN) && fl_arm_r && !(|elig_w)) fl_arm_r <= 1'b0;
    end
  end

  // ---- sub-sequence helpers ---------------------------------------------------
  // X_BUS issues sb_*_r and returns to ret_r with the answer in val_r (a read)
  // or after the write was taken. A read of the dynamic-state store answers
  // one cycle after the request and keeps answering while it is held, so a
  // gap cycle (X_BUSG) follows every access.
  logic sb_done_w;
  assign sb_done_w = sb_req_r && (sb_we_r ? sb_ready_i : sb_rvalid_i);

  // ---- the machine -------------------------------------------------------------
  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      st_r <= W_INIT; ret_r <= W_INIT; ret2_r <= W_INIT;
      cur_r <= '0; scan_r <= '0; cg_r <= '0; ci_r <= '0; cplen_r <= '0; crid_r <= '0;
      taint_r <= 1'b0; own_r <= 1'b0; alarm_r <= 1'b0; retry_r <= '0; writes_r <= '0;
      ptr_r <= '0; bcnt_r <= '0; crc_r <= '0; rcrc_r <= '0; rver_r <= '0; rrid_r <= '0;
      rplen_r <= '0; val_r <= '0; aux_r <= '0; k_r <= '0; n_r <= '0; na_r <= '0; ns_r <= '0;
      pg_r <= '0; npg_r <= '0; img_bad_r <= 1'b0; rs_fail_r <= 1'b0; rs_done_r <= 1'b0;
      chk_done_r <= 1'b0; rs_app_r <= '0; rs_ref_r <= '0; rs_blank_r <= '0; rs_rev_r <= '0;
      frest_r <= '0; sb_req_r <= 1'b0; sb_we_r <= 1'b0; sb_name_r <= 1'b0; sb_addr_r <= '0;
      sb_wdata_r <= '0; sb_didx_r <= '0; sb_errq_r <= 1'b0; am_req_r <= 1'b0; am_sel_r <= '0;
      mr_req_r <= 1'b0; mr_add_r <= 1'b0; mr_from_a_r <= 1'b0; mr_okq_r <= 1'b0;
      fj_req_r <= 1'b0; fj_fmt_r <= '0; sub_r <= '0; fld_off_r <= '0; m_req_r <= 1'b0;
      m_we_r <= 1'b0; hdr_i_r <= '0; eb_r <= '0; ent_acc_r <= '0; fj_out_o <= 1'b0;
      fj_idx_o <= '0; any_rec_r <= 1'b0;
      rpass_r <= 1'b0;
    end else begin
      // taint: a change to the record in hand after its latch
      if ((st_r == F_ACQ) && !prog_busy_i) taint_r <= 1'b0;
      else if (cur_ev_w && (st_r inside {F_LAT, F_LATN, F_MAPW, F_PAD, F_REL, F_CRC,
                                         F_REQ, F_STR, F_WAIT})) taint_r <= 1'b1;

      unique case (st_r)
        W_INIT:   st_r <= W_WAITGO;
        W_WAITGO: if (restore_go_i) st_r <= R_ACQ;

        // =================== RESTORE ===================
        R_ACQ: if (!prog_busy_i) begin own_r <= 1'b1; st_r <= R_IMG; end
        R_IMG: begin
          if (desc_img_valid_i) begin
            cur_r <= '0; st_r <= R_NEXT;
          end else begin
            //! a LOCATE of ENTITY 0 makes the descriptor store walk the image
            //! the firmware loaded, so the name table holds the image before
            //! any name is written back (KL_aecp_desc_store's heal walk)
            sb_req_r <= 1'b1; sb_we_r <= 1'b0; sb_name_r <= 1'b0;
            sb_addr_r <= {RG_LOC_C, 16'd0}; sb_wdata_r <= 64'd0;
            ret_r <= R_IMGW; st_r <= X_BUS;
          end
        end
        R_IMGW: begin
          img_bad_r <= !desc_img_valid_i;
          cur_r <= '0; st_r <= R_NEXT;
        end
        R_NEXT: begin
          if ((32'(cur_r) == N_REC_C) && !rpass_r) begin
            //! pass 0 found no torn stream: walk again, judging and applying
            rpass_r <= 1'b1; cur_r <= '0;
          end else if (32'(cur_r) == N_REC_C) begin
            st_r <= R_FIN;
          end else if (rpass_r && (32'(cur_r) == S_NAME_C) && !chk_done_r) begin
            //! every format and map is back: re-judge the restored formats
            chk_done_r <= 1'b1; k_r <= 8'd0; st_r <= R_CHK;
          end else begin
            cg_r    <= grp_f(cur_r);
            ci_r    <= 16'(cur_r) - base_f(grp_f(cur_r));
            crid_r  <= ridbase_f(grp_f(cur_r)) + 8'(16'(cur_r) - base_f(grp_f(cur_r)));
            cplen_r <= plen_f(grp_f(cur_r), 8'(16'(cur_r) - base_f(grp_f(cur_r))));
            //! a live change made during the restore wins over the saved value
            st_r <= dirty_r[cur_r] ? R_ADV : R_RD;
          end
        end
        R_RD: begin
          m_req_r <= 1'b1; m_we_r <= 1'b0;
          if (m_req_r && m_gnt_i) begin
            m_req_r <= 1'b0; bcnt_r <= '0; crc_r <= 16'hFFFF; st_r <= R_RS;
          end
        end
        R_RS: begin
          if (m_rvalid_i) begin
            if ((bcnt_r != 17'd6) && (bcnt_r != 17'd7)) crc_r <= crc16_f(crc_r, m_rdata_i);
            if (bcnt_r == 17'd2) rver_r <= m_rdata_i;
            if (bcnt_r == 17'd3) rrid_r <= m_rdata_i;
            if (bcnt_r == 17'd4) rplen_r[15:8] <= m_rdata_i;
            if (bcnt_r == 17'd5) rplen_r[7:0] <= m_rdata_i;
            if (bcnt_r == 17'd6) rcrc_r[15:8] <= m_rdata_i;
            if (bcnt_r == 17'd7) rcrc_r[7:0] <= m_rdata_i;
            bcnt_r <= bcnt_r + 17'd1;
          end
          if (m_done_i || m_err_i) begin
            if (bcnt_r == 17'd0) begin
              //! nothing forwarded: an erased or unframed record, no saved value
              if (rpass_r) rs_blank_r <= rs_blank_r + 8'd1;
              st_r <= R_ADV;
            end else if (m_err_i || (bcnt_r < 17'd8) || (bcnt_r != 17'(rplen_r) + 17'd8)) begin
              //! torn mid-record: the device face misbehaved; stop and say so
              rs_fail_r <= 1'b1; st_r <= R_FIN;
            end else if (!rpass_r) begin
              //! pass 0 proves the stream whole and nothing else
              st_r <= R_ADV;
            end else if ((rver_r != LAYOUT_VER_P) || (rrid_r != crid_r)
                         || (rplen_r != cplen_r) || (crc_r != rcrc_r)) begin
              rs_ref_r <= rs_ref_r + 8'd1; st_r <= R_ADV;
            end else if (img_bad_r) begin
              //! no validated image: nothing can be judged, so nothing applies
              rs_ref_r <= rs_ref_r + 8'd1; any_rec_r <= 1'b1; st_r <= R_ADV;
            end else begin
              ptr_r <= '0; val_r <= '0; sub_r <= 4'd0; any_rec_r <= 1'b1; st_r <= R_VAL;
            end
          end
        end
        R_VAL: begin
          //! assemble a scalar payload (at most 8 bytes) right-justified
          if (is_scalar_w && (32'(ptr_r) < 32'(cplen_r))) begin
            val_r <= {val_r[55:0], bs_rd_w}; ptr_r <= ptr_r + PW_C'(1);
          end else begin
            sub_r <= 4'd0; st_r <= R_AUX;
          end
        end
        R_AUX: begin
          // per-group value judgement, by the rule the SET program applies
          unique case (cg_r)
            4'(G_CFG): begin
              if (sub_r == 4'd0) begin
                sb_req_r <= 1'b1; sb_we_r <= 1'b0; sb_name_r <= 1'b0;
                sb_addr_r <= {RG_NCFG_C, 16'd0}; sub_r <= 4'd1; ret_r <= R_AUX; st_r <= X_BUS;
              end else begin
                //! SET_CONFIGURATION: index < configurations_count
                st_r <= (val_r[15:0] < aux_r[15:0]) ? R_APPLY : R_ADV;
                if (!(val_r[15:0] < aux_r[15:0])) rs_ref_r <= rs_ref_r + 8'd1;
              end
            end
            4'(G_RATE), 4'(G_CLKS): begin
              if (sub_r == 4'd0) begin
                //! LOCATE the AUDIO_UNIT or CLOCK_DOMAIN the record names
                sb_req_r <= 1'b1; sb_we_r <= 1'b0; sb_name_r <= 1'b0;
                sb_addr_r <= {RG_LOC_C, 16'd0};
                sb_wdata_r <= {16'd0, ci_r, (cg_r == 4'(G_RATE)) ? T_AU_C : T_CD_C, 16'd0};
                sub_r <= 4'd1; ret_r <= R_AUX; st_r <= X_BUS;
              end else if (sub_r == 4'd1) begin
                if (sb_errq_r) begin
                  rs_ref_r <= rs_ref_r + 8'd1; st_r <= R_ADV;
                end else begin
                  fld_off_r <= (cg_r == 4'(G_RATE)) ? AU_RATE_OFF_C : (CD_SRCCNT_OFF_C & 16'hFFF8);
                  sb_req_r <= 1'b1; sb_we_r <= 1'b0;
                  sb_addr_r <= {RG_DATA_C, ((cg_r == 4'(G_RATE)) ? AU_RATE_OFF_C
                                                                 : (CD_SRCCNT_OFF_C & 16'hFFF8))};
                  sub_r <= 4'd2; ret_r <= R_AUX; st_r <= X_BUS;
                end
              end else if (sub_r == 4'd2) begin
                if (cg_r == 4'(G_CLKS)) begin
                  //! SET_CLOCK_SOURCE: index < clock_sources_count (@74)
                  st_r <= (val_r[15:0] < aux_r[47:32]) ? R_APPLY : R_ADV;
                  if (!(val_r[15:0] < aux_r[47:32])) rs_ref_r <= rs_ref_r + 8'd1;
                end else if (aux_r[31:16] != SSR_LIST_OFF_C) begin
                  //! the list is not where the SET program's walk reads it
                  rs_ref_r <= rs_ref_r + 8'd1; st_r <= R_ADV;
                end else begin
                  //! SET_SAMPLING_RATE: the rate is on the unit's list
                  n_r <= (aux_r[15:0] > 16'(SSR_WALK_MAX_C)) ? 8'(SSR_WALK_MAX_C) : aux_r[7:0];
                  k_r <= 8'd0; sub_r <= 4'd3;
                end
              end else if (sub_r == 4'd3) begin
                if (k_r >= n_r) begin
                  rs_ref_r <= rs_ref_r + 8'd1; st_r <= R_ADV;
                end else begin
                  sb_req_r <= 1'b1; sb_we_r <= 1'b0;
                  sb_addr_r <= {RG_DATA_C, SSR_LIST_OFF_C + {5'd0, k_r[7:1], 3'd0}};
                  sub_r <= 4'd4; ret_r <= R_AUX; st_r <= X_BUS;
                end
              end else begin
                if ((k_r[0] ? aux_r[31:0] : aux_r[63:32]) == val_r[31:0]) begin
                  st_r <= R_APPLY;
                end else begin
                  k_r <= k_r + 8'd1; sub_r <= 4'd3;
                end
              end
            end
            4'(G_PTOF): begin
              //! SET_STREAM_INFO: the engine refuses an offset with bit 31 set
              st_r <= val_r[31] ? R_ADV : R_APPLY;
              if (val_r[31]) rs_ref_r <= rs_ref_r + 8'd1;
            end
            4'(G_FMTI), 4'(G_FMTO): begin
              if (sub_r == 4'd0) begin
                //! judged on "supported" alone: the maps it will be checked
                //! against are not back yet (page section 8.4)
                fj_out_o <= fmt_out_w; fj_idx_o <= ci_r; fj_fmt_r <= val_r;
                fj_req_r <= 1'b1; sub_r <= 4'd1; ret_r <= R_AUX; st_r <= X_FJ;
              end else begin
                if (aux_r[0]) begin
                  frest_r[(cg_r == 4'(G_FMTO)) ? (N_STREAM_IN_P + 32'(ci_r)) : 32'(ci_r)] <= 1'b1;
                  st_r <= R_APPLY;
                end else begin
                  rs_ref_r <= rs_ref_r + 8'd1; st_r <= R_ADV;
                end
              end
            end
            4'(G_MAPI), 4'(G_MAPO): begin
              //! count the saved entries (all-0xFF is an unused entry)
              ns_r <= 8'd0; k_r <= 8'd0; ptr_r <= '0; eb_r <= '0; st_r <= R_MA;
              sub_r <= 4'd0; na_r <= 8'd0; pg_r <= 16'd0; npg_r <= 16'd0;
            end
            default: begin
              ptr_r <= '0; k_r <= 8'd0; eb_r <= '0; st_r <= R_NAMEW;
            end
          endcase
        end
        R_APPLY: begin
          //! write the value back with its valid flag; not a change
          if (sub_r != 4'd15) begin
            sb_req_r <= 1'b1; sb_we_r <= 1'b1; sb_name_r <= 1'b0;
            sb_addr_r <= {RG_DYN_C, sel_f(cg_r), 3'b000};
            sb_didx_r <= (cg_r == 4'(G_CFG)) ? 16'd0 : ci_r;
            sb_wdata_r <= val_r; sub_r <= 4'd15; ret_r <= R_APPLY; st_r <= X_BUS;
          end else begin
            rs_app_r <= rs_app_r + 8'd1; st_r <= R_ADV;
          end
        end
        R_NAMEW: begin
          //! eight lane writes into the writable name table, big-endian lanes
          if (k_r == 8'd8) begin
            rs_app_r <= rs_app_r + 8'd1; st_r <= R_ADV;
          end else if (eb_r != 4'd8) begin
            val_r <= {val_r[55:0], bs_rd_w}; ptr_r <= ptr_r + PW_C'(1); eb_r <= eb_r + 4'd1;
          end else begin
            sb_req_r <= 1'b1; sb_we_r <= 1'b1; sb_name_r <= 1'b1;
            sb_addr_r <= {4'h0, ci_r[9:0], k_r[2:0], 3'b000};
            sb_wdata_r <= val_r; eb_r <= 4'd0; k_r <= k_r + 8'd1;
            ret_r <= R_NAMEW; st_r <= X_BUS;
          end
        end
        // ---- a map record: capture defaults, remove, add saved, fall back ----
        R_MA: begin
          //! walk the port's CURRENT (image-default) set into buffer A
          if (sub_r == 4'd0) begin
            am_sel_r <= 2'd0; pg_r <= 16'd0; am_req_r <= 1'b1; ret2_r <= R_MA;
            sub_r <= 4'd1; st_r <= X_AM;
          end else if (sub_r == 4'd1) begin
            npg_r <= aux_r[15:0]; pg_r <= 16'd0; sub_r <= 4'd2;
          end else if (sub_r == 4'd2) begin
            if (pg_r >= npg_r) begin
              //! buffer A holds na_r entries; now count the saved set
              ptr_r <= '0; k_r <= 8'd0; ns_r <= 8'd0; sub_r <= 4'd6;
            end else begin
              am_sel_r <= 2'd1; am_req_r <= 1'b1; ret2_r <= R_MA; sub_r <= 4'd3; st_r <= X_AM;
            end
          end else if (sub_r == 4'd3) begin
            n_r <= aux_r[7:0]; k_r <= 8'd0; sub_r <= 4'd4;
          end else if (sub_r == 4'd4) begin
            if (k_r >= n_r) begin
              pg_r <= pg_r + 16'd1; sub_r <= 4'd2;
            end else begin
              am_sel_r <= 2'd2; am_req_r <= 1'b1; ret2_r <= R_MA; sub_r <= 4'd5; st_r <= X_AM;
            end
          end else if (sub_r == 4'd5) begin
            //! store the entry, 8 bytes, at na_r * 8
            if (eb_r == 4'd0) begin
              val_r <= aux_r; ptr_r <= PW_C'({na_r, 3'd0}); eb_r <= 4'd1;
            end else if (eb_r != 4'd9) begin
              val_r <= {val_r[55:0], 8'd0}; ptr_r <= ptr_r + PW_C'(1); eb_r <= eb_r + 4'd1;
            end else begin
              eb_r <= 4'd0; na_r <= na_r + 8'd1; k_r <= k_r + 8'd1; sub_r <= 4'd4;
            end
          end else if (sub_r == 4'd6) begin
            //! the saved set: entries of the record whose first byte pair is
            //! not 0xFFFF; they are packed at the head by the flush
            if (32'(k_r) >= 32'(cplen_r[15:3])) begin
              mr_add_r <= 1'b0; mr_from_a_r <= 1'b1; ret_r <= R_MS; st_r <= X_MRH;
            end else begin
              ptr_r <= PW_C'({k_r, 3'd0}); sub_r <= 4'd7;
            end
          end else begin
            if (bs_rd_w != 8'hFF) ns_r <= k_r + 8'd1;
            k_r <= k_r + 8'd1; sub_r <= 4'd6;
          end
        end
        R_MS: begin
          //! the defaults are removed: ADD the saved set, judged whole
          if (!mr_okq_r) begin
            rs_fail_r <= 1'b1; st_r <= R_ADV;
          end else begin
            mr_add_r <= 1'b1; mr_from_a_r <= 1'b0; ret_r <= R_MV; st_r <= X_MRH;
          end
        end
        R_MV: begin
          if (mr_okq_r) begin
            rs_app_r <= rs_app_r + 8'd1; st_r <= R_ADV;
          end else begin
            //! refused: revert each restored format the defaults map to, then
            //! put the defaults back
            rs_ref_r <= rs_ref_r + 8'd1; k_r <= 8'd0; sub_r <= 4'd0; st_r <= R_MVW;
          end
        end
        R_MVW: begin
          if (sub_r == 4'd0) begin
            if (k_r >= na_r) begin
              mr_add_r <= 1'b1; mr_from_a_r <= 1'b1; ret_r <= R_MD; st_r <= X_MRH;
            end else begin
              ptr_r <= PW_C'({k_r, 3'd0}); sub_r <= 4'd1;
            end
          end else if (sub_r == 4'd1) begin
            val_r[15:8] <= ba_rd_w; ptr_r <= ptr_r + PW_C'(1); sub_r <= 4'd2;
          end else if (sub_r == 4'd2) begin
            val_r[7:0] <= ba_rd_w; sub_r <= 4'd3;
          end else if (sub_r == 4'd3) begin
            if ((32'(val_r[15:0]) < (fmt_out_w ? N_STREAM_OUT_P : N_STREAM_IN_P))
                && frest_r[fmt_out_w ? (N_STREAM_IN_P + 32'(val_r[15:0])) : 32'(val_r[15:0])]) begin
              //! LOCATE the stream and write its image-default current_format
              aux_r <= {48'd0, val_r[15:0]};
              sb_req_r <= 1'b1; sb_we_r <= 1'b0; sb_name_r <= 1'b0;
              sb_addr_r <= {RG_LOC_C, 16'd0};
              sb_wdata_r <= {16'd0, val_r[15:0], fmt_out_w ? T_SO_C : T_SI_C, 16'd0};
              sub_r <= 4'd4; ret_r <= R_MVW; st_r <= X_BUS;
            end else begin
              k_r <= k_r + 8'd1; sub_r <= 4'd0;
            end
          end else if (sub_r == 4'd4) begin
            fld_off_r <= val_r[15:0];  // keep the stream index
            sb_req_r <= 1'b1; sb_we_r <= 1'b0;
            sb_addr_r <= {RG_DATA_C, SI_CURFMT_OFF_C & 16'hFFF8};
            sub_r <= 4'd5; ret_r <= R_MVW; st_r <= X_BUS;
          end else if (sub_r == 4'd5) begin
            val_r[63:16] <= aux_r[47:0];   // bytes 74..79 of lane 72
            sb_req_r <= 1'b1; sb_we_r <= 1'b0;
            sb_addr_r <= {RG_DATA_C, (SI_CURFMT_OFF_C & 16'hFFF8) + 16'd8};
            sub_r <= 4'd6; ret_r <= R_MVW; st_r <= X_BUS;
          end else if (sub_r == 4'd6) begin
            val_r[15:0] <= aux_r[63:48];   // bytes 80..81 of lane 80
            sub_r <= 4'd7;
          end else if (sub_r == 4'd7) begin
            sb_req_r <= 1'b1; sb_we_r <= 1'b1; sb_name_r <= 1'b0;
            sb_addr_r <= {RG_DYN_C, fmt_out_w ? 13'd4 : 13'd3, 3'b000};
            sb_didx_r <= fld_off_r; sb_wdata_r <= val_r;
            frest_r[fmt_out_w ? (N_STREAM_IN_P + 32'(fld_off_r)) : 32'(fld_off_r)] <= 1'b0;
            rs_rev_r <= rs_rev_r + 8'd1;
            sub_r <= 4'd8; ret_r <= R_MVW; st_r <= X_BUS;
          end else begin
            k_r <= k_r + 8'd1; sub_r <= 4'd0;
          end
        end
        R_MD: begin
          //! the image defaults must validate; if not, the image is broken
          if (!mr_okq_r) rs_fail_r <= 1'b1;
          st_r <= R_ADV;
        end
        R_CHK: begin
          //! a restored format that orphans a mapped channel goes back to the
          //! image default (the orphan rule, judged on the final maps)
          if (32'(k_r) >= N_STREAM_IN_P + N_STREAM_OUT_P) begin
            st_r <= R_NEXT;
          end else if (!frest_r[FW_C'(k_r)]) begin
            k_r <= k_r + 8'd1;
          end else begin
            cg_r <= (32'(k_r) < N_STREAM_IN_P) ? 4'(G_FMTI) : 4'(G_FMTO);
            ci_r <= (32'(k_r) < N_STREAM_IN_P) ? 16'(k_r) : 16'(32'(k_r) - N_STREAM_IN_P);
            sb_req_r <= 1'b1; sb_we_r <= 1'b0; sb_name_r <= 1'b0;
            sb_addr_r <= {RG_DYN_C, (32'(k_r) < N_STREAM_IN_P) ? 13'd3 : 13'd4, 3'b000};
            sb_didx_r <= (32'(k_r) < N_STREAM_IN_P) ? 16'(k_r) : 16'(32'(k_r) - N_STREAM_IN_P);
            sub_r <= 4'd0; ret_r <= R_CHKJ; st_r <= X_BUS;
          end
        end
        R_CHKJ: begin
          if (sub_r == 4'd0) begin
            fj_out_o <= (cg_r == 4'(G_FMTO)); fj_idx_o <= ci_r; fj_fmt_r <= aux_r;
            fj_req_r <= 1'b1; sub_r <= 4'd1; ret_r <= R_CHKJ; st_r <= X_FJ;
          end else if (sub_r == 4'd1) begin
            if (aux_r[1]) begin
              k_r <= k_r + 8'd1; st_r <= R_CHK;
            end else begin
              //! revert: LOCATE the stream, read current_format, write it
              sb_req_r <= 1'b1; sb_we_r <= 1'b0;
              sb_addr_r <= {RG_LOC_C, 16'd0};
              sb_wdata_r <= {16'd0, ci_r, (cg_r == 4'(G_FMTO)) ? T_SO_C : T_SI_C, 16'd0};
              sub_r <= 4'd2; ret_r <= R_CHKJ; st_r <= X_BUS;
            end
          end else if (sub_r == 4'd2) begin
            sb_req_r <= 1'b1; sb_we_r <= 1'b0;
            sb_addr_r <= {RG_DATA_C, SI_CURFMT_OFF_C & 16'hFFF8};
            sub_r <= 4'd3; ret_r <= R_CHKJ; st_r <= X_BUS;
          end else if (sub_r == 4'd3) begin
            val_r[63:16] <= aux_r[47:0];
            sb_req_r <= 1'b1; sb_we_r <= 1'b0;
            sb_addr_r <= {RG_DATA_C, (SI_CURFMT_OFF_C & 16'hFFF8) + 16'd8};
            sub_r <= 4'd4; ret_r <= R_CHKJ; st_r <= X_BUS;
          end else if (sub_r == 4'd4) begin
            val_r[15:0] <= aux_r[63:48]; sub_r <= 4'd5;
          end else if (sub_r == 4'd5) begin
            sb_req_r <= 1'b1; sb_we_r <= 1'b1; sb_name_r <= 1'b0;
            sb_addr_r <= {RG_DYN_C, (cg_r == 4'(G_FMTO)) ? 13'd4 : 13'd3, 3'b000};
            sb_didx_r <= ci_r; sb_wdata_r <= val_r;
            frest_r[FW_C'(k_r)] <= 1'b0; rs_rev_r <= rs_rev_r + 8'd1;
            sub_r <= 4'd6; ret_r <= R_CHKJ; st_r <= X_BUS;
          end else begin
            k_r <= k_r + 8'd1; st_r <= R_CHK;
          end
        end
        R_ADV: begin
          cur_r <= cur_r + SW_C'(1); st_r <= R_NEXT;
        end
        R_FIN: begin
          own_r <= 1'b0; rs_done_r <= 1'b1; st_r <= F_RUN;
        end

        // =================== STEADY STATE ===================
        F_RUN: begin
          if (fl_arm_r && (|elig_w)) begin
            //! scan for a dirty record, one slot per cycle
            if (elig_w[scan_r]) begin
              cur_r <= scan_r; retry_r <= 8'd0; st_r <= F_ACQ;
            end
            scan_r <= (32'(scan_r) + 1 >= N_REC_C) ? '0 : scan_r + SW_C'(1);
          end
        end
        F_ACQ: begin
          cg_r    <= grp_f(cur_r);
          ci_r    <= 16'(cur_r) - base_f(grp_f(cur_r));
          crid_r  <= ridbase_f(grp_f(cur_r)) + 8'(16'(cur_r) - base_f(grp_f(cur_r)));
          cplen_r <= plen_f(grp_f(cur_r), 8'(16'(cur_r) - base_f(grp_f(cur_r))));
          //! the latch happens only between AECP programs, and no program is
          //! dispatched until it is complete
          if (!prog_busy_i) begin
            own_r <= 1'b1; ptr_r <= '0; sub_r <= 4'd0; eb_r <= '0; k_r <= 8'd0;
            st_r <= (grp_f(cur_r) == 4'(G_NAME)) ? F_LATN
                  : ((grp_f(cur_r) == 4'(G_MAPI)) || (grp_f(cur_r) == 4'(G_MAPO))) ? F_MAPW
                  : F_LAT;
          end
        end
        F_LAT: begin
          //! one read of the scalar, then its bytes into the buffer
          if (sub_r == 4'd0) begin
            sb_req_r <= 1'b1; sb_we_r <= 1'b0; sb_name_r <= 1'b0;
            sb_addr_r <= {RG_DYN_C, sel_f(cg_r), 3'b000};
            sb_didx_r <= (cg_r == 4'(G_CFG)) ? 16'd0 : ci_r;
            sub_r <= 4'd15; ret_r <= F_LAT; st_r <= X_BUS;
          end else if (sub_r == 4'd15) begin
            //! left-justify the cplen_r bytes of the value
            val_r <= aux_r << (7'd64 - {cplen_r[3:0], 3'd0});
            ptr_r <= '0; sub_r <= 4'd1;
          end else if (32'(ptr_r) + 1 < 32'(cplen_r)) begin
            val_r <= {val_r[55:0], 8'd0}; ptr_r <= ptr_r + PW_C'(1);
          end else begin
            st_r <= F_REL;
          end
        end
        F_LATN: begin
          //! eight lane reads of the name
          if (sub_r == 4'd0) begin
            if (k_r == 8'd8) begin
              st_r <= F_REL;
            end else begin
              sb_req_r <= 1'b1; sb_we_r <= 1'b0; sb_name_r <= 1'b1;
              sb_addr_r <= {4'h0, ci_r[9:0], k_r[2:0], 3'b000};
              sub_r <= 4'd15; ret_r <= F_LATN; st_r <= X_BUS;
            end
          end else if (sub_r == 4'd15) begin
            val_r <= aux_r; ptr_r <= PW_C'({k_r, 3'd0}); eb_r <= 4'd0; sub_r <= 4'd1;
          end else if (eb_r != 4'd7) begin
            val_r <= {val_r[55:0], 8'd0}; ptr_r <= ptr_r + PW_C'(1); eb_r <= eb_r + 4'd1;
          end else begin
            k_r <= k_r + 8'd1; sub_r <= 4'd0;
          end
        end
        F_MAPW: begin
          //! the port's live set over the GET_AUDIO_MAP face, packed at the
          //! head of the record, then padded with unused (0xFF) entries
          if (sub_r == 4'd0) begin
            am_sel_r <= 2'd0; pg_r <= 16'd0; am_req_r <= 1'b1; ns_r <= 8'd0;
            ret2_r <= F_MAPW; sub_r <= 4'd1; st_r <= X_AM;
          end else if (sub_r == 4'd1) begin
            npg_r <= aux_r[15:0]; pg_r <= 16'd0; sub_r <= 4'd2;
          end else if (sub_r == 4'd2) begin
            if (pg_r >= npg_r) begin
              ptr_r <= PW_C'({ns_r, 3'd0}); st_r <= F_PAD;
            end else begin
              am_sel_r <= 2'd1; am_req_r <= 1'b1; ret2_r <= F_MAPW; sub_r <= 4'd3; st_r <= X_AM;
            end
          end else if (sub_r == 4'd3) begin
            n_r <= aux_r[7:0]; k_r <= 8'd0; sub_r <= 4'd4;
          end else if (sub_r == 4'd4) begin
            if (k_r >= n_r) begin
              pg_r <= pg_r + 16'd1; sub_r <= 4'd2;
            end else if (map_ovf_w) begin
              //! more mappings than the record has entries: it cannot be
              //! persisted, and part of it must never be saved. The record
              //! stays dirty (pending) and is skipped until it changes.
              own_r <= 1'b0; st_r <= F_RUN;
            end else begin
              am_sel_r <= 2'd2; am_req_r <= 1'b1; ret2_r <= F_MAPW; sub_r <= 4'd5; st_r <= X_AM;
            end
          end else if (sub_r == 4'd5) begin
            val_r <= aux_r; ptr_r <= PW_C'({ns_r, 3'd0}); eb_r <= 4'd0; sub_r <= 4'd6;
          end else if (sub_r == 4'd6) begin
            if (eb_r != 4'd7) begin
              val_r <= {val_r[55:0], 8'd0}; ptr_r <= ptr_r + PW_C'(1); eb_r <= eb_r + 4'd1;
            end else begin
              ns_r <= ns_r + 8'd1; k_r <= k_r + 8'd1; sub_r <= 4'd4;
            end
          end
        end
        F_PAD: begin
          if (32'(ptr_r) + 1 >= 32'(cplen_r)) st_r <= F_REL;
          if (32'(ptr_r) < 32'(cplen_r)) ptr_r <= ptr_r + PW_C'(1);
        end
        F_REL: begin
          //! the latch is complete: programs may run again
          own_r <= 1'b0; crc_r <= 16'hFFFF; hdr_i_r <= 5'd0; ptr_r <= '0; st_r <= F_CRC;
        end
        F_CRC: begin
          //! header without its crc field, then the payload from the buffer
          if (hdr_i_r < 5'd6) begin
            crc_r <= crc16_f(crc_r, hdr_byte_w); hdr_i_r <= hdr_i_r + 5'd1;
          end else if (32'(ptr_r) < 32'(cplen_r)) begin
            crc_r <= crc16_f(crc_r, bs_rd_w); ptr_r <= ptr_r + PW_C'(1);
          end else begin
            hdr_i_r <= 5'd0; ptr_r <= '0; st_r <= F_REQ;
          end
        end
        F_REQ: begin
          m_req_r <= 1'b1; m_we_r <= 1'b1;
          if (m_req_r && m_gnt_i) begin
            m_req_r <= 1'b0; st_r <= F_STR;
          end
        end
        F_STR: begin
          if (m_err_i) begin
            if (32'(retry_r) >= RETRY_MAX_P) begin
              alarm_r <= 1'b1; st_r <= F_RUN;
            end else begin
              retry_r <= retry_r + 8'd1; st_r <= F_ACQ;
            end
          end else if (m_wready_i) begin
            if (!hdr_i_r[3]) begin
              if (hdr_i_r[2:0] == 3'd7) begin
                hdr_i_r <= 5'd8;
                if (cplen_r == 16'd0) st_r <= F_WAIT;
              end else hdr_i_r <= hdr_i_r + 5'd1;
            end else begin
              if (32'(ptr_r) + 1 >= 32'(cplen_r)) st_r <= F_WAIT;
              ptr_r <= ptr_r + PW_C'(1);
            end
          end
        end
        F_WAIT: begin
          if (m_done_i) begin
            writes_r <= writes_r + 16'd1; st_r <= F_RUN;
          end else if (m_err_i) begin
            if (32'(retry_r) >= RETRY_MAX_P) begin
              alarm_r <= 1'b1; st_r <= F_RUN;
            end else begin
              retry_r <= retry_r + 8'd1; st_r <= F_ACQ;
            end
          end
        end

        // =================== SUB-SEQUENCES ===================
        X_BUS: begin
          if (sb_done_w) begin
            sb_req_r <= 1'b0;
            if (!sb_we_r) begin aux_r <= sb_rdata_i; sb_errq_r <= sb_err_i; end
            st_r <= X_BUSG;
          end
        end
        X_BUSG: st_r <= ret_r;
        X_AM: begin
          if (am_req_r && !am_wait_i) begin
            aux_r <= am_data_i; am_req_r <= 1'b0; st_r <= ret2_r;
          end
        end
        X_MRH: begin
          //! stage a set on the edit face: header, then the entries
          mr_req_r <= 1'b1; k_r <= 8'd0; eb_r <= 4'd0; ptr_r <= '0; st_r <= X_MRE;
        end
        X_MRE: begin
          if (k_r >= (mr_from_a_r ? na_r : ns_r)) begin
            st_r <= X_MRW;
          end else if (eb_r != 4'd8) begin
            ent_acc_r <= {ent_acc_r[55:0], mr_from_a_r ? ba_rd_w : bs_rd_w};
            ptr_r <= ptr_r + PW_C'(1); eb_r <= eb_r + 4'd1;
          end else if (mr_ent_rdy_i) begin
            eb_r <= 4'd0; k_r <= k_r + 8'd1;
          end
        end
        X_MRW: begin
          if (mr_done_i) begin
            mr_req_r <= 1'b0; mr_okq_r <= mr_ok_i; st_r <= ret_r;
          end
        end
        X_FJ: begin
          if (fj_req_r && !fj_wait_i) begin
            aux_r <= {62'd0, fj_data_i}; fj_req_r <= 1'b0; st_r <= ret_r;
          end
        end
        default: st_r <= F_RUN;
      endcase
    end
  end

  //! the low address bits carry no field, and a cluster count never
  //! reaches 256 ports
  logic unused_ok_w;
  assign unused_ok_w = ^{u_addr_i[2:0]};

endmodule

`default_nettype wire

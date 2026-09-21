/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : d3_top.sv   (design evidence, milan-fpga #500, scope D3)
//
//  Description : The RTL half of the D3 co-simulation. REAL, at the pinned
//                processor revision 424c688f: KL_aecp_dyn_state (the
//                dynamic-state store) and KL_aecp_desc_store (the descriptor
//                store and its writable name table, walking a real AEMI
//                image the firmware copies into the model's DDR).
//                SHIPPING: hdl/milan/KL_nvm_backend.sv at dev 07294a76.
//                AMENDED PROTOTYPES of two pinned modules (revision c), each
//                the pinned file with declared amendments only (run.py
//                checks it): KL_pp_nvm_port_amd, the port with its terminal
//                cause (seam S1), and KL_acmp_nvm_shadow_amd, the binding
//                manager consuming that cause and bounding its restore walk
//                (seams S1 and S3). PROTOTYPE: KL_aecp_nvm_writer (the D3
//                record writer), KL_pp_nvm_mgr_arb (two managers, one port,
//                the drain of either manager's abandoned read),
//                KL_aecp_desc_mem_guard (response isolation on the
//                descriptor store's memory face, seam S2) and
//                KL_pp_acmp_lsn_admit (boot-owned listener admission, seam
//                S4). Under D3_TRACKED the PINNED port and binding manager are
//                instantiated, as the parent ships them, with no guard and no
//                admission gate.
//
//                THE LISTENER IS REAL (revision d): the pinned
//                KL_pp_acmp_listener, UNCHANGED, with the pinned
//                KL_pp_timer_service on its arm and expiry faces. The binding
//                manager's preload drives its pre_* face and waits on its own
//                pre_ready_o; its record-write port is the binding manager's
//                capture face. Its work faces are driven by the harness's
//                producers (the dispatch head, the event router, the AECP
//                START/STOP holder and injected expiries), through the gate
//                except under D3_TRACKED. The harness capture BFM (cap_*)
//                stays, ORed behind the listener's own writes, as the
//                processor's acmp_nvm suite keeps its tb_cap_* face.
//
//                D3_STAGE1 (a build define) is stage 1's roll-back scope: the
//                dynamic-state store and the descriptor store, and NOT the
//                parent's map plane (stage 3's owner).
//
//                The uCPU is a bus-functional model on the state bus
//                (ub_*), with the dispatch hold-off the page specifies: it
//                starts no program while the writer owns the bus (own_o),
//                and the writer takes the bus only while no program runs
//                (prog_busy_i). The channel-map store, the GET_AUDIO_MAP
//                read face, the map edit face and the format judge are a
//                C++ model of the parent's map plane (d3_bridge.cpp).
//
//                The parent glue is TRANSCRIBED from hdl/milan/KL_pp_shadow.sv
//                with the change the page specifies: the D3 writer's
//                unflushed level REPLACES aecp_dyn_dirty_o and the sticky
//                class-6/7 mark bit in pend_i, and the processor's restore
//                done is the AND of the two walks.
//
//                THE ENTITY ENABLE is released by the restore (processor
//                F07.9, "release entity_enable"): the enable the firmware
//                requests (PP_CTRL[0] OR ADP_CTRL[0]) reaches the entity only
//                once the restore of both walks is done, entity_en_o. A
//                restore that never reaches done keeps the entity dark.
//
//                THE ROLL-BACK (page section 8.6): the writer's rb_rst_o
//                resets the dynamic-state store and the descriptor store as a
//                reset would (the store walks the image again, so its names
//                are the image's), and map_rst_o asks the C++ map plane for
//                its reset sets. The product needs one soft-reset input on
//                each owner; the model uses their rst_n.
//
//                HARNESS-ONLY FACES, not product wiring: lend_bus_i lends the
//                state bus to the uCPU BFM BEFORE the restore starts (the
//                stale-store control seeds rows through it; the writer owns
//                the bus from reset), and the pk_* peek ports read the
//                dynamic-state rows and the name table through the hierarchy
//                for the cleared-first checks, without the bus. Revision d
//                adds lt_exp_inj_i (an expiry injected on the timer bus in a
//                cycle the timer service is quiet) and the lt_* observation
//                ports, which read the listener's state, holder and pending
//                expiries through the hierarchy.
//
//                D3_TRACKED (a build define) is the glue AS IT SHIPS at dev
//                07294a76: no D3 writer, pend_i = aecp_dyn_dirty_o OR the
//                binding manager's unflushed sinks OR the sticky class-6/7
//                mark bit, the restore is the binding walk alone, the enable
//                is not gated, and the port and the binding manager are the
//                pinned ones. It is what "what reproduces today" runs against.
//---------------------------------------------------------------------------//
`default_nettype none

module d3_top
  import pp_acmp_pkg::*;
#(
    parameter int unsigned CLK_HZ_P       = 1_000_000,
    parameter int unsigned N_STREAM_IN_P  = 2,
    parameter int unsigned N_STREAM_OUT_P = 2,
    parameter int unsigned N_SPORT_IN_P   = 1,
    parameter int unsigned N_SPORT_OUT_P  = 1,
    parameter int unsigned N_AUDIO_UNIT_P = 1,
    parameter int unsigned N_CLK_DOM_P    = 1,
    parameter int unsigned N_NAME_P       = 30,
    parameter logic [8*N_SPORT_IN_P-1:0]  MAPI_CLS_P = '0,
    parameter logic [8*N_SPORT_OUT_P-1:0] MAPO_CLS_P = '0,
    parameter int unsigned MAP_ENT_MAX_P  = 17,
    parameter int unsigned IDX_ENTRIES_P  = 32,
    parameter int unsigned D3_DEB_TICKS_P = 500,
    parameter int unsigned T_HOLD_MS_P    = 50,
    //! the D3 restore watchdog, cycles: 20 ms at the model's 1 MHz
    parameter int unsigned D3_RS_TMO_CYC_P = 20000,
    //! the listener's transition ROM, generated by the pinned
    //! hdl/acmp/rom/gen_ltn_rom.py into the build tree
    parameter string       LTN_ROM_P      = "ltn_rom.hex"
) (
    input  wire         clk_i,
    input  wire         rst_n,

    //! ---- listener record-write BFM -> the real binding manager ---------
    input  wire         cap_wr_i,
    input  wire  [7:0]  cap_sink_i,
    input  wire         cap_bound_i,
    input  wire         cap_started_i,
    input  wire         cap_sw_i,
    input  wire  [15:0] cap_uid_i,
    input  wire  [63:0] cap_teid_i,
    input  wire  [63:0] cap_ceid_i,

    //! ---- the pinned listener's work faces: the harness's producers --------
    //! a dispatch transaction (the ACMP head the scoreboard admits)
    input  wire         lt_txn_valid_i,
    input  wire  [3:0]  lt_txn_msg_i,
    input  wire  [4:0]  lt_txn_status_i,
    input  wire  [63:0] lt_txn_target_i,
    input  wire  [63:0] lt_txn_ctlr_i,
    input  wire  [15:0] lt_txn_seq_i,
    input  wire  [15:0] lt_txn_uid_i,
    input  wire  [2:0]  lt_txn_slot_i,
    output logic        lt_txn_ready_o,     //! the producer's pop
    output logic        lt_txn_take_o,      //! the LISTENER took it (its valid AND ready)
    //! a talker event (the event router's sticky presentation)
    input  wire         lt_tk_valid_i,
    input  wire  [1:0]  lt_tk_kind_i,
    input  wire         lt_tk_failed_i,
    input  wire  [15:0] lt_tk_sink_i,
    output logic        lt_tk_ready_o,      //! the router's ack
    output logic        lt_tk_take_o,       //! the LISTENER took it
    //! a START/STOP request (the AECP engine holds it until completion)
    input  wire         lt_strm_valid_i,
    input  wire  [15:0] lt_strm_sink_i,
    input  wire         lt_strm_val_i,
    output logic        lt_strm_ready_o,    //! the listener's completion
    output logic        lt_strm_error_o,
    output logic        lt_strm_take_o,     //! the LISTENER captured it into its holder
    //! an injected expiry on the timer bus (a cycle the timer service is quiet)
    input  wire         lt_exp_inj_i,
    input  wire  [7:0]  lt_exp_owner_i,
    output logic        lt_exp_take_o,      //! an expiry of a listener owner reached it
    //! the RX slot read face, the TX slot face and the PRNG, served by models
    output logic        lt_rxs_rd_en_o,
    output logic [1:0]  lt_rxs_rd_slot_o,
    output logic [9:0]  lt_rxs_rd_addr_o,
    input  wire  [7:0]  lt_rxs_rd_data_i,
    output logic        lt_rxs_free_o,
    output logic        lt_txs_alloc_o,
    input  wire         lt_txs_gnt_i,
    output logic        lt_txs_wr_o,
    output logic [10:0] lt_txs_addr_o,
    output logic [7:0]  lt_txs_data_o,
    output logic        lt_txreq_o,
    output logic        lt_draw_req_o,
    input  wire         lt_draw_valid_i,
    input  wire  [15:0] lt_draw_ms_i,
    //! observation of the listener and the gate
    output logic        lt_own_o,           //! the gate owns the listener's faces
    output logic        lt_released_o,      //! the binding walk's drained terminal
    output logic [4:0]  lt_state_o,         //! the listener's xs_r (hierarchy)
    output logic        lt_pend_any_o,      //! a pending expiry (hierarchy)
    output logic        lt_strq_pend_o,     //! its START/STOP holder (hierarchy)
    output logic        lt_recwr_o,         //! a record write, its sink and fields
    output logic [7:0]  lt_recwr_sink_o,
    output logic        lt_rec_bound_o,
    output logic        lt_rec_started_o,
    output logic        lt_rec_sw_o,
    output logic [63:0] lt_rec_teid_o,
    output logic [2:0]  lt_rec_sm_o,
    output logic        lt_arm_o,           //! A4: arm discovery, its sink and talker
    output logic [63:0] lt_arm_eid_o,
    output logic [7:0]  lt_act_sink_o,
    output logic [6:0]  lt_side_o,          //! timer arm, TX alloc, RX free, settle,
                                            //! teardown, disarm, notify
    output logic [15:0] lt_exp_drop_o,      //! the gate's dropped expiries
    output logic        lt_tm_exp_o,        //! the timer service fired (an injection loses)

    //! ---- the uCPU BFM on the state bus ------------------------------------
    input  wire         prog_busy_i,
    input  wire         ub_req_i,
    input  wire         ub_we_i,
    input  wire         ub_name_i,
    input  wire  [19:0] ub_addr_i,
    input  wire  [63:0] ub_wdata_i,
    input  wire  [15:0] ub_didx_i,
    output logic        ub_ready_o,
    output logic        ub_rvalid_o,
    output logic [63:0] ub_rdata_o,
    output logic        ub_err_o,
    output logic        own_o,
    //! the commit mark a program raises (class and command descriptor), and
    //! the map edit face's commit-one-record beat the map model applies
    input  wire         mk_stb_i,
    input  wire  [7:0]  mk_mark_i,
    input  wire  [15:0] mk_type_i,
    input  wire  [15:0] mk_idx_i,
    input  wire         me_stb_i,
    input  wire  [15:0] me_type_i,
    input  wire  [15:0] me_idx_i,

    //! ---- PP_CTRL[1] ----------------------------------------------------------
    input  wire         restore_go_i,
    //! ---- PP_CTRL[0] OR ADP_CTRL[0]: the enable the firmware requests --------
    input  wire         en_req_i,
    output logic        entity_en_o,    //! the enable the entity sees
    //! harness knob: hold the writer's change snoop off, every source of it
    //! (the stale-store control seeds rows, names and map sets through it)
    input  wire         snoop_off_i,
    //! harness knob: lend the state bus to the uCPU BFM before the restore
    input  wire         lend_bus_i,
    //! the roll-back's request to the map plane (the C++ model)
    output logic        map_rst_o,
    //! harness peeks (observation only)
    input  wire  [3:0]  pk_sel_i,
    input  wire  [15:0] pk_idx_i,
    output logic [63:0] pk_val_o,
    output logic        pk_v_o,
    input  wire  [15:0] pk_lane_i,
    output logic [63:0] pk_name_o,

    //! ---- the descriptor store's memory face, to the C++ DDR model --------
    output logic        dm_req_valid_o,
    input  wire         dm_req_ready_i,
    output logic [31:0] dm_req_addr_o,
    output logic [8:0]  dm_req_beats_o,
    input  wire         dm_rsp_valid_i,
    input  wire  [63:0] dm_rsp_data_i,
    input  wire         dm_rsp_last_i,
    input  wire         dm_rsp_err_i,

    //! ---- the map plane faces, to the C++ map model -------------------------
    output logic        am_req_o,
    output logic [15:0] am_type_o,
    output logic [15:0] am_idx_o,
    output logic [15:0] am_map_o,
    output logic [1:0]  am_sel_o,
    output logic [7:0]  am_rec_o,
    input  wire  [63:0] am_data_i,
    input  wire         am_wait_i,
    output logic        mr_req_o,
    output logic        mr_add_o,
    output logic [15:0] mr_type_o,
    output logic [15:0] mr_idx_o,
    output logic [7:0]  mr_cnt_o,
    output logic        mr_ent_v_o,
    output logic [63:0] mr_ent_o,
    input  wire         mr_ent_rdy_i,
    input  wire         mr_done_i,
    input  wire         mr_ok_i,
    output logic        fj_req_o,
    output logic        fj_out_o,
    output logic [15:0] fj_idx_o,
    output logic [63:0] fj_fmt_o,
    input  wire         fj_wait_i,
    input  wire  [1:0]  fj_data_i,

    //! ---- the backend's memory face, to the C++ memory model -------------
    output logic        mem_req_valid_o,
    input  wire         mem_req_ready_i,
    output logic [31:0] mem_req_addr_o,
    output logic [8:0]  mem_req_beats_o,
    input  wire         mem_rsp_valid_i,
    output logic        mem_rsp_ready_o,
    input  wire  [63:0] mem_rsp_data_i,
    input  wire         mem_rsp_last_i,
    input  wire         mem_rsp_err_i,
    output logic        mem_wr_valid_o,
    input  wire         mem_wr_ready_i,
    output logic [31:0] mem_wr_addr_o,
    output logic [63:0] mem_wr_data_o,
    output logic [7:0]  mem_wr_strb_o,
    input  wire         mem_wr_done_i,
    input  wire         mem_wr_err_i,

    //! ---- the backend's control face ----------------------------------------
    input  wire         csr_sel_i,
    input  wire         csr_we_i,
    input  wire  [5:0]  csr_addr_i,
    input  wire  [31:0] csr_wdata_i,
    output logic [31:0] csr_rdata_o,

    //! ---- observation -----------------------------------------------------------
    output logic        nvm_backed_o,
    output logic        nvm_dirty_o,
    output logic        nvm_stale_o,
    output logic [3:0]  nvm_verdict_o,
    output logic        nvm_img_valid_o,
    output logic        nvm_pend_o,
    output logic        nvm_unres_o,
    output logic        restore_busy_o,
    output logic        restore_done_o,
    output logic        restore_fail_o,
    output logic        restore_blank_o,
    output logic        alarm_o,
    output logic        d3_alarm_o,
    output logic        d3_unflushed_o,
    output logic        d3_restore_done_o,
    output logic        d3_restore_fail_o,
    output logic        d3_restore_rb_o,
    output logic        d3_restore_closed_o,
    output logic [2:0]  d3_rs_cause_o,
    output logic [31:0] d3_wd_o,
    output logic        d3_pass_o,
    output logic        d3_abort_o,
    output logic        d3_busy_o,
    //! a state-bus WRITE the D3 writer made and a store took (observation)
    output logic        wr_st_we_o,
    output logic [7:0]  d3_rs_applied_o,
    output logic [7:0]  d3_rs_refused_o,
    output logic [7:0]  d3_rs_blank_o,
    output logic [7:0]  d3_rs_reverted_o,
    output logic [15:0] d3_writes_o,
    output logic [15:0] d3_slot_o,
    output logic        d3_taint_o,
    output logic [N_AUDIO_UNIT_P + N_CLK_DOM_P + N_STREAM_IN_P + 2*N_STREAM_OUT_P
                  + N_SPORT_IN_P + N_SPORT_OUT_P + N_NAME_P:0] d3_dirty_o,
    output logic [N_STREAM_IN_P-1:0] mgr_dirty_o,
    output logic        mgr_restore_done_o,
    output logic        port_busy_o,
    output logic        desc_img_valid_o,
    output logic [N_STREAM_IN_P*64-1:0]  dyn_fmt_in_o,
    output logic [N_STREAM_IN_P-1:0]     dyn_fmt_in_v_o,
    output logic [N_STREAM_OUT_P*64-1:0] dyn_fmt_out_o,
    output logic [N_STREAM_OUT_P-1:0]    dyn_fmt_out_v_o,
    output logic        dev_req_o,
    output logic        dev_gnt_o,
    output logic [1:0]  dev_op_o,
    output logic [7:0]  dev_region_o,
    output logic        dev_wvalid_o,
    output logic        dev_wready_o,
    output logic [7:0]  dev_wdata_o,
    output logic        dev_busy_o,
    output logic        dev_done_o,
    output logic        dev_err_o,
    output logic        d3_mdone_o,
    output logic        tick_ms_o,
    //! the binding manager's state (KL_acmp_nvm_shadow hs_r, read through
    //! the hierarchy) and the arbiter's grant to the D3 writer: case K15's
    //! premise is a cycle with both H_FL_REQ and that grant
    output logic [3:0]  m0_state_o,
    output logic        arb_m1_gnt_o,
    //! the binding walk's verdicts (the amended manager's cause, 0 tracked),
    //! its deadline count and its abandoned read (observation)
    output logic        mgr_fail_o,
    output logic        mgr_blank_o,
    output logic [1:0]  mgr_cause_o,
    output logic [31:0] m0_wd_o,
    output logic        m0_abort_o,
    //! a preload the binding manager drives, and the LISTENER's own
    //! acceptance of it (its pre_ready_o AND pre_valid)
    output logic        pre_valid_o,
    output logic        pre_take_o,
    output logic [15:0] pre_sink_o,
    //! the binding walk's end as the D3 walk and the combined restore done
    //! see it: the gate's release (the manager's done under D3_TRACKED)
    output logic        bind_end_o,
    //! the writer's roll-back strobe to its owners (observation)
    output logic        rb_rst_o,
    //! the port's terminal cause with its err (0 in the tracked build)
    output logic [1:0]  p_err_cause_o,
    //! the descriptor memory owes an accepted burst its terminal beat (S2)
    output logic        desc_debt_o
);

  // ---- the processor's millisecond tick, a divider ------------------------
  localparam int unsigned MS_DIV_C = CLK_HZ_P / 1000;
  logic [31:0] ms_cnt_r;
  logic        tick_ms_w;
  assign tick_ms_w = (ms_cnt_r == 32'd0);
  always_ff @(posedge clk_i) begin
    if (!rst_n) ms_cnt_r <= 32'(MS_DIV_C - 1);
    else        ms_cnt_r <= tick_ms_w ? 32'(MS_DIV_C - 1) : ms_cnt_r - 32'd1;
  end
  assign tick_ms_o = tick_ms_w;

  // ---- the state bus: the uCPU BFM, or the D3 writer while it owns it ----
  logic        d3_own_w;
  logic        sb_req_w, sb_we_w, sb_name_w;
  logic [19:0] sb_addr_w;
  logic [63:0] sb_wdata_w;
  logic [7:0]  sb_wstrb_w;
  logic [15:0] sb_didx_w;
  logic        st_req_w, st_we_w, st_name_w;
  logic [19:0] st_addr_w;
  logic [63:0] st_wdata_w;
  logic [7:0]  st_wstrb_w;
  logic [15:0] st_didx_w;
  logic        dyn_sel_w;
  logic        dyn_ready_w, dyn_rvalid_w, store_ready_w, store_rvalid_w, store_err_w;
  logic [63:0] dyn_rdata_w, store_rdata_w;
  logic        st_ready_w, st_rvalid_w, st_err_w;
  logic [63:0] st_rdata_w;

  //! the writer drives the bus while it owns it, unless the harness lends
  //! it to the BFM before the restore (lend_bus_i; the writer issues nothing
  //! then). wr_bus_w is who drives; the snoop below still reads d3_own_w.
  logic        wr_bus_w;
  assign wr_bus_w   = d3_own_w && !lend_bus_i;
  assign st_req_w   = wr_bus_w ? sb_req_w   : ub_req_i;
  assign st_we_w    = wr_bus_w ? sb_we_w    : ub_we_i;
  assign st_name_w  = wr_bus_w ? sb_name_w  : ub_name_i;
  assign st_addr_w  = wr_bus_w ? sb_addr_w  : ub_addr_i;
  assign st_wdata_w = wr_bus_w ? sb_wdata_w : ub_wdata_i;
  assign st_wstrb_w = wr_bus_w ? sb_wstrb_w : 8'hFF;
  assign st_didx_w  = wr_bus_w ? sb_didx_w  : ub_didx_i;
  //! KL_aecp_engine's region routing (dyn_sel_w there)
  assign dyn_sel_w  = !st_name_w && ((st_addr_w[19:16] == 4'h1) || (st_addr_w[19:16] == 4'h2));
  assign st_ready_w  = dyn_sel_w ? dyn_ready_w : store_ready_w;
  assign st_rvalid_w = dyn_rvalid_w || store_rvalid_w;
  assign st_rdata_w  = dyn_rvalid_w ? dyn_rdata_w : store_rdata_w;
  assign st_err_w    = store_rvalid_w && store_err_w;
  assign ub_ready_o  = !wr_bus_w && st_ready_w;
  assign ub_rvalid_o = !wr_bus_w && st_rvalid_w;
  assign ub_rdata_o  = st_rdata_w;
  assign ub_err_o    = st_err_w;
  assign own_o       = wr_bus_w;
  assign wr_st_we_o  = wr_bus_w && st_req_w && st_we_w && st_ready_w;

  // ---- the real dynamic-state store ----------------------------------------
  logic [N_STREAM_OUT_P*32-1:0] pt_nc_w;
  logic [N_STREAM_OUT_P-1:0]    ptv_nc_w;
  logic [15:0] cfg_nc_w, cs_nc_w, wr_nc_w, oob_nc_w;
  logic [7:0]  id_nc_w;
  logic        aecp_dyn_dirty_nc_w;

  //! the roll-back's scoped reset (the writer's rb_rst_o); 0 in the tracked glue
  logic rb_rst_w, own_rst_n_w;
  assign own_rst_n_w = rst_n && !rb_rst_w;

  KL_aecp_dyn_state #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOMAIN_P (N_CLK_DOM_P),
      .N_CONTROL_P    (1)
  ) u_dyn (
      .clk_i           (clk_i),
      .rst_n           (own_rst_n_w),
      .st_req_i        (st_req_w && dyn_sel_w),
      .st_we_i         (st_we_w),
      .st_addr_i       (st_addr_w),
      .st_wdata_i      (st_wdata_w),
      .st_ready_o      (dyn_ready_w),
      .st_rvalid_o     (dyn_rvalid_w),
      .st_rdata_o      (dyn_rdata_w),
      .desc_index_i    (st_didx_w),
      .cur_config_o    (cfg_nc_w),
      .identify_o      (id_nc_w),
      .clk_src_index_o (cs_nc_w),
      .pt_offset_o     (pt_nc_w),
      .pt_offset_v_o   (ptv_nc_w),
      .fmt_in_o        (dyn_fmt_in_o),
      .fmt_in_v_o      (dyn_fmt_in_v_o),
      .fmt_out_o       (dyn_fmt_out_o),
      .fmt_out_v_o     (dyn_fmt_out_v_o),
      .dirty_o         (aecp_dyn_dirty_nc_w),
      .dbg_writes_o    (wr_nc_w),
      .dbg_oob_o       (oob_nc_w)
  );

  // ---- the real descriptor store -------------------------------------------
  logic [3:0]  img_fault_nc_w;
  logic [15:0] miss_nc_w, fetch_nc_w, rowr_nc_w, dlen_nc_w;
  logic        dm_rsp_ready_nc_w;
  //! the store's own memory master, before the guard
  logic        s_req_valid_w, s_req_ready_w, s_rsp_valid_w, s_rsp_last_w, s_rsp_err_w;
  logic [31:0] s_req_addr_w;
  logic [8:0]  s_req_beats_w;
  logic [63:0] s_rsp_data_w;

  KL_aecp_desc_store #(
      .DESC_BASE_P       (32'h2000_0000),
      .LINE_BYTES_P      (576),
      .IDX_ENTRIES_P     (IDX_ENTRIES_P),
      .NAME_ENTRIES_P    (N_NAME_P),
      .MEM_TIMEOUT_CYC_P (4096)
  ) u_store (
      .clk_i             (clk_i),
      .rst_n             (own_rst_n_w),
      .st_req_i          (st_req_w && !dyn_sel_w),
      .st_we_i           (st_we_w),
      .st_name_i         (st_name_w),
      .st_addr_i         (st_addr_w),
      .st_wdata_i        (st_wdata_w),
      .st_wstrb_i        (st_wstrb_w),
      .st_ready_o        (store_ready_w),
      .st_rvalid_o       (store_rvalid_w),
      .st_rdata_o        (store_rdata_w),
      .st_err_o          (store_err_w),
      .mem_req_valid_o   (s_req_valid_w),
      .mem_req_ready_i   (s_req_ready_w),
      .mem_req_addr_o    (s_req_addr_w),
      .mem_req_beats_o   (s_req_beats_w),
      .mem_rsp_valid_i   (s_rsp_valid_w),
      .mem_rsp_ready_o   (dm_rsp_ready_nc_w),
      .mem_rsp_data_i    (s_rsp_data_w),
      .mem_rsp_last_i    (s_rsp_last_w),
      .mem_rsp_err_i     (s_rsp_err_w),
      .dbg_img_valid_o   (desc_img_valid_o),
      .dbg_fault_o       (img_fault_nc_w),
      .dbg_locate_miss_o (miss_nc_w),
      .dbg_fetch_cnt_o   (fetch_nc_w),
      .dbg_ro_write_o    (rowr_nc_w),
      .dbg_desc_len_o    (dlen_nc_w)
  );

  // ---- the descriptor memory's response isolation (seam S2) ------------------
  logic desc_debt_w;
`ifdef D3_TRACKED
  //! as the parent ships it: the store's master straight onto the memory
  assign dm_req_valid_o = s_req_valid_w;
  assign s_req_ready_w  = dm_req_ready_i;
  assign dm_req_addr_o  = s_req_addr_w;
  assign dm_req_beats_o = s_req_beats_w;
  assign s_rsp_valid_w  = dm_rsp_valid_i;
  assign s_rsp_data_w   = dm_rsp_data_i;
  assign s_rsp_last_w   = dm_rsp_last_i;
  assign s_rsp_err_w    = dm_rsp_err_i;
  assign desc_debt_w    = 1'b0;
`else
  logic dm_rsp_ready_g_nc_w;
  //! on the HARD reset only: the roll-back strobe never reaches it
  KL_aecp_desc_mem_guard u_desc_guard (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .s_req_valid_i (s_req_valid_w),
      .s_req_ready_o (s_req_ready_w),
      .s_req_addr_i  (s_req_addr_w),
      .s_req_beats_i (s_req_beats_w),
      .s_rsp_valid_o (s_rsp_valid_w),
      .s_rsp_ready_i (dm_rsp_ready_nc_w),
      .s_rsp_data_o  (s_rsp_data_w),
      .s_rsp_last_o  (s_rsp_last_w),
      .s_rsp_err_o   (s_rsp_err_w),
      .m_req_valid_o (dm_req_valid_o),
      .m_req_ready_i (dm_req_ready_i),
      .m_req_addr_o  (dm_req_addr_o),
      .m_req_beats_o (dm_req_beats_o),
      .m_rsp_valid_i (dm_rsp_valid_i),
      .m_rsp_ready_o (dm_rsp_ready_g_nc_w),
      .m_rsp_data_i  (dm_rsp_data_i),
      .m_rsp_last_i  (dm_rsp_last_i),
      .m_rsp_err_i   (dm_rsp_err_i),
      .debt_o        (desc_debt_w)
  );
`endif
  assign desc_debt_o = desc_debt_w;

  // ---- harness peeks: the rows and the name table, through the hierarchy ----
  //! pk_sel_i is the dynamic-state selector (0..5); pk_idx_i the row
  localparam int unsigned PAUW_C = (N_AUDIO_UNIT_P > 1) ? $clog2(N_AUDIO_UNIT_P) : 1;
  localparam int unsigned PCDW_C = (N_CLK_DOM_P > 1)    ? $clog2(N_CLK_DOM_P)    : 1;
  localparam int unsigned PSIW_C = (N_STREAM_IN_P > 1)  ? $clog2(N_STREAM_IN_P)  : 1;
  localparam int unsigned PSOW_C = (N_STREAM_OUT_P > 1) ? $clog2(N_STREAM_OUT_P) : 1;
  localparam int unsigned PNLW_C = $clog2(8 * N_NAME_P);
  always_comb begin : peek_dyn
    pk_val_o = 64'd0;
    pk_v_o   = 1'b0;
    unique case (pk_sel_i)
      4'd0: begin pk_val_o = {48'd0, u_dyn.cfg_r}; pk_v_o = u_dyn.cfg_v_r; end
      4'd1: if (32'(pk_idx_i) < N_AUDIO_UNIT_P) begin
              pk_val_o = {32'd0, u_dyn.rate_r[PAUW_C'(pk_idx_i)]}; pk_v_o = u_dyn.rate_v_r[PAUW_C'(pk_idx_i)]; end
      4'd2: if (32'(pk_idx_i) < N_CLK_DOM_P) begin
              pk_val_o = {48'd0, u_dyn.clksrc_r[PCDW_C'(pk_idx_i)]}; pk_v_o = u_dyn.clksrc_v_r[PCDW_C'(pk_idx_i)]; end
      4'd3: if (32'(pk_idx_i) < N_STREAM_IN_P) begin
              pk_val_o = u_dyn.fmtin_r[PSIW_C'(pk_idx_i)]; pk_v_o = u_dyn.fmtin_v_r[PSIW_C'(pk_idx_i)]; end
      4'd4: if (32'(pk_idx_i) < N_STREAM_OUT_P) begin
              pk_val_o = u_dyn.fmtout_r[PSOW_C'(pk_idx_i)]; pk_v_o = u_dyn.fmtout_v_r[PSOW_C'(pk_idx_i)]; end
      4'd5: if (32'(pk_idx_i) < N_STREAM_OUT_P) begin
              pk_val_o = {32'd0, u_dyn.ptoff_r[PSOW_C'(pk_idx_i)]}; pk_v_o = u_dyn.ptoff_v_r[PSOW_C'(pk_idx_i)]; end
      default: ;
    endcase
  end
  assign pk_name_o = (32'(pk_lane_i) < 8 * N_NAME_P) ? u_store.name_r[PNLW_C'(pk_lane_i)] : 64'd0;

  // ---- the pinned ACMP listener, its timer service and its admission ----------
  localparam int unsigned SIW_C = (N_STREAM_IN_P > 1) ? $clog2(N_STREAM_IN_P) : 1;
  //! the listener's own entity_id: a transaction names it as its target
  localparam logic [63:0] LSN_EID_C = 64'h0011_2233_4455_6677;
  //! the timer service's slots (the listener's shared SM slots are 9 .. 9+N-1)
  localparam int unsigned TMR_SLOTS_C = 32;
  localparam int unsigned TMR_AW_C    = 5;

  logic        mgr_alarm_w, mgr_busy_w, mgr_done_w, mgr_fail_w, mgr_blank_w;
  logic        pre_valid_w, pre_sw_w, pre_started_w, lsn_pre_ready_w;
  logic [15:0] pre_sink_w, pre_uid_w;
  logic [63:0] pre_teid_w, pre_ceid_w;
  //! the binding walk's end for the D3 walk and the combined restore done
  logic        bind_end_w, lsn_own_w;

  //! the listener's record-write port, and the harness BFM behind it
  logic                         lsn_recwr_w;
  logic [SIW_C-1:0]             lsn_recwr_sink_w;
  logic [ACMP_REC_W_C-1:0]      lsn_recwr_rec_w;
  acmp_rec_t                    lsn_rec_view_w, bfm_rec_w, cap_rec_w;
  logic                         cap_wr_w;
  logic [SIW_C-1:0]             cap_sink_w;

  always_comb begin
    bfm_rec_w               = '0;
    bfm_rec_w.f_bound       = cap_bound_i;
    bfm_rec_w.f_started     = cap_started_i;
    bfm_rec_w.f_sw          = cap_sw_i;
    bfm_rec_w.talker_uid    = cap_uid_i;
    bfm_rec_w.talker_eid    = cap_teid_i;
    bfm_rec_w.bind_ctlr_eid = cap_ceid_i;
  end
  assign lsn_rec_view_w = acmp_rec_t'(lsn_recwr_rec_w);
  //! the listener's write wins a cycle both use, as in the processor's
  //! acmp_nvm suite (tb_cap_* behind the listener)
  assign cap_wr_w   = lsn_recwr_w || cap_wr_i;
  assign cap_sink_w = lsn_recwr_w ? lsn_recwr_sink_w : SIW_C'(cap_sink_i);
  assign cap_rec_w  = lsn_recwr_w ? lsn_rec_view_w : bfm_rec_w;

  //! the transaction the dispatch head presents (03 section 4 record)
  pp_pkg::pp_txn_t lt_txn_w;
  always_comb begin
    lt_txn_w                    = '0;
    lt_txn_w.origin             = pp_pkg::PP_ORIGIN_RX;
    lt_txn_w.protocol           = pp_pkg::PP_PROTO_ACMP;
    lt_txn_w.msg_type           = lt_txn_msg_i;
    lt_txn_w.status_in          = lt_txn_status_i;
    lt_txn_w.controller_eid     = lt_txn_ctlr_i;
    lt_txn_w.target_eid         = lt_txn_target_i;
    lt_txn_w.sequence_id        = lt_txn_seq_i;
    lt_txn_w.operands.unique_id = lt_txn_uid_i;
    lt_txn_w.rx_slot            = lt_txn_slot_i;
  end

  //! the timer service: armed by the listener alone; an injected expiry
  //! rides the bus in a cycle the service does not fire
  logic                  tm_arm_valid_w, tm_arm_cancel_w, tm_exp_valid_w, tm_tick_nc_w;
  logic [TMR_AW_C-1:0]   tm_arm_slot_w, tm_exp_slot_w;
  logic [7:0]            tm_arm_owner_w, tm_exp_owner_w;
  logic [31:0]           tm_arm_deadline_w, tm_now_ms_w;
  logic                  exp_bus_valid_w;
  logic [7:0]            exp_bus_owner_w;

  KL_pp_timer_service #(
      .CLK_HZ_P (CLK_HZ_P),
      .SLOTS_P  (TMR_SLOTS_C)
  ) u_lsn_timer (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .tick_ms_o         (tm_tick_nc_w),
      .now_ms_o          (tm_now_ms_w),
      .arm_valid_i       (tm_arm_valid_w),
      .arm_cancel_i      (tm_arm_cancel_w),
      .arm_slot_i        (tm_arm_slot_w),
      .arm_owner_i       (tm_arm_owner_w),
      .arm_deadline_ms_i (tm_arm_deadline_w),
      .exp_valid_o       (tm_exp_valid_w),
      .exp_slot_o        (tm_exp_slot_w),
      .exp_owner_o       (tm_exp_owner_w)
  );
  assign exp_bus_valid_w = tm_exp_valid_w || lt_exp_inj_i;
  assign exp_bus_owner_w = tm_exp_valid_w ? tm_exp_owner_w : lt_exp_owner_i;

  //! the listener's four work faces, after the admission gate
  logic        l_txn_valid_w, l_txn_ready_w, l_tk_valid_w, l_tk_ready_w;
  logic        l_strm_valid_w, l_exp_valid_w;
  logic [15:0] exp_drop_w;
  logic        lsn_busy_w, lsn_arm_w;

`ifdef D3_TRACKED
  //! as the parent ships it: every producer straight onto the listener, and
  //! the restore is the binding walk alone
  assign l_txn_valid_w  = lt_txn_valid_i;
  assign lt_txn_ready_o = l_txn_ready_w;
  assign l_tk_valid_w   = lt_tk_valid_i;
  assign lt_tk_ready_o  = l_tk_ready_w;
  assign l_strm_valid_w = lt_strm_valid_i;
  assign l_exp_valid_w  = exp_bus_valid_w;
  assign exp_drop_w     = 16'd0;
  assign lsn_own_w      = 1'b0;
  assign bind_end_w     = mgr_done_w;
`else
  //! seam S4: owned from the hard reset, released at the binding walk's
  //! drained terminal
  KL_pp_acmp_lsn_admit #(
      .N_SINKS_P        (N_STREAM_IN_P),
      .TMR_OWNER_BASE_P (32),
      .OWNER_W_P        (8)
  ) u_lsn_admit (
      .clk_i          (clk_i),
      .rst_n          (rst_n),
      .walk_done_i    (mgr_done_w),
      .pre_valid_i    (pre_valid_w),
      .lsn_busy_i     (lsn_busy_w),
      .lsn_arm_i      (lsn_arm_w),
      .own_o          (lsn_own_w),
      .released_o     (bind_end_w),
      .p_txn_valid_i  (lt_txn_valid_i),
      .p_txn_ready_o  (lt_txn_ready_o),
      .l_txn_valid_o  (l_txn_valid_w),
      .l_txn_ready_i  (l_txn_ready_w),
      .p_tk_valid_i   (lt_tk_valid_i),
      .p_tk_ready_o   (lt_tk_ready_o),
      .l_tk_valid_o   (l_tk_valid_w),
      .l_tk_ready_i   (l_tk_ready_w),
      .p_strm_valid_i (lt_strm_valid_i),
      .l_strm_valid_o (l_strm_valid_w),
      .p_exp_valid_i  (exp_bus_valid_w),
      .p_exp_owner_i  (exp_bus_owner_w),
      .l_exp_valid_o  (l_exp_valid_w),
      .dbg_exp_drop_o (exp_drop_w)
  );
`endif

  logic [SIW_C-1:0] lsn_act_sink_w;
  logic             lsn_tmr_cancel_nc_w, lsn_draw_busy_nc_w;
  logic [2:0]       lsn_draw_kind_nc_w;
  logic             lsn_rxs_free_w, lsn_txs_oversize_nc_w, lsn_txs_commit_w;
  logic [2:0]       lsn_txs_wr_slot_nc_w, lsn_txreq_slot_nc_w;
  logic [10:0]      lsn_txs_len_nc_w;
  logic [1:0]       lsn_rxs_free_slot_nc_w;
  logic [63:0]      lsn_settle_sid_nc_w;
  logic [47:0]      lsn_settle_da_nc_w;
  logic [11:0]      lsn_settle_vlan_nc_w;
  logic             lsn_settle_w, lsn_teardown_w, lsn_disarm_w, lsn_nvm_nc_w, lsn_nvm_set_nc_w;
  logic             lsn_notify_w, lsn_strt_chg_nc_w, lsn_strt_cmd_chg_nc_w;
  logic [N_STREAM_IN_P-1:0] lsn_started_nc_w;
  logic [15:0]      lsn_strq_drop_nc_w;

  //! the PINNED listener, UNCHANGED (hdl/acmp/KL_pp_acmp_listener.sv)
  KL_pp_acmp_listener #(
      .N_SINKS_P        (N_STREAM_IN_P),
      .TROM_HEX_P       (LTN_ROM_P),
      .TMR_SLOT_AW_P    (TMR_AW_C),
      .TMR_BASE_SLOT_P  (9),
      .TMR_OWNER_BASE_P (32)
  ) u_lsn (
      .clk_i                 (clk_i),
      .rst_n                 (rst_n),
      .entity_id_i           (LSN_EID_C),
      .txn_valid_i           (l_txn_valid_w),
      .txn_i                 (lt_txn_w),
      .txn_ready_o           (l_txn_ready_w),
      .evt_tk_valid_i        (l_tk_valid_w),
      .evt_tk_kind_i         (lt_tk_kind_i),
      .evt_tk_failed_i       (lt_tk_failed_i),
      .evt_tk_sink_i         (lt_tk_sink_i),
      .evt_tk_ready_o        (l_tk_ready_w),
      .pre_valid_i           (pre_valid_w),
      .pre_sink_i            (pre_sink_w),
      .pre_talker_eid_i      (pre_teid_w),
      .pre_talker_uid_i      (pre_uid_w),
      .pre_ctlr_eid_i        (pre_ceid_w),
      .pre_sw_i              (pre_sw_w),
      .pre_started_i         (pre_started_w),
      .pre_ready_o           (lsn_pre_ready_w),
      .strm_set_valid_i      (l_strm_valid_w),
      .strm_set_sink_i       (lt_strm_sink_i),
      .strm_set_val_i        (lt_strm_val_i),
      .strm_set_ready_o      (lt_strm_ready_o),
      .strm_set_error_o      (lt_strm_error_o),
      .strm_started_o        (lsn_started_nc_w),
      .now_ms_i              (tm_now_ms_w),
      .tmr_arm_valid_o       (tm_arm_valid_w),
      .tmr_arm_cancel_o      (tm_arm_cancel_w),
      .tmr_arm_slot_o        (tm_arm_slot_w),
      .tmr_arm_owner_o       (tm_arm_owner_w),
      .tmr_arm_deadline_ms_o (tm_arm_deadline_w),
      .tmr_exp_valid_i       (l_exp_valid_w),
      .tmr_exp_slot_i        (tm_exp_slot_w),
      .tmr_exp_owner_i       (exp_bus_owner_w),
      .draw_req_o            (lt_draw_req_o),
      .draw_kind_o           (lsn_draw_kind_nc_w),
      .draw_busy_i           (1'b0),
      .draw_valid_i          (lt_draw_valid_i),
      .draw_ms_i             (lt_draw_ms_i),
      .rxs_rd_slot_o         (lt_rxs_rd_slot_o),
      .rxs_rd_addr_o         (lt_rxs_rd_addr_o),
      .rxs_rd_en_o           (lt_rxs_rd_en_o),
      .rxs_rd_data_i         (lt_rxs_rd_data_i),
      .rxs_free_o            (lsn_rxs_free_w),
      .rxs_free_slot_o       (lsn_rxs_free_slot_nc_w),
      .txs_alloc_req_o       (lt_txs_alloc_o),
      .txs_oversize_o        (lsn_txs_oversize_nc_w),
      .txs_alloc_gnt_i       (lt_txs_gnt_i),
      .txs_alloc_slot_i      (3'd1),
      .txs_wr_slot_o         (lsn_txs_wr_slot_nc_w),
      .txs_wr_addr_o         (lt_txs_addr_o),
      .txs_wr_valid_o        (lt_txs_wr_o),
      .txs_wr_data_o         (lt_txs_data_o),
      .txs_wr_commit_o       (lsn_txs_commit_w),
      .txs_wr_len_o          (lsn_txs_len_nc_w),
      .txreq_valid_o         (lt_txreq_o),
      .txreq_slot_o          (lsn_txreq_slot_nc_w),
      .lock_held_i           (1'b0),
      .lock_ctlr_i           (64'd0),
      .act_settle_o          (lsn_settle_w),
      .act_settle_sid_o      (lsn_settle_sid_nc_w),
      .act_settle_da_o       (lsn_settle_da_nc_w),
      .act_settle_vlan_o     (lsn_settle_vlan_nc_w),
      .act_teardown_o        (lsn_teardown_w),
      .act_disc_arm_o        (lsn_arm_w),
      .act_disc_talker_eid_o (lt_arm_eid_o),
      .act_disc_disarm_o     (lsn_disarm_w),
      .act_nvm_o             (lsn_nvm_nc_w),
      .act_nvm_set_o         (lsn_nvm_set_nc_w),
      .act_notify_o          (lsn_notify_w),
      .act_sink_o            (lsn_act_sink_w),
      .dbg_busy_o            (lsn_busy_w),
      .dbg_strq_drop_o       (lsn_strq_drop_nc_w),
      .act_strt_chg_o        (lsn_strt_chg_nc_w),
      .act_strt_cmd_chg_o    (lsn_strt_cmd_chg_nc_w),
      .dbg_recwr_o           (lsn_recwr_w),
      .dbg_recwr_sink_o      (lsn_recwr_sink_w),
      .dbg_recwr_rec_o       (lsn_recwr_rec_w)
  );

  //! the listener's acceptances at ITS faces, not the producers'
  assign lt_txn_take_o    = l_txn_valid_w && l_txn_ready_w;
  assign lt_tk_take_o     = l_tk_valid_w && l_tk_ready_w;
  assign lt_strm_take_o   = l_strm_valid_w && !u_lsn.strq_busy_r;
  assign lt_exp_take_o    = l_exp_valid_w && (exp_bus_owner_w >= 8'd32)
                            && (32'(exp_bus_owner_w) < 32 + N_STREAM_IN_P);
  assign lt_rxs_free_o    = lsn_rxs_free_w;
  assign lt_own_o         = lsn_own_w;
  assign lt_released_o    = bind_end_w;
  assign lt_state_o       = 5'(u_lsn.xs_r);
  assign lt_pend_any_o    = |u_lsn.pendexp_r;
  assign lt_strq_pend_o   = u_lsn.strq_pend_r || u_lsn.strq_busy_r;
  assign lt_recwr_o       = lsn_recwr_w;
  assign lt_recwr_sink_o  = 8'(lsn_recwr_sink_w);
  assign lt_rec_bound_o   = lsn_rec_view_w.f_bound;
  assign lt_rec_started_o = lsn_rec_view_w.f_started;
  assign lt_rec_sw_o      = lsn_rec_view_w.f_sw;
  assign lt_rec_teid_o    = lsn_rec_view_w.talker_eid;
  assign lt_rec_sm_o      = lsn_rec_view_w.sm_state;
  assign lt_arm_o         = lsn_arm_w;
  assign lt_act_sink_o    = 8'(lsn_act_sink_w);
  assign lt_side_o        = {lsn_notify_w, lsn_disarm_w, lsn_teardown_w, lsn_settle_w,
                             lsn_rxs_free_w, lt_txs_alloc_o, tm_arm_valid_w};
  assign lt_exp_drop_o    = exp_drop_w;
  assign lt_tm_exp_o      = tm_exp_valid_w;

  // ---- the real binding manager ----------------------------------------------
  logic        m0_req_w, m0_we_w, m0_wvalid_w, m0_wready_w, m0_rvalid_w, m0_rready_w;
  logic        m0_busy_w, m0_done_w, m0_err_w, m0_abort_w;
  logic [1:0]  m0_err_cause_w, mgr_cause_w;
  logic [7:0]  m0_rid_w, m0_wdata_w, m0_rdata_w;
  logic [N_STREAM_IN_P-1:0] mgr_dirty_w, mgr_valid_nc_w, mgr_touched_nc_w;

`ifdef D3_TRACKED
  //! the PINNED binding manager, as the parent ships it: no cause, no deadline
  assign m0_abort_w  = 1'b0;
  assign mgr_cause_w = 2'd0;
  assign m0_wd_o     = 32'd0;
  KL_acmp_nvm_shadow #(
      .N_SINKS_P (N_STREAM_IN_P)
  ) u_nvm_shadow (
`else
  //! the AMENDED binding manager (seams S1 and S3): the cause, the deadline
  KL_acmp_nvm_shadow_amd #(
      .N_SINKS_P    (N_STREAM_IN_P),
      .RS_TMO_CYC_P (D3_RS_TMO_CYC_P)
  ) u_nvm_shadow (
      .nvm_err_cause_i  (m0_err_cause_w),
      .nvm_abort_o      (m0_abort_w),
      .restore_cause_o  (mgr_cause_w),
`endif
      .clk_i            (clk_i),
      .rst_n            (rst_n),
      .tick_i           (tick_ms_w),
      .restore_go_i     (restore_go_i),
      .restore_busy_o   (mgr_busy_w),
      .restore_done_o   (mgr_done_w),
      .restore_fail_o   (mgr_fail_w),
      .restore_blank_o  (mgr_blank_w),
      .alarm_o          (mgr_alarm_w),
      .cap_wr_i         (cap_wr_w),
      .cap_sink_i       (cap_sink_w),
      .cap_rec_i        (cap_rec_w),
      .pre_valid_o      (pre_valid_w),
      .pre_sink_o       (pre_sink_w),
      .pre_talker_eid_o (pre_teid_w),
      .pre_talker_uid_o (pre_uid_w),
      .pre_ctlr_eid_o   (pre_ceid_w),
      .pre_sw_o         (pre_sw_w),
      .pre_started_o    (pre_started_w),
      .pre_ready_i      (lsn_pre_ready_w),
      .nvm_req_o        (m0_req_w),
      .nvm_we_o         (m0_we_w),
      .nvm_record_id_o  (m0_rid_w),
      .nvm_wvalid_o     (m0_wvalid_w),
      .nvm_wready_i     (m0_wready_w),
      .nvm_wdata_o      (m0_wdata_w),
      .nvm_rvalid_i     (m0_rvalid_w),
      .nvm_rready_o     (m0_rready_w),
      .nvm_rdata_i      (m0_rdata_w),
      .nvm_busy_i       (m0_busy_w),
      .nvm_done_i       (m0_done_w),
      .nvm_err_i        (m0_err_w),
      .dbg_dirty_o      (mgr_dirty_w),
      .dbg_valid_o      (mgr_valid_nc_w),
      .dbg_touched_o    (mgr_touched_nc_w)
  );
  assign mgr_dirty_o        = mgr_dirty_w;
  assign mgr_restore_done_o = mgr_done_w;
  assign m0_state_o         = 4'(u_nvm_shadow.hs_r);
`ifndef D3_TRACKED
  assign m0_wd_o            = u_nvm_shadow.rs_wd_r;
`endif
  assign mgr_fail_o         = mgr_fail_w;
  assign mgr_blank_o        = mgr_blank_w;
  assign mgr_cause_o        = mgr_cause_w;
  assign m0_abort_o         = m0_abort_w;
  //! a preload the LISTENER took: its own pre_ready_o with the valid
  assign pre_valid_o        = pre_valid_w;
  assign pre_take_o         = pre_valid_w && lsn_pre_ready_w;
  assign pre_sink_o         = pre_sink_w;
  assign bind_end_o         = bind_end_w;

  // ---- the prototype D3 record writer ------------------------------------------
  logic        m1_req_w, m1_we_w, m1_gnt_w, m1_wvalid_w, m1_wready_w;
  logic        m1_rvalid_w, m1_rready_w, m1_done_w, m1_err_w;
  logic [1:0]  m1_err_cause_w;
  logic [7:0]  m1_rid_w, m1_wdata_w, m1_rdata_w;
  logic        d3_busy_w, d3_done_w, d3_fail_w, d3_alarm_w, d3_unfl_w, d3_blank_w;
  logic        d3_rb_w, d3_closed_w, m1_abort_w;
  logic        u_dyn_ack_w, u_name_ack_w;
  assign arb_m1_gnt_o = m1_gnt_w;

`ifdef D3_TRACKED
  //! the tracked glue has no D3 writer: nothing owns the state bus but the
  //! uCPU, nothing answers the map faces, and nothing requests the port but
  //! the binding manager
  assign d3_own_w = 1'b0;
  assign {sb_req_w, sb_we_w, sb_name_w} = 3'b000;
  assign sb_addr_w = '0; assign sb_wdata_w = '0; assign sb_wstrb_w = '0; assign sb_didx_w = '0;
  assign {am_req_o, mr_req_o, mr_add_o, mr_ent_v_o, fj_req_o, fj_out_o} = 6'b000000;
  assign am_type_o = '0; assign am_idx_o = '0; assign am_map_o = '0; assign am_sel_o = '0;
  assign am_rec_o = '0; assign mr_type_o = '0; assign mr_idx_o = '0; assign mr_cnt_o = '0;
  assign mr_ent_o = '0; assign fj_idx_o = '0; assign fj_fmt_o = '0;
  assign {m1_req_w, m1_we_w, m1_wvalid_w, m1_rready_w} = 4'b0000;
  assign m1_rid_w = '0; assign m1_wdata_w = '0;
  assign d3_busy_w = 1'b0; assign d3_done_w = mgr_done_w; assign d3_fail_w = 1'b0;
  assign d3_blank_w = 1'b1;
  assign d3_alarm_w = 1'b0; assign d3_unfl_w = 1'b0;
  assign {u_dyn_ack_w, u_name_ack_w} = 2'b00;
  assign d3_rs_applied_o = '0; assign d3_rs_refused_o = '0; assign d3_rs_blank_o = '0;
  assign d3_rs_reverted_o = '0; assign d3_writes_o = '0; assign d3_slot_o = '0;
  assign d3_taint_o = 1'b0; assign d3_dirty_o = '0;
  assign rb_rst_w = 1'b0; assign m1_abort_w = 1'b0;
  assign d3_rb_w = 1'b0; assign d3_closed_w = 1'b0; assign d3_rs_cause_o = '0;
  assign d3_wd_o = '0; assign d3_pass_o = 1'b0;
`else
  //! the change sources are the uCPU's own accesses: the writer's restore
  //! writes never reach them, so a restore write is not a change
  assign u_dyn_ack_w  = !snoop_off_i && !d3_own_w && ub_req_i && ub_we_i && dyn_sel_w && dyn_ready_w;
  assign u_name_ack_w = !snoop_off_i && !d3_own_w && ub_req_i && ub_we_i && ub_name_i && store_ready_w;

  KL_aecp_nvm_writer #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_SPORT_IN_P   (N_SPORT_IN_P),
      .N_SPORT_OUT_P  (N_SPORT_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOM_P    (N_CLK_DOM_P),
      .N_NAME_P       (N_NAME_P),
      .MAPI_CLS_P     (MAPI_CLS_P),
      .MAPO_CLS_P     (MAPO_CLS_P),
      .MAP_ENT_MAX_P  (MAP_ENT_MAX_P),
      .LAYOUT_VER_P   (8'h02),
      .DEB_TICKS_P    (D3_DEB_TICKS_P),
      .RETRY_MAX_P    (2),
      .RS_TMO_CYC_P   (D3_RS_TMO_CYC_P)
  ) u_d3 (
      .clk_i            (clk_i),
      .rst_n            (rst_n),
      .tick_i           (tick_ms_w),
      .u_dyn_ack_i      (u_dyn_ack_w),
      .u_name_ack_i     (u_name_ack_w),
      .u_addr_i         (ub_addr_i),
      .u_didx_i         (ub_didx_i),
      .me_stb_i         (me_stb_i && !snoop_off_i),
      .me_type_i        (me_type_i),
      .me_idx_i         (me_idx_i),
      .prog_busy_i      (prog_busy_i),
      .own_o            (d3_own_w),
      .sb_req_o         (sb_req_w),
      .sb_we_o          (sb_we_w),
      .sb_name_o        (sb_name_w),
      .sb_addr_o        (sb_addr_w),
      .sb_wdata_o       (sb_wdata_w),
      .sb_wstrb_o       (sb_wstrb_w),
      .sb_didx_o        (sb_didx_w),
      .sb_ready_i       (st_ready_w),
      .sb_rvalid_i      (st_rvalid_w),
      .sb_rdata_i       (st_rdata_w),
      .sb_err_i         (st_err_w),
      .desc_img_valid_i (desc_img_valid_o),
      .desc_debt_i      (desc_debt_w),
      .am_req_o         (am_req_o),
      .am_type_o        (am_type_o),
      .am_idx_o         (am_idx_o),
      .am_map_o         (am_map_o),
      .am_sel_o         (am_sel_o),
      .am_rec_o         (am_rec_o),
      .am_data_i        (am_data_i),
      .am_wait_i        (am_wait_i),
      .mr_req_o         (mr_req_o),
      .mr_add_o         (mr_add_o),
      .mr_type_o        (mr_type_o),
      .mr_idx_o         (mr_idx_o),
      .mr_cnt_o         (mr_cnt_o),
      .mr_ent_v_o       (mr_ent_v_o),
      .mr_ent_o         (mr_ent_o),
      .mr_ent_rdy_i     (mr_ent_rdy_i),
      .mr_done_i        (mr_done_i),
      .mr_ok_i          (mr_ok_i),
      .fj_req_o         (fj_req_o),
      .fj_out_o         (fj_out_o),
      .fj_idx_o         (fj_idx_o),
      .fj_fmt_o         (fj_fmt_o),
      .fj_wait_i        (fj_wait_i),
      .fj_data_i        (fj_data_i),
      .m_req_o          (m1_req_w),
      .m_we_o           (m1_we_w),
      .m_rid_o          (m1_rid_w),
      .m_gnt_i          (m1_gnt_w),
      .m_wvalid_o       (m1_wvalid_w),
      .m_wdata_o        (m1_wdata_w),
      .m_wready_i       (m1_wready_w),
      .m_rvalid_i       (m1_rvalid_w),
      .m_rdata_i        (m1_rdata_w),
      .m_rready_o       (m1_rready_w),
      .m_done_i         (m1_done_w),
      .m_err_i          (m1_err_w),
      .m_err_cause_i    (m1_err_cause_w),
      .m_abort_o        (m1_abort_w),
      .rb_rst_o         (rb_rst_w),
      //! the D3 walk starts at the binding walk's DRAINED terminal (seam S4)
      .restore_go_i     (bind_end_w),
      .restore_busy_o   (d3_busy_w),
      .restore_done_o   (d3_done_w),
      .restore_fail_o   (d3_fail_w),
      .restore_blank_o  (d3_blank_w),
      .restore_rb_o     (d3_rb_w),
      .restore_closed_o (d3_closed_w),
      .rs_cause_o       (d3_rs_cause_o),
      .rs_applied_o     (d3_rs_applied_o),
      .rs_refused_o     (d3_rs_refused_o),
      .rs_blank_o       (d3_rs_blank_o),
      .rs_reverted_o    (d3_rs_reverted_o),
      .unflushed_o      (d3_unfl_w),
      .alarm_o          (d3_alarm_w),
      .writes_o         (d3_writes_o),
      .dbg_slot_o       (d3_slot_o),
      .dbg_taint_o      (d3_taint_o),
      .dbg_wd_o         (d3_wd_o),
      .dbg_pass_o       (d3_pass_o),
      .dbg_dirty_o      (d3_dirty_o)
  );
`endif
`ifdef D3_STAGE1
  //! stage 1's roll-back scope: the map plane is stage 3's owner
  assign map_rst_o           = 1'b0;
`else
  assign map_rst_o           = rb_rst_w;
`endif
  assign rb_rst_o            = rb_rst_w;
  assign d3_restore_rb_o     = d3_rb_w;
  assign d3_restore_closed_o = d3_closed_w;
  assign d3_abort_o          = m1_abort_w;
  assign d3_busy_o           = d3_busy_w;
  assign d3_alarm_o        = d3_alarm_w;
  assign d3_mdone_o        = m1_done_w;
  assign d3_unflushed_o    = d3_unfl_w;
  assign d3_restore_done_o = d3_done_w;
  assign d3_restore_fail_o = d3_fail_w;

  // ---- two managers, one port ------------------------------------------------------
  logic        p_req_w, p_we_w, p_wvalid_w, p_rready_w, p_wready_w, p_rvalid_w;
  logic        p_busy_w, p_done_w, p_err_w;
  logic [1:0]  p_err_cause_w;
  logic [7:0]  p_rid_w, p_wdata_w, p_rdata_w;

  KL_pp_nvm_mgr_arb u_arb (
      .clk_i       (clk_i),
      .rst_n       (rst_n),
      .m0_req_i    (m0_req_w),
      .m0_we_i     (m0_we_w),
      .m0_rid_i    (m0_rid_w),
      .m0_wvalid_i (m0_wvalid_w),
      .m0_wdata_i  (m0_wdata_w),
      .m0_rready_i (m0_rready_w),
      .m0_wready_o (m0_wready_w),
      .m0_rvalid_o (m0_rvalid_w),
      .m0_rdata_o  (m0_rdata_w),
      .m0_busy_o   (m0_busy_w),
      .m0_done_o   (m0_done_w),
      .m0_err_o    (m0_err_w),
      .m0_err_cause_o (m0_err_cause_w),
      .m0_abort_i  (m0_abort_w),
      .m1_req_i    (m1_req_w),
      .m1_we_i     (m1_we_w),
      .m1_rid_i    (m1_rid_w),
      .m1_wvalid_i (m1_wvalid_w),
      .m1_wdata_i  (m1_wdata_w),
      .m1_rready_i (m1_rready_w),
      .m1_gnt_o    (m1_gnt_w),
      .m1_wready_o (m1_wready_w),
      .m1_rvalid_o (m1_rvalid_w),
      .m1_rdata_o  (m1_rdata_w),
      .m1_done_o   (m1_done_w),
      .m1_err_o    (m1_err_w),
      .m1_err_cause_o (m1_err_cause_w),
      .m1_abort_i  (m1_abort_w),
      .p_req_o     (p_req_w),
      .p_we_o      (p_we_w),
      .p_rid_o     (p_rid_w),
      .p_wvalid_o  (p_wvalid_w),
      .p_wdata_o   (p_wdata_w),
      .p_rready_o  (p_rready_w),
      .p_wready_i  (p_wready_w),
      .p_rvalid_i  (p_rvalid_w),
      .p_rdata_i   (p_rdata_w),
      .p_busy_i    (p_busy_w),
      .p_done_i    (p_done_w),
      .p_err_i     (p_err_w),
      .p_err_cause_i (p_err_cause_w)
  );

  // ---- the real port: the ONE device-face initiator ------------------------------
  logic        d_req_w, d_wvalid_w, d_rready_w;
  logic [1:0]  d_op_w;
  logic [7:0]  d_region_w, d_wdata_w;
  logic [15:0] d_offset_w, d_len_w;
  logic        b_gnt_w, b_wready_w, b_rvalid_w, b_busy_w, b_done_w, b_err_w;
  logic [7:0]  b_rdata_w;

`ifdef D3_TRACKED
  //! the PINNED port: no cause
  assign p_err_cause_w = 2'd0;
  KL_pp_nvm_port u_nvm_port (
`else
  //! the AMENDED port (seam S1): its terminal cause
  KL_pp_nvm_port_amd u_nvm_port (
      .nvm_err_cause_o (p_err_cause_w),
`endif
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .nvm_req_i       (p_req_w),
      .nvm_we_i        (p_we_w),
      .nvm_record_id_i (p_rid_w),
      .nvm_wvalid_i    (p_wvalid_w),
      .nvm_wready_o    (p_wready_w),
      .nvm_wdata_i     (p_wdata_w),
      .nvm_rvalid_o    (p_rvalid_w),
      .nvm_rready_i    (p_rready_w),
      .nvm_rdata_o     (p_rdata_w),
      .nvm_busy_o      (p_busy_w),
      .nvm_done_o      (p_done_w),
      .nvm_err_o       (p_err_w),
      .dev_req_o       (d_req_w),
      .dev_gnt_i       (b_gnt_w),
      .dev_op_o        (d_op_w),
      .dev_region_o    (d_region_w),
      .dev_offset_o    (d_offset_w),
      .dev_len_o       (d_len_w),
      .dev_wvalid_o    (d_wvalid_w),
      .dev_wready_i    (b_wready_w),
      .dev_wdata_o     (d_wdata_w),
      .dev_rvalid_i    (b_rvalid_w),
      .dev_rdata_i     (b_rdata_w),
      .dev_rready_o    (d_rready_w),
      .dev_busy_i      (b_busy_w),
      .dev_done_i      (b_done_w),
      .dev_err_i       (b_err_w)
  );
  assign port_busy_o  = p_busy_w;
  assign p_err_cause_o = p_err_cause_w;
  assign dev_req_o    = d_req_w;
  assign dev_op_o     = d_op_w;
  assign dev_region_o = d_region_w;
  assign dev_gnt_o    = b_gnt_w;
  assign dev_wvalid_o = d_wvalid_w;
  assign dev_wready_o = b_wready_w;
  assign dev_wdata_o  = d_wdata_w;
  assign dev_busy_o   = b_busy_w;
  assign dev_done_o   = b_done_w;
  assign dev_err_o    = b_err_w;

  // ---- the parent glue (KL_pp_shadow, with the D3 change) --------------------------
  //! pend_i: the binding manager's unflushed sinks OR the D3 writer's
  //! unflushed records. The dyn store's sticky level and the sticky class-6/7
  //! mark bit are REPLACED: a writer exists for every group they reported.
  logic pend_w, alarm_w;
`ifdef D3_TRACKED
  //! KL_pp_shadow at dev 07294a76, transcribed: the class-6/7 mark sets a
  //! bit only reset clears, and the dyn store's level is passed straight in
  logic aecp_mark_pend_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      aecp_mark_pend_r <= 1'b0;
    end else if (mk_stb_i && ((mk_mark_i == 8'd6) || (mk_mark_i == 8'd7))) begin
      aecp_mark_pend_r <= 1'b1;
    end
  end
  assign pend_w  = aecp_dyn_dirty_nc_w | (|mgr_dirty_w) | aecp_mark_pend_r;
`else
  assign pend_w  = (|mgr_dirty_w) | d3_unfl_w;
`endif
  assign alarm_w = mgr_alarm_w | d3_alarm_w;
  assign alarm_o = alarm_w;

  //! the processor's restore is BOTH walks: the binding walk, then D3
  logic rs_busy_w, rs_done_w;
  //! ...and the binding walk ENDS at its drained terminal (seam S4): the
  //! restore stays busy from the manager's done to the gate's release
  assign rs_busy_w = mgr_busy_w | d3_busy_w | (mgr_done_w && !bind_end_w);
  assign rs_done_w = bind_end_w & d3_done_w;

  logic restore_busy_q, walk_blind_r, img_valid_w;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      restore_busy_q <= 1'b0;
      walk_blind_r   <= 1'b1;
    end else begin
      restore_busy_q <= rs_busy_w;
      if (rs_busy_w && !restore_busy_q)   walk_blind_r <= ~img_valid_w;
      else if (rs_busy_w && !img_valid_w) walk_blind_r <= 1'b1;
    end
  end
  assign restore_busy_o  = rs_busy_w;
  assign restore_done_o  = rs_done_w;
  assign restore_fail_o  = mgr_fail_w || d3_fail_w || (rs_done_w && walk_blind_r);
`ifdef D3_TRACKED
  assign restore_blank_o = mgr_blank_w & d3_blank_w;
`else
  //! blank: NEITHER walk validated a record, so a restore that put names
  //! back and no binding does not read "nothing restored"; and a FAILED
  //! restore is never blank (revision c): a device error that loses the one
  //! saved record must not read as a clean first boot
  assign restore_blank_o = mgr_blank_w & d3_blank_w & !restore_fail_o;
`endif

  //! F07.9: the restore releases entity_enable. The enable the firmware asks
  //! for reaches the entity only once both walks are done.
`ifdef D3_TRACKED
  assign entity_en_o = en_req_i;
`else
  assign entity_en_o = en_req_i && rs_done_w;
`endif

  // ---- the shipping backend ----------------------------------------------------------
  KL_nvm_backend #(
      .CLK_HZ_P       (CLK_HZ_P),
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_SPORT_IN_P   (N_SPORT_IN_P),
      .N_SPORT_OUT_P  (N_SPORT_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOM_P    (N_CLK_DOM_P),
      .N_NAME_P       (N_NAME_P),
      .T_HOLD_MS_P    (T_HOLD_MS_P),
      .CAP_ID_W_P     (16)
  ) u_nvm (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .dev_req_i       (d_req_w),
      .dev_gnt_o       (b_gnt_w),
      .dev_op_i        (d_op_w),
      .dev_region_i    (d_region_w),
      .dev_offset_i    (d_offset_w),
      .dev_len_i       (d_len_w),
      .dev_wvalid_i    (d_wvalid_w),
      .dev_wready_o    (b_wready_w),
      .dev_wdata_i     (d_wdata_w),
      .dev_rvalid_o    (b_rvalid_w),
      .dev_rdata_o     (b_rdata_w),
      .dev_rready_i    (d_rready_w),
      .dev_busy_o      (b_busy_w),
      .dev_done_o      (b_done_w),
      .dev_err_o       (b_err_w),
      .mem_req_valid_o (mem_req_valid_o),
      .mem_req_ready_i (mem_req_ready_i),
      .mem_req_addr_o  (mem_req_addr_o),
      .mem_req_beats_o (mem_req_beats_o),
      .mem_rsp_valid_i (mem_rsp_valid_i),
      .mem_rsp_ready_o (mem_rsp_ready_o),
      .mem_rsp_data_i  (mem_rsp_data_i),
      .mem_rsp_last_i  (mem_rsp_last_i),
      .mem_rsp_err_i   (mem_rsp_err_i),
      .mem_wr_valid_o  (mem_wr_valid_o),
      .mem_wr_ready_i  (mem_wr_ready_i),
      .mem_wr_addr_o   (mem_wr_addr_o),
      .mem_wr_data_o   (mem_wr_data_o),
      .mem_wr_strb_o   (mem_wr_strb_o),
      .mem_wr_done_i   (mem_wr_done_i),
      .mem_wr_err_i    (mem_wr_err_i),
      .csr_sel_i       (csr_sel_i),
      .csr_we_i        (csr_we_i),
      .csr_addr_i      (csr_addr_i),
      .csr_wdata_i     (csr_wdata_i),
      .csr_rdata_o     (csr_rdata_o),
      .pend_i          (pend_w),
      .alarm_i         (alarm_w),
      .nvm_backed_o    (nvm_backed_o),
      .nvm_dirty_o     (nvm_dirty_o),
      .nvm_stale_o     (nvm_stale_o),
      .nvm_verdict_o   (nvm_verdict_o),
      .img_valid_o     (img_valid_w),
      .nvm_pend_o      (nvm_pend_o),
      .nvm_unres_o     (nvm_unres_o)
  );
  assign nvm_img_valid_o = img_valid_w;

endmodule

`default_nettype wire

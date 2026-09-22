/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : acmp_nvm_wrap.sv
//  Project     : IEEE 1722.1 protocol processor — acmp_nvm suite wrap
//                (docs/architecture/05 §5, 07 §5, 02 §8)
//
//  Description : Integration wrap for the KL_acmp_nvm_shadow suite: the
//                shadow, the REAL KL_pp_nvm_port and the REAL
//                KL_pp_acmp_listener wired at their landed faces — the
//                shadow's capture face on the listener's record write
//                port, the shadow's pre_* driving the listener's preload
//                face, the shadow's class-F face on the port's manager
//                face; the port's device face and the listener's inert
//                faces surface to the harness. tb_cap_* lets the harness
//                inject record writes (started-change and executor
//                traffic stand-ins) ORed behind the listener's own
//                writes; evt_block_i parks a droppable TK event on the
//                listener to backpressure pre_ready.
//
//                The one design decision that matters: the suite compiles
//                the three landed modules TOGETHER so face compatibility
//                is proven by elaboration, not by transcription — a port
//                rename or width change in any neighbor breaks this build.
//---------------------------------------------------------------------------//
`default_nettype none

module acmp_nvm_wrap
  import pp_pkg::*;
  import pp_acmp_pkg::*;
#(
    parameter int unsigned  N_SINKS_P     = 8,
    parameter logic [7:0]   REC_ID_BASE_P = 8'h20,
    parameter int unsigned  DEB_TICKS_P   = 500,
    parameter int unsigned  RETRY_MAX_P   = 2,
    parameter string        TROM_HEX_P    = "ltn_rom.hex",
    localparam int unsigned SINK_W_C = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1
) (
    input  wire                      clk_i,           //! core clock
    input  wire                      rst_n,           //! sync active-low reset

    //! ---- shadow control -------------------------------------------------
    input  wire                      tick_i,          //! debounce tick
    input  wire                      restore_go_i,    //! start boot restore
    output logic                     restore_busy_o,  //! restore running
    output logic                     restore_done_o,  //! restore complete level
    output logic                     restore_fail_o,  //! whole-restore abort level
    output logic                     restore_blank_o, //! completed walk validated ZERO records
    output logic                     alarm_o,         //! commit-retry alarm

    //! ---- harness capture injection (behind the listener's writes) ------
    input  wire                      tb_cap_wr_i,     //! inject a record write
    input  wire  [SINK_W_C-1:0]      tb_cap_sink_i,   //! injected sink
    input  wire  [ACMP_REC_W_C-1:0]  tb_cap_rec_i,    //! injected F07.6 image

    //! ---- listener backpressure lever ------------------------------------
    input  wire                      evt_block_i,     //! hold a droppable TK event

    //! ---- device face (harness region-store model) -----------------------
    output logic                     dev_req_o,       //! command request
    input  wire                      dev_gnt_i,       //! command accept
    output logic [1:0]               dev_op_o,        //! READ/WRITE/ERASE
    output logic [7:0]               dev_region_o,    //! region id = record id
    output logic [15:0]              dev_offset_o,    //! byte offset
    output logic [15:0]              dev_len_o,       //! byte count
    output logic                     dev_wvalid_o,    //! write byte present
    input  wire                      dev_wready_i,    //! backend accepts
    output logic [7:0]               dev_wdata_o,     //! write byte
    input  wire                      dev_rvalid_i,    //! read byte present
    input  wire  [7:0]               dev_rdata_i,     //! read byte
    output logic                     dev_rready_o,    //! port accepts
    input  wire                      dev_busy_i,      //! backend busy
    input  wire                      dev_done_i,      //! command complete
    input  wire                      dev_err_i,       //! command failed

    //! ---- observability out ----------------------------------------------
    output logic                     pre_valid_o,     //! shadow preload valid
    output logic [15:0]              pre_sink_o,      //! shadow preload sink
    output logic [63:0]              pre_talker_eid_o,//! shadow preload talker EID
    output logic [15:0]              pre_talker_uid_o,//! shadow preload talker uid
    output logic [63:0]              pre_ctlr_eid_o,  //! shadow preload ctlr EID
    output logic                     pre_sw_o,        //! shadow preload SW
    output logic                     pre_started_o,   //! shadow preload started
    output logic                     pre_ready_o,     //! listener's pre_ready
    output logic                     lsn_recwr_o,     //! listener record write
    output logic [SINK_W_C-1:0]      lsn_recwr_sink_o,//! listener written sink
    output logic [ACMP_REC_W_C-1:0]  lsn_recwr_rec_o, //! listener written record
    output logic                     lsn_disc_arm_o,  //! listener A4 strobe
    output logic [63:0]              lsn_disc_eid_o,  //! listener A4 talker EID
    output logic                     lsn_busy_o,      //! listener executor busy
    output logic [N_SINKS_P-1:0]     dbg_dirty_o,     //! shadow dirty bits
    output logic [N_SINKS_P-1:0]     dbg_valid_o,     //! shadow valid bits
    output logic [N_SINKS_P-1:0]     dbg_touched_o,   //! shadow touched bits
    //! the port's MANAGER-face completion, the pulse the shadow clears a
    //! dirty bit on. The device face's own dev_done_i is two cycles earlier
    //! (KL_pp_nvm_port S_RPWAIT -> S_FIN), so a suite grading WHEN the
    //! unflushed export falls has to see this one.
    output logic                     dbg_port_done_o
);

  localparam logic [63:0] ENTITY_ID_C = 64'h0A0B_0C0D_0E0F_1011;

  // ---- shadow <-> port manager face ---------------------------------------
  logic        nvm_req_w, nvm_we_w;
  logic [7:0]  nvm_record_id_w;
  logic        nvm_wvalid_w, nvm_wready_w;
  logic [7:0]  nvm_wdata_w;
  logic        nvm_rvalid_w, nvm_rready_w;
  logic [7:0]  nvm_rdata_w;
  logic        nvm_busy_w, nvm_done_w, nvm_err_w;

  // ---- shadow <-> listener preload face -----------------------------------
  logic        pre_valid_w;
  logic [15:0] pre_sink_w;
  logic [63:0] pre_talker_eid_w;
  logic [15:0] pre_talker_uid_w;
  logic [63:0] pre_ctlr_eid_w;
  logic        pre_sw_w, pre_started_w, pre_ready_w;

  // ---- listener record write port + harness injection ---------------------
  logic                    lsn_recwr_w;
  logic [SINK_W_C-1:0]     lsn_recwr_sink_w;
  logic [ACMP_REC_W_C-1:0] lsn_recwr_rec_w;

  logic                    cap_wr_w;
  logic [SINK_W_C-1:0]     cap_sink_w;
  logic [ACMP_REC_W_C-1:0] cap_rec_w;

  assign cap_wr_w   = lsn_recwr_w || tb_cap_wr_i;
  assign cap_sink_w = lsn_recwr_w ? lsn_recwr_sink_w : tb_cap_sink_i;
  assign cap_rec_w  = lsn_recwr_w ? lsn_recwr_rec_w : tb_cap_rec_i;

  // ---- DUT ---------------------------------------------------------------
  KL_acmp_nvm_shadow #(
      .N_SINKS_P    (N_SINKS_P),
      .REC_ID_BASE_P(REC_ID_BASE_P),
      .DEB_TICKS_P  (DEB_TICKS_P),
      .RETRY_MAX_P  (RETRY_MAX_P)
  ) u_shadow (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .tick_i          (tick_i),
      .restore_go_i    (restore_go_i),
      .restore_busy_o  (restore_busy_o),
      .restore_done_o  (restore_done_o),
      .restore_fail_o  (restore_fail_o),
      .restore_blank_o (restore_blank_o),
      .alarm_o         (alarm_o),
      .cap_wr_i        (cap_wr_w),
      .cap_sink_i      (cap_sink_w),
      .cap_rec_i       (cap_rec_w),
      .pre_valid_o     (pre_valid_w),
      .pre_sink_o      (pre_sink_w),
      .pre_talker_eid_o(pre_talker_eid_w),
      .pre_talker_uid_o(pre_talker_uid_w),
      .pre_ctlr_eid_o  (pre_ctlr_eid_w),
      .pre_sw_o        (pre_sw_w),
      .pre_started_o   (pre_started_w),
      .pre_ready_i     (pre_ready_w),
      .nvm_req_o       (nvm_req_w),
      .nvm_we_o        (nvm_we_w),
      .nvm_record_id_o (nvm_record_id_w),
      .nvm_wvalid_o    (nvm_wvalid_w),
      .nvm_wready_i    (nvm_wready_w),
      .nvm_wdata_o     (nvm_wdata_w),
      .nvm_rvalid_i    (nvm_rvalid_w),
      .nvm_rready_o    (nvm_rready_w),
      .nvm_rdata_i     (nvm_rdata_w),
      .nvm_busy_i      (nvm_busy_w),
      .nvm_done_i      (nvm_done_w),
      .nvm_err_i       (nvm_err_w),
      .dbg_dirty_o     (dbg_dirty_o),
      .dbg_valid_o     (dbg_valid_o),
      .dbg_touched_o   (dbg_touched_o)
  );

  // ---- the real class-F port ----------------------------------------------
  KL_pp_nvm_port #(
      .MAX_PAYLOAD_P(1024)
  ) u_port (
      .clk_i          (clk_i),
      .rst_n          (rst_n),
      .nvm_req_i      (nvm_req_w),
      .nvm_we_i       (nvm_we_w),
      .nvm_record_id_i(nvm_record_id_w),
      .nvm_wvalid_i   (nvm_wvalid_w),
      .nvm_wready_o   (nvm_wready_w),
      .nvm_wdata_i    (nvm_wdata_w),
      .nvm_rvalid_o   (nvm_rvalid_w),
      .nvm_rready_i   (nvm_rready_w),
      .nvm_rdata_o    (nvm_rdata_w),
      .nvm_busy_o     (nvm_busy_w),
      .nvm_done_o     (nvm_done_w),
      .nvm_err_o      (nvm_err_w),
      .dev_req_o      (dev_req_o),
      .dev_gnt_i      (dev_gnt_i),
      .dev_op_o       (dev_op_o),
      .dev_region_o   (dev_region_o),
      .dev_offset_o   (dev_offset_o),
      .dev_len_o      (dev_len_o),
      .dev_wvalid_o   (dev_wvalid_o),
      .dev_wready_i   (dev_wready_i),
      .dev_wdata_o    (dev_wdata_o),
      .dev_rvalid_i   (dev_rvalid_i),
      .dev_rdata_i    (dev_rdata_i),
      .dev_rready_o   (dev_rready_o),
      .dev_busy_i     (dev_busy_i),
      .dev_done_i     (dev_done_i),
      .dev_err_i      (dev_err_i)
  );

  // ---- the real listener, protocol faces inert ----------------------------
  // A droppable TK event (sink out of range) parks on the event face while
  // evt_block_i holds, which deasserts pre_ready (X_IDLE priority order) —
  // the suite's preload-backpressure lever.
  KL_pp_acmp_listener #(
      .N_SINKS_P (N_SINKS_P),
      .TROM_HEX_P(TROM_HEX_P)
  ) u_listener (
      .clk_i                (clk_i),
      .rst_n                (rst_n),
      .entity_id_i          (ENTITY_ID_C),
      .txn_valid_i          (1'b0),
      .txn_i                (pp_txn_t'('0)),
      .txn_ready_o          (),
      .evt_tk_valid_i       (evt_block_i),
      .evt_tk_kind_i        (2'd0),
      .evt_tk_failed_i      (1'b0),
      .evt_tk_sink_i        (16'hFFFF),
      .evt_tk_ready_o       (),
      .pre_valid_i          (pre_valid_w),
      .pre_sink_i           (pre_sink_w),
      .pre_talker_eid_i     (pre_talker_eid_w),
      .pre_talker_uid_i     (pre_talker_uid_w),
      .pre_ctlr_eid_i       (pre_ctlr_eid_w),
      .pre_sw_i             (pre_sw_w),
      .pre_started_i        (pre_started_w),
      .pre_ready_o          (pre_ready_w),
      .now_ms_i             (32'd0),
      .tmr_arm_valid_o      (),
      .tmr_arm_cancel_o     (),
      .tmr_arm_slot_o       (),
      .tmr_arm_owner_o      (),
      .tmr_arm_deadline_ms_o(),
      .tmr_exp_valid_i      (1'b0),
      .tmr_exp_slot_i       (7'd0),
      .tmr_exp_owner_i      (8'd0),
      .draw_req_o           (),
      .draw_kind_o          (),
      .draw_busy_i          (1'b0),
      .draw_valid_i         (1'b0),
      .draw_ms_i            (16'd0),
      .rxs_rd_slot_o        (),
      .rxs_rd_addr_o        (),
      .rxs_rd_en_o          (),
      .rxs_rd_data_i        (8'd0),
      .rxs_free_o           (),
      .rxs_free_slot_o      (),
      .txs_alloc_req_o      (),
      .txs_oversize_o       (),
      .txs_alloc_gnt_i      (1'b0),
      .txs_alloc_slot_i     (3'd0),
      .txs_wr_slot_o        (),
      .txs_wr_addr_o        (),
      .txs_wr_valid_o       (),
      .txs_wr_data_o        (),
      .txs_wr_commit_o      (),
      .txs_wr_len_o         (),
      .txreq_valid_o        (),
      .txreq_slot_o         (),
      .lock_held_i          (1'b0),
      .lock_ctlr_i          (64'd0),
      .act_settle_o         (),
      .act_settle_sid_o     (),
      .act_settle_da_o      (),
      .act_settle_vlan_o    (),
      .act_teardown_o       (),
      .act_disc_arm_o       (lsn_disc_arm_o),
      .act_disc_talker_eid_o(lsn_disc_eid_o),
      .act_disc_disarm_o    (),
      .act_nvm_o            (),
      .act_nvm_set_o        (),
      .act_notify_o         (),
      .act_sink_o           (),
      .dbg_busy_o           (lsn_busy_o),
      .dbg_recwr_o          (lsn_recwr_w),
      .dbg_recwr_sink_o     (lsn_recwr_sink_w),
      .dbg_recwr_rec_o      (lsn_recwr_rec_w)
  );

  // ---- observability mirrors ----------------------------------------------
  assign pre_valid_o      = pre_valid_w;
  assign pre_sink_o       = pre_sink_w;
  assign pre_talker_eid_o = pre_talker_eid_w;
  assign pre_talker_uid_o = pre_talker_uid_w;
  assign pre_ctlr_eid_o   = pre_ctlr_eid_w;
  assign pre_sw_o         = pre_sw_w;
  assign pre_started_o    = pre_started_w;
  assign pre_ready_o      = pre_ready_w;
  assign lsn_recwr_o      = lsn_recwr_w;
  assign lsn_recwr_sink_o = lsn_recwr_sink_w;
  assign lsn_recwr_rec_o  = lsn_recwr_rec_w;
  assign dbg_port_done_o  = nvm_done_w;

endmodule

`default_nettype wire

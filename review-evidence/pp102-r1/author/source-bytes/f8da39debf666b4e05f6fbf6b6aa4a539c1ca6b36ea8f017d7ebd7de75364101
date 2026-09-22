/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : srp_tb_wrap.sv
//  Project     : IEEE 1722.1 protocol processor — SRP encoder suite wrap
//
//  Description : Binds KL_srp_encoder to a REAL KL_pp_tx_slots pool
//                (alloc/write/commit wired module-to-module, serialize face
//                exposed to the harness so captured frames crossed the
//                actual slot RAM), and instantiates KL_srp_domain and
//                KL_srp_vlan stand-alone with every port exposed — the
//                harness plays the not-yet-landed event router when it
//                bridges their declaration events into the encoder.
//---------------------------------------------------------------------------//
`default_nettype none

module srp_tb_wrap (
    input  wire          clk_i,               //! shared clock
    input  wire          rst_n,               //! shared sync active-low reset

    // ---- encoder event push ----------------------------------------------
    input  wire          enc_ev_valid_i,      //! event offered
    output logic         enc_ev_ready_o,      //! encoder accepts
    input  wire          enc_ev_app_i,        //! 0 MSRP / 1 MVRP
    input  wire  [7:0]   enc_ev_attr_type_i,  //! AttributeType
    input  wire  [2:0]   enc_ev_event_i,      //! attribute event
    input  wire  [1:0]   enc_ev_fourpack_i,   //! Listener declaration lane
    input  wire  [271:0] enc_ev_value_i,      //! FirstValue lane
    output logic         enc_ev_drop_o,       //! bad-type drop strobe

    input  wire  [1:0]   enc_join_tick_i,     //! T-MRP-JOIN per participant
    input  wire  [1:0]   enc_leaveall_i,      //! LeaveAll injection per participant
    input  wire  [47:0]  enc_own_mac_i,       //! station MAC

    output logic         enc_txreq_valid_o,   //! committed-frame request
    output logic [2:0]   enc_txreq_slot_o,    //! committed slot handle
    input  wire          enc_txreq_ready_i,   //! harness-arbiter accept
    output logic [3:0]   enc_dbg_cnt_msrp_o,  //! pending MSRP events
    output logic [3:0]   enc_dbg_cnt_mvrp_o,  //! pending MVRP events
    output logic         dbg_alloc_gnt_o,     //! pool grant pulse (cadence proof)
    output logic         dbg_commit_o,        //! pool commit pulse (cadence proof)

    // ---- pool serialize face (harness drains committed frames) ------------
    input  wire          ser_req_i,           //! start streaming ser_slot_i
    input  wire  [2:0]   ser_slot_i,          //! slot to stream
    output logic         ser_valid_o,         //! byte valid
    output logic [7:0]   ser_data_o,          //! frame byte
    output logic         ser_last_o,          //! final byte
    input  wire          ser_ready_i,         //! harness consumes

    // ---- Domain FSM (stand-alone) -----------------------------------------
    input  wire          dom_link_up_i,       //! link level
    input  wire          dom_rx_valid_i,      //! received Domain vector strobe
    input  wire  [7:0]   dom_rx_class_id_i,   //! FirstValue SRclassID
    input  wire  [7:0]   dom_rx_prio_i,       //! FirstValue SRclassPriority
    input  wire  [15:0]  dom_rx_vid_i,        //! FirstValue SRclassVID
    input  wire  [12:0]  dom_rx_nov_i,        //! NumberOfValues
    input  wire          dom_periodic_tick_i, //! T-MRP-PERIODIC
    input  wire          dom_leaveall_tick_i, //! MSRP LeaveAll cycle
    output logic         dom_ev_valid_o,      //! declaration event pending
    output logic [2:0]   dom_ev_event_o,      //! event code
    output logic [31:0]  dom_ev_value_o,      //! Domain FirstValue
    input  wire          dom_ev_ready_i,      //! harness/bridge accepts
    output logic         dom_evt_change_o,    //! DOMAIN_CHANGE strobe
    output logic [2:0]   dom_class_a_prio_o,  //! class-D level
    output logic [11:0]  dom_class_a_vid_o,   //! class-D level
    output logic         dom_adopted_o,       //! FSM state observability

    // ---- VLAN FSM (stand-alone) -------------------------------------------
    input  wire          vlan_user_valid_i,   //! user op offered
    input  wire          vlan_user_join_i,    //! 1 join / 0 leave
    input  wire  [11:0]  vlan_user_vid_i,     //! the user's stream VID
    output logic         vlan_user_ready_o,   //! op accepted
    output logic         vlan_user_err_o,     //! full-table / unknown-VID strobe
    input  wire          vlan_periodic_tick_i,//! T-MRP-PERIODIC
    input  wire          vlan_leaveall_tick_i,//! MVRP LeaveAll cycle
    output logic         vlan_ev_valid_o,     //! declaration event pending
    output logic [2:0]   vlan_ev_event_o,     //! event code
    output logic [15:0]  vlan_ev_vid_o,       //! MVRP FirstValue (VID)
    input  wire          vlan_ev_ready_i,     //! harness/bridge accepts
    output logic [3:0]   vlan_vid_active_o    //! table-live bits
);

  // ---- encoder <-> pool wiring --------------------------------------------
  logic        alloc_req_w, oversize_w, alloc_gnt_w;
  logic [2:0]  alloc_slot_w;
  logic [2:0]  wr_slot_w;
  logic [10:0] wr_addr_w;
  logic        wr_valid_w;
  logic [7:0]  wr_data_w;
  logic        wr_commit_w;
  logic [10:0] wr_len_w;

  assign dbg_alloc_gnt_o = alloc_gnt_w;
  assign dbg_commit_o    = wr_commit_w;

  KL_srp_encoder u_enc (
      .clk_i          (clk_i),
      .rst_n          (rst_n),
      .ev_valid_i     (enc_ev_valid_i),
      .ev_ready_o     (enc_ev_ready_o),
      .ev_app_i       (enc_ev_app_i),
      .ev_attr_type_i (enc_ev_attr_type_i),
      .ev_event_i     (enc_ev_event_i),
      .ev_fourpack_i  (enc_ev_fourpack_i),
      .ev_value_i     (enc_ev_value_i),
      .ev_drop_o      (enc_ev_drop_o),
      .join_tick_i    (enc_join_tick_i),
      .leaveall_i     (enc_leaveall_i),
      .own_mac_i      (enc_own_mac_i),
      .alloc_req_o    (alloc_req_w),
      .oversize_o     (oversize_w),
      .alloc_slot_i   (alloc_slot_w),
      .alloc_gnt_i    (alloc_gnt_w),
      .wr_slot_o      (wr_slot_w),
      .wr_addr_o      (wr_addr_w),
      .wr_valid_o     (wr_valid_w),
      .wr_data_o      (wr_data_w),
      .wr_commit_o    (wr_commit_w),
      .wr_len_o       (wr_len_w),
      .txreq_valid_o  (enc_txreq_valid_o),
      .txreq_slot_o   (enc_txreq_slot_o),
      .txreq_ready_i  (enc_txreq_ready_i),
      .dbg_cnt_msrp_o (enc_dbg_cnt_msrp_o),
      .dbg_cnt_mvrp_o (enc_dbg_cnt_mvrp_o)
  );

  /* verilator lint_off PINCONNECTEMPTY */
  KL_pp_tx_slots u_pool (
      .clk_i         (clk_i),
      .rst_n         (rst_n),
      .alloc_req_i   (alloc_req_w),
      .oversize_i    (oversize_w),
      .alloc_gnt_o   (alloc_gnt_w),
      .alloc_slot_o  (alloc_slot_w),
      .wr_slot_i     (wr_slot_w),
      .wr_addr_i     (wr_addr_w),
      .wr_valid_i    (wr_valid_w),
      .wr_data_i     (wr_data_w),
      .wr_commit_i   (wr_commit_w),
      .wr_len_i      (wr_len_w),
      .hold_valid_i  (1'b0),
      .hold_slot_i   ('0),
      .release_valid_i(1'b0),
      .release_slot_i('0),
      .ser_req_i     (ser_req_i),
      .ser_slot_i    (ser_slot_i),
      .ser_valid_o   (ser_valid_o),
      .ser_data_o    (ser_data_o),
      .ser_last_o    (ser_last_o),
      .ser_ready_i   (ser_ready_i),
      .slots_ready_o (),
      .slots_free_o  ()
  );
  /* verilator lint_on PINCONNECTEMPTY */

  KL_srp_domain u_dom (
      .clk_i               (clk_i),
      .rst_n               (rst_n),
      .link_up_i           (dom_link_up_i),
      .rxdom_valid_i       (dom_rx_valid_i),
      .rxdom_class_id_i    (dom_rx_class_id_i),
      .rxdom_prio_i        (dom_rx_prio_i),
      .rxdom_vid_i         (dom_rx_vid_i),
      .rxdom_nov_i         (dom_rx_nov_i),
      .periodic_tick_i     (dom_periodic_tick_i),
      .leaveall_tick_i     (dom_leaveall_tick_i),
      .dom_ev_valid_o      (dom_ev_valid_o),
      .dom_ev_event_o      (dom_ev_event_o),
      .dom_ev_value_o      (dom_ev_value_o),
      .dom_ev_ready_i      (dom_ev_ready_i),
      .evt_domain_change_o (dom_evt_change_o),
      .class_a_prio_o      (dom_class_a_prio_o),
      .class_a_vid_o       (dom_class_a_vid_o),
      .adopted_o           (dom_adopted_o)
  );

  KL_srp_vlan u_vlan (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .user_valid_i    (vlan_user_valid_i),
      .user_join_i     (vlan_user_join_i),
      .user_vid_i      (vlan_user_vid_i),
      .user_ready_o    (vlan_user_ready_o),
      .user_err_o      (vlan_user_err_o),
      .periodic_tick_i (vlan_periodic_tick_i),
      .leaveall_tick_i (vlan_leaveall_tick_i),
      .vlan_ev_valid_o (vlan_ev_valid_o),
      .vlan_ev_event_o (vlan_ev_event_o),
      .vlan_ev_vid_o   (vlan_ev_vid_o),
      .vlan_ev_ready_i (vlan_ev_ready_i),
      .vid_active_o    (vlan_vid_active_o)
  );

endmodule : srp_tb_wrap
`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_top.sv
  Description : AECP / AEM listener subsystem — top-level wiring.

                Milan v1.2 hardware entity: answers AECP (IEEE 1722.1-2021 §9)
                commands against a fixed 5-descriptor model (ENTITY,
                CONFIGURATION, one AVB_INTERFACE, one AUDIO_UNIT, one
                STREAM_OUTPUT) and drives the ADP advertiser's discover
                response.

                Pipeline:
                  RX tap (monitor) -> KL_aecp_ingress (filter + big-lane
                    replay + src-MAC capture)
                  -> KL_aecp_packet_validator (message_type / CDL gate)
                  -> KL_aecp_common_parser (aecp_hdr_t, entity_id match)
                  -> KL_aecp_l0_state (LOCK yes / ACQUIRE not-supported)
                   + KL_aecp_response_builder (READ_DESCRIPTOR, getters/
                     setters, MVU GET_MILAN_INFO) <-> KL_aecp_aem_store
                     through KL_aecp_aem_dyn_mux (live-field overlay)
                  -> response AXIS master (merged into MAC TX upstream).

                Store read latency is 1 cycle; the dynamic overlay mux is fed
                the read ADDRESS delayed one cycle so it aligns with the store
                DATA it overlays.

  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_top #(
  parameter int unsigned CLK_FREQ_HZ_P = 100_000_000
) (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire          enable_i,          //! AECP + discover-response enable

  // ---- identity / live fields (CSR 0x600 group + ADP state) ----------
  input  wire [47:0]   station_mac_i,     //! [47:40] = first wire byte
  input  wire [63:0]   entity_id_i,
  input  wire [63:0]   entity_model_id_i,
  input  wire [63:0]   entity_name8_i,     //! board-name overlay (CSR)
  input  wire [31:0]   entity_caps_i,
  input  wire [15:0]   talker_sources_i,
  input  wire [15:0]   talker_caps_i,
  input  wire [15:0]   listener_sinks_i,
  input  wire [15:0]   listener_caps_i,
  input  wire [31:0]   controller_caps_i,
  input  wire [31:0]   available_index_i,
  input  wire [63:0]   association_id_i,
  input  wire [63:0]   gptp_gm_id_i,
  input  wire [31:0]   pdelay_ns_i,        //! measured gPTP neighbor propagation delay (ns)
  input  wire [7:0]    gptp_domain_i,

  // ---- live talker stream state (docs/design/MILAN_TALKER_SM.md) ------
  input  wire [47:0]   aaf_dmac_i,         //! stream dest MAC (framer CSR)
  input  wire [11:0]   aaf_vid_i,          //! stream VLAN id (framer CSR)
  input  wire          talker_active_i,    //! ACMP probe SM state
  input  wire          listener_observed_i,//! lwSRP registrar hook
  output wire [31:0]   pres_offset_o,      //! live presentation offset (ns) -> framer
  output wire          identify_o,         //! IDENTIFY control active (LED hook)
  input  wire          link_up_i,          //! PHY link (AVB_INTERFACE counters)
  input  wire [31:0]   frames_tx_i,        //! AAF frames sent (STREAM_OUTPUT counters)

  // ---- listener sink state (KL_acmp_listener; STREAM_INPUT[0]) --------
  input  wire          lstn_bound_i,
  input  wire [63:0]   lstn_sid_i,
  input  wire [47:0]   lstn_dmac_i,
  input  wire [11:0]   lstn_vlan_i,
  input  wire [1:0]    lstn_pbsta_i,
  input  wire [4:0]    lstn_acmpsta_i,
  input  wire          lstn_ta_reg_i,
  input  wire          lstn_ta_fail_i,
  input  wire [63:0]   as_parent_ckid_i,   //! 802.1AS parent bridge ckid (CSR)
  input  wire [7:0]    lstn_fail_code_i,   //! listener-side MSRP failure code
  input  wire [63:0]   lstn_fail_bridge_i, //! ...and failing bridge_id
  input  wire [11:0]   lstn_ta_vlan_i,     //! registered Talker-attr vlan
  input  wire [31:0]   lstn_ta_acclat_i,   //! ...AccumulatedLatency
  input  wire          tk_fail_valid_i,    //! our-talker TF registered
  input  wire [7:0]    tk_fail_code_i,     //! ...code
  input  wire [63:0]   tk_fail_bridge_i,   //! ...bridge_id
  input  wire [11:0]   srp_domain_vid_i,   //! SRP domain VID (AVB_INFO map)

  // ---- STREAM_INPUT[0] diagnostics (KL_avtp_rx_monitor) --------------
  input  wire [31:0]   in0_cnt_locked_i,
  input  wire [31:0]   in0_cnt_unlocked_i,
  input  wire [31:0]   in0_cnt_interrupted_i,
  input  wire [31:0]   in0_cnt_seqmm_i,
  input  wire [31:0]   in0_cnt_tu_i,
  input  wire [31:0]   in0_cnt_unsupp_i,
  input  wire [31:0]   in0_cnt_frx_i,
  input  wire [31:0]   in0_cnt_mreset_i,
  input  wire [31:0]   in0_cnt_late_i,
  input  wire [31:0]   in0_cnt_early_i,
  input  wire          in0_cnt_dirty_p_i,
  output wire [63:0]   in0_fmt_o,          //! live STREAM_INPUT[0] format
  output wire [15:0]   clk_src_o,          //! live clock_source_index

  // ---- RX monitor tap (MAC RX AXIS, little lane, inputs only) --------
  input  wire          rx_tvalid_i,
  input  wire [63:0]   rx_tdata_i,
  input  wire [7:0]    rx_tkeep_i,
  input  wire          rx_tlast_i,

  // ---- ADP discover-response trigger (-> adp_advertiser.rcv_discover_i)
  output wire          adp_discover_o,

  // ---- response AXIS master (little lane; -> TX arbiter) -------------
  output wire [63:0]   m_axis_tdata,
  output wire [7:0]    m_axis_tkeep,
  output wire          m_axis_tvalid,
  output wire          m_axis_tlast,
  input  wire          m_axis_tready,

  // ---- status / counters ---------------------------------------------
  output wire          locked_o,
  output wire [15:0]   current_config_o,
  output wire [15:0]   cmd_count_o,       //! commands accepted
  output wire [15:0]   resp_count_o       //! responses sent
);

  // ---- internal AXIS links (flat: sv2v v0.0.13 renders interface
  //      members of non-top modules as top-absolute hierarchical paths,
  //      which breaks the Yosys portability gate when this module is
  //      instantiated inside milan_datapath) -----------------------------
  logic        ig_to_val_tvalid,  ig_to_val_tready,  ig_to_val_tlast;
  logic [63:0] ig_to_val_tdata;
  logic [7:0]  ig_to_val_tkeep;
  logic        val_to_par_tvalid, val_to_par_tready, val_to_par_tlast;
  logic [63:0] val_to_par_tdata;
  logic [7:0]  val_to_par_tkeep;
  logic        par_to_bld_tvalid, par_to_bld_tready, par_to_bld_tlast;
  logic [63:0] par_to_bld_tdata;
  logic [7:0]  par_to_bld_tkeep;

  // ---- parser / l0 buses --------------------------------------------
  aecp_hdr_t     hdr_w;
  logic          mismatch_w;
  aecp_l0_state_t l0_state_w;
  logic [4:0]    l0_status_w;
  logic          l0_reject_w;

  // ---- validator sideband -------------------------------------------
  logic          val_valid_w, val_drop_w;
  logic [4:0]    val_status_w;
  logic [3:0]    val_msgtype_w;

  // ---- timers --------------------------------------------------------
  logic tick_1khz_w;
  KL_aecp_timers #(.CLK_FREQ_HZ_P(CLK_FREQ_HZ_P)) u_timers (
    .clk_i(clk_i), .rst_n(rst_n), .ptp_ts_i(64'd0),
    .tick_1khz_o(tick_1khz_w),
    .lock_start_i(1'b0), .lock_clear_i(1'b0), .lock_expired_o(),
    .counter_gate_o(), .stale_tick_o()
  );

  // ---- ingress: RX monitor -> big-lane replay -----------------------
  logic [47:0] req_src_mac_w;
  logic        req_valid_w, req_pop_w;
  //! 1024 B: a full-size 7.4.76 batch AECPDU (up to ~520 B on the wire)
  //! must fit even while the builder drains a previous response
  KL_aecp_ingress #(.FIFO_DEPTH_BYTES(1024)) u_ingress (
    .clk_i(clk_i), .rst_n(rst_n), .enable_i(enable_i),
    .station_mac_i(station_mac_i), .entity_id_i(entity_id_i),
    .rx_tvalid_i(rx_tvalid_i), .rx_tdata_i(rx_tdata_i),
    .rx_tkeep_i(rx_tkeep_i), .rx_tlast_i(rx_tlast_i),
    .m_axis_tvalid(ig_to_val_tvalid), .m_axis_tready(ig_to_val_tready), .m_axis_tdata(ig_to_val_tdata), .m_axis_tkeep(ig_to_val_tkeep), .m_axis_tlast(ig_to_val_tlast),
    .req_src_mac_o(req_src_mac_w), .req_valid_o(req_valid_w), .req_pop_i(req_pop_w),
    .adp_discover_o(adp_discover_o)
  );

  // ---- validator -----------------------------------------------------
  KL_aecp_packet_validator u_val (
    .clk_i(clk_i), .rst_n(rst_n),
    .s_axis_tvalid(ig_to_val_tvalid), .s_axis_tready(ig_to_val_tready), .s_axis_tdata(ig_to_val_tdata), .s_axis_tkeep(ig_to_val_tkeep), .s_axis_tlast(ig_to_val_tlast),
    .m_axis_tvalid(val_to_par_tvalid), .m_axis_tready(val_to_par_tready), .m_axis_tdata(val_to_par_tdata), .m_axis_tkeep(val_to_par_tkeep), .m_axis_tlast(val_to_par_tlast),
    .valid_o(val_valid_w), .drop_o(val_drop_w),
    .status_o(val_status_w), .message_type_o(val_msgtype_w)
  );

  // ---- common parser -------------------------------------------------
  KL_aecp_common_parser u_parser (
    .clk_i(clk_i), .rst_n(rst_n),
    .l0_state_i(l0_state_w),
    .s_axis_tvalid(val_to_par_tvalid), .s_axis_tready(val_to_par_tready), .s_axis_tdata(val_to_par_tdata), .s_axis_tkeep(val_to_par_tkeep), .s_axis_tlast(val_to_par_tlast),
    .m_axis_tvalid(par_to_bld_tvalid), .m_axis_tready(par_to_bld_tready), .m_axis_tdata(par_to_bld_tdata), .m_axis_tkeep(par_to_bld_tkeep), .m_axis_tlast(par_to_bld_tlast),
    .hdr_o(hdr_w), .mismatch_o(mismatch_w)
  );

  // ---- L0 entity state (LOCK / ACQUIRE-unsupported / config) ---------
  KL_aecp_l0_state u_l0 (
    .clk_i(clk_i), .rst_n(rst_n),
    .entity_id_i(entity_id_i),
    .hdr_i(hdr_w), .message_type_i(val_msgtype_w),
    .tick_1khz_i(tick_1khz_w), .cmd_done_i(1'b0),
    .l0_state_o(l0_state_w), .status_o(l0_status_w), .reject_o(l0_reject_w)
  );

  // ---- AEM store <-> dynamic overlay mux -----------------------------
  logic [15:0] st_raddr_w, st_waddr_w;
  logic        st_rd_w, st_wr_w;
  logic [7:0]  st_wdata_w, st_rom_byte_w, st_ovl_byte_w;
  logic [15:0] st_raddr_d1;               //! read addr delayed to match data

  always_ff @(posedge clk_i) st_raddr_d1 <= st_raddr_w;

  KL_aecp_aem_store u_store (
    .clk_i(clk_i), .rst_n(rst_n),
    .addr_i(st_raddr_w), .rd_i(st_rd_w), .data_o(st_rom_byte_w),
    .wr_addr_i(st_waddr_w), .wr_i(st_wr_w), .wr_data_i(st_wdata_w),
    .factory_reset_i(1'b0), .flush_in_progress_o()
  );

  KL_aecp_aem_dyn_mux u_dyn (
    .addr_i(st_raddr_d1), .rom_byte_i(st_rom_byte_w),
    .entity_id_i(entity_id_i), .entity_model_id_i(entity_model_id_i),
    .entity_name8_i(entity_name8_i),
    .entity_caps_i(entity_caps_i), .talker_sources_i(talker_sources_i),
    .talker_caps_i(talker_caps_i), .listener_sinks_i(listener_sinks_i),
    .listener_caps_i(listener_caps_i), .controller_caps_i(controller_caps_i),
    .available_index_i(available_index_i), .association_id_i(association_id_i),
    .current_config_i(l0_state_w.current_configuration_index),
    .station_mac_i(station_mac_i), .byte_o(st_ovl_byte_w)
  );

  // ---- presentation-time offset (SET_STREAM_INFO MSRP_ACC_LAT target) --
  //      Reset = 2 000 000 ns: the Milan class-A max transit time the framer
  //      has always stamped (aaf_talker_i2s TRANSIT) and the reference's
  //      stream->mtt default. GET_STREAM_INFO reports it live.
  logic        pres_wr_p_w;
  logic [31:0] pres_wr_val_w;
  logic [31:0] pres_offset_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n)           pres_offset_r <= 32'd2_000_000;
    else if (pres_wr_p_w) pres_offset_r <= pres_wr_val_w;
  end
  assign pres_offset_o = pres_offset_r;

  // ---- response builder ---------------------------------------------
  logic evt_cmd_w, evt_resp_w, evt_drop_w;
  KL_aecp_response_builder u_bld (
    .clk_i(clk_i), .rst_n(rst_n), .enable_i(enable_i),
    .hdr_i(hdr_w), .mismatch_i(mismatch_w),
    .frame_ok_i(val_valid_w), .frame_bad_i(val_drop_w),
    .message_type_i(val_msgtype_w),
    .s_axis_tvalid(par_to_bld_tvalid), .s_axis_tready(par_to_bld_tready), .s_axis_tdata(par_to_bld_tdata), .s_axis_tkeep(par_to_bld_tkeep), .s_axis_tlast(par_to_bld_tlast),
    .req_src_mac_i(req_src_mac_w), .req_meta_valid_i(req_valid_w),
    .req_meta_pop_o(req_pop_w),
    .l0_state_i(l0_state_w), .l0_status_i(l0_status_w), .l0_reject_i(l0_reject_w),
    .station_mac_i(station_mac_i), .entity_id_i(entity_id_i),
    .gptp_gm_id_i(gptp_gm_id_i), .pdelay_ns_i(pdelay_ns_i), .gptp_domain_i(gptp_domain_i),
    .aaf_dmac_i(aaf_dmac_i), .aaf_vid_i(aaf_vid_i),
    .talker_active_i(talker_active_i),
    .listener_observed_i(listener_observed_i),
    .pres_offset_i(pres_offset_r),
    .pres_wr_p_o(pres_wr_p_w), .pres_wr_val_o(pres_wr_val_w),
    .identify_o(identify_o),
    .link_up_i(link_up_i), .frames_tx_i(frames_tx_i),
    .lstn_bound_i(lstn_bound_i), .lstn_sid_i(lstn_sid_i),
    .as_parent_ckid_i(as_parent_ckid_i),
    .lstn_fail_code_i(lstn_fail_code_i), .lstn_fail_bridge_i(lstn_fail_bridge_i),
    .lstn_ta_vlan_i(lstn_ta_vlan_i), .lstn_ta_acclat_i(lstn_ta_acclat_i),
    .tk_fail_valid_i(tk_fail_valid_i), .tk_fail_code_i(tk_fail_code_i),
    .tk_fail_bridge_i(tk_fail_bridge_i), .srp_domain_vid_i(srp_domain_vid_i),
    .lstn_dmac_i(lstn_dmac_i), .lstn_vlan_i(lstn_vlan_i),
    .lstn_pbsta_i(lstn_pbsta_i), .lstn_acmpsta_i(lstn_acmpsta_i),
    .lstn_ta_reg_i(lstn_ta_reg_i), .lstn_ta_fail_i(lstn_ta_fail_i),
    .tick_1khz_i(tick_1khz_w),
    .in0_cnt_locked_i(in0_cnt_locked_i),
    .in0_cnt_unlocked_i(in0_cnt_unlocked_i),
    .in0_cnt_interrupted_i(in0_cnt_interrupted_i),
    .in0_cnt_seqmm_i(in0_cnt_seqmm_i),
    .in0_cnt_tu_i(in0_cnt_tu_i),
    .in0_cnt_unsupp_i(in0_cnt_unsupp_i),
    .in0_cnt_frx_i(in0_cnt_frx_i),
    .in0_cnt_mreset_i(in0_cnt_mreset_i),
    .in0_cnt_late_i(in0_cnt_late_i),
    .in0_cnt_early_i(in0_cnt_early_i),
    .in0_cnt_dirty_p_i(in0_cnt_dirty_p_i),
    .in0_fmt_o(in0_fmt_o), .clk_src_o(clk_src_o),
    .st_addr_o(st_raddr_w), .st_rd_o(st_rd_w), .st_byte_i(st_ovl_byte_w),
    .st_waddr_o(st_waddr_w), .st_wr_o(st_wr_w), .st_wdata_o(st_wdata_w),
    .m_axis_tdata(m_axis_tdata), .m_axis_tkeep(m_axis_tkeep),
    .m_axis_tvalid(m_axis_tvalid), .m_axis_tlast(m_axis_tlast),
    .m_axis_tready(m_axis_tready),
    .evt_cmd_o(evt_cmd_w), .evt_resp_o(evt_resp_w), .evt_drop_o(evt_drop_w)
  );

  // ---- status counters ----------------------------------------------
  logic [15:0] cmd_cnt_r, resp_cnt_r;
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      cmd_cnt_r <= 16'd0; resp_cnt_r <= 16'd0;
    end else begin
      if (evt_cmd_w)  cmd_cnt_r  <= cmd_cnt_r  + 16'd1;
      if (evt_resp_w) resp_cnt_r <= resp_cnt_r + 16'd1;
    end
  end

  assign locked_o         = l0_state_w.locked;
  assign current_config_o = l0_state_w.current_configuration_index;
  assign cmd_count_o      = cmd_cnt_r;
  assign resp_count_o     = resp_cnt_r;

  // verilator lint_off UNUSED
  wire unused = &{1'b0, val_status_w, evt_drop_w, l0_state_w.entity_id};
  // verilator lint_on  UNUSED

endmodule

`default_nettype wire

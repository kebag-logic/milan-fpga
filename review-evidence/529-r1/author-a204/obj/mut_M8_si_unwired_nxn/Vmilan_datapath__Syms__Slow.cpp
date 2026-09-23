// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vmilan_datapath__pch.h"

Vmilan_datapath__Syms::Vmilan_datapath__Syms(VerilatedContext* contextp, const char* namep, Vmilan_datapath* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(4933);
    // Setup sub module instances
    TOP__milan_datapath__DOT__rx_axis_fabric.ctor(this, "milan_datapath.rx_axis_fabric");
    TOP__milan_datapath__DOT__rx_axis_from_mac.ctor(this, "milan_datapath.rx_axis_from_mac");
    TOP__milan_datapath__DOT__tx_axis_to_mac.ctor(this, "milan_datapath.tx_axis_to_mac");
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    TOP.__PVT__milan_datapath__DOT__rx_axis_fabric = &TOP__milan_datapath__DOT__rx_axis_fabric;
    TOP.__PVT__milan_datapath__DOT__rx_axis_from_mac = &TOP__milan_datapath__DOT__rx_axis_from_mac;
    TOP.__PVT__milan_datapath__DOT__tx_axis_to_mac = &TOP__milan_datapath__DOT__tx_axis_to_mac;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    TOP__milan_datapath__DOT__rx_axis_fabric.__Vconfigure(true);
    TOP__milan_datapath__DOT__rx_axis_from_mac.__Vconfigure(false);
    TOP__milan_datapath__DOT__tx_axis_to_mac.__Vconfigure(false);
    // Setup scopes
    __Vscopep_milan_datapath = new VerilatedScope{this, "milan_datapath", "milan_datapath", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__chan_map_capture = new VerilatedScope{this, "milan_datapath.chan_map_capture", "chan_map_capture", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__media_clock_restart = new VerilatedScope{this, "milan_datapath.media_clock_restart", "media_clock_restart", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__pp_shadow__u_pp__u_aecp__u_dyn = new VerilatedScope{this, "milan_datapath.pp_shadow.u_pp.u_aecp.u_dyn", "u_dyn", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__talker_diag = new VerilatedScope{this, "milan_datapath.talker_diag", "talker_diag", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_milan_datapath->varInsert("aaf_stream_en_raw_w", &(TOP.milan_datapath__DOT__aaf_stream_en_raw_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("aaf_stream_en_w", &(TOP.milan_datapath__DOT__aaf_stream_en_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("amap_edit_out_resv_r", &(TOP.milan_datapath__DOT__amap_edit_out_resv_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("asp_count_w", &(TOP.milan_datapath__DOT__asp_count_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("asp_gen_w", &(TOP.milan_datapath__DOT__asp_gen_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("asp_path_w", &(TOP.milan_datapath__DOT__asp_path_w), false, VLVT_WDATA, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,447,0);
    __Vscopep_milan_datapath->varInsert("asp_resp_capture_w", &(TOP.milan_datapath__DOT__asp_resp_capture_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("asp_resp_entry_w", &(TOP.milan_datapath__DOT__asp_resp_entry_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("avtprx_accept_p", &(TOP.milan_datapath__DOT__avtprx_accept_p), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("avtprx_idx", &(TOP.milan_datapath__DOT__avtprx_idx), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,1,0);
    __Vscopep_milan_datapath->varInsert("chmap_phys_v_w", &(TOP.milan_datapath__DOT__chmap_phys_v_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("clkv_tu_w", &(TOP.milan_datapath__DOT__clkv_tu_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("crf_clk_selected_r", &(TOP.milan_datapath__DOT__crf_clk_selected_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_milan_datapath->varInsert("crf_earlycnt_w", &(TOP.milan_datapath__DOT__crf_earlycnt_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("crf_intrcnt_w", &(TOP.milan_datapath__DOT__crf_intrcnt_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("crf_latecnt_w", &(TOP.milan_datapath__DOT__crf_latecnt_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("crf_lockcnt_w", &(TOP.milan_datapath__DOT__crf_lockcnt_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("crf_mrcnt_w", &(TOP.milan_datapath__DOT__crf_mrcnt_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("crf_tucnt_w", &(TOP.milan_datapath__DOT__crf_tucnt_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("crf_unlockcnt_w", &(TOP.milan_datapath__DOT__crf_unlockcnt_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("ctr_gmchg_r", &(TOP.milan_datapath__DOT__ctr_gmchg_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("lb_dup_cnt_w", &(TOP.milan_datapath__DOT__lb_dup_cnt_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("lb_skip_cnt_w", &(TOP.milan_datapath__DOT__lb_skip_cnt_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("lb_tap_tlast_w", &(TOP.milan_datapath__DOT__lb_tap_tlast_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("lb_tap_tuser_w", &(TOP.milan_datapath__DOT__lb_tap_tuser_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("lb_tap_tvalid_w", &(TOP.milan_datapath__DOT__lb_tap_tvalid_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("mcsrv_stat_w", &(TOP.milan_datapath__DOT__mcsrv_stat_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("media_clk_src_r", &(TOP.milan_datapath__DOT__media_clk_src_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("media_tick_p", &(TOP.milan_datapath__DOT__media_tick_p), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("media_tick_phase_w", &(TOP.milan_datapath__DOT__media_tick_phase_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("mga_engaged_w", &(TOP.milan_datapath__DOT__mga_engaged_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("mga_err_w", &(TOP.milan_datapath__DOT__mga_err_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_SIGNED|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("mnco_servo_en_w", &(TOP.milan_datapath__DOT__mnco_servo_en_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("mnco_servo_trim_w", &(TOP.milan_datapath__DOT__mnco_servo_trim_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_SIGNED|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("pp_aecp_clk_src_index_w", &(TOP.milan_datapath__DOT__pp_aecp_clk_src_index_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("pp_aecp_cur_config_w", &(TOP.milan_datapath__DOT__pp_aecp_cur_config_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("pp_aecp_identify_w", &(TOP.milan_datapath__DOT__pp_aecp_identify_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY, 0, 1 ,7,0);
    __Vscopep_milan_datapath->varInsert("pp_cd_acmp_bound_w", &(TOP.milan_datapath__DOT__pp_cd_acmp_bound_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,4,0);
    __Vscopep_milan_datapath->varInsert("pp_cd_acmp_declaring_w", &(TOP.milan_datapath__DOT__pp_cd_acmp_declaring_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,4,0);
    __Vscopep_milan_datapath->varInsert("pp_cd_adp_avail_index_w", &(TOP.milan_datapath__DOT__pp_cd_adp_avail_index_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("pp_ctr_evt_index_w", &(TOP.milan_datapath__DOT__pp_ctr_evt_index_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("pp_ctr_evt_type_w", &(TOP.milan_datapath__DOT__pp_ctr_evt_type_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("pp_ctr_evt_valid_w", &(TOP.milan_datapath__DOT__pp_ctr_evt_valid_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_milan_datapath->varInsert("pp_gm_change_p_w", &(TOP.milan_datapath__DOT__pp_gm_change_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_milan_datapath->varInsert("pp_gm_id_change_p_w", &(TOP.milan_datapath__DOT__pp_gm_id_change_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_milan_datapath->varInsert("pp_maap_req_ready_w", &(TOP.milan_datapath__DOT__pp_maap_req_ready_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("pp_maap_req_release_w", &(TOP.milan_datapath__DOT__pp_maap_req_release_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("pp_maap_req_valid_w", &(TOP.milan_datapath__DOT__pp_maap_req_valid_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("pp_maap_rsp_da_w", &(TOP.milan_datapath__DOT__pp_maap_rsp_da_w), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,47,0);
    __Vscopep_milan_datapath->varInsert("pp_maap_rsp_ok_w", &(TOP.milan_datapath__DOT__pp_maap_rsp_ok_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("pp_maap_rsp_valid_w", &(TOP.milan_datapath__DOT__pp_maap_rsp_valid_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("rend_pcm_tvalid_w", &(TOP.milan_datapath__DOT__rend_pcm_tvalid_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("render_recentre_p_w", &(TOP.milan_datapath__DOT__render_recentre_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("rsp_converged_w", &(TOP.milan_datapath__DOT__rsp_converged_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("rsp_fill_w", &(TOP.milan_datapath__DOT__rsp_fill_w), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_milan_datapath->varInsert("rsp_overruns_w", &(TOP.milan_datapath__DOT__rsp_overruns_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("rsp_pop_p_w", &(TOP.milan_datapath__DOT__rsp_pop_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("rsp_prefill_w", &(TOP.milan_datapath__DOT__rsp_prefill_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("rsp_rails_w", &(TOP.milan_datapath__DOT__rsp_rails_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("rsp_recentres_w", &(TOP.milan_datapath__DOT__rsp_recentres_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("rsp_tdata_w", &(TOP.milan_datapath__DOT__rsp_tdata_w), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,63,0);
    __Vscopep_milan_datapath->varInsert("rsp_tvalid_w", &(TOP.milan_datapath__DOT__rsp_tvalid_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("rsp_underruns_w", &(TOP.milan_datapath__DOT__rsp_underruns_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("src_recentre_p_r", &(TOP.milan_datapath__DOT__src_recentre_p_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_milan_datapath->varInsert("strtbl_bind_fall_w", &(TOP.milan_datapath__DOT__strtbl_bind_fall_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("strtbl_en_w", &(TOP.milan_datapath__DOT__strtbl_en_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("strtbl_sid_w", &(TOP.milan_datapath__DOT__strtbl_sid_w), false, VLVT_WDATA, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,255,0);
    __Vscopep_milan_datapath->varInsert("tdm_dup_cnt_w", &(TOP.milan_datapath__DOT__tdm_dup_cnt_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("tdm_skip_cnt_w", &(TOP.milan_datapath__DOT__tdm_skip_cnt_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("tdmr_adopt_p_w", &(TOP.milan_datapath__DOT__tdmr_adopt_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("tdmr_commit_en_w", &(TOP.milan_datapath__DOT__tdmr_commit_en_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("tdmr_commit_p_w", &(TOP.milan_datapath__DOT__tdmr_commit_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("tdmr_epochs_w", &(TOP.milan_datapath__DOT__tdmr_epochs_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("tdmr_frame_p_w", &(TOP.milan_datapath__DOT__tdmr_frame_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath->varInsert("tdmr_frames_w", &(TOP.milan_datapath__DOT__tdmr_frames_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("tdmr_lane_streams_w", &(TOP.milan_datapath__DOT__tdmr_lane_streams_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 1 ,3,0);
    __Vscopep_milan_datapath->varInsert("tdmr_overruns_w", &(TOP.milan_datapath__DOT__tdmr_overruns_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("tdmr_skips_w", &(TOP.milan_datapath__DOT__tdmr_skips_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("tdmr_underruns_w", &(TOP.milan_datapath__DOT__tdmr_underruns_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_milan_datapath->varInsert("tkd_dirty_p_w", &(TOP.milan_datapath__DOT__tkd_dirty_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 1 ,4,0);
    __Vscopep_milan_datapath__chan_map_capture->varInsert("tdm_fed_r", &(TOP.milan_datapath__DOT__chan_map_capture__DOT__tdm_fed_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_milan_datapath__chan_map_capture->varInsert("tdm_frame_pend_r", &(TOP.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_milan_datapath__chan_map_capture->varInsert("tdm_hold_r", &(TOP.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RD, 1, 1 ,0,3 ,47,0);
    __Vscopep_milan_datapath__chan_map_capture->varInsert("tdm_pair_valid_i", &(TOP.milan_datapath__DOT__chan_map_capture__DOT__tdm_pair_valid_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 0);
    __Vscopep_milan_datapath__media_clock_restart->varInsert("tgt_r", &(TOP.milan_datapath__DOT__media_clock_restart__DOT__tgt_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_milan_datapath__pp_shadow__u_pp__u_aecp__u_dyn->varInsert("clksrc_r", &(TOP.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,0 ,15,0);
    __Vscopep_milan_datapath__talker_diag->varInsert("ftx_r", &(TOP.milan_datapath__DOT__talker_diag__DOT__ftx_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,4 ,31,0);
    __Vscopep_milan_datapath__talker_diag->varInsert("mreset_r", &(TOP.milan_datapath__DOT__talker_diag__DOT__mreset_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,4 ,31,0);
    __Vscopep_milan_datapath__talker_diag->varInsert("start_r", &(TOP.milan_datapath__DOT__talker_diag__DOT__start_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,4 ,31,0);
    __Vscopep_milan_datapath__talker_diag->varInsert("stop_r", &(TOP.milan_datapath__DOT__talker_diag__DOT__stop_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,4 ,31,0);
    __Vscopep_milan_datapath__talker_diag->varInsert("tuiv_r", &(TOP.milan_datapath__DOT__talker_diag__DOT__tuiv_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,4 ,31,0);
}

Vmilan_datapath__Syms::~Vmilan_datapath__Syms() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_milan_datapath, __Vscopep_milan_datapath = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__chan_map_capture, __Vscopep_milan_datapath__chan_map_capture = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__media_clock_restart, __Vscopep_milan_datapath__media_clock_restart = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__pp_shadow__u_pp__u_aecp__u_dyn, __Vscopep_milan_datapath__pp_shadow__u_pp__u_aecp__u_dyn = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__talker_diag, __Vscopep_milan_datapath__talker_diag = nullptr);
    // Tear down sub module instances
    TOP__milan_datapath__DOT__tx_axis_to_mac.dtor();
    TOP__milan_datapath__DOT__rx_axis_from_mac.dtor();
    TOP__milan_datapath__DOT__rx_axis_fabric.dtor();
}

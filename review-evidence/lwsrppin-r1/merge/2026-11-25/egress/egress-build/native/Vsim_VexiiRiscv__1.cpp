// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__14(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__14\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__FetchL1Plugin_logic_refill_pushCounter 
        = vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_pushCounter;
    vlSelfRef.__PVT__AlignerPlugin_logic_feeder_harts_0_dopId 
        = vlSelfRef.__Vdly__AlignerPlugin_logic_feeder_harts_0_dopId;
    vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_ls_storeId 
        = vlSelfRef.__Vdly__LsuPlugin_logic_onAddress0_ls_storeId;
    vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_SEL_lane0 
        = vlSelfRef.__Vdly__execute_ctrl3_up_LsuL1_SEL_lane0;
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_validBuffer 
        = vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_interrupt_validBuffer;
    vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_id 
        = vlSelfRef.__Vdly__PcPlugin_logic_harts_0_self_id;
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_pushCounter 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_pushCounter;
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_busy 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_busy;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid;
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat;
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2 
        = vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2;
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2 
        = vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2;
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2 
        = vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2;
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2 
        = vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2;
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2 
        = vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2;
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2 
        = vlSelfRef.__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2;
    vlSelfRef.__PVT__DecoderPlugin_logic_harts_0_uopId 
        = vlSelfRef.__Vdly__DecoderPlugin_logic_harts_0_uopId;
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loaded 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loaded;
    vlSelfRef.FetchL1Plugin_logic_bus_cmd_ready = (1U 
                                                   & (~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_bus_a_rValid)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_value 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_c_freezeTimeout_counter_value;
    vlSelfRef.__PVT__fetch_logic_ctrls_1_up_valid = vlSelfRef.__Vdly__fetch_logic_ctrls_1_up_valid;
    vlSelfRef.LsuPlugin_logic_bus_cmd_ready = (1U & 
                                               (~ (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_dBus_bus_a_rValid)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_full 
        = (0U == (2U ^ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push) 
                        ^ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop))));
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_wordIndex 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_read_wordIndex;
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_wordIndex 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_write_wordIndex;
    vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg 
        = vlSelfRef.__Vdly__CsrRamPlugin_logic_readLogic_ohReg;
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight;
    vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_wordIndex 
        = vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_onRsp_wordIndex;
    vlSelfRef.__PVT__integer_RegFilePlugin_logic_initalizer_counter 
        = vlSelfRef.__Vdly__integer_RegFilePlugin_logic_initalizer_counter;
    vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mpie 
        = vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mpie;
    vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mie 
        = vlSelfRef.__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mie;
    vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid 
        = vlSelfRef.__Vdly__FetchL1Plugin_logic_refill_slots_0_valid;
    vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter 
        = vlSelfRef.__Vdly__CsrRamPlugin_logic_flush_counter;
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_flushReg 
        = vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_flushReg;
    vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter 
        = vlSelfRef.__Vdly__FetchL1Plugin_logic_invalidate_counter;
    vlSelfRef.__PVT__execute_ctrl1_up_LANE_SEL_lane0 
        = vlSelfRef.__Vdly__execute_ctrl1_up_LANE_SEL_lane0;
    vlSelfRef.__PVT__execute_ctrl3_up_LANE_SEL_lane0 
        = vlSelfRef.__Vdly__execute_ctrl3_up_LANE_SEL_lane0;
    vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent 
        = vlSelfRef.__Vdly__FetchL1Plugin_logic_ctrl_trapSent;
    vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid = vlSelfRef.__Vdly__fetch_logic_ctrls_2_up_valid;
    vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_initializer_counter;
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled 
        = vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_inject_sampled;
    vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rValid 
        = vlSelfRef.__Vdly__LsuPlugin_logic_bus_rsp_toStream_rValid;
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid;
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_valid 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_valid;
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_wordIndex 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_read_wordIndex;
    vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0 
        = vlSelfRef.__Vdly__execute_ctrl2_up_LANE_SEL_lane0;
    vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0 
        = vlSelfRef.__Vdly__execute_ctrl4_up_LANE_SEL_lane0;
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_ready 
        = (1U & (~ ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_bus_e_rValid) 
                    & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rValid))));
    vlSelfRef.__PVT__fetch_logic_ctrls_0_up_isValid 
        = (1U & (~ (IData)(vlSelfRef.__PVT__PcPlugin_logic_harts_0_holdReg)));
    vlSelfRef.__PVT__when_RegFilePlugin_l132 = (1U 
                                                & (~ 
                                                   ((IData)(vlSelfRef.__PVT__integer_RegFilePlugin_logic_initalizer_counter) 
                                                    >> 5U)));
    vlSelfRef.__PVT___zz_when = (1U & (~ (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid)));
    vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_askCmd 
        = ((~ (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_cmdSent)) 
           & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid));
    vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_2_valid 
        = ((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_meip) 
           & (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_meie));
    vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_1_valid 
        = ((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_msip) 
           & (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_msie));
    vlSelfRef.__PVT___zz_CsrRamPlugin_logic_flush_counter_1 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter) 
                    >> 2U)));
    vlSelfRef.__PVT___zz_fetch_logic_ctrls_0_haltRequest_FetchL1Plugin_l218 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                    >> 7U)));
    vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counterIncr 
        = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter)));
    vlSelfRef.__PVT___zz_4 = (1U & ((~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                                        >> 7U)) | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_valid)));
    vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_tag_loaded = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                  >> 7U)))) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_tag_loaded = 0U;
    }
    if ((0x00000080U & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter))) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_tag_loaded = 1U;
    }
    vlSelfRef.__PVT__TrapPlugin_logic_fetchL1Invalidate_0_cmd_ready = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                  >> 7U)))) {
        if ((0x00000080U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter)))) {
            vlSelfRef.__PVT__TrapPlugin_logic_fetchL1Invalidate_0_cmd_ready = 1U;
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_1 
        = (0x0000000fU & ((((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo_io_pop_valid) 
                            << 3U) | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid) 
                                      << 2U)) | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo_io_pop_valid) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid))));
    vlSelfRef.__PVT__when_FetchL1Plugin_l545 = (1U 
                                                & (~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid)));
    vlSelfRef.LsuPlugin_logic_bus_cmd_valid = ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_allowIt) 
                                               & ((~ 
                                                   ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_cmdSent) 
                                                    | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_tooEarly))) 
                                                  & (IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_doItReg)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_FORCE_HAZARD 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                    >> 7U)));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_resetToRunConditions_0 
        = (1U & (~ ((~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter) 
                        >> 2U)) | ((~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                                       >> 7U)) | ((~ 
                                                   ((IData)(vlSelfRef.__PVT__integer_RegFilePlugin_logic_initalizer_counter) 
                                                    >> 5U)) 
                                                  | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_firstEver))))));
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCount 
        = (1U & (2U >> (IData)(vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0)));
    vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCount_1 
        = ((IData)(vlSelfRef.__PVT__decode_ctrls_1_up_valid) 
           & ((~ (IData)(vlSelfRef.__PVT__DispatchPlugin_logic_feeds_0_sent)) 
              & (IData)(vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0)));
    if (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1) {
        vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy = 0U;
    } else {
        if (vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div_io_cmd_ready) {
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy 
                = vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div_io_cmd_valid;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
            vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy = 0U;
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_free 
        = (1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid)));
    vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid 
        = (((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_mtip) 
            & (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_mtie)) 
           | (IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_1_valid));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_2 
        = ((~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_1) 
               - (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_0) 
                   << 1U) | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_1)))) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_1));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__15(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__15\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*1:0*/ __PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_3;
    __PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_3 = 0;
    // Body
    vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id_1 
        = (1U & ((~ (IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_2_valid)) 
                 | ((1U > ((IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_1_valid)
                            ? 2U : 3U)) & (IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid))));
    __PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_3 
        = (3U & (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_2) 
                  >> 2U) | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_2)));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div_io_cmd_ready 
        = (1U & (~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__busy)));
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__locked) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_1 
            = (1U & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_1));
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_0));
    } else {
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_1 
            = (1U & ((IData)(__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_3) 
                     >> 1U));
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0 
            = (1U & (IData)(__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_3));
    }
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__16(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__16\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.LsuPlugin_logic_bus_rsp_valid = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_dBus_noDecoder_toDown_d_rValid;
    vlSelfRef.FetchL1Plugin_logic_bus_rsp_valid = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid;
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__17(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__17\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.PrivilegedPlugin_logic_harts_0_int_m_software 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_softwareInterrupt;
}

extern const VlUnpacked<CData/*0:0*/, 32> Vsim__ConstPool__TABLE_h19c9bdaa_0;

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__18(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__18\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__counter 
        = vlSelfRef.__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter;
    vlSelfRef.PrivilegedPlugin_logic_harts_0_int_m_timer 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__peripheral_clint_thread_core__DOT__logic_harts_0_timerInterrupt;
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_timer_counter 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_timer_counter;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93 = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_CLEAN_lane0) 
                                                 | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_INVALID_lane0));
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedCounter 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_refill_slots_0_loadedCounter;
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty;
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_payload_error 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_denied) 
           | (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_corrupt));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15 = (((
                                                   (((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_Fetch_PC_FAULT) 
                                                     << 3U) 
                                                    | ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_HAZARD) 
                                                       << 2U)) 
                                                   | (((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_REFILL) 
                                                       << 1U) 
                                                      | (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_ACCESS_FAULT))) 
                                                  << 3U) 
                                                 | (((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_PAGE_FAULT) 
                                                     << 2U) 
                                                    | (((IData)(vlSelfRef.__PVT__when_FetchL1Plugin_l488) 
                                                        << 1U) 
                                                       | (1U 
                                                          & ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HIT)) 
                                                             | (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_HAZARD))))));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_WB_HAZARD) 
           | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_SET_HAZARD) 
              | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_FORCE_HAZARD) 
                 | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_LOCK_HIT))));
    if (vlSelfRef.__PVT__when_LsuPlugin_l1000) {
        if (vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_WAIT_REFILL_lane0) {
            vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_refill 
                = vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_WAIT_REFILL_lane0;
        }
    }
    if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_down_valid) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_arg 
            = (7U & (IData)((vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_trap_pending_arbiter_down_payload_exception 
                             >> 0x00000026U)));
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code 
            = (0x0000001fU & (IData)((vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_trap_pending_arbiter_down_payload_exception 
                                      >> 0x00000021U)));
    }
    if ((1U & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_data 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_payload_data;
    }
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg 
        = vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap;
    if (Vsim__ConstPool__TABLE_h19c9bdaa_0[(((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_trigger_oh) 
                                             << 4U) 
                                            | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))]) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_valid 
            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_result_valid;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_DIRTY) 
           & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_UNIQUE)) 
              & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA)));
    if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        if ((2U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            if ((3U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
                vlSelfRef.__PVT__REG_CSR_772 = (0x0304U 
                                                == 
                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_768 = (0x0300U 
                                                == 
                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U));
                vlSelfRef.__PVT__REG_CSR_834 = (0x0342U 
                                                == 
                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U));
            }
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_loaded 
            = (1U & vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1);
        vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0 
            = vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_LSU_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_SEL_lane0 
            = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0)) 
               & ((0x00002050U == (0x00002050U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                  | (0x00001050U == (0x00001050U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))));
        vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem
            [(0x0000007fU & (vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
                             >> 6U))];
        vlSelfRef.__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_LSU_lane0 = 1U;
        vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0 
            = vlSelfRef.__PVT__execute_ctrl0_down_COMPLETED_lane0;
        vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
            = vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA;
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt 
        = ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_valid) 
           & (0U == (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_loadedDirties 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_SHARED_lane0_dirty) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_loaded));
    vlSelfRef.__PVT__when_LsuL1Plugin_l1168 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HIT) 
                                               & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA) 
                                                  | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_TAG_UPDATE)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_UNIQUE 
        = ((IData)(vlSelfRef.__PVT__when_LsuL1Bus_l235)
            ? (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE)
            : (0U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_param)));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_code 
        = ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt)
            ? (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_code)
            : (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code));
    vlSelfRef.__PVT__when_TrapPlugin_l454 = ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_exception) 
                                             | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt));
    if (vlSelfRef.__VdlySet__LsuL1Plugin_logic_ways_0_mem__v0) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_ways_0_mem[vlSelfRef.__VdlyDim0__LsuL1Plugin_logic_ways_0_mem__v0] 
            = vlSelfRef.__VdlyVal__LsuL1Plugin_logic_ways_0_mem__v0;
    }
    vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_SrcStageables_REVERT_lane0) 
           + (vlSelfRef.__PVT__early0_SrcPlugin_logic_addsub_combined_rs2Patched 
              + vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE 
        = vlSelfRef.__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE;
    vlSelfRef.__PVT___zz_early0_IntAluPlugin_logic_alu_result_5 
        = (1U & (((vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                   >> 0x0000001fU) == (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0 
                                       >> 0x0000001fU))
                  ? (vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address 
                     >> 0x0000001fU) : ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_SrcStageables_UNSIGNED_lane0)
                                         ? (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0 
                                            >> 0x0000001fU)
                                         : (vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 
                                            >> 0x0000001fU))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE) 
                                                 & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE));
    vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_address 
        = ((((2U == (2U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                           >> 0x00000014U))) | (0U 
                                                == 
                                                (0x0040U 
                                                 & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                    >> 0x00000014U)))) 
            << 1U) | (1U == (3U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                   >> 0x00000014U))));
    vlSelfRef.__PVT__COMB_CSR_CsrRamPlugin_csrMapper_selFilter 
        = ((0x0341U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                        >> 0x00000014U)) | ((0x0305U 
                                             == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U)) 
                                            | ((0x0340U 
                                                == 
                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U)) 
                                               | (0x0343U 
                                                  == 
                                                  (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                   >> 0x00000014U)))));
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_alu_mask 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_IMM_lane0)
            ? (0x0000001fU & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                              >> 0x0000000fU)) : vlSelfRef.__PVT__execute_ctrl2_up_integer_RS1_lane0);
    vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_write 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_MASK_lane0) 
                    & (0U == (0x000f8000U & vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87 = (((
                                                   (2U 
                                                    == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_BranchPlugin_BRANCH_CTRL_lane0))
                                                    ? vlSelfRef.__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0
                                                    : vlSelfRef.__PVT__execute_ctrl2_up_PC_lane0) 
                                                  + 
                                                  ((1U 
                                                    == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_BranchPlugin_BRANCH_CTRL_lane0))
                                                    ? 
                                                   ((((0x00000ffeU 
                                                       & ((- (IData)(
                                                                     (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                      >> 0x0000001fU))) 
                                                          << 1U)) 
                                                      | (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                         >> 0x0000001fU)) 
                                                     << 0x00000014U) 
                                                    | ((((0x000001feU 
                                                          & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                             >> 0x0000000bU)) 
                                                         | (1U 
                                                            & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                               >> 0x00000014U))) 
                                                        << 0x0000000bU) 
                                                       | (0x000007feU 
                                                          & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                             >> 0x00000014U))))
                                                    : 
                                                   ((2U 
                                                     == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_BranchPlugin_BRANCH_CTRL_lane0))
                                                     ? 
                                                    (((- (IData)(
                                                                 (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                  >> 0x0000001fU))) 
                                                      << 0x0000000cU) 
                                                     | (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                        >> 0x00000014U))
                                                     : 
                                                    (((- (IData)(
                                                                 (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                  >> 0x0000001fU))) 
                                                      << 0x0000000dU) 
                                                     | ((((2U 
                                                           & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                              >> 0x0000001eU)) 
                                                          | (1U 
                                                             & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                >> 7U))) 
                                                         << 0x0000000bU) 
                                                        | ((0x000007e0U 
                                                            & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                               >> 0x00000014U)) 
                                                           | (0x0000001eU 
                                                              & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                 >> 7U)))))))) 
                                                 >> 1U);
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__19(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__19\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0 
            = vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0;
    }
    vlSelfRef.__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_jumpLogic_COND_lane0 
        = (1U & ((2U == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_BranchPlugin_BRANCH_CTRL_lane0)) 
                 | ((1U == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_BranchPlugin_BRANCH_CTRL_lane0)) 
                    | ((0U == (7U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                     >> 0x0000000cU)))
                        ? (IData)(vlSelfRef.__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_alu_EQ_lane0)
                        : ((1U == (7U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                         >> 0x0000000cU)))
                            ? (~ (IData)(vlSelfRef.__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_alu_EQ_lane0))
                            : ((5U == (5U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                             >> 0x0000000cU)))
                                ? (~ (IData)(vlSelfRef.__PVT___zz_early0_IntAluPlugin_logic_alu_result_5))
                                : (IData)(vlSelfRef.__PVT___zz_early0_IntAluPlugin_logic_alu_result_5)))))));
    vlSelfRef.__PVT__execute_ctrl1_down_early0_SrcPlugin_logic_SRC2_CTRL_lane0 
        = ((((4U == (4U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
             | (0x00000020U == (0x00000070U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))) 
            << 1U) | ((0U == (0x00000050U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                      | (0U == (0x00000024U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86 = ((4U 
                                                  == 
                                                  (4U 
                                                   & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
                                                 | (0U 
                                                    == 
                                                    (0x00004000U 
                                                     & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
    vlSelfRef.__PVT___zz_execute_ctrl1_down_AguPlugin_SEL_lane0 
        = ((0U == (0x00000058U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)) 
           | (0U == (0x00001050U & vlSelfRef.__PVT__execute_ctrl1_up_Decode_UOP_lane0)));
    if (vlSelfRef.__PVT__decode_ctrls_0_down_isReady) {
        vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
            = vlSelfRef.__PVT__decode_ctrls_0_down_Decode_INSTRUCTION_0;
    }
    vlSelfRef.__PVT__decode_ctrls_0_down_Decode_INSTRUCTION_0 
        = ((vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_BANKS_MUXES_1 
            & (- (IData)((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_1)))) 
           | (vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_BANKS_MUXES_0 
              & (- (IData)((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_0)))));
    vlSelfRef.__PVT___zz_decode_ctrls_1_down_DispatchPlugin_FENCE_OLDER_0 
        = ((0x00002050U == (0x00002050U & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
           | (0x00001050U == (0x00001050U & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__20(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__20\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onD_sel 
        = ((5U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode)) 
           | ((4U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode)) 
              | ((1U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode)) 
                 | (0U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode)))));
}

extern const VlUnpacked<CData/*0:0*/, 256> Vsim__ConstPool__TABLE_hef103ca9_0;
extern const VlUnpacked<CData/*0:0*/, 256> Vsim__ConstPool__TABLE_hb7cce103_0;

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_write_payload_address 
        = ((0x000007f0U & (vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_address 
                           >> 2U)) | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_wordIndex));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83 = ((IData)(vlSelfRef.__PVT__execute_ctrl5_up_LANE_SEL_lane0) 
                                                 & (IData)(vlSelfRef.__PVT__execute_ctrl5_up_RD_ENABLE_lane0));
    vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input 
        = ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_cmdSent)
            ? vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rData_data
            : (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_BANKS_MUXES_lane0_0 
               & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)))));
    vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_address = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                  >> 7U)))) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_address 
            = (0x0000007fU & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter));
    }
    vlSelfRef.__PVT__fetch_logic_ctrls_0_down_FetchL1Plugin_logic_cmd_PLRU_BYPASS_DATA_0 
        = ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_payload_data_0) 
           & ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
              >> 7U));
    vlSelfRef.__PVT__FetchL1Plugin_logic_refill_start_valid 
        = ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid) 
           & ((~ (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent)) 
              & Vsim__ConstPool__TABLE_hef103ca9_0[
              ((((((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_Fetch_PC_FAULT) 
                   << 3U) | ((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_HAZARD) 
                             << 2U)) | (((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_REFILL) 
                                         << 1U) | (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_ACCESS_FAULT))) 
                << 4U) | ((((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_PAGE_FAULT) 
                            << 3U) | ((IData)(vlSelfRef.__PVT__when_FetchL1Plugin_l488) 
                                      << 2U)) | (((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_HAZARD) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HIT))))]));
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackRequest 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid) 
           & (6U == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackTimer)));
    vlSelfRef.__PVT__when_CsrService_l199 = (1U & (~ 
                                                   ((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_mcounteren_tm) 
                                                    | VL_LTES_III(3, 3U, (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege)))));
    vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_accessFault 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_CACHED_RSP_lane0_fault)
            ? ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rValid) 
               & (IData)(vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rData_error))
            : (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_FAULT_lane0));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_refillHazards 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_valid) 
           & ((0x0000003fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_address 
                              >> 6U)) == (0x0000003fU 
                                          & (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0 
                                             >> 6U))));
    vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_readCmdDone)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid));
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_slotsWithId_0_0 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid) 
           & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_writeCmdDone)) 
              & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_victimBufferReady)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_writebackHazards 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid) 
           & ((0x0000003fU & (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0 
                              >> 6U)) == (0x0000003fU 
                                          & (vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_address 
                                             >> 6U))));
    vlSelfRef.__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_valid 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_AguPlugin_SEL_lane0));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_request 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_DivPlugin_SEL_lane0));
    vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_valid 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_SEL_lane0));
    vlSelfRef.__PVT__when_LsuPlugin_l915 = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0) 
                                            & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_AguPlugin_SEL_lane0));
    vlSelfRef.FetchL1Plugin_logic_bus_cmd_valid = ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onCmd_locked)
                                                    ? (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onCmd_lockedOh)
                                                    : (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_askCmd));
    vlSelfRef.__PVT___zz_FetchL1Plugin_logic_ways_0_mem_port 
        = ((0x001ffffcU & ((vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_address 
                            >> 0x0000000bU) & ((- (IData)(
                                                          (1U 
                                                           & ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                                                              >> 7U)))) 
                                               << 2U))) 
           | ((0x03fffffeU & (((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                               >> 6U) & (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid) 
                                          & (IData)(vlSelfRef.FetchL1Plugin_logic_bus_rsp_payload_error)) 
                                         << 1U))) | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_tag_loaded)));
    vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                  >> 7U)))) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask = 3U;
    }
    if ((0x00000080U & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter))) {
        vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_address 
            = (0x0000007fU & (vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_address 
                              >> 6U));
        vlSelfRef.__PVT__FetchL1Plugin_logic_plru_write_payload_address 
            = (0x0000007fU & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_payload_address));
        if (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_iBus_noDecoder_toDown_d_rValid) 
             & ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_firstCycle) 
                | (IData)(vlSelfRef.FetchL1Plugin_logic_bus_rsp_payload_error)))) {
            vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask 
                = ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask) 
                   | (3U & ((IData)(1U) << (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_wayToAllocate))));
        }
    } else {
        vlSelfRef.__PVT__FetchL1Plugin_logic_plru_write_payload_address 
            = (0x0000007fU & (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter));
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_last 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty)) 
                 | (0x0fU == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_wordIndex))));
    vlSelfRef.__PVT__decode_ctrls_0_down_TRAP_0 = ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent) 
                                                   | Vsim__ConstPool__TABLE_hb7cce103_0
                                                   [
                                                   ((0x00000080U 
                                                     & (((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid)) 
                                                         | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent)) 
                                                        << 7U)) 
                                                    | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15))]);
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_result_valid 
        = ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid) 
           & (VL_GTS_III(3, 3U, (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege)) 
              | (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mie)));
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0 
        = ((~ ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0)) 
               & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0))) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_SEL_lane0));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76 = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
                                                 & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_SEL_lane0));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_targetPrivilege 
        = ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt)
            ? (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_targetPrivilege)
            : (VL_GTS_III(3, 3U, (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege))
                ? 3U : (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_coherencyHazard = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD)))) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
                vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_coherencyHazard = 1U;
            }
        }
    }
    vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_xretPriv 
        = ((((3U != (3U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                           >> 0x0000001cU))) & ((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege) 
                                                >> 2U)) 
            << 2U) | (3U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                            >> 0x0000001cU)));
    vlSelfRef.__PVT__early0_BranchPlugin_logic_pcPort_valid 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
           & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_BranchPlugin_SEL_lane0) 
              & (IData)(vlSelfRef.__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_jumpLogic_COND_lane0)));
    vlSelfRef.__PVT__when_DecoderPlugin_l229 = ((IData)(vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0) 
                                                & ((~ 
                                                    ((~ (IData)(vlSelfRef.__PVT__decode_ctrls_1_up_Decode_DECOMPRESSION_FAULT_0)) 
                                                     & ((0x00004063U 
                                                         == 
                                                         (0x0000407fU 
                                                          & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                        | ((0x00002013U 
                                                            == 
                                                            (0x0000207fU 
                                                             & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                           | ((0x30200073U 
                                                               == vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0) 
                                                              | ((0x10500073U 
                                                                  == vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0) 
                                                                 | ((0x00000073U 
                                                                     == 
                                                                     (0xffefffffU 
                                                                      & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                    | ((0x00000033U 
                                                                        == 
                                                                        (0xbe00707fU 
                                                                         & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                       | ((0x00005033U 
                                                                           == 
                                                                           (0xbe00707fU 
                                                                            & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                          | ((0x00005013U 
                                                                              == 
                                                                              (0xbc00707fU 
                                                                               & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                             | ((0x00001013U 
                                                                                == 
                                                                                (0xfc00305fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x00000033U 
                                                                                == 
                                                                                (0xfc00007fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x0000000fU 
                                                                                == 
                                                                                (0x0000607fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x00000063U 
                                                                                == 
                                                                                (0x0000707bU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000505fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000207fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x00000023U 
                                                                                == 
                                                                                (0x0000603fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x00000013U 
                                                                                == 
                                                                                (0x0000107fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x00000017U 
                                                                                == 
                                                                                (0x0000005fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x0000006fU 
                                                                                == 
                                                                                (0x0000007fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | ((0x00001073U 
                                                                                == 
                                                                                (0x0000107fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                                                                | (0x00002073U 
                                                                                == 
                                                                                (0x0000207fU 
                                                                                & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0))))))))))))))))))))))) 
                                                   | (IData)(vlSelfRef.__PVT__DecoderPlugin_logic_interrupt_buffered)));
    vlSelfRef.__PVT__DispatchPlugin_logic_scheduler_arbiters_0_doIt 
        = ((~ (((IData)(vlSelfRef.__PVT___zz_decode_ctrls_1_down_DispatchPlugin_FENCE_OLDER_0) 
                & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
                   & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_MAY_FLUSH_PRECISE_3_lane0))) 
               | (((IData)(vlSelfRef.__PVT___zz_decode_ctrls_1_down_DispatchPlugin_FENCE_OLDER_0) 
                   & ((IData)(vlSelfRef.__PVT__execute_ctrl1_up_LANE_SEL_lane0) 
                      & (IData)(vlSelfRef.__PVT___zz_execute_ctrl1_down_AguPlugin_SEL_lane0))) 
                  | ((((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0) 
                       | ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LANE_SEL_lane0) 
                          | ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
                             | (IData)(vlSelfRef.__PVT__execute_ctrl1_up_LANE_SEL_lane0)))) 
                      & (IData)(vlSelfRef.__PVT___zz_decode_ctrls_1_down_DispatchPlugin_FENCE_OLDER_0)) 
                     | ((((0U == (0x00000044U & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                          | ((0U == (0x00000018U & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                             | ((0x00002000U == (0x00006004U 
                                                 & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                                | (0x00001000U == (0x00005004U 
                                                   & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0))))) 
                         & (((IData)(vlSelfRef.__PVT__execute_ctrl1_up_RD_ENABLE_lane0) 
                             & ((IData)(vlSelfRef.__PVT__execute_ctrl1_up_RD_PHYS_lane0) 
                                == (0x0000001fU & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                                   >> 0x0000000fU)))) 
                            | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_RD_ENABLE_lane0) 
                                & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_BYPASSED_AT_4_lane0)) 
                                   & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_RD_PHYS_lane0) 
                                      == (0x0000001fU 
                                          & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                             >> 0x0000000fU))))) 
                               | (((~ (IData)(vlSelfRef.__PVT__execute_ctrl2_up_BYPASSED_AT_2_lane0)) 
                                   & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_RD_ENABLE_lane0) 
                                      & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_RD_PHYS_lane0) 
                                         == (0x0000001fU 
                                             & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                                >> 0x0000000fU))))) 
                                  | ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_RD_ENABLE_lane0) 
                                     & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl3_up_BYPASSED_AT_3_lane0)) 
                                        & ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_RD_PHYS_lane0) 
                                           == (0x0000001fU 
                                               & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                                  >> 0x0000000fU))))))))) 
                        | (((0x00000020U == (0x00000034U 
                                             & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0)) 
                            | (0x00000020U == (0x00000064U 
                                               & vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0))) 
                           & (((IData)(vlSelfRef.__PVT__execute_ctrl1_up_RD_ENABLE_lane0) 
                               & ((IData)(vlSelfRef.__PVT__execute_ctrl1_up_RD_PHYS_lane0) 
                                  == (0x0000001fU & 
                                      (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                       >> 0x00000014U)))) 
                              | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_RD_ENABLE_lane0) 
                                  & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_BYPASSED_AT_4_lane0)) 
                                     & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_RD_PHYS_lane0) 
                                        == (0x0000001fU 
                                            & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                               >> 0x00000014U))))) 
                                 | (((~ (IData)(vlSelfRef.__PVT__execute_ctrl2_up_BYPASSED_AT_2_lane0)) 
                                     & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_RD_ENABLE_lane0) 
                                        & ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_RD_PHYS_lane0) 
                                           == (0x0000001fU 
                                               & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                                  >> 0x00000014U))))) 
                                    | ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_RD_ENABLE_lane0) 
                                       & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl3_up_BYPASSED_AT_3_lane0)) 
                                          & ((IData)(vlSelfRef.__PVT__execute_ctrl3_up_RD_PHYS_lane0) 
                                             == (0x0000001fU 
                                                 & (vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 
                                                    >> 0x00000014U)))))))))))))) 
           & (IData)(vlSelfRef.__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCount_1));
}

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__when_LsuL1Plugin_l466 = ((5U != (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode)) 
                                              | (0x0fU 
                                                 == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_wordIndex)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rValid) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onD_sel));
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_arbiter_oh 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_arbiter_lock) 
           | (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_a_valid));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_last 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__VdfgRegularize_h6e95ff9d_0_82) 
           | (0x0fU == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat)));
    vlSelfRef.__PVT__execute_lane0_bypasser_integer_RS1_bypassEnables_bools_0 
        = (((IData)(vlSelfRef.__PVT__execute_ctrl1_up_RS1_PHYS_lane0) 
            == (IData)(vlSelfRef.__PVT__execute_ctrl5_up_RD_PHYS_lane0)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83));
    vlSelfRef.__PVT__execute_lane0_bypasser_integer_RS2_bypassEnables_bools_0 
        = (((IData)(vlSelfRef.__PVT__execute_ctrl1_up_RS2_PHYS_lane0) 
            == (IData)(vlSelfRef.__PVT__execute_ctrl5_up_RD_PHYS_lane0)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_83));
    vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_raw 
        = ((((0xffff0000U & vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input) 
             | ((0x0000ff00U & (((2U & vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0)
                                  ? (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input 
                                     >> 0x00000018U)
                                  : (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input 
                                     >> 8U)) << 8U)) 
                | (0x000000ffU & ((0U == (3U & vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0))
                                   ? vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input
                                   : ((1U == (3U & vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0))
                                       ? (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input 
                                          >> 8U) : 
                                      ((2U == (3U & vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0))
                                        ? (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input 
                                           >> 0x00000010U)
                                        : (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_loadData_input 
                                           >> 0x00000018U))))))) 
            & (- (IData)((IData)(vlSelfRef.__PVT__LsuPlugin_logic_iwb_valid)))) 
           | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_MulPlugin_HIGH_lane0)
                ? vlSelfRef.__PVT__execute_ctrl4_down_early0_MulPlugin_logic_steps_1_adders_0_lane0[1U]
                : vlSelfRef.__PVT__execute_ctrl4_down_early0_MulPlugin_logic_steps_1_adders_0_lane0[0U]) 
              & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_SEL_lane0)))));
    vlSelfRef.__PVT__when_FetchL1Plugin_l256 = ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_start_valid) 
                                                & ((~ 
                                                    ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid) 
                                                     & ((0x0000007fU 
                                                         & (vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_address 
                                                            >> 6U)) 
                                                        == 
                                                        (0x0000007fU 
                                                         & (vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_TRANSLATED 
                                                            >> 6U))))) 
                                                   & ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                                                      >> 7U)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_arbiter_oh 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_arbiter_lock) 
           | (IData)(vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1));
    vlSelfRef.__PVT__when_LsuL1Plugin_l608 = ((0x0fU 
                                               == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_read_wordIndex)) 
                                              & (IData)(vlSelfRef.__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1));
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_oh 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_lock) 
           | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_slotsWithId_0_0));
    vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div_io_cmd_valid 
        = ((~ (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_cmdSent)) 
           & (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_request));
    vlSelfRef.__PVT__execute_ctrl2_down_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0) 
           & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0) 
              & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0) 
                 & ((~ ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_PREFETCH_lane0) 
                        | ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_preCtrl_MISS_ALIGNED_lane0) 
                           | ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_FAULT_lane0) 
                              | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0) 
                                  & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onTrigger_HIT_lane0)) 
                                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16)))))) 
                    & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_fault)) 
                       & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique))))));
    vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_doIt 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0) 
           & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_IO_lane0) 
              & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0)));
    vlSelfRef.__PVT__when_EnvPlugin_l86 = VL_LTES_III(3, (IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_xretPriv), (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege));
    vlSelfRef.__PVT__early0_BranchPlugin_logic_trapPort_valid 
        = ((IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_pcPort_valid) 
           & ((0U != (2U & (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87 
                            << 1U))) & (IData)(vlSelfRef.__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_jumpLogic_COND_lane0)));
    vlSelfRef.__PVT__execute_ctrl0_down_COMPLETED_lane0 
        = ((IData)(vlSelfRef.__PVT__decode_ctrls_1_up_TRAP_0) 
           | (IData)(vlSelfRef.__PVT__when_DecoderPlugin_l229));
    vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_trapPort_valid 
        = (((~ (IData)(vlSelfRef.__PVT__decode_ctrls_1_up_TRAP_0)) 
            | (IData)(vlSelfRef.__PVT__DecoderPlugin_logic_interrupt_buffered)) 
           & (IData)(vlSelfRef.__PVT__when_DecoderPlugin_l229));
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedSet = 0U;
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_refillHazards) 
           | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_state) 
              | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_LOAD_lane0) 
                  & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PREFETCH_lane0)) 
                     & ((0U != (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WRITE_TO_READ_HAZARDS_lane0)) 
                        | ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_BANK_BUSY_REMAPPED_lane0) 
                           & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0))))) 
                 | (((~ ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid)) 
                         | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PREFETCH_lane0))) 
                     & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0)) 
                    | ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_HAZARD_FORCED_lane0) 
                       | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_hazardReg) 
                          | ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_FREEZE_HAZARD_lane0) 
                             | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_coherencyHazard))))))));
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_reservation_take = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_loadedSet = 1U;
            vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_reservation_take = 1U;
        }
        vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeData 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_data;
        vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_address 
            = (0x000007ffU & ((0x000007f0U & (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_address 
                                              >> 2U)) 
                              | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_wordIndex)));
    } else {
        vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeData 
            = vlSelfRef.__PVT___zz_execute_ctrl4_down_LsuL1_WRITE_DATA_lane0;
        vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_address 
            = (0x000007ffU & (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0 
                              >> 2U));
    }
    vlSelfRef.__PVT__execute_ctrl1_down_integer_RS1_lane0 
        = ((vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga.__PVT__asMem_ram_spinal_port1 
            & (- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__execute_lane0_bypasser_integer_RS1_bypassEnables_bools_0)))))) 
           | (vlSelfRef.__PVT__execute_ctrl5_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
              & (- (IData)((IData)(vlSelfRef.__PVT__execute_lane0_bypasser_integer_RS1_bypassEnables_bools_0)))));
    vlSelfRef.__PVT__execute_ctrl1_down_integer_RS2_lane0 
        = ((vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga.__PVT__asMem_ram_spinal_port2 
            & (- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__execute_lane0_bypasser_integer_RS2_bypassEnables_bools_0)))))) 
           | (vlSelfRef.__PVT__execute_ctrl5_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
              & (- (IData)((IData)(vlSelfRef.__PVT__execute_lane0_bypasser_integer_RS2_bypassEnables_bools_0)))));
    vlSelfRef.__PVT___zz_lane0_IntFormatPlugin_logic_stages_1_segments_1_sign_value = 0U;
    if ((0U == (IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0))) {
        vlSelfRef.__PVT___zz_lane0_IntFormatPlugin_logic_stages_1_segments_1_sign_value 
            = (1U & (vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_raw 
                     >> 7U));
    } else if ((1U == (IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0))) {
        vlSelfRef.__PVT___zz_lane0_IntFormatPlugin_logic_stages_1_segments_1_sign_value 
            = (1U & (vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_raw 
                     >> 0x0000000fU));
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_mask 
        = ((5U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_opcode)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid));
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid)))) {
        if (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_mask 
                = vlSelfRef.__PVT__execute_ctrl2_down_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0;
        }
    }
    vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1 
        = (((~ (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_unfreeze)) 
            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76)) 
           | ((((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_tooEarly) 
                | ((~ (IData)(vlSelfRef.__PVT__LsuPlugin_logic_bus_rsp_toStream_rValid)) 
                   & (IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_allowIt))) 
               & (IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_io_doIt)) 
              | ((~ ((IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_unscheduleRequest) 
                     | (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_div__DOT__done))) 
                 & (IData)(vlSelfRef.__PVT__early0_DivPlugin_logic_processing_request))));
    vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_commit = 0U;
    vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_exception = 1U;
    vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_arg = 0U;
    if ((2U == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0))) {
        if (vlSelfRef.__PVT__when_EnvPlugin_l86) {
            vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_commit = 1U;
            vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_exception = 0U;
            vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_arg 
                = vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_xretPriv;
        }
    } else if ((5U == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0))) {
        vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_commit = 1U;
        vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_exception = 0U;
    } else if ((3U == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0))) {
        vlSelfRef.__PVT__early0_EnvPlugin_logic_exe_commit = 1U;
        vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_exception = 0U;
    }
    vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_flushPort_valid 
        = ((IData)(vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl0_down_COMPLETED_lane0));
    vlSelfRef.__PVT__when_LsuPlugin_l1000 = ((IData)(vlSelfRef.__PVT__when_LsuPlugin_l915) 
                                             & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_PREFETCH_lane0)) 
                                                & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_IO_lane0)) 
                                                   & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FENCE_lane0)) 
                                                      & ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0) 
                                                         | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16))))));
    vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_l1Failed 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0) 
           & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_CACHED_RSP_lane0_fault)) 
              & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16) 
                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69)) 
                 | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0))));
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_FLUSH_HAZARD_lane0 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_flushHazardReg) 
           | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_reservation_take) 
              & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_91 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_reservation_take) 
                                                 | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid));
    vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_wb_payload 
        = vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_raw;
    if ((1U > (IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0))) {
        vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_wb_payload 
            = ((0xffff00ffU & vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_wb_payload) 
               | (0x0000ff00U & ((- (IData)(((IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_SIGNED_lane0) 
                                             & ((vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_raw 
                                                 >> 7U) 
                                                & (0U 
                                                   == (IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0)))))) 
                                 << 8U)));
    }
    if ((2U > (IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0))) {
        vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_wb_payload 
            = ((0x0000ffffU & vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_wb_payload) 
               | ((- (IData)(((IData)(vlSelfRef.__PVT___zz_lane0_IntFormatPlugin_logic_stages_1_segments_1_sign_value) 
                              & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_SIGNED_lane0)))) 
                  << 0x00000010U));
    }
}

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_valueNext 
        = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_value)));
    if ((0x4fU == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_value))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_valueNext = 0U;
    }
    if ((1U & (~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_valueNext = 0U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_slotsFreeze 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_freezeTimeout_state)) 
           & (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5 = ((~ (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1)) 
                                                & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0));
    vlSelfRef.__PVT__DispatchPlugin_logic_candidates_0_fire 
        = ((~ ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_valid) 
               | (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1))) 
           & (IData)(vlSelfRef.__PVT__DispatchPlugin_logic_scheduler_arbiters_0_doIt));
    vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 0U;
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_accessFault) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 1U;
    }
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_l1Failed) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 0U;
    }
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_pmaFault) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_PAGE_FAULT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_ACCESS_FAULT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_REFILL_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 0U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_HAZARD_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 0U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_FROM_LSU_MSB_FAILED_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_preCtrl_MISS_ALIGNED_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 1U;
    }
    vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 0U;
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_accessFault) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 5U;
        if (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0) {
            vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code 
                = (2U | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code));
        }
    }
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_l1Failed) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 4U;
    }
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_pmaFault) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 5U;
        if (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0) {
            vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code 
                = (2U | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code));
        }
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_PAGE_FAULT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 0x0dU;
        if (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0) {
            vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code 
                = (2U | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code));
        }
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_ACCESS_FAULT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 5U;
        if (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0) {
            vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code 
                = (2U | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code));
        }
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_REFILL_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 7U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_HAZARD_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 4U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_FROM_LSU_MSB_FAILED_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 5U;
        if (vlSelfRef.__PVT__execute_ctrl4_up_AguPlugin_STORE_lane0) {
            vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code 
                = (2U | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code));
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_MMU_BYPASS_TRANSLATION_lane0)))) {
            vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code 
                = (8U | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code));
        }
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_preCtrl_MISS_ALIGNED_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code 
            = (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0)
                 ? 6U : 4U) & (- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_preCtrl_MISS_ALIGNED_lane0))));
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onTrigger_HIT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 3U;
    }
    vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 0U;
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_accessFault) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_l1Failed) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_traps_pmaFault) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_PAGE_FAULT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_ACCESS_FAULT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_REFILL_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_MMU_HAZARD_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_FROM_LSU_MSB_FAILED_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_preCtrl_MISS_ALIGNED_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onTrigger_HIT_lane0) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FENCE_lane0) 
         | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_PREFETCH_lane0))) {
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 0U;
    }
    if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_fenceTrap_doItReg) {
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception = 0U;
        vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code = 4U;
        vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap = 1U;
    }
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_ABORD_lane0 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_FLUSH_HAZARD_lane0) 
           | (((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_fenceTrap_doItReg) 
               & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0)) 
              | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_FAILURE_lane0) 
                  & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0) 
                     | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_PREFETCH_lane0))) 
                 | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0) 
                     & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0)) 
                        | (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_FENCE_lane0))) 
                    | (((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0)) 
                        & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_CACHED_RSP_lane0_fault)) 
                       | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0))))));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0) 
           & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0) 
              & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_91)) 
                 & ((~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_valid) 
                        | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_writebackHazards))) 
                    & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_loadedDirties)))));
    vlSelfRef.__PVT__when_LsuL1Plugin_l1170 = (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_reservation_take) 
                                                & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_TAG_UPDATE)) 
                                               | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_91)));
    vlSelfRef.__PVT__execute_ctrl4_down_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
        = (vlSelfRef.__PVT__execute_ctrl4_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 
           | (vlSelfRef.__PVT__lane0_IntFormatPlugin_logic_stages_1_wb_payload 
              & (- (IData)(((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0) 
                            & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_early0_MulPlugin_SEL_lane0) 
                               | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_iwb_valid)))))));
    vlSelfRef.__PVT__when_DispatchPlugin_l373 = ((IData)(vlSelfRef.__PVT__decode_ctrls_1_up_LANE_SEL_0) 
                                                 & ((~ (IData)(vlSelfRef.__PVT__DispatchPlugin_logic_feeds_0_sent)) 
                                                    & (~ (IData)(vlSelfRef.__PVT__DispatchPlugin_logic_candidates_0_fire))));
    vlSelfRef.__PVT__execute_ctrl4_COMMIT_lane0_bypass 
        = vlSelfRef.__PVT__execute_ctrl4_up_COMMIT_lane0;
    vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid = 0U;
    vlSelfRef.__PVT__execute_ctrl4_TRAP_lane0_bypass 
        = vlSelfRef.__PVT__execute_ctrl4_up_TRAP_lane0;
    vlSelfRef.__PVT__LsuPlugin_logic_trapPort_valid = 0U;
    if (vlSelfRef.__PVT__when_LsuPlugin_l915) {
        if (vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_lsuTrap) {
            vlSelfRef.__PVT__execute_ctrl4_COMMIT_lane0_bypass = 0U;
            vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid = 1U;
            vlSelfRef.__PVT__execute_ctrl4_TRAP_lane0_bypass = 1U;
            vlSelfRef.__PVT__LsuPlugin_logic_trapPort_valid = 1U;
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_ABORD_lane0) 
           | (IData)(vlSelfRef.__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_sideEffect = 0U;
    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_loaded = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_loaded = 1U;
        }
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_loaded = 1U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD)))) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170)))) {
                    vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_sideEffect = 1U;
                    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_loaded 
                        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED) 
                           | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE));
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                  >> 7U)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_loaded = 0U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_address = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_address 
                = (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_address 
                   >> 0x0dU);
        }
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_address 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_address;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address 
                = (0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_address 
                                  >> 6U));
        }
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address 
            = (0x0000007fU & (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0 
                              >> 6U));
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD)))) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170)))) {
                    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_address 
                        = (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS 
                           >> 0x0dU);
                    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address 
                        = (0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS 
                                          >> 6U));
                }
            }
        }
    }
}

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_fault = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_unique = 0U;
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_fault 
                = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_hadError) 
                   | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_payload_error));
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_unique 
                = (0U == (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rData_param));
        }
    } else {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_unique = 0U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address 
        = (0x0000007fU & (vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0 
                          >> 6U));
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_fault 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_fault;
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_unique 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD)))) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170)))) {
                    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_fault 
                        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_FAULT;
                    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_tag_unique 
                        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE) 
                           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE));
                    vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address 
                        = (0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS 
                                          >> 6U));
                }
            }
        }
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo = 0U;
    vlSelfRef.integer_write_0_data = vlSelfRef.__PVT__execute_ctrl4_down_lane0_integer_WriteBackPlugin_logic_DATA_lane0;
    vlSelfRef.__PVT__decode_ctrls_1_up_isMoving = (
                                                   (~ (IData)(vlSelfRef.__PVT__when_DispatchPlugin_l373)) 
                                                   & (IData)(vlSelfRef.__PVT__decode_ctrls_1_up_valid));
    vlSelfRef.__PVT__decode_ctrls_0_down_isReady = 
        (1U & (~ ((IData)(vlSelfRef.__PVT__decode_ctrls_1_up_valid) 
                  & (IData)(vlSelfRef.__PVT__when_DispatchPlugin_l373))));
    vlSelfRef.WhiteboxerPlugin_logic_commits_ports_0_valid 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_COMMIT_lane0_bypass) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5));
    vlSelfRef.__PVT__lane0_integer_WriteBackPlugin_logic_write_port_valid 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5) 
           & ((IData)(vlSelfRef.__PVT__execute_ctrl4_up_RD_ENABLE_lane0) 
              & ((IData)(vlSelfRef.__PVT__execute_ctrl4_COMMIT_lane0_bypass) 
                 & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_lane0_integer_WriteBackPlugin_SEL_lane0))));
    vlSelfRef.__PVT__execute_ctrl2_LANE_SEL_lane0_bypass 
        = ((~ (IData)(vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid)) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_trigger_oh 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_TRAP_lane0_bypass) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_5));
    vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeMask = 0x0fU;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeMask 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MASK_lane0;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid) {
        if (vlSelfRef.__PVT__when_LsuL1Plugin_l466) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask = 1U;
        }
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_loadedDirties;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_read_rsp_valid)))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_banksWrite_writeMask = 0U;
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_reservation_take)))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask = 0U;
        }
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
        if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo = 1U;
        } else if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1170) {
                vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo = 1U;
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD)))) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170)))) {
                    vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask 
                        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HITS;
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                  >> 7U)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_address 
            = (0x0000007fU & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter));
        vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address 
            = (0x0000007fU & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter));
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask = 1U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_hit 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_sideEffect) 
           & ((0x0000007fU & (vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 
                              >> 6U)) == (0x0000007fU 
                                          & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS 
                                             >> 6U))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81 = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo)) 
                                                 & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA));
    vlSelfRef.__PVT__decode_ctrls_0_up_isFiring = ((IData)(vlSelfRef.__PVT__decode_ctrls_0_down_isReady) 
                                                   & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid));
    vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid)) 
                 | (IData)(vlSelfRef.__PVT__decode_ctrls_0_down_isReady)));
    vlSelfRef.WhiteboxerPlugin_logic_commits_ports_0_pc 
        = (vlSelfRef.__PVT__execute_ctrl4_up_PC_lane0 
           & (- (IData)((IData)(vlSelfRef.WhiteboxerPlugin_logic_commits_ports_0_valid))));
    vlSelfRef.integer_write_0_valid = vlSelfRef.__PVT__lane0_integer_WriteBackPlugin_logic_write_port_valid;
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_valid 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid));
    vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_read_cmd_valid 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_up_valid)) 
                 | (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_takeWhen_valid 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_valid));
    vlSelfRef.__PVT__when_LsuL1Bus_l235 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo) 
                                           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_valid));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram_wr_en 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_full)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_takeWhen_valid));
    vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = 1U;
    if ((2U == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight))) {
        vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = 0U;
    }
    if (vlSelfRef.__PVT__when_LsuL1Bus_l235) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS;
        vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = 0U;
    } else {
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_address;
    }
}

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.PrivilegedPlugin_logic_harts_0_int_m_external 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__peripheral_plic_intc_thread_logic_io_targets;
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__21(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__21\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid) 
                                                  | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_slots_0_valid));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg 
        = vlSelfRef.__Vdly__TrapPlugin_logic_harts_0_trap_fsm_stateReg;
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg 
        = vlSelfRef.__Vdly__CsrAccessPlugin_logic_fsm_stateReg;
    vlSelfRef.WhiteboxerPlugin_logic_trap_ports_0_valid 
        = (1U & (0x0080U >> (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)));
}

void Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__22(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__22\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_c_fire 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) 
           & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid));
    vlSelfRef.__PVT___zz_LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight_5 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo_io_pop_valid) 
           & ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) 
              & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_1)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter_io_inputs_0_ready 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0));
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_ready 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid)) 
                 | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter_io_inputs_0_ready)));
}

extern const VlUnpacked<CData/*0:0*/, 32> Vsim__ConstPool__TABLE_hb22a0920_0;
extern const VlUnpacked<CData/*4:0*/, 512> Vsim__ConstPool__TABLE_h6ac5ae98_0;
extern const VlUnpacked<CData/*0:0*/, 1024> Vsim__ConstPool__TABLE_hcc7d2afb_0;

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_canRefill 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_writebackHazards) 
                    | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_valid) 
                        & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_loaded)) 
                       | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105)))));
    vlSelfRef.WhiteboxerPlugin_logic_trap_ports_0_interrupt 
        = Vsim__ConstPool__TABLE_hb22a0920_0[(((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt) 
                                               << 4U) 
                                              | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))];
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_crsPorts_write_data = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))) {
                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_crsPorts_write_data 
                        = (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_tval 
                           & (- (IData)((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt))))));
                    if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_triggerEbreakReg) {
                        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_crsPorts_write_data 
                            = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_pc;
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_crsPorts_write_data 
                    = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_pc;
            }
        }
    }
    vlSelfRef.WhiteboxerPlugin_logic_trap_ports_0_cause 
        = Vsim__ConstPool__TABLE_h6ac5ae98_0[(((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_code) 
                                               << 4U) 
                                              | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))];
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pcPort_payload_pc = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg) 
                      >> 2U)))) {
            if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))) {
                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pcPort_payload_pc 
                        = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_jumpTarget;
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pcPort_payload_pc 
                    = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_readed;
            }
        }
    } else if ((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
        if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pcPort_payload_pc 
                    = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_readed;
            }
        }
    } else if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__when_TrapPlugin_l454)))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                              >> 4U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                                  >> 3U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                                      >> 2U)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                                          >> 1U)))) {
                                if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)))) {
                                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pcPort_payload_pc 
                                        = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_pc;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.__PVT___zz_PcPlugin_logic_harts_0_aggregator_target_2 
        = (1U & (~ (Vsim__ConstPool__TABLE_hcc7d2afb_0
                    [(((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                       << 5U) | (((IData)(vlSelfRef.__PVT__when_TrapPlugin_l454) 
                                  << 4U) | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))] 
                    | (IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_pcPort_valid))));
    vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_valid 
        = ((IData)(vlSelfRef.__PVT__REG_CSR_CsrRamPlugin_csrMapper_selFilter) 
           & ((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_read) 
              & (1U == (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))));
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesDo = 0U;
    if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        if ((2U == (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesDo 
                = vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_write;
        }
    }
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo 
        = ((0U == (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid;
    if ((2U == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid = 0U;
    }
    if (vlSelfRef.__PVT__when_LsuL1Bus_l235) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid = 1U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_fire = 0U;
    if (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid) 
         & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter_io_inputs_0_ready) 
            & ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_release)) 
               & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_last))))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_fire = 1U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onD_sel)) 
         & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_d_rValid))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_slots_0_fire = 1U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_fire 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_ready) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_slotsWithId_0_0));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_askUpgrade 
        = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0)) 
           & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_canRefill) 
              & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_MISS_UNIQUE_lane0)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_payload_data 
        = ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0)) 
           & ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)) 
              & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_canRefill)));
    vlSelfRef.__PVT___zz_PcPlugin_logic_harts_0_aggregator_fault 
        = ((IData)(vlSelfRef.__PVT___zz_PcPlugin_logic_harts_0_aggregator_target_2) 
           & (IData)(vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_fault));
    vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
        = ((vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pcPort_payload_pc 
            & (- (IData)(Vsim__ConstPool__TABLE_hcc7d2afb_0
                         [(((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                            << 5U) | (((IData)(vlSelfRef.__PVT__when_TrapPlugin_l454) 
                                       << 4U) | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))]))) 
           | (((vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_state 
                + (4U & (- (IData)((IData)(vlSelfRef.__PVT__PcPlugin_logic_harts_0_self_increment))))) 
               & (- (IData)((IData)(vlSelfRef.__PVT___zz_PcPlugin_logic_harts_0_aggregator_target_2)))) 
              | ((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87 
                  << 1U) & (- (IData)(((~ (IData)(Vsim__ConstPool__TABLE_hcc7d2afb_0
                                                  [
                                                  (((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                                                    << 5U) 
                                                   | (((IData)(vlSelfRef.__PVT__when_TrapPlugin_l454) 
                                                       << 4U) 
                                                      | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))])) 
                                       & (IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_pcPort_valid)))))));
    vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_hits 
        = (((IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_valid) 
            << 1U) | (1U & (0x0120U >> (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))));
    vlSelfRef.__PVT__CsrAccessPlugin_bus_read_toWriteBits 
        = ((0x2eU & (- (IData)((IData)(vlSelfRef.__PVT__REG_CSR_3858)))) 
           | ((0x40001100U & (- (IData)((IData)(vlSelfRef.__PVT__REG_CSR_769)))) 
              | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mpie) 
                   & (IData)(vlSelfRef.__PVT__REG_CSR_768)) 
                  << 7U) | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mie) 
                              & (IData)(vlSelfRef.__PVT__REG_CSR_768)) 
                             << 3U) | ((0x1800U & (- (IData)((IData)(vlSelfRef.__PVT__REG_CSR_768)))) 
                                       | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_status_mprv) 
                                            & (IData)(vlSelfRef.__PVT__REG_CSR_768)) 
                                           << 0x00000011U) 
                                          | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_interrupt) 
                                               & (IData)(vlSelfRef.__PVT__REG_CSR_834)) 
                                              << 0x0000001fU) 
                                             | (((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_cause_code) 
                                                 & (- (IData)((IData)(vlSelfRef.__PVT__REG_CSR_834)))) 
                                                | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_meip) 
                                                     & (IData)(vlSelfRef.__PVT__REG_CSR_836)) 
                                                    << 0x0000000bU) 
                                                   | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_mtip) 
                                                        & (IData)(vlSelfRef.__PVT__REG_CSR_836)) 
                                                       << 7U) 
                                                      | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ip_msip) 
                                                           & (IData)(vlSelfRef.__PVT__REG_CSR_836)) 
                                                          << 3U) 
                                                         | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_meie) 
                                                              & (IData)(vlSelfRef.__PVT__REG_CSR_772)) 
                                                             << 0x0000000bU) 
                                                            | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_mtie) 
                                                                 & (IData)(vlSelfRef.__PVT__REG_CSR_772)) 
                                                                << 7U) 
                                                               | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_ie_msie) 
                                                                    & (IData)(vlSelfRef.__PVT__REG_CSR_772)) 
                                                                   << 3U) 
                                                                  | (((IData)(vlSelfRef.__PVT__REG_CSR_4016) 
                                                                      & (0U 
                                                                         != (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_topi_interrupt))) 
                                                                     | ((((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_m_topi_interrupt) 
                                                                          << 0x00000010U) 
                                                                         & (- (IData)((IData)(vlSelfRef.__PVT__REG_CSR_4016)))) 
                                                                        | ((((IData)(vlSelfRef.__PVT__REG_CSR_774) 
                                                                             & (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_mcounteren_tm)) 
                                                                            << 1U) 
                                                                           | (((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT___zz_vexiis_0_priv_rdtime) 
                                                                               & (- (IData)((IData)(vlSelfRef.__PVT__REG_CSR_3073)))) 
                                                                              | ((vlSelfRef.__PVT__CsrRamPlugin_logic_mem_spinal_port1 
                                                                                & (- (IData)((IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_read_valid)))) 
                                                                                | ((IData)(
                                                                                (vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT___zz_vexiis_0_priv_rdtime 
                                                                                >> 0x00000020U)) 
                                                                                & (- (IData)((IData)(vlSelfRef.__PVT__REG_CSR_3201)))))))))))))))))))))));
    vlSelfRef.__PVT__CsrRamPlugin_csrMapper_write_valid 
        = ((IData)(vlSelfRef.__PVT__REG_CSR_CsrRamPlugin_csrMapper_selFilter) 
           & ((~ (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_fired)) 
              & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesDo)));
    vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_MASK_lane0)
            ? ((IData)(vlSelfRef.__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_CLEAR_lane0)
                ? ((~ vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_alu_mask) 
                   & vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_aluInput)
                : (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_aluInput 
                   | vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_alu_mask))
            : vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_alu_mask);
    if (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesDo) 
         & (IData)(vlSelfRef.__PVT__REG_CSR_PrivilegedPlugin_logic_readAnyWriteLegal_tvecFilter))) {
        vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
            = (0xfffffffcU & vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits);
    }
    if (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesDo) 
         & (IData)(vlSelfRef.__PVT__REG_CSR_PrivilegedPlugin_logic_readAnyWriteLegal_epcFilter))) {
        vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits 
            = (0xfffffffcU & vlSelfRef.__PVT__CsrAccessPlugin_bus_write_bits);
    }
    vlSelfRef.__PVT__when_CsrAccessPlugin_l157_6 = 
        ((0x0300U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                      >> 0x00000014U)) & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo));
}

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__CsrAccessPlugin_logic_trapPort_payload_code = 2U;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77 = (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg) 
                                                  << 4U) 
                                                 | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled) 
                                                     << 3U) 
                                                    | (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo) 
                                                        << 2U) 
                                                       | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))));
    vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_exception = 0U;
    if ((((3U & (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege)) 
          < (3U & (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                   >> 0x0000001cU))) | ((IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_write) 
                                        & (3U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                  >> 0x0000001eU))))) {
        vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_exception = 1U;
    }
    if (((0x0c01U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                      >> 0x00000014U)) & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo))) {
        if (vlSelfRef.__PVT__when_CsrService_l199) {
            vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_exception = 1U;
        }
    }
    if (((0x0c81U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                      >> 0x00000014U)) & (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo))) {
        if (vlSelfRef.__PVT__when_CsrService_l199) {
            vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_exception = 1U;
        }
    }
    vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass 
        = vlSelfRef.__PVT__execute_ctrl2_up_TRAP_lane0;
    if (vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_valid) {
        vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass = 1U;
    }
    if (vlSelfRef.__PVT__early0_BranchPlugin_logic_trapPort_valid) {
        vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass = 1U;
    }
    if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_flushReg) {
        vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass = 1U;
    }
    if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        if ((2U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            if ((3U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
                if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo) {
                    if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_sampled) {
                        if ((1U & (~ (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg)))) {
                            if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapReg) {
                                vlSelfRef.__PVT__CsrAccessPlugin_logic_trapPort_payload_code 
                                    = vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapCodeReg;
                            }
                        }
                        if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg) {
                            vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass = 1U;
                        } else if (vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapReg) {
                            vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass = 1U;
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.__PVT__when_LsuL1Plugin_l679 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_last) 
                                              & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_fire));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doUpgrade 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_askUpgrade));
    vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill 
        = ((IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_payload_data));
    vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_WAIT_REFILL_lane0 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_refillHazards) 
           | ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0)) 
              & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_askUpgrade) 
                 | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_payload_data))));
    vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_hits_ohFirst_masked 
        = ((~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_hits) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_hits));
    vlSelfRef.__PVT___zz_3 = (1U & ((0x0018U >> (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)) 
                                    | ((~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter) 
                                           >> 2U)) 
                                       | (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_write_valid))));
    vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits 
        = ((4U & ((~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_flush_counter) 
                      >> 2U)) << 2U)) | (((IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_write_valid) 
                                          << 1U) | 
                                         (1U & (0x0018U 
                                                >> (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)))));
    vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trap = 0U;
    vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trapCode = 0U;
    if (vlSelfRef.__PVT__when_CsrAccessPlugin_l157_6) {
        if (vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_write) {
            vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trap = 1U;
            vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_trapCode = 5U;
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 = (((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapReg) 
                                                  << 5U) 
                                                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77));
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_trap 
        = (1U & ((~ ((0x0300U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                  >> 0x00000014U)) 
                     | ((IData)(vlSelfRef.__PVT__COMB_CSR_CsrRamPlugin_csrMapper_selFilter) 
                        | ((0x0341U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                        >> 0x00000014U)) 
                           | ((0x0305U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                           >> 0x00000014U)) 
                              | ((0x0c81U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                              >> 0x00000014U)) 
                                 | ((0x0c01U == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                 >> 0x00000014U)) 
                                    | ((0x0306U == 
                                        (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                         >> 0x00000014U)) 
                                       | ((0x0fb0U 
                                           == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                               >> 0x00000014U)) 
                                          | ((0x0304U 
                                              == (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                  >> 0x00000014U)) 
                                             | ((0x0344U 
                                                 == 
                                                 (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                  >> 0x00000014U)) 
                                                | ((0x0342U 
                                                    == 
                                                    (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                     >> 0x00000014U)) 
                                                   | ((0x07a0U 
                                                       == 
                                                       (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                        >> 0x00000014U)) 
                                                      | ((0x07a1U 
                                                          == 
                                                          (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                           >> 0x00000014U)) 
                                                         | ((0x07a2U 
                                                             == 
                                                             (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                              >> 0x00000014U)) 
                                                            | ((0x0f11U 
                                                                == 
                                                                (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                 >> 0x00000014U)) 
                                                               | ((0x0f12U 
                                                                   == 
                                                                   (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                    >> 0x00000014U)) 
                                                                  | ((0x0f13U 
                                                                      == 
                                                                      (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                       >> 0x00000014U)) 
                                                                     | ((0x0f14U 
                                                                         == 
                                                                         (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                          >> 0x00000014U)) 
                                                                        | ((0x0301U 
                                                                            == 
                                                                            (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                             >> 0x00000014U)) 
                                                                           | (0x0300U 
                                                                              == 
                                                                              (vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                                               >> 0x00000014U)))))))))))))))))))))) 
                 | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_bus_decode_exception)));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_holdPort 
        = ((IData)(vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_flushPort_valid) 
           | ((1U != (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg)) 
              | (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LANE_SEL_lane0) 
                  & (IData)(vlSelfRef.__PVT__execute_ctrl4_TRAP_lane0_bypass)) 
                 | (((IData)(vlSelfRef.__PVT__execute_ctrl3_up_LANE_SEL_lane0) 
                     & (IData)(vlSelfRef.__PVT__execute_ctrl3_up_TRAP_lane0)) 
                    | (((IData)(vlSelfRef.__PVT__execute_ctrl2_up_LANE_SEL_lane0) 
                        & (IData)(vlSelfRef.__PVT__execute_ctrl2_TRAP_lane0_bypass)) 
                       | (((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid) 
                           & (IData)(vlSelfRef.__PVT__decode_ctrls_0_down_TRAP_0)) 
                          | ((IData)(vlSelfRef.__PVT__execute_ctrl1_up_LANE_SEL_lane0) 
                             & (IData)(vlSelfRef.__PVT__execute_ctrl1_up_TRAP_lane0))))))));
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_fromUnique = 0U;
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_address = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_fromUnique 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_address 
            = ((vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_address 
                << 0x0000000dU) | (0x00001fc0U & vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0));
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty = 0U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_SHARED_lane0_dirty;
    } else {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty = 0U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_fromUnique 
            = vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique;
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_address 
            = ((vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_address 
                << 0x0000000dU) | (0x00001fc0U & vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0));
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_loadedDirties;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_toShared = 0U;
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_toShared 
            = (1U & (~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique)));
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_toShared = 0U;
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD)))) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170)))) {
                    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_fromUnique 
                        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE;
                    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_address 
                        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS;
                    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty 
                        = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_DIRTY;
                    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_push_payload_c_toShared 
                        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED) 
                           & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE) 
                                 & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE))));
                }
            }
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18 = (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush));
    vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty 
        = (((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_SHARED_lane0_dirty) 
            | ((IData)(vlSelfRef.__PVT__execute_ctrl2_down_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0) 
               & (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0))) 
           & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill) 
                 | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush) 
                    & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_loadedDirties)))));
}

extern const VlUnpacked<CData/*0:0*/, 128> Vsim__ConstPool__TABLE_h2ec615e0_0;
extern const VlUnpacked<CData/*0:0*/, 64> Vsim__ConstPool__TABLE_h351a1f2e_0;
extern const VlUnpacked<CData/*0:0*/, 512> Vsim__ConstPool__TABLE_h5eb9ad86_0;
extern const VlUnpacked<CData/*4:0*/, 512> Vsim__ConstPool__TABLE_hb76b7511_0;
extern const VlUnpacked<CData/*0:0*/, 64> Vsim__ConstPool__TABLE_h1fed2e5e_0;
extern const VlUnpacked<CData/*4:0*/, 256> Vsim__ConstPool__TABLE_hd401da92_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vsim__ConstPool__TABLE_h4b0f789b_0;

void Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___nba_comb__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_92;
    __VdfgRegularize_h6e95ff9d_0_92 = 0;
    // Body
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD)))) {
            if (vlSelfRef.__PVT__when_LsuL1Plugin_l1168) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170)))) {
                    vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty 
                        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_SHARED_dirty) 
                           & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HITS)));
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                  >> 7U)))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty = 0U;
    }
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_valid 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects)) 
           & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill) 
              | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doUpgrade)));
    vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_port_cmd_valid 
        = ((~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_busy) 
               | (IData)(vlSelfRef.__PVT___zz_3))) 
           & (0U != (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_hits_ohFirst_masked)));
    vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked 
        = ((~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits) 
               - (IData)(1U))) & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits));
    vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel 
        = ((IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_valid) 
           | (Vsim__ConstPool__TABLE_h2ec615e0_0[(((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17) 
                                                   << 1U) 
                                                  | (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_inject_flushReg))] 
              | ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_flushPort_valid) 
                 | (IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_pcPort_valid))));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_ports_1_valid 
        = (Vsim__ConstPool__TABLE_h351a1f2e_0[vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17] 
           | ((IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_valid) 
              | (IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_trapPort_valid)));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_down_valid 
        = ((IData)(vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_trapPort_valid) 
           | (Vsim__ConstPool__TABLE_h351a1f2e_0[vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17] 
              | ((IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_trapPort_valid) 
                 | ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_valid) 
                    | (Vsim__ConstPool__TABLE_hb7cce103_0
                       [((0x00000080U & (((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid)) 
                                          | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent)) 
                                         << 7U)) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15))] 
                       | (IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_valid))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90 = (1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_holdPort) 
                                                     | ((~ 
                                                         ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_invalidate_counter) 
                                                          >> 7U)) 
                                                        | ((0U 
                                                            != (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_waysWrite_mask)) 
                                                           | ((IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_valid) 
                                                              & (((0x0000007fU 
                                                                   & (vlSelfRef.__PVT__FetchL1Plugin_logic_refill_slots_0_address 
                                                                      >> 6U)) 
                                                                  == 
                                                                  (0x0000007fU 
                                                                   & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                                                                      >> 6U))) 
                                                                 & ((0x0000000fU 
                                                                     & (vlSelfRef.__PVT__PcPlugin_logic_harts_0_aggregator_target 
                                                                        >> 2U)) 
                                                                    >= (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_refill_onRsp_wordIndex)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78 = ((((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                   << 5U) 
                                                  | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168) 
                                                      << 4U) 
                                                     | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                                                        << 3U))) 
                                                 | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                                                     << 2U) 
                                                    | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_SHARED_dirty 
        = ((Vsim__ConstPool__TABLE_h5eb9ad86_0[((((
                                                   (4U 
                                                    & ((~ 
                                                        ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_initializer_counter) 
                                                         >> 7U)) 
                                                       << 2U)) 
                                                   | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                       << 1U) 
                                                      | (IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168))) 
                                                  << 6U) 
                                                 | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                                                     << 5U) 
                                                    | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                                                       << 4U))) 
                                                | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects) 
                                                    << 3U) 
                                                   | ((((~ 
                                                         ((~ (IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0)) 
                                                          | (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0))) 
                                                        & (IData)(vlSelfRef.__PVT__execute_ctrl4_down_LsuL1_SEL_lane0)) 
                                                       << 2U) 
                                                      | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))))] 
            & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_address) 
               == (0x0000007fU & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS 
                                  >> 6U)))) ? (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty)
            : ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_rt0_SHARED_BYPASS_VALID)
                ? (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_rt0_SHARED_BYPASS_VALUE_dirty)
                : (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_shared_mem_spinal_port2)));
    vlSelfRef.__PVT__CsrAccessPlugin_bus_write_moving 
        = (1U & (~ ((~ ((IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked) 
                        >> 1U)) & (IData)(vlSelfRef.__PVT__CsrRamPlugin_csrMapper_write_valid))));
    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext 
        = vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg;
    if ((8U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
        if ((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_resetToRunConditions_0) {
                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
                if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_resetToRunConditions_0) {
                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 1U;
                }
            } else if (vlSelfRef.__PVT__TrapPlugin_logic_fetchL1Invalidate_0_cmd_ready) {
                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 0x0aU;
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext 
                = ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))
                    ? 0x0cU : 1U);
        } else if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 1U;
        } else if ((1U & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg))) {
            vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 9U;
        }
    } else if ((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
        if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext 
                = ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))
                    ? 1U : 7U);
        } else if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((1U & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_readLogic_ohReg))) {
                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 6U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked))) {
            vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 3U;
        }
    } else if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
        if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
            if ((1U & (IData)(vlSelfRef.__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked))) {
                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 5U;
            }
        } else if (vlSelfRef.__PVT__when_TrapPlugin_l454) {
            vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 4U;
        } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                             >> 4U)))) {
            if ((8U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                              >> 2U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code) 
                                  >> 1U)))) {
                        if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)))) {
                            if (((IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_2_valid) 
                                 | (IData)(vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid))) {
                                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 0x0aU;
                            }
                        }
                    }
                }
            } else if ((4U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                    if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)))) {
                        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 0x0aU;
                    }
                } else {
                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 0x0aU;
                }
            } else if ((2U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code)))) {
                    vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 0x0bU;
                }
            } else {
                vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext 
                    = ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code))
                        ? 8U : 1U);
            }
        }
    } else if ((1U & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg))) {
        if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_trigger_oh) {
            vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 2U;
        }
    } else if (vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_resetToRunConditions_0) {
        vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = 1U;
    }
    vlSelfRef.__PVT__execute_ctrl0_up_LANE_SEL_lane0 
        = ((~ ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_valid) 
               | (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel))) 
           & (IData)(vlSelfRef.__PVT__DispatchPlugin_logic_scheduler_arbiters_0_doIt));
    vlSelfRef.__PVT__fetch_logic_ctrls_2_up_cancel 
        = ((IData)(vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_flushPort_valid) 
           | (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel));
    __VdfgRegularize_h6e95ff9d_0_92 = ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_valid) 
                                       | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_ports_1_valid));
    vlSelfRef.__PVT__fetch_logic_ctrls_0_up_isFiring 
        = ((~ (IData)(vlSelfRef.__PVT__PcPlugin_logic_harts_0_holdReg)) 
           & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90) 
              & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_DIRTY 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_SHARED_dirty) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT));
    vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesFireDo = 0U;
    if ((1U != (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
        if ((2U == (IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_stateReg))) {
            if (vlSelfRef.__PVT__CsrAccessPlugin_bus_write_moving) {
                vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesFireDo 
                    = vlSelfRef.__PVT__CsrAccessPlugin_logic_fsm_interface_write;
            }
        }
    }
    vlSelfRef.__PVT__execute_ctrl0_LANE_SEL_lane0_bypass 
        = ((~ (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel)) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl0_up_LANE_SEL_lane0));
    vlSelfRef.__PVT___zz_TrapPlugin_logic_harts_0_trap_pending_arbiter_down_payload_exception 
        = (((((QData)((IData)(((0x00000020U & ((- (IData)((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_STORE_lane0))) 
                                               << 5U)) 
                               | (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_code)))) 
              << 0x00000021U) | (((QData)((IData)(vlSelfRef.__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0)) 
                                  << 1U) | (QData)((IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_payload_exception)))) 
            & (- (QData)((IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_valid)))) 
           | (((- (QData)((IData)(((~ (IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_valid)) 
                                   & (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_ports_1_valid))))) 
               & (((((QData)((IData)((((IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_arg) 
                                       << 5U) | Vsim__ConstPool__TABLE_hb76b7511_0
                                      [(0x00000080U 
                                        | ((((0x00000018U 
                                              & ((- (IData)(
                                                            (1U 
                                                             & ((IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege) 
                                                                >> 2U)))) 
                                                 << 3U)) 
                                             | (IData)(vlSelfRef.__PVT__PrivilegedPlugin_logic_harts_0_privilege)) 
                                            << 4U) 
                                           | (((IData)(vlSelfRef.__PVT__when_EnvPlugin_l86) 
                                               << 3U) 
                                              | (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0))))]))) 
                     << 0x00000021U) | (((QData)((IData)(
                                                         ((vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0 
                                                           & (- (IData)(
                                                                        ((4U 
                                                                          == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0)) 
                                                                         | ((5U 
                                                                             == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0)) 
                                                                            | (2U 
                                                                               == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0))))))) 
                                                          | (vlSelfRef.__PVT__execute_ctrl2_up_PC_lane0 
                                                             & (- (IData)(
                                                                          (1U 
                                                                           == (IData)(vlSelfRef.__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0)))))))) 
                                         << 1U) | (QData)((IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_payload_exception)))) 
                   & (- (QData)((IData)(vlSelfRef.__PVT__early0_EnvPlugin_logic_trapPort_valid)))) 
                  | (((- (QData)((IData)(Vsim__ConstPool__TABLE_h351a1f2e_0
                                         [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17]))) 
                      & (((QData)((IData)(vlSelfRef.__PVT__CsrAccessPlugin_logic_trapPort_payload_code)) 
                          << 0x00000021U) | (((QData)((IData)(vlSelfRef.__PVT__execute_ctrl2_up_Decode_UOP_lane0)) 
                                              << 1U) 
                                             | (QData)((IData)(Vsim__ConstPool__TABLE_h1fed2e5e_0
                                                               [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17]))))) 
                     | ((- (QData)((IData)(vlSelfRef.__PVT__early0_BranchPlugin_logic_trapPort_valid))) 
                        & (1ULL | ((QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87)) 
                                   << 2U)))))) | ((
                                                   (((QData)((IData)(
                                                                     (0x00000040U 
                                                                      | Vsim__ConstPool__TABLE_hd401da92_0
                                                                      [
                                                                      ((0x00000080U 
                                                                        & ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_MMU_BYPASS_TRANSLATION)) 
                                                                           << 7U)) 
                                                                       | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15))]))) 
                                                     << 0x00000021U) 
                                                    | (((QData)((IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_Fetch_WORD_PC)) 
                                                        << 1U) 
                                                       | (QData)((IData)(Vsim__ConstPool__TABLE_h4b0f789b_0
                                                                         [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15])))) 
                                                   & (- (QData)((IData)(
                                                                        ((~ 
                                                                          ((IData)(vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_trapPort_valid) 
                                                                           | (IData)(__VdfgRegularize_h6e95ff9d_0_92))) 
                                                                         & Vsim__ConstPool__TABLE_hb7cce103_0
                                                                         [
                                                                         ((0x00000080U 
                                                                           & (((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_2_up_valid)) 
                                                                               | (IData)(vlSelfRef.__PVT__FetchL1Plugin_logic_ctrl_trapSent)) 
                                                                              << 7U)) 
                                                                          | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15))]))))) 
                                                  | ((- (QData)((IData)(
                                                                        ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_92)) 
                                                                         & (IData)(vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_trapPort_valid))))) 
                                                     & (((QData)((IData)(
                                                                         (2U 
                                                                          & (- (IData)(
                                                                                (1U 
                                                                                & (~ (IData)(vlSelfRef.__PVT__DecoderPlugin_logic_interrupt_buffered)))))))) 
                                                         << 0x00000021U) 
                                                        | (((QData)((IData)(vlSelfRef.__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_RAW_0)) 
                                                            << 1U) 
                                                           | (QData)((IData)(
                                                                             (1U 
                                                                              & (~ (IData)(vlSelfRef.__PVT__DecoderPlugin_logic_interrupt_buffered)))))))))));
}

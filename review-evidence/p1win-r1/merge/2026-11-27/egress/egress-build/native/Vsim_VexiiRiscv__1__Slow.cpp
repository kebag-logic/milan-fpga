// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

extern const VlUnpacked<CData/*0:0*/, 512> Vsim__ConstPool__TABLE_h5eb9ad86_0;
extern const VlUnpacked<CData/*4:0*/, 512> Vsim__ConstPool__TABLE_hb76b7511_0;
extern const VlUnpacked<CData/*0:0*/, 64> Vsim__ConstPool__TABLE_h351a1f2e_0;
extern const VlUnpacked<CData/*0:0*/, 64> Vsim__ConstPool__TABLE_h1fed2e5e_0;
extern const VlUnpacked<CData/*4:0*/, 256> Vsim__ConstPool__TABLE_hd401da92_0;
extern const VlUnpacked<CData/*0:0*/, 128> Vsim__ConstPool__TABLE_h4b0f789b_0;
extern const VlUnpacked<CData/*0:0*/, 256> Vsim__ConstPool__TABLE_hb7cce103_0;

VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__8\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_92;
    __VdfgRegularize_h6e95ff9d_0_92 = 0;
    // Body
    vlSelfRef.__PVT__LsuL1Plugin_logic_refill_push_valid 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects)) 
           & ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill) 
              | (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_lsu_ctrl_doUpgrade)));
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
        if ((1U & (~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_refill_read_reservation_take)))) {
            vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask = 0U;
        }
    }
    if (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) {
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
        vlSelfRef.__PVT__LsuL1Plugin_logic_waysWrite_mask = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78 = ((((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1170) 
                                                   << 5U) 
                                                  | (((IData)(vlSelfRef.__PVT__when_LsuL1Plugin_l1168) 
                                                      << 4U) 
                                                     | ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD) 
                                                        << 3U))) 
                                                 | (((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid) 
                                                     << 2U) 
                                                    | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_hit 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_sideEffect) 
           & ((0x0000007fU & (vlSelfRef.__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 
                              >> 6U)) == (0x0000007fU 
                                          & (vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS 
                                             >> 6U))));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81 = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo)) 
                                                 & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA));
    vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_fire 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_ready) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_arbiter_slotsWithId_0_0));
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
    __VdfgRegularize_h6e95ff9d_0_92 = ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_trapPort_valid) 
                                       | (IData)(vlSelfRef.__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_ports_1_valid));
    vlSelfRef.__PVT__FetchL1Plugin_logic_banks_0_read_cmd_valid 
        = (1U & ((~ (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_up_valid)) 
                 | (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady)));
    vlSelfRef.WhiteboxerPlugin_logic_commits_ports_0_pc 
        = (vlSelfRef.__PVT__execute_ctrl4_up_PC_lane0 
           & (- (IData)((IData)(vlSelfRef.WhiteboxerPlugin_logic_commits_ports_0_valid))));
    vlSelfRef.integer_write_0_valid = vlSelfRef.__PVT__lane0_integer_WriteBackPlugin_logic_write_port_valid;
    vlSelfRef.__PVT__fetch_logic_ctrls_2_up_cancel 
        = ((IData)(vlSelfRef.__PVT__DecoderPlugin_logic_laneLogic_0_flushPort_valid) 
           | (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel));
    vlSelfRef.__PVT__execute_ctrl0_up_LANE_SEL_lane0 
        = ((~ ((IData)(vlSelfRef.__PVT__LsuPlugin_logic_onCtrl_hartRegulation_valid) 
               | (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel))) 
           & (IData)(vlSelfRef.__PVT__DispatchPlugin_logic_scheduler_arbiters_0_doIt));
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
    vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_DIRTY 
        = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_SHARED_dirty) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_valid 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid));
    vlSelfRef.__PVT__when_LsuL1Plugin_l679 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_last) 
                                              & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_fire));
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

VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__9\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__execute_ctrl0_LANE_SEL_lane0_bypass 
        = ((~ (IData)(vlSelfRef.__PVT__decode_ctrls_1_lane0_upIsCancel)) 
           & (IData)(vlSelfRef.__PVT__execute_ctrl0_up_LANE_SEL_lane0));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_takeWhen_valid 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_valid));
    vlSelfRef.__PVT__when_LsuL1Bus_l235 = ((IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_c_onCtrl_redo) 
                                           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_valid));
    vlSelfRef.__PVT__fetch_logic_ctrls_0_up_isFiring 
        = ((~ (IData)(vlSelfRef.__PVT__PcPlugin_logic_harts_0_holdReg)) 
           & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90) 
              & (IData)(vlSelfRef.__PVT__fetch_logic_ctrls_1_down_isReady)));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram_wr_en 
        = ((~ (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_full)) 
           & (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_takeWhen_valid));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid 
        = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rValid;
    if ((2U == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight))) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid = 0U;
        vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = 1U;
        vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = 0U;
    } else {
        vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = 1U;
    }
    if (vlSelfRef.__PVT__when_LsuL1Bus_l235) {
        vlSelfRef.__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid = 1U;
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
            = vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS;
        vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = 0U;
    } else {
        vlSelfRef.__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS 
            = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_noDecoder_toDown_b_rData_address;
    }
}

VL_ATTR_COLD void Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___stl_sequent__TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__10\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__LsuL1TileLinkPlugin_logic_down_c_fire 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_lsuL1Bus_bus_c_rValidN) 
           & (IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__vexiis_0_logic_core_LsuL1TileLinkPlugin_logic_down_c_valid));
    vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_last 
        = ((IData)(vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__VdfgRegularize_h6e95ff9d_0_82) 
           | (0x0fU == (IData)(vlSelfRef.__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat)));
}

VL_ATTR_COLD void Vsim_VexiiRiscv___ctor_var_reset_0(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___ctor_var_reset_0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->__PVT__PrivilegedPlugin_logic_rdtime = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11150710017461547717ull);
    vlSelf->PrivilegedPlugin_logic_harts_0_int_m_timer = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7275950598515650268ull);
    vlSelf->PrivilegedPlugin_logic_harts_0_int_m_software = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16288956082571543111ull);
    vlSelf->PrivilegedPlugin_logic_harts_0_int_m_external = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11139037878695476537ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13495847842985713937ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4888721487971431677ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_a_payload_opcode = 4U;
    ;
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_a_payload_param = 0U;
    ;
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_a_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11393872414079481367ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_a_payload_size = 6U;
    ;
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17396895725698956968ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_ready = 1U;
    ;
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10233674007314412972ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11852452540169638452ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4964728911031664997ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_payload_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13582626095062249904ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5458570959695473133ull);
    vlSelf->__PVT__FetchL1TileLinkPlugin_logic_down_d_payload_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14538563850392487347ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9760227902326265575ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3888123692036643922ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_a_payload_opcode = 6U;
    ;
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_a_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17839377969105908969ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_a_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12563267846252858491ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_a_payload_size = 6U;
    ;
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_b_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16170531339873777095ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_b_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8344381162307403753ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_b_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 659258618967795185ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_b_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7164769241158482524ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_b_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8567785931103675164ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_b_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17725337740827729845ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6538436680615127761ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12909423683980171581ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10910122847183361101ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 716751910919247241ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6446285192094417884ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_payload_size = 6U;
    ;
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7440031033220376669ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_payload_corrupt = 0U;
    ;
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13464029822580863348ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_ready = 1U;
    ;
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8512679517994801210ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12240137681550953176ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_payload_sink = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 13024750120649134875ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_payload_size = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13017194842762369510ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_payload_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10807632007141972975ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13526118775395295722ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_d_payload_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 199962824409200969ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_e_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17994398417624621076ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_e_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2457005180942993974ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_e_payload_sink = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 13839036321251744483ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5139495323315014078ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10203599134674550395ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15779204126818370692ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_payload_param = 0U;
    ;
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10672584278212638155ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_payload_size = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17310787623795987139ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_payload_mask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3427089216210466208ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10796668402868462510ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_a_payload_corrupt = 0U;
    ;
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9209992950903849826ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_ready = 1U;
    ;
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_payload_opcode = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15479534224842604336ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_payload_param = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2467005477107038959ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_payload_size = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16190336018776281058ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_payload_denied = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2096476771030873638ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_payload_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9290505115693092873ull);
    vlSelf->__PVT__LsuTileLinkPlugin_logic_bridge_down_d_payload_corrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9745732892644007154ull);
    vlSelf->__PVT__litex_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7160073992957751673ull);
    vlSelf->__PVT__cpuResetCtrl_reset = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3165815507858932020ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div_io_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17506585229203935400ull);
    vlSelf->__PVT__FetchL1Plugin_logic_banks_0_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15731137301924944462ull);
    vlSelf->__PVT__FetchL1Plugin_logic_banks_1_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1973342002565950126ull);
    vlSelf->__PVT__FetchL1Plugin_logic_ways_0_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(21, __VscopeHash, 3543695827114700533ull);
    vlSelf->__PVT__FetchL1Plugin_logic_ways_1_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(21, __VscopeHash, 5860169880028459004ull);
    vlSelf->__PVT__FetchL1Plugin_logic_plru_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15995761105635216929ull);
    vlSelf->__PVT__CsrRamPlugin_logic_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18382132665750525305ull);
    vlSelf->__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(22, __VscopeHash, 6972749232497440972ull);
    vlSelf->__PVT__LsuL1Plugin_logic_ways_0_mem_spinal_port2 = VL_SCOPED_RAND_RESET_I(22, __VscopeHash, 18439755556208378486ull);
    vlSelf->__PVT__LsuL1Plugin_logic_shared_mem_spinal_port1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13303100588748487446ull);
    vlSelf->__PVT__LsuL1Plugin_logic_shared_mem_spinal_port2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2244477834900725321ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_victimBuffer_spinal_port1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12396998407475303655ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div_io_cmd_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7287277227094156585ull);
    vlSelf->__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12414871424560918917ull);
    vlSelf->__PVT__LsuPlugin_logic_onAddress0_arbiter_io_output_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9296881112885406140ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo_io_pop_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8873991239375764930ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter_io_inputs_0_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5271643308857726800ull);
    vlSelf->__PVT___zz_early0_IntAluPlugin_logic_alu_result_5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5098153158479734639ull);
    vlSelf->__PVT___zz_early0_BarrelShifterPlugin_logic_shift_shifted = VL_SCOPED_RAND_RESET_Q(33, __VscopeHash, 14869542007956595645ull);
    vlSelf->__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_1 = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 13279093467449740784ull);
    vlSelf->__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_1_lane0_3 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16512470420044263227ull);
    vlSelf->__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_1 = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 4062298030843443768ull);
    vlSelf->__PVT___zz_execute_ctrl2_down_early0_MulPlugin_logic_mul_VALUES_2_lane0_2 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2535421096010570724ull);
    vlSelf->__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8294534665569825318ull);
    vlSelf->__PVT___zz_execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7810271010624815335ull);
    vlSelf->__PVT___zz_FetchL1Plugin_logic_ways_0_mem_port = VL_SCOPED_RAND_RESET_I(21, __VscopeHash, 8760254785274260666ull);
    vlSelf->__PVT___zz_when = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9732959257103619139ull);
    vlSelf->__PVT___zz_decode_ctrls_1_down_DispatchPlugin_FENCE_OLDER_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7877688713446329784ull);
    vlSelf->__PVT___zz_PcPlugin_logic_harts_0_aggregator_fault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2385242081271635163ull);
    vlSelf->__PVT___zz_CsrRamPlugin_logic_flush_counter_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1268149379299614886ull);
    vlSelf->__PVT___zz_LsuL1Plugin_logic_writeback_read_wordIndex_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2123234524279771803ull);
    vlSelf->__PVT___zz_LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_UNIQUE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3765759036775672011ull);
    vlSelf->__PVT___zz_LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight_5 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3543636522523480284ull);
    vlSelf->__PVT___zz_execute_ctrl1_down_AguPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6310166842822106803ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCount_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1095838788618830438ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCount = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4158364252339724864ull);
    vlSelf->__PVT___zz___05Fzz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_1_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12107009570111522331ull);
    vlSelf->__PVT__fetch_logic_ctrls_0_up_isValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14109339882566305089ull);
    vlSelf->__PVT__execute_ctrl5_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10178875102398425434ull);
    vlSelf->__PVT__execute_ctrl5_up_RD_PHYS_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6339763062465252202ull);
    vlSelf->__PVT__execute_ctrl4_up_MMU_BYPASS_TRANSLATION_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11391482089242947216ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_HITS_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9804994303583603008ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_loaded = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17428041894744234563ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_address = VL_SCOPED_RAND_RESET_I(19, __VscopeHash, 10537353378077165134ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_fault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7878661152097828517ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WAYS_TAGS_lane0_0_unique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4755732329464450013ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_WRITE_TO_READ_HAZARDS_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4769521934897759282ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_BANKS_MUXES_lane0_0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4003137297441400254ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_BANK_BUSY_REMAPPED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6579101877025098338ull);
    vlSelf->__PVT__execute_ctrl4_up_MMU_HAZARD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8140982078862044218ull);
    vlSelf->__PVT__execute_ctrl4_up_MMU_REFILL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8216937708547725799ull);
    vlSelf->__PVT__execute_ctrl4_up_MMU_ACCESS_FAULT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12850868732183301264ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_FAILURE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14622140361556995059ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_MMU_PAGE_FAULT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10337185011653837945ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_FROM_LSU_MSB_FAILED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8388998039551315514ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_IO_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5307310251938335619ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_IO_RSP_lane0_fault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3170139319488699845ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_onPma_CACHED_RSP_lane0_fault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16189659104464902217ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_preCtrl_MISS_ALIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13231077729210837932ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_PHYSICAL_ADDRESS_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12326069223664496064ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_onTrigger_HIT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16386338590174550482ull);
    vlSelf->__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_1_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3758608080581029324ull);
    vlSelf->__PVT__execute_ctrl4_up_early0_MulPlugin_logic_steps_0_adders_0_lane0 = VL_SCOPED_RAND_RESET_Q(63, __VscopeHash, 11248302648548515648ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_SHARED_lane0_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7379861620091196307ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_PREFETCH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 479431181833691042ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_FROM_LSU_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1048421351879635054ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_FLUSH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9719130126662963162ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_PREFETCH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13084962574323738810ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_INVALID_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8446687420814736316ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_CLEAN_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5213045393130700215ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_STORE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9020462869089615564ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_ATOMIC_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6758555565343706113ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_LOAD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14996028256359404962ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_SIZE_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9043668142356853572ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_MASK_lane0 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8285593670558913141ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_MIXED_ADDRESS_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1895064022320589022ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_HAZARD_FORCED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14167199103189730674ull);
    vlSelf->__PVT__execute_ctrl4_up_AguPlugin_FLOAT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7672307668896433975ull);
    vlSelf->__PVT__execute_ctrl4_up_AguPlugin_STORE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8859336955743698557ull);
    vlSelf->__PVT__execute_ctrl4_up_MulPlugin_HIGH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5919977667044914725ull);
    vlSelf->__PVT__execute_ctrl4_up_BYPASSED_AT_4_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8660754561702648883ull);
    vlSelf->__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9307320183651164846ull);
    vlSelf->__PVT__execute_ctrl4_up_lane0_IntFormatPlugin_logic_SIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6329982650743207361ull);
    vlSelf->__PVT__execute_ctrl4_up_lane0_integer_WriteBackPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12173630236761377034ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuPlugin_logic_FENCE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16567106095157793597ull);
    vlSelf->__PVT__execute_ctrl4_up_AguPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13606992373192465244ull);
    vlSelf->__PVT__execute_ctrl4_up_early0_MulPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16724052399600968531ull);
    vlSelf->__PVT__execute_ctrl4_up_Decode_UOP_ID_lane0 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1261190874839143295ull);
    vlSelf->__PVT__execute_ctrl4_up_PC_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8957125997935374912ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_lsu_rt0_SHARED_BYPASS_VALUE_lane0_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4038649795028559340ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_lsu_rt0_SHARED_BYPASS_VALID_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10997200230845560291ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_MASK_lane0 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4115300050181710074ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_ADDRESS_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2669941858717750350ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9485566172325996838ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_BANK_BUSY_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8322273008085341058ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_PREFETCH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1248541202110642801ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_LSU_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9442494103328739629ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_FLUSH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5871548566215299074ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_PREFETCH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12817471358579199445ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_INVALID_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14926053336980275402ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_CLEAN_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7060477335721525205ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_STORE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9320449539913388512ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_ATOMIC_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10769966409579940149ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_LOAD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16921124092105978720ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_SIZE_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17171558488396993306ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_MASK_lane0 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13272745296153939069ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_MIXED_ADDRESS_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3622649927301526480ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuPlugin_logic_FROM_ACCESS_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9596980224657661627ull);
    vlSelf->__PVT__execute_ctrl3_up_DivPlugin_DIV_RESULT_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15170165949769263720ull);
    vlSelf->__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_3_lane0 = VL_SCOPED_RAND_RESET_I(30, __VscopeHash, 7950174084423555373ull);
    vlSelf->__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_2_lane0 = VL_SCOPED_RAND_RESET_Q(47, __VscopeHash, 8846343447165542172ull);
    vlSelf->__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_1_lane0 = VL_SCOPED_RAND_RESET_Q(47, __VscopeHash, 15547674404159967712ull);
    vlSelf->__PVT__execute_ctrl3_up_early0_MulPlugin_logic_mul_VALUES_0_lane0 = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 3194296029668043027ull);
    vlSelf->__PVT__execute_ctrl3_up_COMMIT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11654734657856281553ull);
    vlSelf->__PVT__execute_ctrl3_up_AguPlugin_FLOAT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1339116220194696321ull);
    vlSelf->__PVT__execute_ctrl3_up_AguPlugin_STORE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 391972579615617769ull);
    vlSelf->__PVT__execute_ctrl3_up_MulPlugin_HIGH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5243480683002266548ull);
    vlSelf->__PVT__execute_ctrl3_up_BYPASSED_AT_4_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8097148804124604332ull);
    vlSelf->__PVT__execute_ctrl3_up_BYPASSED_AT_3_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6831926324132183522ull);
    vlSelf->__PVT__execute_ctrl3_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2456231593640922116ull);
    vlSelf->__PVT__execute_ctrl3_up_lane0_IntFormatPlugin_logic_SIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8834568031663321613ull);
    vlSelf->__PVT__execute_ctrl3_up_lane0_integer_WriteBackPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17915360683079563874ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuPlugin_logic_FENCE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2514844658423200788ull);
    vlSelf->__PVT__execute_ctrl3_up_AguPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 992459410655351455ull);
    vlSelf->__PVT__execute_ctrl3_up_CsrAccessPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2598896838157997025ull);
    vlSelf->__PVT__execute_ctrl3_up_early0_DivPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14486909130720871716ull);
    vlSelf->__PVT__execute_ctrl3_up_early0_MulPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4363643252997688068ull);
    vlSelf->__PVT__execute_ctrl3_up_integer_RS2_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11233182735168189828ull);
    vlSelf->__PVT__execute_ctrl3_up_Decode_UOP_ID_lane0 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17484368925451154254ull);
    vlSelf->__PVT__execute_ctrl3_up_TRAP_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 63863339791932833ull);
    vlSelf->__PVT__execute_ctrl3_up_PC_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3056627957833840561ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_EnvPlugin_OP_lane0 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6846225456744384606ull);
    vlSelf->__PVT__execute_ctrl2_up_AguPlugin_FLOAT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15784451719511216514ull);
    vlSelf->__PVT__execute_ctrl2_up_AguPlugin_ATOMIC_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4174346244220523090ull);
    vlSelf->__PVT__execute_ctrl2_up_AguPlugin_STORE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4099271076526513756ull);
    vlSelf->__PVT__execute_ctrl2_up_AguPlugin_LOAD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17540888788232259809ull);
    vlSelf->__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_CLEAR_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7093587969099189300ull);
    vlSelf->__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_MASK_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12271877547194538905ull);
    vlSelf->__PVT__execute_ctrl2_up_CsrAccessPlugin_CSR_IMM_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13632913260549023834ull);
    vlSelf->__PVT__execute_ctrl2_up_DivPlugin_REM_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10727061411712663234ull);
    vlSelf->__PVT__execute_ctrl2_up_RsUnsignedPlugin_RS2_SIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14476586639416505419ull);
    vlSelf->__PVT__execute_ctrl2_up_RsUnsignedPlugin_RS1_SIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7661615027284845992ull);
    vlSelf->__PVT__execute_ctrl2_up_MulPlugin_HIGH_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3727882233892813432ull);
    vlSelf->__PVT__execute_ctrl2_up_BranchPlugin_BRANCH_CTRL_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7623117839262859178ull);
    vlSelf->__PVT__execute_ctrl2_up_BarrelShifterPlugin_SIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9900160296357416093ull);
    vlSelf->__PVT__execute_ctrl2_up_BarrelShifterPlugin_LEFT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17155911396682817317ull);
    vlSelf->__PVT__execute_ctrl2_up_SrcStageables_UNSIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7549122395805116696ull);
    vlSelf->__PVT__execute_ctrl2_up_BYPASSED_AT_4_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7149348231751841375ull);
    vlSelf->__PVT__execute_ctrl2_up_BYPASSED_AT_3_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8894641787190986353ull);
    vlSelf->__PVT__execute_ctrl2_up_BYPASSED_AT_2_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11866268716049876938ull);
    vlSelf->__PVT__execute_ctrl2_up_lane0_IntFormatPlugin_logic_WIDTH_ID_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14212662831854466763ull);
    vlSelf->__PVT__execute_ctrl2_up_lane0_IntFormatPlugin_logic_SIGNED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4864837772523073196ull);
    vlSelf->__PVT__execute_ctrl2_up_SrcStageables_ZERO_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10600668263132298547ull);
    vlSelf->__PVT__execute_ctrl2_up_SrcStageables_REVERT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8431137356742974726ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_BITWISE_CTRL_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2039611507745839950ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_SLTX_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12115337788783473208ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_IntAluPlugin_ALU_ADD_SUB_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5952698362024221700ull);
    vlSelf->__PVT__execute_ctrl2_up_lane0_integer_WriteBackPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3284328803639582807ull);
    vlSelf->__PVT__execute_ctrl2_up_AguPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2373504367793395388ull);
    vlSelf->__PVT__execute_ctrl2_up_CsrAccessPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 630130568224723823ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_EnvPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17187774108940160615ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_DivPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8175780186900244013ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_MulPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17646660239102339906ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_BranchPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2956813964405850354ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_BarrelShifterPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 936807803340423771ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_IntAluPlugin_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3830457147417227904ull);
    vlSelf->__PVT__execute_ctrl2_up_MAY_FLUSH_PRECISE_3_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6419913810102080953ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC2_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1529984673641231229ull);
    vlSelf->__PVT__execute_ctrl2_up_early0_SrcPlugin_SRC1_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7733329633704952499ull);
    vlSelf->__PVT__execute_ctrl2_up_AguPlugin_SIZE_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8088421899698287003ull);
    vlSelf->__PVT__execute_ctrl2_up_Decode_UOP_ID_lane0 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15749559364842975491ull);
    vlSelf->__PVT__execute_ctrl2_up_PC_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10596343562550174164ull);
    vlSelf->__PVT__execute_ctrl2_up_Decode_UOP_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 568860624426468301ull);
    vlSelf->__PVT__execute_ctrl0_down_COMPLETED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4294856960196827560ull);
    vlSelf->__PVT__execute_ctrl1_up_AguPlugin_SIZE_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16981739238577320839ull);
    vlSelf->__PVT__execute_ctrl1_up_RS2_PHYS_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 5073566022088628272ull);
    vlSelf->__PVT__execute_ctrl1_up_RS1_PHYS_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8637308768812821824ull);
    vlSelf->__PVT__execute_ctrl1_up_Decode_UOP_ID_lane0 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2094587094230917285ull);
    vlSelf->__PVT__execute_ctrl1_up_TRAP_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13939931623444867846ull);
    vlSelf->__PVT__execute_ctrl1_up_PC_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3589688516328729202ull);
    vlSelf->__PVT__execute_ctrl1_up_Decode_UOP_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11256926009577175712ull);
    vlSelf->__PVT__decode_ctrls_0_down_Decode_INSTRUCTION_0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9609942391034408196ull);
    vlSelf->__PVT__decode_ctrls_0_down_isReady = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15947640718386916421ull);
    vlSelf->__PVT__decode_ctrls_1_up_PC_0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6387376515214131465ull);
    vlSelf->__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_RAW_0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17578070917255178614ull);
    vlSelf->__PVT__decode_ctrls_1_up_Decode_DECOMPRESSION_FAULT_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14817167401237022566ull);
    vlSelf->__PVT__decode_ctrls_1_up_Decode_INSTRUCTION_0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13433696627557486655ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_down_isReady = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14762614421825734374ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_MMU_BYPASS_TRANSLATION = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1472539786152946411ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_MMU_ACCESS_FAULT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5245525611532499608ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_MMU_PAGE_FAULT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13810084822611534628ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_MMU_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17412914476888925628ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_MMU_REFILL = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8983368947189592123ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HIT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7975830384259229771ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_MMU_TRANSLATED = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6895571243255036684ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5847696983483207020ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_HITS_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 94085370021678613ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11044759380234865443ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_BANKS_MUXES_0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15381584402394486424ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_BANKS_MUXES_1 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14077744306856670363ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_PLRU_BYPASSED_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10282584627843990416ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_TAGS_0_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9008476555942796088ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_FetchL1Plugin_logic_WAYS_TAGS_1_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6098403496140343356ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_Fetch_PC_FAULT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1697390572929044670ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_Fetch_WORD_PC = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17707099993356213914ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_TAGS_UPDATE_ADDRESS = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 8693267834269551615ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_TAGS_UPDATE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14378549967992752952ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_PLRU_BYPASS_DATA_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13179438637002167518ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_up_FetchL1Plugin_logic_cmd_PLRU_BYPASS_VALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3138761222708826936ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_up_Fetch_PC_FAULT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7986333660986221592ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_up_Fetch_WORD_PC = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4215765481352200793ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13673367627403956972ull);
    vlSelf->__PVT__fetch_logic_ctrls_2_up_cancel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3149845334143882294ull);
    vlSelf->__PVT__execute_ctrl2_LANE_SEL_lane0_bypass = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1671761574095450140ull);
    vlSelf->__PVT__execute_ctrl0_LANE_SEL_lane0_bypass = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4560336074792846907ull);
    vlSelf->__PVT__execute_ctrl5_up_RD_ENABLE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9837957002523826331ull);
    vlSelf->__PVT__execute_ctrl5_up_LANE_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1058686193451855710ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_TAG_UPDATE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15703593745072371969ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_ASK_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 682629617482071968ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_DIRTY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1180048584429446898ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_FAULT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4482362735595151081ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_HIT_UNIQUE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17601326363694806896ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_LOCK_HIT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 204476438281178858ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_onPreCtrl_WB_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11816521142621530017ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HIT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16824102261052413045ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_WAYS_HITS = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5684328945730131094ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_SHARED_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4944095524343838714ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_SET_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5055362812078660475ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_FORCE_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15387640816877958178ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_PROBE_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5170735576732691861ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9983866174651669827ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3402198296207424113ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_LsuL1_PHYSICAL_ADDRESS = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12739773304829914773ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_FORCE_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3675597024771245248ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_rt0_SHARED_BYPASS_VALUE_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14854222278899651656ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_rt0_SHARED_BYPASS_VALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16725694457413394182ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_FORCE_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13685470803736401515ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17119075138384667196ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_SHARED = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12609118883397296006ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_UNIQUE = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12244937610153955844ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_LsuL1_PHYSICAL_ADDRESS = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 282425475912668058ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3375294507187179297ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4221032079760132208ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_HAZARD_FORCED_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16189618468852906225ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_2_down_LsuL1_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13476929493621629107ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_onPreCtrl_HIT_DIRTY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9847529694562165402ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_WAYS_HIT = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2432208186376951629ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_up_SET_HAZARD = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17005689856440037675ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_1_down_SHARED_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11029874625454470476ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_pip_ctrl_0_down_LsuL1_PHYSICAL_ADDRESS = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10599996440092503562ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1_WAIT_REFILL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13347629249122137844ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1Plugin_logic_NEED_UNIQUE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7689847728340884480ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1Plugin_logic_FREEZE_HAZARD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6515407904376055041ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1Plugin_logic_FREEZE_HAZARD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15295446987052207841ull);
    vlSelf->__PVT__execute_ctrl2_down_LsuL1Plugin_logic_EVENT_WRITE_VALID_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 733368417567508675ull);
    vlSelf->__PVT___zz_3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9206227403773069285ull);
    vlSelf->__PVT__fetch_logic_ctrls_0_up_isFiring = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12925176172678174158ull);
    vlSelf->__PVT__decode_ctrls_0_down_TRAP_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14083671706064694631ull);
    vlSelf->__PVT__execute_ctrl4_down_lane0_integer_WriteBackPlugin_logic_DATA_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5038307712405861497ull);
    vlSelf->__PVT__execute_ctrl4_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1299394885230039560ull);
    vlSelf->__PVT__execute_ctrl3_up_lane0_integer_WriteBackPlugin_logic_DATA_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3608185006373802001ull);
    vlSelf->__PVT__execute_ctrl0_up_LANE_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18373073004239773131ull);
    vlSelf->__PVT__execute_ctrl4_up_RD_PHYS_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13003984687771256887ull);
    vlSelf->__PVT__execute_ctrl4_up_RD_ENABLE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15776904710887248878ull);
    vlSelf->__PVT__execute_ctrl3_up_RD_PHYS_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16176978717626347005ull);
    vlSelf->__PVT__execute_ctrl3_up_RD_ENABLE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1119958212939606770ull);
    vlSelf->__PVT__execute_ctrl2_up_RD_PHYS_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4691085528506911384ull);
    vlSelf->__PVT__execute_ctrl2_up_RD_ENABLE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15513182956575099667ull);
    vlSelf->__PVT__execute_ctrl1_up_RD_PHYS_lane0 = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6948285716046181020ull);
    vlSelf->__PVT__execute_ctrl1_up_RD_ENABLE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3876287833532384390ull);
    vlSelf->__PVT__decode_ctrls_1_up_TRAP_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7994855390892920362ull);
    vlSelf->__PVT__decode_ctrls_1_up_LANE_SEL_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6546548708081629275ull);
    vlSelf->__PVT__decode_ctrls_1_up_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2103809539656783089ull);
    vlSelf->__PVT__decode_ctrls_1_up_isMoving = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4016707947326853069ull);
    vlSelf->__PVT__execute_ctrl1_up_LANE_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11674703118549435514ull);
    vlSelf->__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_jumpLogic_COND_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14750805501319626364ull);
    vlSelf->__PVT__execute_ctrl2_down_early0_BranchPlugin_logic_alu_EQ_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5080456595162129556ull);
    vlSelf->__PVT__execute_ctrl2_up_TRAP_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4876527276170953938ull);
    vlSelf->__PVT__execute_ctrl2_TRAP_lane0_bypass = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13031551760135511953ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1_ABORD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4595714722798562544ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1_FLUSH_HAZARD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4701513472249118975ull);
    vlSelf->__PVT__execute_ctrl4_up_COMMIT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13843172555158160884ull);
    vlSelf->__PVT__execute_ctrl4_COMMIT_lane0_bypass = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12819168595822225556ull);
    vlSelf->__PVT__execute_ctrl4_up_TRAP_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8222408219004711347ull);
    vlSelf->__PVT__execute_ctrl4_TRAP_lane0_bypass = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5110932751844520163ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1_MISS_UNIQUE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10178060801257281628ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1_HAZARD_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1960797711476410323ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1_FAULT_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 930143338405865382ull);
    vlSelf->__PVT__execute_ctrl4_up_integer_RS2_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9414166086915161505ull);
    vlSelf->__PVT__execute_ctrl3_down_LsuPlugin_logic_onPma_IO_RSP_lane0_fault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14284456346448678487ull);
    vlSelf->__PVT__execute_ctrl4_down_LsuL1_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5909388813944414252ull);
    vlSelf->__PVT__execute_ctrl4_up_LsuL1_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14350838540166212678ull);
    vlSelf->__PVT__execute_ctrl3_up_LsuL1_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5835935581370377566ull);
    vlSelf->__PVT__execute_ctrl2_up_LsuPlugin_logic_FENCE_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4583567283579492625ull);
    vlSelf->__PVT__decode_ctrls_0_up_isFiring = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2774719461919963588ull);
    vlSelf->__PVT__execute_ctrl3_up_LANE_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3851599131807927924ull);
    vlSelf->__PVT__execute_ctrl4_up_LANE_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11057980414654134026ull);
    vlSelf->__PVT__execute_ctrl1_down_integer_RS2_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1570168396913777395ull);
    vlSelf->__PVT__execute_ctrl1_down_early0_SrcPlugin_logic_SRC2_CTRL_lane0 = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13504136216398276175ull);
    vlSelf->__PVT__execute_ctrl1_down_integer_RS1_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7736329270201938799ull);
    vlSelf->__PVT__decode_ctrls_1_lane0_upIsCancel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8293529092924545819ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10248776544226401004ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_down_FetchL1Plugin_logic_WAYS_HITS_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 843214988829478326ull);
    vlSelf->__PVT__fetch_logic_ctrls_0_down_FetchL1Plugin_logic_cmd_PLRU_BYPASS_DATA_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2152856364398538011ull);
    vlSelf->__PVT__fetch_logic_ctrls_1_up_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10218635785549191123ull);
    vlSelf->__PVT___zz_fetch_logic_ctrls_0_haltRequest_FetchL1Plugin_l218 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9540653331488808926ull);
    vlSelf->__PVT___zz_4 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4843458603979061121ull);
    vlSelf->__PVT__execute_ctrl2_up_LANE_SEL_lane0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4050759865481414433ull);
    vlSelf->__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS2_UNSIGNED_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18219331083423898857ull);
    vlSelf->__PVT__execute_ctrl2_down_RsUnsignedPlugin_RS1_UNSIGNED_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6204622563973805434ull);
    VL_SCOPED_RAND_RESET_W(66, vlSelf->__PVT__execute_ctrl4_down_early0_MulPlugin_logic_steps_1_adders_0_lane0, __VscopeHash, 8294255144027385151ull);
    vlSelf->__PVT__execute_ctrl2_up_integer_RS2_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7622011437516560371ull);
    vlSelf->__PVT__execute_ctrl2_up_integer_RS1_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6591829473872145760ull);
    vlSelf->__PVT__CsrAccessPlugin_bus_decode_exception = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 259622401371585462ull);
    vlSelf->__PVT__CsrAccessPlugin_bus_decode_write = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8895865733033665866ull);
    vlSelf->__PVT__CsrAccessPlugin_bus_decode_trap = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12512011037388372383ull);
    vlSelf->FetchL1Plugin_logic_bus_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1966426188693623390ull);
    vlSelf->FetchL1Plugin_logic_bus_cmd_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5486551836428168990ull);
    vlSelf->FetchL1Plugin_logic_bus_cmd_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16195305360738007721ull);
    vlSelf->FetchL1Plugin_logic_bus_rsp_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17391102372888547936ull);
    vlSelf->FetchL1Plugin_logic_bus_rsp_payload_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8003982746536292534ull);
    vlSelf->__PVT__early0_BranchPlugin_logic_pcPort_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16086687070274339007ull);
    vlSelf->__PVT__LsuPlugin_logic_trapPort_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16832563893254791108ull);
    vlSelf->__PVT__LsuPlugin_logic_trapPort_payload_exception = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11928746719125357083ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_divRevertResult = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8884289985756105500ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_cmdSent = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7452444384102622511ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_request = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11721765805091622510ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_unscheduleRequest = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17102103407013089274ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_selected = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3555036002042049492ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_privilege = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 803020430447494803ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_status_mie = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4885690417490070667ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_status_mpie = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15355648350209593825ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_status_mprv = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13139636157345253847ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_cause_interrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18298939041694919087ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_cause_code = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 2749200601406335560ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_ip_meip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3048965919653051401ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_ip_mtip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6886163216057583825ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_ip_msip = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12868719963638192141ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_ie_meie = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17738242042976953954ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_ie_mtie = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8169819792827824860ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_ie_msie = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15463674397579799195ull);
    vlSelf->__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7436698589905588569ull);
    vlSelf->__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_interrupts_2_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9057774457407910046ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_m_topi_interrupt = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11458415036317790793ull);
    vlSelf->__PVT__PrivilegedPlugin_logic_harts_0_mcounteren_tm = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8308236567972734700ull);
    vlSelf->__PVT__TrapPlugin_logic_fetchL1Invalidate_0_cmd_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3567146832831336373ull);
    vlSelf->__PVT__early0_EnvPlugin_logic_trapPort_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2582036212828874568ull);
    vlSelf->__PVT__early0_EnvPlugin_logic_trapPort_payload_exception = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8707216306596090974ull);
    vlSelf->__PVT__early0_EnvPlugin_logic_trapPort_payload_arg = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9174431056796603051ull);
    vlSelf->__PVT__CsrAccessPlugin_bus_decode_trapCode = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11435720301183942642ull);
    vlSelf->__PVT__CsrAccessPlugin_bus_read_toWriteBits = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 932250030423452554ull);
    vlSelf->__PVT__CsrAccessPlugin_bus_write_moving = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8369085581232531378ull);
    vlSelf->__PVT__CsrAccessPlugin_bus_write_bits = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12062834028402537282ull);
    vlSelf->__PVT__FetchL1Plugin_logic_banks_0_write_payload_address = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 1905887500616619302ull);
    vlSelf->__PVT__FetchL1Plugin_logic_banks_0_read_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4400324635678604836ull);
    vlSelf->__PVT__FetchL1Plugin_logic_waysWrite_mask = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11905869772669052251ull);
    vlSelf->__PVT__FetchL1Plugin_logic_waysWrite_address = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 10945505206551604474ull);
    vlSelf->__PVT__FetchL1Plugin_logic_waysWrite_tag_loaded = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13309440999396257905ull);
    vlSelf->__PVT__FetchL1Plugin_logic_plru_write_payload_address = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9463072766103657685ull);
    vlSelf->__PVT__FetchL1Plugin_logic_invalidate_counter = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13356987496450077931ull);
    vlSelf->__PVT__FetchL1Plugin_logic_invalidate_counterIncr = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10948425295861317713ull);
    vlSelf->__PVT__FetchL1Plugin_logic_invalidate_firstEver = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10346403839411837926ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_start_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11179550993996911124ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_slots_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7953663766893350704ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_slots_0_cmdSent = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3306987310643877273ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_slots_0_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14729686764083389945ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_slots_0_wayToAllocate = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4553970175940977095ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_slots_0_askCmd = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13852350870421953887ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_pushCounter = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9184777135659271343ull);
    vlSelf->__PVT__when_FetchL1Plugin_l256 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12944572117077690798ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_onCmd_locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4432287051528001244ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_onCmd_lockedOh = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17201588666351111528ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_onRsp_wordIndex = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8767531577748840181ull);
    vlSelf->__PVT__FetchL1Plugin_logic_refill_onRsp_firstCycle = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16610888106844973020ull);
    vlSelf->__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13209591850018915592ull);
    vlSelf->__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_payload_address = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 5780636835629990682ull);
    vlSelf->__PVT__FetchL1Plugin_logic_ctrl_plruLogic_buffer_regNext_payload_data_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17129649996825336248ull);
    vlSelf->__PVT__FetchL1Plugin_logic_ctrl_trapSent = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4245884822399520004ull);
    vlSelf->__PVT__when_FetchL1Plugin_l488 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10952940797715948689ull);
    vlSelf->__PVT__when_FetchL1Plugin_l545 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6905895317675155406ull);
    vlSelf->__PVT__LsuPlugin_logic_trapPort_payload_code = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17481862514765857249ull);
    vlSelf->__PVT__LsuPlugin_logic_flushPort_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2122891031661128589ull);
    vlSelf->__PVT__LsuPlugin_logic_iwb_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6452008665511928800ull);
    vlSelf->__PVT__early0_BranchPlugin_logic_trapPort_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12330114601610833808ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_trapPort_payload_code = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17438483964932356653ull);
    vlSelf->__PVT__early0_SrcPlugin_logic_addsub_combined_rs2Patched = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11076918838012283834ull);
    vlSelf->__PVT__lane0_IntFormatPlugin_logic_stages_1_wb_payload = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4933771686983328826ull);
    vlSelf->__PVT__lane0_IntFormatPlugin_logic_stages_1_raw = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6273828392311204019ull);
    vlSelf->__PVT___zz_lane0_IntFormatPlugin_logic_stages_1_segments_1_sign_value = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 364200695247214541ull);
    vlSelf->__PVT__AlignerPlugin_logic_feeder_harts_0_dopId = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 18138740022305544129ull);
    vlSelf->LsuPlugin_logic_bus_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 342729512205465918ull);
    vlSelf->LsuPlugin_logic_bus_cmd_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16222728294395729616ull);
    vlSelf->LsuPlugin_logic_bus_cmd_payload_write = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15756845601915117073ull);
    vlSelf->LsuPlugin_logic_bus_cmd_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17478379942998225068ull);
    vlSelf->LsuPlugin_logic_bus_rsp_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9956602135331855665ull);
    vlSelf->LsuPlugin_logic_bus_rsp_payload_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11641842236645283696ull);
    vlSelf->__PVT__LsuPlugin_logic_onAddress0_ls_storeId = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 545870546613172249ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_lsuTrap = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 745633631843416781ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_io_tooEarly = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11676464665723448691ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_io_allowIt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 503438865940929546ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_io_doIt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2019025615540687367ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_io_doItReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8169247384952900809ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_io_cmdSent = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12752396244646341460ull);
    vlSelf->__PVT__LsuPlugin_logic_bus_rsp_toStream_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1898339337784608973ull);
    vlSelf->__PVT__LsuPlugin_logic_bus_rsp_toStream_rData_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4708653219372078386ull);
    vlSelf->__PVT__LsuPlugin_logic_bus_rsp_toStream_rData_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2238391732143778342ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_loadData_input = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8519213492644027394ull);
    vlSelf->__PVT___zz_execute_ctrl4_down_LsuL1_WRITE_DATA_lane0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3988620042005145042ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_traps_accessFault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17308394320602826688ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_traps_l1Failed = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6549773944805390309ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_traps_pmaFault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7180930504065480574ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_fenceTrap_doItReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10150716877833711589ull);
    vlSelf->__PVT__when_LsuPlugin_l915 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2040971816715655691ull);
    vlSelf->__PVT__early0_EnvPlugin_logic_exe_xretPriv = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11354967121948952114ull);
    vlSelf->__PVT__early0_EnvPlugin_logic_exe_commit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4206120957535537566ull);
    vlSelf->__PVT__when_EnvPlugin_l86 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 639426479196258813ull);
    vlSelf->__PVT__CsrRamPlugin_csrMapper_read_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11352234892550286494ull);
    vlSelf->__PVT__CsrRamPlugin_csrMapper_read_address = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6706314619471536791ull);
    vlSelf->__PVT__CsrRamPlugin_csrMapper_write_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4934222204640587457ull);
    vlSelf->__PVT__DecoderPlugin_logic_harts_0_uopId = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9133983679927433275ull);
    vlSelf->__PVT__DecoderPlugin_logic_interrupt_buffered = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 883749373016126419ull);
    vlSelf->__PVT__DecoderPlugin_logic_laneLogic_0_trapPort_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8612645699863151588ull);
    vlSelf->__PVT__when_DecoderPlugin_l229 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 638103099815012857ull);
    vlSelf->__PVT__DecoderPlugin_logic_laneLogic_0_flushPort_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6115827392244985587ull);
    vlSelf->__PVT__DispatchPlugin_logic_candidates_0_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8219534590894968067ull);
    vlSelf->__PVT__DispatchPlugin_logic_feeds_0_sent = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15016474200562885456ull);
    vlSelf->__PVT__when_DispatchPlugin_l373 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16927650803374270602ull);
    vlSelf->__PVT__DispatchPlugin_logic_scheduler_arbiters_0_doIt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10088979473434979119ull);
    vlSelf->__PVT__CsrRamPlugin_csrMapper_fired = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11349419550026180352ull);
    vlSelf->__PVT__lane0_integer_WriteBackPlugin_logic_write_port_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3077865053696872448ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_crsPorts_write_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10591647395510305617ull);
    vlSelf->__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7682786198075566239ull);
}

VL_ATTR_COLD void Vsim_VexiiRiscv___ctor_var_reset_1(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___ctor_var_reset_1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->__PVT___zz_TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14318725045165055360ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_id = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10564847488750428981ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_privilege = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9310978748550597532ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_interrupt_privilegeTriggers_0_triggered_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13405592066352146147ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_interrupt_result_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16035808385304476096ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_interrupt_validBuffer = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9816583759600871763ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_ports_1_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11366538219634060569ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_arbiter_down_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2858669043376922139ull);
    vlSelf->__PVT___zz_TrapPlugin_logic_harts_0_trap_pending_arbiter_down_payload_exception = VL_SCOPED_RAND_RESET_Q(41, __VscopeHash, 6364114894653905939ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_state_exception = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15600917177721677981ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_state_tval = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3939147321611114278ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_state_code = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 14751650035746187078ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_state_arg = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9065157568539724605ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_pc = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3629056860075226502ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pending_slices = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7561091409488403291ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_trigger_oh = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2304366425304245910ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_pcPort_payload_pc = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10596376827404919149ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_holdPort = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17202270319259797773ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13593041109100944336ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_code = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12216878905459086770ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_i_targetPrivilege = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6831783729528220660ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_interrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14066014150771661508ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_targetPrivilege = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4373094797851128841ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_buffer_trap_code = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 14488787819402258173ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_resetToRunConditions_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8037081169421492894ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_jumpTarget = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 629759901304342651ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_triggerEbreakReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16981830498220340260ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_readed = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15435851471452182167ull);
    vlSelf->__PVT__PcPlugin_logic_harts_0_self_id = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 15081344482595962400ull);
    vlSelf->__PVT__PcPlugin_logic_harts_0_self_increment = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2209808638124658191ull);
    vlSelf->__PVT__PcPlugin_logic_harts_0_self_fault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16767583230898561279ull);
    vlSelf->__PVT__PcPlugin_logic_harts_0_self_state = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3023334728350850580ull);
    vlSelf->__PVT__PcPlugin_logic_harts_0_aggregator_target = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12619184484589746766ull);
    vlSelf->__PVT___zz_PcPlugin_logic_harts_0_aggregator_target_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6754790873434034413ull);
    vlSelf->__PVT__PcPlugin_logic_harts_0_holdReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6368596553964735713ull);
    vlSelf->__PVT__REG_CSR_3858 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11477588176495580737ull);
    vlSelf->__PVT__REG_CSR_769 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2794854670075673104ull);
    vlSelf->__PVT__REG_CSR_768 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12997885599160921116ull);
    vlSelf->__PVT__REG_CSR_834 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8724967729016742587ull);
    vlSelf->__PVT__REG_CSR_836 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3143135100208043894ull);
    vlSelf->__PVT__REG_CSR_772 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16571186382933918719ull);
    vlSelf->__PVT__REG_CSR_4016 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4104301579060973868ull);
    vlSelf->__PVT__REG_CSR_774 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2207867283245468536ull);
    vlSelf->__PVT__REG_CSR_3073 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9708255371278458558ull);
    vlSelf->__PVT__REG_CSR_3201 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14733950632424707992ull);
    vlSelf->__PVT__REG_CSR_PrivilegedPlugin_logic_readAnyWriteLegal_tvecFilter = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5279864186306516012ull);
    vlSelf->__PVT__REG_CSR_PrivilegedPlugin_logic_readAnyWriteLegal_epcFilter = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8052110585954512633ull);
    vlSelf->__PVT__REG_CSR_CsrRamPlugin_csrMapper_selFilter = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17854651458011584777ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_interface_read = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11852717977991222392ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_interface_write = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7437230710566848776ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_interface_aluInput = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7434726423668650719ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_interface_csrValue = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9026616877456103403ull);
    vlSelf->__PVT__COMB_CSR_CsrRamPlugin_csrMapper_selFilter = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12146117450326384751ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_onDecodeDo = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13966058394870656337ull);
    vlSelf->__PVT__when_CsrService_l199 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11355838498670130574ull);
    vlSelf->__PVT__when_CsrAccessPlugin_l157_6 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15406081697219216789ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_trap = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8260295150448792463ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_unfreeze = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11950316232486337820ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_flushReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12495754950761063774ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_sampled = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 33721594228313231ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_trapReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2540416716048128578ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2899914021816347054ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_inject_busTrapCodeReg = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 2415996673482682778ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_writeLogic_alu_mask = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10252390145190637227ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesDo = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10035070582017668822ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_writeLogic_onWritesFireDo = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10660406104724150372ull);
    vlSelf->__PVT__CsrRamPlugin_logic_writeLogic_hits = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9487364561688416454ull);
    vlSelf->__PVT__CsrRamPlugin_logic_writeLogic_hits_ohFirst_masked = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9880268386016400200ull);
    vlSelf->__PVT__CsrRamPlugin_logic_readLogic_hits = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1648675783214568003ull);
    vlSelf->__PVT__CsrRamPlugin_logic_readLogic_hits_ohFirst_masked = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10658617374445501136ull);
    vlSelf->__PVT__CsrRamPlugin_logic_readLogic_port_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7993042750402538761ull);
    vlSelf->__PVT__CsrRamPlugin_logic_readLogic_ohReg = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13184639188346933444ull);
    vlSelf->__PVT__CsrRamPlugin_logic_readLogic_busy = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13476159586738663100ull);
    vlSelf->__PVT__CsrRamPlugin_logic_flush_counter = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8428455851429778039ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_read_rsp_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17013864917296060188ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_read_rsp_payload_error = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6988191297455456824ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_probe_cmd_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4237470109105023460ull);
    vlSelf->__PVT__LsuL1Plugin_logic_banksWrite_mask = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7643396989474533871ull);
    vlSelf->__PVT__LsuL1Plugin_logic_banksWrite_address = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 11892450420234447136ull);
    vlSelf->__PVT__LsuL1Plugin_logic_banksWrite_writeData = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6716444017466127006ull);
    vlSelf->__PVT__LsuL1Plugin_logic_banksWrite_writeMask = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3925993394201480337ull);
    vlSelf->__PVT__LsuL1Plugin_logic_waysWrite_mask = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 92920091491585669ull);
    vlSelf->__PVT__LsuL1Plugin_logic_waysWrite_address = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 12463183877846381706ull);
    vlSelf->__PVT__LsuL1Plugin_logic_waysWrite_tag_loaded = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9354392691023371732ull);
    vlSelf->__PVT__LsuL1Plugin_logic_waysWrite_tag_address = VL_SCOPED_RAND_RESET_I(19, __VscopeHash, 910096673817240039ull);
    vlSelf->__PVT__LsuL1Plugin_logic_waysWrite_tag_fault = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3897431443080006722ull);
    vlSelf->__PVT__LsuL1Plugin_logic_waysWrite_tag_unique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5287101746354660350ull);
    vlSelf->__PVT__LsuL1Plugin_logic_shared_write_payload_address = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9228440124639229209ull);
    vlSelf->__PVT__LsuL1Plugin_logic_shared_write_payload_data_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15999928395831019827ull);
    vlSelf->__PVT__LsuL1Plugin_logic_slotsFreeze = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12394148832162289323ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17047147802192983544ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6152989141191356634ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_cmdSent = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8863598691983501254ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_c_unique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1281367012143167330ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_c_data = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5514959362578387227ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackId = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 11562067524023121977ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17808353430735609939ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackTimer = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17005321121166556682ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_c_ackRequest = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11374252156820750077ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_loadedSet = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10332116066952267982ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_loaded = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7200841066913018268ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_loadedCounter = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14941455834716939439ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_slots_0_victim = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15841748819187128529ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_push_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12482109197589557212ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_push_payload_data = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9428638459181328057ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_pushCounter = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7684450220822322545ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_read_arbiter_oh = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7603949525945175483ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_read_arbiter_lock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8347884054360528673ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_read_wordIndex = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2437119274007479891ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_read_hadError = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6303629282232527163ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_read_reservation_take = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16254535386440626259ull);
    vlSelf->__PVT__when_LsuL1Plugin_l466 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16785527594870890224ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_ackSender_ack_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7019241811868231557ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15869749589053934619ull);
    vlSelf->__PVT__LsuL1Plugin_logic_refill_ackSender_ack_rData_ackId = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 15305103234587174295ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12953084784658699850ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10786852799088613865ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_busy = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5673585214602515684ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17819283538890942221ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_readCmdDone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5803820257741877493ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_victimBufferReady = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15722681962171776254ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_writeCmdDone = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17351440901717710121ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_release = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10146652035376681294ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8737321435583801446ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_fromUnique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16193440825689577551ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_toShared = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15761344037294440606ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_coherency_toUnique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 587049792528054250ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_timer_counter = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3028970566567212567ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_slots_0_free = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12017438204251648149ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_push_payload_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3033112940647569408ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_push_payload_c_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10267537519257679256ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_push_payload_c_fromUnique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16290196839693582378ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_push_payload_c_toShared = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15139114217964581370ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_read_arbiter_oh = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10232920393445641889ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_read_arbiter_lock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14081760545956464941ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_read_wordIndex = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9229929642862192233ull);
    vlSelf->__PVT__when_LsuL1Plugin_l608 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1531462118354824323ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3115851016844318583ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_read_slotReadLast_payload_wordIndex = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13709442658809427736ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_arbiter_slotsWithId_0_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4217081422783316407ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_arbiter_oh = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3543938720393603452ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_arbiter_lock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12790114832477586732ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_wordIndex = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9243500763353153800ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 988900989532856632ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11643328344735445222ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16435597723217981321ull);
    vlSelf->__PVT__when_LsuL1Plugin_l679 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9071206594688425298ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rValid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3583060860949569503ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_address = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9416691442411185838ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11292949374245006565ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_release = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 922911529169899805ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_dirty = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6582110862453747449ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_fromUnique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12960272153481795008ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toShared = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8580857186574495371ull);
    vlSelf->__PVT__LsuL1Plugin_logic_writeback_write_bufferRead_rData_coherency_toUnique = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14766985267096587319ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_rb1_onBanks_0_busyReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11682990167530877818ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_refillHazards = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16352656345392215216ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_writebackHazards = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13074565373568765488ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_loadedDirties = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 75253553148864931ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_preventSideEffects = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17184707681415186946ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_coherencyHazard = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15027900321850813667ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_hazardReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13764257739181570456ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_flushHazardReg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 270989672437720818ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_canRefill = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6832368600133417562ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_askUpgrade = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13857962775855280173ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_doRefill = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14223986126805279568ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_doUpgrade = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15421457938069024871ull);
    vlSelf->__PVT__LsuL1Plugin_logic_lsu_ctrl_doFlush = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1146730610154936132ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_freezeTimeout_state = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2586677600796644694ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_valueNext = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 10194581831846433462ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_freezeTimeout_counter_value = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 8973376908143603210ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_onCtrl_sideEffect = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13333876010181506398ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_onCtrl_redo = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4144820429701087231ull);
    vlSelf->__PVT__when_LsuL1Plugin_l1170 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15947646307007187734ull);
    vlSelf->__PVT__when_LsuL1Plugin_l1168 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12512936486620778514ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17561435517203192571ull);
    vlSelf->__PVT__LsuL1Plugin_logic_c_onCtrl_lsuHazarder_1_persistance = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17819662768192124154ull);
    vlSelf->__PVT__LsuL1Plugin_logic_initializer_counter = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5890135013826293209ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_hartRegulation_refill = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7385085723506166006ull);
    vlSelf->__PVT__LsuPlugin_logic_onCtrl_hartRegulation_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5834029769395810533ull);
    vlSelf->__PVT__when_LsuPlugin_l1000 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18109920551078429551ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9690216117099596561ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5962493468586280506ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFlow_takeWhen_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14527559256636109110ull);
    vlSelf->__PVT__when_LsuL1Bus_l235 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12029688583036811645ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7994564924013935871ull);
    vlSelf->__PVT__LsuL1TileLinkPlugin_logic_down_c_fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3771540939000065578ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onD_sel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5554047312774056799ull);
    vlSelf->__PVT__execute_lane0_bypasser_integer_RS1_bypassEnables_bools_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1982514112329553860ull);
    vlSelf->__PVT__execute_lane0_bypasser_integer_RS2_bypassEnables_bools_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1188168701802670011ull);
    vlSelf->__PVT__LsuPlugin_pmaBuilder_io_argsBits = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9451966496104794374ull);
    vlSelf->__PVT__integer_RegFilePlugin_logic_initalizer_counter = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3334778920537653167ull);
    vlSelf->__PVT__when_RegFilePlugin_l132 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11145425668394015200ull);
    vlSelf->integer_write_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10165337556710390313ull);
    vlSelf->integer_write_0_address = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 14754445455866255888ull);
    vlSelf->integer_write_0_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 987627654100834427ull);
    vlSelf->integer_write_0_uopId = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15917984719290852714ull);
    vlSelf->WhiteboxerPlugin_logic_commits_ports_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15524410634819194540ull);
    vlSelf->WhiteboxerPlugin_logic_commits_ports_0_pc = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2363804478803423639ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2 = VL_SCOPED_RAND_RESET_Q(60, __VscopeHash, 8917268762225514630ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2 = VL_SCOPED_RAND_RESET_Q(60, __VscopeHash, 3525598077440989605ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2 = VL_SCOPED_RAND_RESET_Q(60, __VscopeHash, 3324849017912984372ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2 = VL_SCOPED_RAND_RESET_Q(60, __VscopeHash, 18334295132584322921ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2 = VL_SCOPED_RAND_RESET_Q(60, __VscopeHash, 16647609600945100723ull);
    vlSelf->__PVT___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2 = VL_SCOPED_RAND_RESET_Q(60, __VscopeHash, 16745955006692741366ull);
    vlSelf->WhiteboxerPlugin_logic_trap_ports_0_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8525774269248659480ull);
    vlSelf->WhiteboxerPlugin_logic_trap_ports_0_interrupt = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14184219214102813028ull);
    vlSelf->WhiteboxerPlugin_logic_trap_ports_0_cause = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1336118133443799604ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateReg = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13588910026403628278ull);
    vlSelf->__PVT__TrapPlugin_logic_harts_0_trap_fsm_stateNext = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16173623881546417210ull);
    vlSelf->__PVT__when_TrapPlugin_l454 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8265522404442007491ull);
    vlSelf->__PVT__CsrAccessPlugin_logic_fsm_stateReg = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13996620389395470840ull);
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->__PVT__FetchL1Plugin_logic_banks_0_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14028030717280221089ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->__PVT__FetchL1Plugin_logic_banks_1_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2235710066564378506ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__FetchL1Plugin_logic_ways_0_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(21, __VscopeHash, 16173063480793078317ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__FetchL1Plugin_logic_ways_1_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(21, __VscopeHash, 14490113365478731127ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__FetchL1Plugin_logic_plru_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6901834987807664960ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__CsrRamPlugin_logic_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16647322997818462076ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__LsuL1Plugin_logic_ways_0_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(22, __VscopeHash, 10824238501046038272ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->__PVT__LsuL1Plugin_logic_shared_mem[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16586079904205597226ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->__PVT__LsuL1Plugin_logic_writeback_victimBuffer[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13614413116454300079ull);
    }
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram_wr_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15568945475720346127ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_full = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6418093491910475509ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_push = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2308372469216774754ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ptr_pop = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15608577228747841320ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block[__Vi0] = VL_SCOPED_RAND_RESET_Q(41, __VscopeHash, 16944230993558853644ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4765300388722770206ull);
    }
    vlSelf->__PVT__LsuL1Plugin_logic_banks_0_mem__DOT__ram_rd_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1735094393198226620ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11116791740413845315ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7634838253935632614ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskLocked_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11750173514446450001ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16112414170232683398ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__maskRouted_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14202831555454172571ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_1 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16960523091450213289ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT___zz_maskProposal_0_2 = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9121001295958225326ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_beat = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10751005437324979087ull);
    vlSelf->__PVT__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_arbiter__DOT__io_output_tracker_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7300239532004957744ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__counter = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13310399467120462042ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__busy = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9978140825050680280ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11447941940638490359ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__shifter = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13477734421072377445ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__numerator = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12190318740153274347ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__result = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10985629472479365071ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__div1 = VL_SCOPED_RAND_RESET_Q(33, __VscopeHash, 12543878909732917551ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__shifted = VL_SCOPED_RAND_RESET_Q(33, __VscopeHash, 7247161119885418986ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__sub1 = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 2786469133627731502ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11702692093986765398ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18280577394799625919ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT___zz_sel_6 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7066829239774018112ull);
    vlSelf->__PVT__early0_DivPlugin_logic_processing_div__DOT__sel = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6693339814266303923ull);
    vlSelf->__VdfgRegularize_h6e95ff9d_0_5 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_15 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_16 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_17 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_18 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_21 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_69 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_76 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_77 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_78 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_80 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_81 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_83 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_86 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_87 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_88 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_90 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_91 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_93 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_105 = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_refill_slots_0_loadedCounter = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_writeback_slots_0_timer_counter = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_writeback_slots_0_coherency_dirty = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_ALLOW_PROBE_DATA = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_UNIQUE = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_ALLOW_SHARED = 0;
    vlSelf->__Vdly__early0_DivPlugin_logic_processing_div__DOT__counter = 0;
    vlSelf->__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mie = 0;
    vlSelf->__Vdly__PrivilegedPlugin_logic_harts_0_m_status_mpie = 0;
    vlSelf->__Vdly__FetchL1Plugin_logic_invalidate_counter = 0;
    vlSelf->__Vdly__FetchL1Plugin_logic_refill_slots_0_valid = 0;
    vlSelf->__Vdly__FetchL1Plugin_logic_refill_pushCounter = 0;
    vlSelf->__Vdly__FetchL1Plugin_logic_refill_onRsp_wordIndex = 0;
    vlSelf->__Vdly__FetchL1Plugin_logic_ctrl_trapSent = 0;
    vlSelf->__Vdly__AlignerPlugin_logic_feeder_harts_0_dopId = 0;
    vlSelf->__Vdly__LsuPlugin_logic_onAddress0_ls_storeId = 0;
    vlSelf->__Vdly__execute_ctrl3_up_LsuL1_SEL_lane0 = 0;
    vlSelf->__Vdly__LsuPlugin_logic_bus_rsp_toStream_rValid = 0;
    vlSelf->__Vdly__DecoderPlugin_logic_harts_0_uopId = 0;
    vlSelf->__Vdly__TrapPlugin_logic_harts_0_interrupt_validBuffer = 0;
    vlSelf->__Vdly__PcPlugin_logic_harts_0_self_id = 0;
    vlSelf->__Vdly__CsrAccessPlugin_logic_fsm_inject_flushReg = 0;
    vlSelf->__Vdly__CsrAccessPlugin_logic_fsm_inject_sampled = 0;
    vlSelf->__Vdly__CsrRamPlugin_logic_readLogic_ohReg = 0;
    vlSelf->__Vdly__CsrRamPlugin_logic_flush_counter = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_refill_slots_0_valid = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_refill_slots_0_loaded = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_refill_pushCounter = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_refill_read_wordIndex = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_writeback_slots_0_busy = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_writeback_read_wordIndex = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_writeback_write_wordIndex = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_c_freezeTimeout_counter_value = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_initializer_counter = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_c_pip_ctrl_1_up_valid = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_c_pip_ctrl_2_up_valid = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_inflight = 0;
    vlSelf->__Vdly__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_beat = 0;
    vlSelf->__Vdly__execute_ctrl1_up_LANE_SEL_lane0 = 0;
    vlSelf->__Vdly__execute_ctrl2_up_LANE_SEL_lane0 = 0;
    vlSelf->__Vdly__execute_ctrl3_up_LANE_SEL_lane0 = 0;
    vlSelf->__Vdly__execute_ctrl4_up_LANE_SEL_lane0 = 0;
    vlSelf->__Vdly__integer_RegFilePlugin_logic_initalizer_counter = 0;
    vlSelf->__Vdly___zz_WhiteboxerPlugin_logic_perf_executeFreezedCounter_2 = 0;
    vlSelf->__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchHazardsCounter_2 = 0;
    vlSelf->__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_0_2 = 0;
    vlSelf->__Vdly___zz_WhiteboxerPlugin_logic_perf_candidatesCountCounters_1_2 = 0;
    vlSelf->__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_0_2 = 0;
    vlSelf->__Vdly___zz_WhiteboxerPlugin_logic_perf_dispatchFeedCounters_1_2 = 0;
    vlSelf->__Vdly__fetch_logic_ctrls_1_up_valid = 0;
    vlSelf->__Vdly__fetch_logic_ctrls_2_up_valid = 0;
    vlSelf->__Vdly__TrapPlugin_logic_harts_0_trap_fsm_stateReg = 0;
    vlSelf->__Vdly__CsrAccessPlugin_logic_fsm_stateReg = 0;
    vlSelf->__VdlyVal__FetchL1Plugin_logic_banks_0_mem__v0 = 0;
    vlSelf->__VdlyDim0__FetchL1Plugin_logic_banks_0_mem__v0 = 0;
    vlSelf->__VdlySet__FetchL1Plugin_logic_banks_0_mem__v0 = 0;
    vlSelf->__VdlyVal__FetchL1Plugin_logic_banks_1_mem__v0 = 0;
    vlSelf->__VdlyDim0__FetchL1Plugin_logic_banks_1_mem__v0 = 0;
    vlSelf->__VdlySet__FetchL1Plugin_logic_banks_1_mem__v0 = 0;
    vlSelf->__VdlyVal__FetchL1Plugin_logic_ways_0_mem__v0 = 0;
    vlSelf->__VdlyDim0__FetchL1Plugin_logic_ways_0_mem__v0 = 0;
    vlSelf->__VdlySet__FetchL1Plugin_logic_ways_0_mem__v0 = 0;
    vlSelf->__VdlyVal__FetchL1Plugin_logic_ways_1_mem__v0 = 0;
    vlSelf->__VdlyDim0__FetchL1Plugin_logic_ways_1_mem__v0 = 0;
    vlSelf->__VdlySet__FetchL1Plugin_logic_ways_1_mem__v0 = 0;
    vlSelf->__VdlyVal__FetchL1Plugin_logic_plru_mem__v0 = 0;
    vlSelf->__VdlyDim0__FetchL1Plugin_logic_plru_mem__v0 = 0;
    vlSelf->__VdlySet__FetchL1Plugin_logic_plru_mem__v0 = 0;
    vlSelf->__VdlyVal__CsrRamPlugin_logic_mem__v0 = 0;
    vlSelf->__VdlyDim0__CsrRamPlugin_logic_mem__v0 = 0;
    vlSelf->__VdlySet__CsrRamPlugin_logic_mem__v0 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_ways_0_mem__v0 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_ways_0_mem__v0 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_ways_0_mem__v0 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_shared_mem__v0 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_shared_mem__v0 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_shared_mem__v0 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_writeback_victimBuffer__v0 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_writeback_victimBuffer__v0 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_writeback_victimBuffer__v0 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_bus_toTilelink_coherent_onC_rspFifo__DOT__logic_ram__DOT__ram_block__v0 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v0 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v1 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v2 = 0;
    vlSelf->__VdlyVal__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3 = 0;
    vlSelf->__VdlyDim0__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3 = 0;
    vlSelf->__VdlySet__LsuL1Plugin_logic_banks_0_mem__DOT__ram_block__v3 = 0;
}

VL_ATTR_COLD void Vsim_VexiiRiscv___ctor_var_reset(Vsim_VexiiRiscv* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+          Vsim_VexiiRiscv___ctor_var_reset\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vsim_VexiiRiscv___ctor_var_reset_0(vlSelf);
    Vsim_VexiiRiscv___ctor_var_reset_1(vlSelf);
}

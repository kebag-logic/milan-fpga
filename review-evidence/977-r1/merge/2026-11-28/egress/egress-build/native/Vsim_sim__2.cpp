// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___nba_sequent__TOP__sim__6(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vdly__ctrlmemory1_sram2_bus_ack = 0U;
    if ((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_cyc) 
          & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
         & (~ (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_bus_ack)))) {
        vlSelfRef.__Vdly__ctrlmemory1_sram2_bus_ack = 1U;
    }
    vlSelfRef.__Vdly__ctrlmemory1_sram3_bus_ack = 0U;
    if ((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_cyc) 
          & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
         & (~ (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_bus_ack)))) {
        vlSelfRef.__Vdly__ctrlmemory1_sram3_bus_ack = 1U;
    }
    vlSelfRef.__Vdly__ctrlmemory1_sram4_bus_ack = 0U;
    if ((((IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_cyc) 
          & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
         & (~ (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_bus_ack)))) {
        vlSelfRef.__Vdly__ctrlmemory1_sram4_bus_ack = 1U;
    }
    vlSelfRef.__Vdly__ctrlmemory0_sram1_bus_ack = 0U;
    if ((((((IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel) 
            >> 1U) & (IData)(vlSelfRef.__PVT__ctrlmemory0_bus_cyc)) 
          & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
         & (~ (IData)(vlSelfRef.__PVT__ctrlmemory0_sram1_bus_ack)))) {
        vlSelfRef.__Vdly__ctrlmemory0_sram1_bus_ack = 1U;
    }
    vlSelfRef.__Vdly__ctrlmemory0_sram0_bus_ack = 0U;
    if (((((IData)(vlSelfRef.__PVT__ctrlmemory0_slave_sel) 
           & (IData)(vlSelfRef.__PVT__ctrlmemory0_bus_cyc)) 
          & (IData)(vlSelfRef.__PVT__builder_rhs_self4)) 
         & (~ (IData)(vlSelfRef.__PVT__ctrlmemory0_sram0_bus_ack)))) {
        vlSelfRef.__Vdly__ctrlmemory0_sram0_bus_ack = 1U;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__builder_litespi_grant = 0U;
        vlSelfRef.__Vdly__ctrlmemory1_sram2_bus_ack = 0U;
        vlSelfRef.__Vdly__ctrlmemory1_sram3_bus_ack = 0U;
        vlSelfRef.__Vdly__ctrlmemory1_sram4_bus_ack = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_data_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__amap_data_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__gsi_data_r__v0 = 1U;
        vlSelfRef.__Vdly__ctrlmemory0_sram1_bus_ack = 0U;
        vlSelfRef.__Vdly__ctrlmemory0_sram0_bus_ack = 0U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_pend_r__v0 = 0ULL;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_seen_r__v0 = 0ULL;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v0 = 1U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__mismatch_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__bus_err_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__head_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__seq_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__k_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__busy_r = 0U;
    } else {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_pend_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[0U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__ctr_seen_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[0U];
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w) 
             & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v5 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[0U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v6 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w) 
             & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v7 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[1U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v8 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w) 
             & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v9 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[2U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v10 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w) 
             & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v11 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[3U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v12 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w) 
             & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v13 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[4U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__held_r__v14 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_w) 
             & (0xffffU != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mismatch_r)))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__mismatch_r 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mismatch_r)));
        }
        if (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__refused_w) 
               | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__tmr_bad_p_w)) 
              | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w)) 
             & (0xffffU != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bus_err_r)))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__bus_err_r 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bus_err_r)));
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__k_r = 0U;
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__busy_r = 1U;
        } else if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__busy_r) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__k_r 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r)));
            if ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__head_r 
                    = (0x0000ffffU & ((IData)(4U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r)));
                vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__seq_r 
                    = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__seq_r)));
                vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__busy_r = 0U;
            }
        }
    }
    if ((1U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we))) {
        vlSelfRef.__VdlyVal__sram_bank0__v0 = (0x000000ffU 
                                               & vlSelfRef.__PVT__builder_rhs_self1);
        vlSelfRef.__VdlyDim0__sram_bank0__v0 = (0x00003fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank0__v0 = 1U;
    }
    if ((2U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we))) {
        vlSelfRef.__VdlyVal__sram_bank0__v1 = (0x000000ffU 
                                               & (vlSelfRef.__PVT__builder_rhs_self1 
                                                  >> 8U));
        vlSelfRef.__VdlyDim0__sram_bank0__v1 = (0x00003fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank0__v1 = 1U;
    }
    if ((4U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we))) {
        vlSelfRef.__VdlyVal__sram_bank0__v2 = (0x000000ffU 
                                               & (vlSelfRef.__PVT__builder_rhs_self1 
                                                  >> 0x10U));
        vlSelfRef.__VdlyDim0__sram_bank0__v2 = (0x00003fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank0__v2 = 1U;
    }
    if ((8U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram2_we))) {
        vlSelfRef.__VdlyVal__sram_bank0__v3 = (vlSelfRef.__PVT__builder_rhs_self1 
                                               >> 0x18U);
        vlSelfRef.__VdlyDim0__sram_bank0__v3 = (0x00003fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank0__v3 = 1U;
    }
    if ((1U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we))) {
        vlSelfRef.__VdlyVal__sram_bank1__v0 = (0x000000ffU 
                                               & vlSelfRef.__PVT__builder_rhs_self1);
        vlSelfRef.__VdlyDim0__sram_bank1__v0 = (0x00001fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank1__v0 = 1U;
    }
    if ((2U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we))) {
        vlSelfRef.__VdlyVal__sram_bank1__v1 = (0x000000ffU 
                                               & (vlSelfRef.__PVT__builder_rhs_self1 
                                                  >> 8U));
        vlSelfRef.__VdlyDim0__sram_bank1__v1 = (0x00001fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank1__v1 = 1U;
    }
    if ((4U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we))) {
        vlSelfRef.__VdlyVal__sram_bank1__v2 = (0x000000ffU 
                                               & (vlSelfRef.__PVT__builder_rhs_self1 
                                                  >> 0x10U));
        vlSelfRef.__VdlyDim0__sram_bank1__v2 = (0x00001fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank1__v2 = 1U;
    }
    if ((8U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram3_we))) {
        vlSelfRef.__VdlyVal__sram_bank1__v3 = (vlSelfRef.__PVT__builder_rhs_self1 
                                               >> 0x18U);
        vlSelfRef.__VdlyDim0__sram_bank1__v3 = (0x00001fffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank1__v3 = 1U;
    }
    if ((1U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we))) {
        vlSelfRef.__VdlyVal__sram_bank2__v0 = (0x000000ffU 
                                               & vlSelfRef.__PVT__builder_rhs_self1);
        vlSelfRef.__VdlyDim0__sram_bank2__v0 = (0x000001ffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank2__v0 = 1U;
    }
    if ((2U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we))) {
        vlSelfRef.__VdlyVal__sram_bank2__v1 = (0x000000ffU 
                                               & (vlSelfRef.__PVT__builder_rhs_self1 
                                                  >> 8U));
        vlSelfRef.__VdlyDim0__sram_bank2__v1 = (0x000001ffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank2__v1 = 1U;
    }
    if ((4U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we))) {
        vlSelfRef.__VdlyVal__sram_bank2__v2 = (0x000000ffU 
                                               & (vlSelfRef.__PVT__builder_rhs_self1 
                                                  >> 0x10U));
        vlSelfRef.__VdlyDim0__sram_bank2__v2 = (0x000001ffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank2__v2 = 1U;
    }
    if ((8U & (IData)(vlSelfRef.__PVT__ctrlmemory1_sram4_we))) {
        vlSelfRef.__VdlyVal__sram_bank2__v3 = (vlSelfRef.__PVT__builder_rhs_self1 
                                               >> 0x18U);
        vlSelfRef.__VdlyDim0__sram_bank2__v3 = (0x000001ffU 
                                                & vlSelfRef.__PVT__builder_rhs_self0);
        vlSelfRef.__VdlySet__sram_bank2__v3 = 1U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__7(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__7\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vfunc_mbx_field_f__54__word;
    __Vfunc_mbx_field_f__54__word = 0;
    // Body
    if (((IData)(vlSelfRef.__PVT__builder_rhs_self4) 
         & ((~ (IData)(vlSelfRef.__PVT__builder_shared_ack)) 
            & (IData)(vlSelfRef.__PVT__builder_rhs_self3)))) {
        if ((0U != vlSelfRef.__PVT__builder_count)) {
            vlSelfRef.__PVT__builder_count = (0x000fffffU 
                                              & (vlSelfRef.__PVT__builder_count 
                                                 - (IData)(1U)));
        }
    } else {
        vlSelfRef.__PVT__builder_count = 0x000f4240U;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__builder_count = 0x000f4240U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v0 = 1U;
        vlSelfRef.__Vdly__KL_mbx__DOT__now_ms_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__fw_busy_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_lo_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_hi_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_da_gate_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_licence_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v0 = 1U;
    } else {
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[0U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v5 = 1U;
        } else if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v6 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v6 = 1U;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[1U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v7 = 1U;
        } else if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v8 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[1U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v8 = 1U;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[2U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v9 = 1U;
        } else if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v10 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[2U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v10 = 1U;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[3U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v11 = 1U;
        } else if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v12 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[3U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v12 = 1U;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[4U]) {
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v13 = 1U;
        } else if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__refill_r__v14 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[4U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__refill_r__v14 = 1U;
        }
        if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
            vlSelfRef.__Vdly__KL_mbx__DOT__now_ms_r 
                = ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r);
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__fw_busy_r) 
             & (0x40U == (IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_waited0)))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__fw_busy_r = 0U;
        }
        __Vfunc_mbx_field_f__54__word = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.KL_mbx__DOT____VlemCall_54__mbx_field_f 
            = (1U & __Vfunc_mbx_field_f__54__word);
        if (((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                 & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w))) 
                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
              & (0x0018U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
             & (0U != vlSelfRef.KL_mbx__DOT____VlemCall_54__mbx_field_f))) {
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__fw_busy_r 
                    = ((IData)(vlSelfRef.__Vdly__KL_mbx__DOT__fw_busy_r) 
                       | (1U & ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))));
            }
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0080U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__own_mac_lo_r__v1 
                = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
            vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_lo_r__v1 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0084U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__own_mac_hi_r__v1 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__own_mac_hi_r__v1 = 1U;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__cmd_ok_w) {
            if ((1U == (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                        >> 0x0000001eU))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__dl_r__v16 
                    = vlSelfRef.__PVT__KL_mbx__DOT__tmr_deadline_r;
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_evt__DOT__dl_r__v16 
                    = (0x0000000fU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
                vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__dl_r__v16 = 1U;
            }
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_at_w))) {
            if ((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w)) 
                  & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w))) 
                 & (0x0010U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_136__mbx_place_f = 0x0000ffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_talker_decl_r__v1 
                        = (0x0000ffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                          & vlSelfRef.KL_mbx__DOT____VlemCall_136__mbx_place_f));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_talker_decl_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_talker_decl_r__v1 = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w)) 
                  & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w))) 
                 & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_132__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_idle_slope_r__v1 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_132__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_idle_slope_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_idle_slope_r__v1 = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w)) 
                  & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w))) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_130__mbx_place_f = 0x0000ffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_da_gate_r__v1 
                        = (0x0000ffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                          & vlSelfRef.KL_mbx__DOT____VlemCall_130__mbx_place_f));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_da_gate_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_da_gate_r__v1 = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w)) 
                  & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w))) 
                 & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_131__mbx_place_f = 0x0000ffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_licence_r__v1 
                        = (0x0000ffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                          & vlSelfRef.KL_mbx__DOT____VlemCall_131__mbx_place_f));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_licence_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_licence_r__v1 = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w)) 
                  & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w))) 
                 & (0x000cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_133__mbx_place_f = 0x00000fffU;
                vlSelfRef.KL_mbx__DOT____VlemCall_134__mbx_place_f = 0x00070000U;
                vlSelfRef.KL_mbx__DOT____VlemCall_135__mbx_place_f = 0x01000000U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_sr_domain_r__v1 
                        = (0x01ffffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                          & ((vlSelfRef.KL_mbx__DOT____VlemCall_133__mbx_place_f 
                                              | vlSelfRef.KL_mbx__DOT____VlemCall_134__mbx_place_f) 
                                             | vlSelfRef.KL_mbx__DOT____VlemCall_135__mbx_place_f)));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_sr_domain_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sr_domain_r__v1 = 1U;
                }
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
              & (5U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) 
             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v1 
                = vlSymsp->TOP.mbx_avb_chg;
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v1 = 1U;
        } else if (((IData)(vlSymsp->TOP.mbx_avb_chg) 
                    & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[0U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v2 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__avb_cnt_r__v2 = 1U;
        }
    }
    if (((IData)(vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i) 
         & (2U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w)))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0 
            = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0 
            = (0x0000001fU & (VL_MULS_III(32, (IData)(2U), (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w)) 
                              + (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w))));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rb_mem_r__v0 = 1U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__8(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__8\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v0 = 1U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_div_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v0 = 1U;
    } else {
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
              & (6U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) 
             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v1 
                = vlSymsp->TOP.mbx_asp_chg;
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v1 = 1U;
        } else if (((IData)(vlSymsp->TOP.mbx_asp_chg) 
                    & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[0U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v2 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__asp_cnt_r__v2 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
              & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) 
             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v1 
                = vlSymsp->TOP.mbx_amap_wr;
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v1 = 1U;
        } else if (((IData)(vlSymsp->TOP.mbx_amap_wr) 
                    & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[0U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v2 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_evt__DOT__amap_cnt_r__v2 = 1U;
        }
        if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
              | (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w)) 
             & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v5 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[0U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v5 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v5 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[0U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v5 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[0U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v6 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[0U];
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v6 = 1U;
        }
        if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
              | (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w)) 
             & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v6 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[1U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v6 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v7 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[1U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v7 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[1U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v8 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[1U];
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v8 = 1U;
        }
        if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
              | (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w)) 
             & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v7 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[2U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v7 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v9 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[2U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v9 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[2U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v10 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[2U];
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v10 = 1U;
        }
        if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
              | (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w)) 
             & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v8 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[3U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v8 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v11 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[3U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v11 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[3U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v12 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[3U];
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v12 = 1U;
        }
        if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
              | (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w)) 
             & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__wr_head_r__v9 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[4U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__wr_head_r__v9 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v13 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[4U]) 
                                                 + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r))));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v13 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[4U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_r__v14 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r[4U];
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_r__v14 = 1U;
        }
        if ((1U & vlSelfRef.__PVT__KL_mbx__DOT__tick_ctl_r)) {
            if (vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_div_r 
                    = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_p_w)
                        ? 0U : (0x000000ffU & ((IData)(1U) 
                                               + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_div_r))));
            }
        } else {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_div_r = 0U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w)))) {
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0094U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_38__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_value_hi_r__v1 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_38__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_value_hi_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_hi_r__v1 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0090U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_37__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_value_lo_r__v1 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_37__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_value_lo_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_value_lo_r__v1 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_0__mbx_place_f = 1U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_ctrl_r__v1 
                        = (1U & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                 & vlSelfRef.KL_mbx__DOT____VlemCall_0__mbx_place_f));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_ctrl_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_ctrl_r__v1 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0088U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_35__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_record_lo_r__v1 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_35__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_record_lo_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_lo_r__v1 = 1U;
                }
            }
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__9(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__9\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_clock_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_word_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_entity_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_req_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_req_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_req_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_aecp_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_req_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v0 = 1U;
    } else if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
                & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w)))) {
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_3__mbx_place_f = 0x0000ffffU;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_clock_r__v1 
                    = (0x0000ffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                      & vlSelfRef.KL_mbx__DOT____VlemCall_3__mbx_place_f));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_clock_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_clock_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x00c8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_44__mbx_place_f = 0xffffffffU;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_prop_lo_r__v1 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                       & vlSelfRef.KL_mbx__DOT____VlemCall_44__mbx_place_f);
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_prop_lo_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_lo_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x008cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_36__mbx_place_f = 0xffffffffU;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_record_hi_r__v1 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                       & vlSelfRef.KL_mbx__DOT____VlemCall_36__mbx_place_f);
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_record_hi_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_record_hi_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x00ccU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_45__mbx_place_f = 0xffffffffU;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_prop_hi_r__v1 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                       & vlSelfRef.KL_mbx__DOT____VlemCall_45__mbx_place_f);
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_prop_hi_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_prop_hi_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x0044U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_23__mbx_place_f = 0x0000003fU;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_ctr_word_r__v1 
                    = (0x0000003fU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                      & vlSelfRef.KL_mbx__DOT____VlemCall_23__mbx_place_f));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_ctr_word_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_word_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_1__mbx_place_f = 0x0000ffffU;
            vlSelfRef.KL_mbx__DOT____VlemCall_2__mbx_place_f = 0x00ff0000U;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_entity_r__v1 
                    = (0x00ffffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                      & (vlSelfRef.KL_mbx__DOT____VlemCall_1__mbx_place_f 
                                         | vlSelfRef.KL_mbx__DOT____VlemCall_2__mbx_place_f)));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_entity_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_entity_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x00c0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_39__mbx_place_f = 0x0000ffffU;
            vlSelfRef.KL_mbx__DOT____VlemCall_40__mbx_place_f = 0xffff0000U;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_req_r__v1 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                       & (vlSelfRef.KL_mbx__DOT____VlemCall_39__mbx_place_f 
                          | vlSelfRef.KL_mbx__DOT____VlemCall_40__mbx_place_f));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_req_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_req_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x0060U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_24__mbx_place_f = 0x0000ffffU;
            vlSelfRef.KL_mbx__DOT____VlemCall_25__mbx_place_f = 0xffff0000U;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_amap_req_r__v1 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                       & (vlSelfRef.KL_mbx__DOT____VlemCall_24__mbx_place_f 
                          | vlSelfRef.KL_mbx__DOT____VlemCall_25__mbx_place_f));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_amap_req_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_req_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x0080U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_29__mbx_place_f = 0x0000ffffU;
            vlSelfRef.KL_mbx__DOT____VlemCall_30__mbx_place_f = 0xffff0000U;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_req_r__v1 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                       & (vlSelfRef.KL_mbx__DOT____VlemCall_29__mbx_place_f 
                          | vlSelfRef.KL_mbx__DOT____VlemCall_30__mbx_place_f));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_req_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_req_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x000cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_4__mbx_place_f = 1U;
            vlSelfRef.KL_mbx__DOT____VlemCall_5__mbx_place_f = 2U;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_aecp_r__v1 
                    = (3U & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                             & (vlSelfRef.KL_mbx__DOT____VlemCall_4__mbx_place_f 
                                | vlSelfRef.KL_mbx__DOT____VlemCall_5__mbx_place_f)));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_aecp_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_aecp_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x0040U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_21__mbx_place_f = 0x0000ffffU;
            vlSelfRef.KL_mbx__DOT____VlemCall_22__mbx_place_f = 0xffff0000U;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_ctr_req_r__v1 
                    = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                       & (vlSelfRef.KL_mbx__DOT____VlemCall_21__mbx_place_f 
                          | vlSelfRef.KL_mbx__DOT____VlemCall_22__mbx_place_f));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_ctr_req_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_ctr_req_r__v1 = 1U;
            }
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
             & (0x00c4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
            vlSelfRef.KL_mbx__DOT____VlemCall_41__mbx_place_f = 3U;
            vlSelfRef.KL_mbx__DOT____VlemCall_42__mbx_place_f = 0x000000f0U;
            vlSelfRef.KL_mbx__DOT____VlemCall_43__mbx_place_f = 0x0000ff00U;
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__face_gsi_sel_r__v1 
                    = (0x0000ffffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                      & ((vlSelfRef.KL_mbx__DOT____VlemCall_41__mbx_place_f 
                                          | vlSelfRef.KL_mbx__DOT____VlemCall_42__mbx_place_f) 
                                         | vlSelfRef.KL_mbx__DOT____VlemCall_43__mbx_place_f)));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_gsi_sel_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__face_gsi_sel_r__v1 = 1U;
            }
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__10(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__10\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_page_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_beat_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_nvm_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__pub_binding_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_restore_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v0 = 1U;
    } else {
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w)))) {
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0064U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_26__mbx_place_f = 0x0000ffffU;
                vlSelfRef.KL_mbx__DOT____VlemCall_27__mbx_place_f = 0x00030000U;
                vlSelfRef.KL_mbx__DOT____VlemCall_28__mbx_place_f = 0xff000000U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_amap_page_r__v1 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & ((vlSelfRef.KL_mbx__DOT____VlemCall_26__mbx_place_f 
                               | vlSelfRef.KL_mbx__DOT____VlemCall_27__mbx_place_f) 
                              | vlSelfRef.KL_mbx__DOT____VlemCall_28__mbx_place_f));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_amap_page_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_amap_page_r__v1 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0084U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_31__mbx_place_f = 7U;
                vlSelfRef.KL_mbx__DOT____VlemCall_32__mbx_place_f = 0x00000010U;
                vlSelfRef.KL_mbx__DOT____VlemCall_33__mbx_place_f = 0x0000ff00U;
                vlSelfRef.KL_mbx__DOT____VlemCall_34__mbx_place_f = 0xffff0000U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_edit_beat_r__v1 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & (((vlSelfRef.KL_mbx__DOT____VlemCall_31__mbx_place_f 
                                | vlSelfRef.KL_mbx__DOT____VlemCall_32__mbx_place_f) 
                               | vlSelfRef.KL_mbx__DOT____VlemCall_33__mbx_place_f) 
                              | vlSelfRef.KL_mbx__DOT____VlemCall_34__mbx_place_f));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_edit_beat_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_edit_beat_r__v1 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0014U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_14__mbx_place_f = 1U;
                vlSelfRef.KL_mbx__DOT____VlemCall_15__mbx_place_f = 2U;
                vlSelfRef.KL_mbx__DOT____VlemCall_16__mbx_place_f = 4U;
                vlSelfRef.KL_mbx__DOT____VlemCall_17__mbx_place_f = 8U;
                vlSelfRef.KL_mbx__DOT____VlemCall_18__mbx_place_f = 0x00000010U;
                vlSelfRef.KL_mbx__DOT____VlemCall_19__mbx_place_f = 0x00000020U;
                vlSelfRef.KL_mbx__DOT____VlemCall_20__mbx_place_f = 0x00000f00U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_nvm_r__v1 
                        = (0x00000fffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                          & ((((((vlSelfRef.KL_mbx__DOT____VlemCall_14__mbx_place_f 
                                                  | vlSelfRef.KL_mbx__DOT____VlemCall_15__mbx_place_f) 
                                                 | vlSelfRef.KL_mbx__DOT____VlemCall_16__mbx_place_f) 
                                                | vlSelfRef.KL_mbx__DOT____VlemCall_17__mbx_place_f) 
                                               | vlSelfRef.KL_mbx__DOT____VlemCall_18__mbx_place_f) 
                                              | vlSelfRef.KL_mbx__DOT____VlemCall_19__mbx_place_f) 
                                             | vlSelfRef.KL_mbx__DOT____VlemCall_20__mbx_place_f)));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_nvm_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_nvm_r__v1 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x0010U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_6__mbx_place_f = 1U;
                vlSelfRef.KL_mbx__DOT____VlemCall_7__mbx_place_f = 2U;
                vlSelfRef.KL_mbx__DOT____VlemCall_8__mbx_place_f = 4U;
                vlSelfRef.KL_mbx__DOT____VlemCall_9__mbx_place_f = 8U;
                vlSelfRef.KL_mbx__DOT____VlemCall_10__mbx_place_f = 0x00000010U;
                vlSelfRef.KL_mbx__DOT____VlemCall_11__mbx_place_f = 0x00000020U;
                vlSelfRef.KL_mbx__DOT____VlemCall_12__mbx_place_f = 0x00000700U;
                vlSelfRef.KL_mbx__DOT____VlemCall_13__mbx_place_f = 0x00003000U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_restore_r__v1 
                        = (0x00003fffU & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                          & (((((((vlSelfRef.KL_mbx__DOT____VlemCall_6__mbx_place_f 
                                                   | vlSelfRef.KL_mbx__DOT____VlemCall_7__mbx_place_f) 
                                                  | vlSelfRef.KL_mbx__DOT____VlemCall_8__mbx_place_f) 
                                                 | vlSelfRef.KL_mbx__DOT____VlemCall_9__mbx_place_f) 
                                                | vlSelfRef.KL_mbx__DOT____VlemCall_10__mbx_place_f) 
                                               | vlSelfRef.KL_mbx__DOT____VlemCall_11__mbx_place_f) 
                                              | vlSelfRef.KL_mbx__DOT____VlemCall_12__mbx_place_f) 
                                             | vlSelfRef.KL_mbx__DOT____VlemCall_13__mbx_place_f)));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_restore_r__v1 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_restore_r__v1 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_52__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_52__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_k_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_hi_r__v16 = 1U;
                }
            }
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_at_w))) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_137__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_src_sid_lo_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_137__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_src_sid_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_s_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_src_sid_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_lo_r__v16 = 1U;
                }
            }
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_src_w) 
                 & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_138__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_src_sid_hi_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_138__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_src_sid_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_s_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_src_sid_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_src_sid_hi_r__v16 = 1U;
                }
            }
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_139__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_sid_lo_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_139__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_sid_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_k_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_sid_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_lo_r__v16 = 1U;
                }
            }
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w) 
                 & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_140__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_sid_hi_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_140__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_sid_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_k_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_sid_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_sid_hi_r__v16 = 1U;
                }
            }
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_sink_w) 
                 & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_141__mbx_place_f = 1U;
                vlSelfRef.KL_mbx__DOT____VlemCall_142__mbx_place_f = 2U;
                vlSelfRef.KL_mbx__DOT____VlemCall_143__mbx_place_f = 4U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__pub_binding_r__v16 
                        = (7U & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                 & ((vlSelfRef.KL_mbx__DOT____VlemCall_141__mbx_place_f 
                                     | vlSelfRef.KL_mbx__DOT____VlemCall_142__mbx_place_f) 
                                    | vlSelfRef.KL_mbx__DOT____VlemCall_143__mbx_place_f)));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__pub_binding_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_k_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__pub_binding_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__pub_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__pub_binding_r__v16 = 1U;
                }
            }
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__11(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__11\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v0 = 1U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_cnt_r = 0U;
        vlSelfRef.__Vdly__KL_mbx_dma__DOT__pend_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx_dma__DOT__buf_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v0 = 1U;
    } else {
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
              & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w)))) {
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_51__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_51__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_k_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_in_lo_r__v16 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_53__mbx_place_f = 1U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_snk_valid_r__v16 
                        = (1U & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                 & vlSelfRef.KL_mbx__DOT____VlemCall_53__mbx_place_f));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_snk_valid_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_k_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_snk_valid_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_snk_valid_r__v16 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_47__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_47__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_s_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_lo_r__v16 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_48__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_48__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_s_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_fmt_out_hi_r__v16 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_46__mbx_place_f = 0xffffffffU;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_pt_offset_r__v16 
                        = (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                           & vlSelfRef.KL_mbx__DOT____VlemCall_46__mbx_place_f);
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_pt_offset_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_s_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_pt_offset_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_pt_offset_r__v16 = 1U;
                }
            }
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w) 
                  & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
                 & (0x000cU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w)))) {
                vlSelfRef.KL_mbx__DOT____VlemCall_49__mbx_place_f = 1U;
                vlSelfRef.KL_mbx__DOT____VlemCall_50__mbx_place_f = 2U;
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                    vlSelfRef.__VdlyVal__KL_mbx__DOT__face_f_src_valid_r__v16 
                        = (3U & (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                 & (vlSelfRef.KL_mbx__DOT____VlemCall_49__mbx_place_f 
                                    | vlSelfRef.KL_mbx__DOT____VlemCall_50__mbx_place_f)));
                    vlSelfRef.__VdlyDim0__KL_mbx__DOT__face_f_src_valid_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_s_w;
                    vlSelfRef.__VdlyDim1__KL_mbx__DOT__face_f_src_valid_r__v16 
                        = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                    vlSelfRef.__VdlySet__KL_mbx__DOT__face_f_src_valid_r__v16 = 1U;
                }
            }
        }
        if ((1U & vlSelfRef.__PVT__KL_mbx__DOT__tick_ctl_r)) {
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
                 & (3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w)))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_cnt_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_p_w;
            } else if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_p_w) 
                        & (0xffffU != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r)))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_cnt_r 
                    = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r)));
            }
        } else {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__tick_cnt_r = 0U;
        }
        if (((0U != (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
             & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma0))) {
            vlSelfRef.__Vdly__KL_mbx_dma__DOT__pend_r = 1U;
        } else if (((0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
                    & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r))) {
            vlSelfRef.__Vdly__KL_mbx_dma__DOT__pend_r = 0U;
        }
        if (((1U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
             & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r))) {
            vlSelfRef.__VdlyVal__KL_mbx_dma__DOT__buf_r__v16 
                = vlSymsp->TOP.mbx_host_rdata;
            vlSelfRef.__VdlyDim0__KL_mbx_dma__DOT__buf_r__v16 
                = (0x0000000fU & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__count_r));
            vlSelfRef.__VdlySet__KL_mbx_dma__DOT__buf_r__v16 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0104U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v5 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v5 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0124U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v6 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v6 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0144U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v7 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v7 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0164U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v8 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v8 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0184U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__rx_tail_r__v9 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__rx_tail_r__v9 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w) 
              & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v5 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v5 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w) 
              & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v6 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v6 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w) 
              & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v7 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v7 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w) 
              & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v8 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v8 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w) 
              & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[4U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__drop_r__v9 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[4U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__drop_r__v9 = 1U;
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__12(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__12\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v0 = 1U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_busy_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_k_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_b_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_pub_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v0 = 1U;
    } else {
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w) 
              & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v5 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v5 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w) 
              & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v6 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v6 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w) 
              & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v7 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v7 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w) 
              & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v8 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v8 = 1U;
        }
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w) 
              & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
             & (0xffffU != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[4U]))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v9 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[4U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__rate_drop_r__v9 = 1U;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_busy_r) {
            if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_step_w) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_b_r 
                    = (7U & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r)));
                if ((7U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r))) {
                    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_busy_r = 0U;
                    vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r))) 
                           & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r));
                }
            }
        } else if ((1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                          >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_busy_r = 1U;
        } else {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_k_r 
                = ((0x0fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r))
                    ? 0U : (0x0000000fU & ((IData)(1U) 
                                           + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r))));
        }
        if ((((2U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w))
               ? ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                  >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w))
               : vlSelfRef.__PVT__add_devices_ctrlmailboxdma10) 
             & (IData)(vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r 
                = ((IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__owed_r) 
                   | (0x0000ffffU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w))));
            if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_busy_r) 
                 & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w) 
                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cp_b_r = 0U;
            }
        }
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v5 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[0U];
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__head_pub_r__v5 = 1U;
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v6 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[1U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v7 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[2U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v8 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[3U];
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__head_pub_r__v9 
            = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r[4U];
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0108U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v5 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v5 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0128U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v6 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v6 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0148U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v7 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v7 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0168U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v8 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v8 = 1U;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0188U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__tx_head_r__v9 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
            vlSelfRef.__VdlySet__KL_mbx__DOT__tx_head_r__v9 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v5 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v5 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[0U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v6 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v6 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v7 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v7 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[1U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v8 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v8 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v9 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v9 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[2U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v10 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v10 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v11 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v11 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[3U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v12 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v12 = 1U;
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
             & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v13 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[4U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v13 = 1U;
        } else if (vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[4U]) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__pass_r__v14 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[4U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__pass_r__v14 = 1U;
        }
    }
    vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r = 
        ((1U & (~ (IData)(vlSymsp->TOP.sys_reset))) 
         && (((0U == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
              & ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_r) 
                 | (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma0))) 
             | ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r) 
                & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__ack_r)))));
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_en_w) 
         & (3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_ch_w)))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__rxw_data_w;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0 
            = (0x0000007fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_addr_w));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_maap_rx__DOT__mem_r__v0 = 1U;
    }
}

void Vsim_sim___nba_sequent__TOP__sim__13(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__13\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_en_w) 
         & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_ch_w)))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__rxw_data_w;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0 
            = (0x000001ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_addr_w));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_aecp_rx__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_en_w) 
         & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_ch_w)))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__rxw_data_w;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0 
            = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_addr_w));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_acmp_rx__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_en_w) 
         & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_ch_w)))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__rxw_data_w;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0 
            = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_addr_w));
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_adp_rx__DOT__mem_r__v0 = 1U;
    }
    if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_en_w) 
         & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rxw_ch_w)))) {
        vlSelfRef.__VdlyVal__KL_mbx__DOT__u_srp_rx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__rxw_data_w;
        vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_srp_rx__DOT__mem_r__v0 
            = vlSelfRef.__PVT__KL_mbx__DOT__rxw_addr_w;
        vlSelfRef.__VdlySet__KL_mbx__DOT__u_srp_rx__DOT__mem_r__v0 = 1U;
    }
    if (vlSelfRef.__PVT__soc_tx_fifo_do_read) {
        vlSelfRef.__PVT__storage_1_dat1 = vlSelfRef.__PVT__storage_1
            [vlSelfRef.__PVT__soc_tx_fifo_consume];
    }
    if (vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2) {
        vlSelfRef.__PVT__add_devices_mmap_byte_count 
            = vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2;
    }
    if (vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3) {
        vlSelfRef.__PVT__add_devices_mmap_burst_adr 
            = vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value3;
    }
    vlSelfRef.__PVT__mem_dat0 = ((0x30U >= (0x0000003fU 
                                            & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                  ? vlSelfRef.__PVT__mem
                                 [(0x0000003fU & (IData)(vlSelfRef.__PVT__builder_interface1_adr))]
                                  : 0U);
    vlSelfRef.__PVT__flashboundary_cs = vlSelfRef.__PVT__add_devices_crossbar_cs;
    vlSelfRef.__PVT__pending_wr_stb = vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_pending_re;
    if (vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0) {
        vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div 
            = vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0;
    }
    vlSelfRef.__PVT__soc_pending_wr_stb = vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_pending_re;
    if (vlSelfRef.__PVT__soc_data_socbushandler_next_value_ce1) {
        vlSelfRef.__PVT__soc_data = vlSelfRef.__PVT__soc_data_socbushandler_next_value1;
    }
    if (vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0) {
        vlSelfRef.__PVT__soc_last_ar_aw_n = vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0;
    }
    vlSelfRef.__PVT__soc_reset_wr_stb = vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_reset_re;
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_pending_re) {
        vlSelfRef.__PVT__pending_wr_data = (1U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_pending_re) {
        vlSelfRef.__PVT__soc_pending_wr_data = (3U 
                                                & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1) {
        vlSelfRef.__PVT__add_devices_mmap_burst_cs 
            = vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1;
    }
    vlSelfRef.__PVT__builder_csr_bankarray_sel_r = 
        (1U == (0x0000001fU & ((IData)(vlSelfRef.__PVT__builder_interface1_adr) 
                               >> 9U)));
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v0 = 1U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__domain_snap_r__v0 = 1U;
        vlSelfRef.__PVT__flashboundary_cs = 0U;
        vlSelfRef.__PVT__pending_wr_stb = 0U;
        vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div = 0U;
        vlSelfRef.__PVT__soc_pending_wr_stb = 0U;
        vlSelfRef.__PVT__soc_data = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r = 0U;
        vlSelfRef.__PVT__soc_last_ar_aw_n = 0U;
        vlSelfRef.__PVT__soc_reset_wr_stb = 0U;
        vlSelfRef.__PVT__pending_wr_data = 0U;
        vlSelfRef.__PVT__soc_pending_wr_data = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_drop_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__srp_tx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__maap_tx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__aecp_tx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__acmp_tx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__adp_tx_rdata_w = 0U;
        vlSelfRef.__PVT__add_devices_mmap_burst_cs = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__rsel_r = 0U;
        vlSelfRef.__PVT__builder_csr_bankarray_sel_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__maap_rx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__aecp_rx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__acmp_rx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__adp_rx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__srp_rx_rdata_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__evt_rdata_w = 0U;
    } else {
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_q_r) 
             & (0x0040U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)))) {
            vlSelfRef.__VdlyVal__KL_mbx__DOT__gm_hi_snap_r__v1 
                = (IData)((vlSymsp->TOP.mbx_gm_id >> 0x20U));
            vlSelfRef.__VdlySet__KL_mbx__DOT__gm_hi_snap_r__v1 = 1U;
            vlSelfRef.__VdlyVal__KL_mbx__DOT__domain_snap_r__v1 
                = vlSymsp->TOP.mbx_domain;
            vlSelfRef.__VdlySet__KL_mbx__DOT__domain_snap_r__v1 = 1U;
        }
        vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r = vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w;
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__fin_ready_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_drop_r 
                = (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hit_r) 
                    & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w)) 
                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bad_w));
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w) 
             & (4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__srp_tx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_srp_tx__DOT__mem_r
                [(0x000001ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w))];
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w) 
             & (3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__maap_tx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_maap_tx__DOT__mem_r
                [(0x0000007fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w))];
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w) 
             & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__aecp_tx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_aecp_tx__DOT__mem_r
                [(0x000001ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w))];
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w) 
             & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__acmp_tx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_acmp_tx__DOT__mem_r
                [(0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w))];
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_en_w) 
             & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_w)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__adp_tx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_adp_tx__DOT__mem_r
                [(0x0000007fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_addr_w))];
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__evt_host_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__rsel_r = 1U;
            vlSelfRef.__PVT__KL_mbx__DOT__evt_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_evt_ring__DOT__mem_r
                [(0x0000003fU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                   << 2U) - (IData)(0x0400U)) 
                                 >> 2U))];
        } else {
            vlSelfRef.__PVT__KL_mbx__DOT__rsel_r = 
                ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__adp_rx_host_w)
                  ? 2U : ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__acmp_rx_host_w)
                           ? 3U : ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__aecp_rx_host_w)
                                    ? 4U : ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__maap_rx_host_w)
                                             ? 5U : 
                                            ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__srp_rx_host_w)
                                              ? 6U : 0U)))));
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__maap_rx_host_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__maap_rx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_maap_rx__DOT__mem_r
                [(0x0000007fU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                   << 2U) - (IData)(0x3000U)) 
                                 >> 2U))];
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__aecp_rx_host_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__aecp_rx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_aecp_rx__DOT__mem_r
                [(0x000001ffU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                   << 2U) - (IData)(0x2000U)) 
                                 >> 2U))];
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__acmp_rx_host_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__acmp_rx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_acmp_rx__DOT__mem_r
                [(0x000000ffU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                   << 2U) - (IData)(0x1800U)) 
                                 >> 2U))];
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__adp_rx_host_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__adp_rx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_adp_rx__DOT__mem_r
                [(0x000000ffU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                   << 2U) - (IData)(0x1000U)) 
                                 >> 2U))];
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__srp_rx_host_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__srp_rx_rdata_w 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_srp_rx__DOT__mem_r
                [(0x000003ffU & ((((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                                   << 2U) - (IData)(0x4000U)) 
                                 >> 2U))];
        }
    }
    vlSelfRef.__PVT__builder_csr_bankarray_interface2_bank_bus_dat_r = 0U;
    if ((0x1cU == (0x0000001fU & ((IData)(vlSelfRef.__PVT__builder_interface1_adr) 
                                  >> 9U)))) {
        if ((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface2_bank_bus_dat_r 
                = vlSelfRef.__PVT__storage;
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__14(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__14\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_litespi_state = vlSelfRef.__PVT__builder_litespi_next_state;
    vlSelfRef.__PVT__builder_slave_sel_r = vlSelfRef.__PVT__builder_slave_sel;
    vlSelfRef.__PVT__sram_bank0_adr0 = (0x00003fffU 
                                        & vlSelfRef.__PVT__builder_rhs_self0);
    vlSelfRef.__PVT__sram_bank1_adr0 = (0x00001fffU 
                                        & vlSelfRef.__PVT__builder_rhs_self0);
    vlSelfRef.__PVT__sram_bank2_adr0 = (0x000001ffU 
                                        & vlSelfRef.__PVT__builder_rhs_self0);
    vlSelfRef.__PVT__rom_bank0_dat0 = vlSelfRef.__PVT__rom_bank0
        [(0x00007fffU & vlSelfRef.__PVT__builder_rhs_self0)];
    vlSelfRef.__PVT__rom_bank1_dat0 = vlSelfRef.__PVT__rom_bank1
        [(0x000007ffU & vlSelfRef.__PVT__builder_rhs_self0)];
    vlSelfRef.__PVT__builder_wishbone2csr_state = vlSelfRef.__PVT__builder_wishbone2csr_next_state;
    vlSelfRef.__PVT__builder_csr_bankarray_interface0_bank_bus_dat_r = 0U;
    if ((0U == (0x0000001fU & ((IData)(vlSelfRef.__PVT__builder_interface1_adr) 
                               >> 9U)))) {
        if ((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface0_bank_bus_dat_r 
                = vlSelfRef.__PVT__soc_reset_storage;
        } else if ((1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface0_bank_bus_dat_r 
                = vlSelfRef.__PVT__soc_scratch_storage;
        } else if ((2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface0_bank_bus_dat_r 
                = vlSelfRef.__PVT__soc_bus_errors;
        }
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid)) 
               | (IData)(vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready)))) {
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid 
            = vlSelfRef.__PVT__add_devices_master_rxtx_re;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_first = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_last = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_data 
            = vlSelfRef.__PVT__builder_interface1_dat_w;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_len 
            = (0x0000003fU & vlSelfRef.__PVT__add_devices_master_phyconfig_storage);
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_width 
            = (0x0000000fU & (vlSelfRef.__PVT__add_devices_master_phyconfig_storage 
                              >> 8U));
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_mask 
            = (0x000000ffU & (vlSelfRef.__PVT__add_devices_master_phyconfig_storage 
                              >> 0x00000010U));
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_clk_div 
            = vlSelfRef.__PVT__add_devices_master_clk_divisor_storage;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__arrival_ms_r = 0U;
        vlSelfRef.__PVT__builder_litespi_state = 0U;
        vlSelfRef.__PVT__builder_slave_sel_r = 0U;
        vlSelfRef.__PVT__builder_wishbone2csr_state = 0U;
        vlSelfRef.__PVT__KL_mbx_wb__DOT__busy_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_rate_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_acc_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__gm_pend_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__posted_up_r = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_data = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_len = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_width = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_mask = 0U;
        vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_clk_div = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__irq_enable_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__own_eid_lo_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__own_eid_hi_r = 0U;
    } else {
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w) {
            if (vlSymsp->TOP.mbx_rx_last) {
                vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__arrival_ms_r 
                    = vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r;
            }
        }
        if (vlSelfRef.__PVT__add_devices_ctrlmailboxdma0) {
            vlSelfRef.__PVT__KL_mbx_wb__DOT__busy_r = 1U;
        } else if (vlSelfRef.__PVT__add_devices_ctrlmailboxdma5) {
            vlSelfRef.__PVT__KL_mbx_wb__DOT__busy_r = 0U;
        }
        if (vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i) {
            if ((2U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w))) {
                if ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r 
                        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vhi_r) 
                           | (0x0000ffffU & ((IData)(1U) 
                                             << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w))));
                }
                if ((1U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r 
                        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vlo_r) 
                           | (0x0000ffffU & ((IData)(1U) 
                                             << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w))));
                }
            }
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__fin_ready_w) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_rate_r 
                = (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hit_r) 
                      & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w)) 
                     & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bad_w))) 
                    & (0U == ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                               ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r
                              [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                               : 0U))) & ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)) 
                                          && vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r
                                          [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]));
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_acc_r 
                = ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hit_r) 
                     & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rule_pass_w)) 
                    & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bad_w))) 
                   & ((0U != ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                               ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r
                              [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                               : 0U)) | (~ ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)) 
                                            && vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r
                                            [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]))));
        }
        if (vlSymsp->TOP.mbx_gm_change) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__gm_pend_r = 1U;
        } else if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
                     & (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) 
                    & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__gm_pend_r = 0U;
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) {
            if ((0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) {
                if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))) {
                    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__posted_up_r 
                        = (((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))) 
                            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__posted_up_r)) 
                           | (1U & (((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)) 
                                     && (1U & ((IData)(vlSymsp->TOP.mbx_link_up) 
                                               >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)))) 
                                    << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w))));
                }
            }
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x000cU == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__irq_enable_r 
                = (0x800001ffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0020U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__own_eid_lo_r 
                = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0024U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__own_eid_hi_r 
                = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        }
    }
    vlSelfRef.__PVT__builder_csr_bankarray_interface5_bank_bus_dat_r = 0U;
    if ((2U == (0x0000001fU & ((IData)(vlSelfRef.__PVT__builder_interface1_adr) 
                               >> 9U)))) {
        if (((((((((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr))) 
                   | (1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                  | (2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                 | (3U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                | (4U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
               | (5U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
              | (6U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
             | (7U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr))))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface5_bank_bus_dat_r 
                = ((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                    ? (0x000000ffU & (IData)(vlSelfRef.__PVT__storage_2_dat1))
                    : ((1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                        ? (0x10U == (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0))
                        : ((2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                            ? (1U & (~ (IData)(vlSelfRef.__PVT__soc_rx_fifo_readable)))
                            : ((3U == (0x000001ffU 
                                       & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                ? (IData)(vlSelfRef.__PVT__soc_status_status)
                                : ((4U == (0x000001ffU 
                                           & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                    ? (IData)(vlSelfRef.__PVT__soc_pending_status)
                                    : ((5U == (0x000001ffU 
                                               & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                        ? (IData)(vlSelfRef.__PVT__soc_enable_storage)
                                        : ((6U == (0x000001ffU 
                                                   & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                            ? (1U & 
                                               (~ (IData)(vlSelfRef.__PVT__soc_tx_fifo_readable)))
                                            : (1U & 
                                               (~ (IData)(vlSymsp->TOP.serial_sink_ready))))))))));
        }
    }
}

void Vsim_sim___nba_sequent__TOP__sim__15(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__15\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vfunc_mbx_field_f__55__word;
    __Vfunc_mbx_field_f__55__word = 0;
    IData/*31:0*/ __Vfunc_mbx_field_f__127__word;
    __Vfunc_mbx_field_f__127__word = 0;
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrd_r 
        = ((1U & (~ (IData)(vlSymsp->TOP.sys_reset))) 
           && ((IData)(vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_req_i) 
               & (~ (IData)(vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i))));
    vlSelfRef.__PVT__builder_csr_bankarray_interface3_bank_bus_dat_r = 0U;
    if ((3U == (0x0000001fU & ((IData)(vlSelfRef.__PVT__builder_interface1_adr) 
                               >> 9U)))) {
        if (((((((((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr))) 
                   | (1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                  | (2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                 | (3U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
                | (4U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
               | (5U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
              | (6U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) 
             | (7U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr))))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface3_bank_bus_dat_r 
                = ((0U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                    ? (IData)(vlSelfRef.__PVT__flashboundary_clk_divisor_storage)
                    : ((1U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                        ? (IData)(vlSelfRef.__PVT__flashboundary_mode_storage)
                        : ((2U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                            ? (IData)(vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage)
                            : ((3U == (0x000001ffU 
                                       & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                ? (IData)(vlSelfRef.__PVT__add_devices_mmap_dummy_bits_storage)
                                : ((4U == (0x000001ffU 
                                           & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                    ? (IData)(vlSelfRef.__PVT__add_devices_master_cs_storage)
                                    : ((5U == (0x000001ffU 
                                               & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                        ? vlSelfRef.__PVT__add_devices_master_phyconfig_storage
                                        : ((6U == (0x000001ffU 
                                                   & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))
                                            ? vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_payload_data
                                            : (IData)(vlSelfRef.__PVT__add_devices_master_status_status))))))));
        } else if ((8U == (0x000001ffU & (IData)(vlSelfRef.__PVT__builder_interface1_adr)))) {
            vlSelfRef.__PVT__builder_csr_bankarray_interface3_bank_bus_dat_r 
                = vlSelfRef.__PVT__add_devices_master_clk_divisor_storage;
        }
    }
    if ((1U & ((~ (IData)(vlSymsp->TOP.flash_tx_ready)) 
               & (~ (IData)(vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid))))) {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_valid 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_data 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_data;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_len 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_len;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_width 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_width;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__KL_mbx__DOT__evt_tail_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__maap_base_lo_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__maap_base_hi_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__err_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrhi_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__scan_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_wdata_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_be_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_we_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrk_r = 0U;
        vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_addr_r = 0U;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_valid = 0U;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_data = 0U;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_len = 0U;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_width = 0U;
        vlSelfRef.__Vdly__KL_mbx__DOT__ctr_busy_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_done_r = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__ctr_tmo_r = 0U;
        vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_tag_r__v0 = 1U;
    } else {
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0064U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__evt_tail_r 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0034U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__maap_count_r 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x002cU == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__maap_base_lo_r 
                = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
             & (0x0030U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__maap_base_hi_r 
                = (0x0000ffffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
        }
        if (((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w) 
                 | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_w) 
                    | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w))) 
                | (7U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__st_r))) 
               | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__tmr_bad_p_w)) 
              | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__refused_w)) 
             | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w))) {
            vlSelfRef.__PVT__KL_mbx__DOT__err_r = 1U;
        } else {
            __Vfunc_mbx_field_f__127__word = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
            vlSelfRef.KL_mbx__DOT____VlemCall_127__mbx_field_f 
                = (__Vfunc_mbx_field_f__127__word >> 0x0000001fU);
            if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                  & (8U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                            << 2U))) & (0U != vlSelfRef.KL_mbx__DOT____VlemCall_127__mbx_field_f))) {
                vlSelfRef.__PVT__KL_mbx__DOT__err_r = 0U;
            }
        }
        if (((IData)(vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_req_i) 
             & (~ (IData)(vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__bnd_we_i)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrhi_r 
                = (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__bnd_reg_w));
            vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrk_r 
                = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hk_w;
        }
        vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__scan_r 
            = ((0x0fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r))
                ? 0U : (0x0000000fU & ((IData)(1U) 
                                       + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r))));
        if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__armed_r) 
              >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r)) 
             & VL_LTES_III(32, 0U, (vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r 
                                    - vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__dl_r
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r])))) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r))) 
                   & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r));
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r 
                = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                   | (0x0000ffffU & ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__scan_r))));
        }
        if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
             & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w)))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w))) 
                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r));
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__cmd_ok_w) {
            vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r 
                = (((~ ((IData)(1U) << (0x0000000fU 
                                        & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10))) 
                    & (IData)(vlSelfRef.__Vdly__KL_mbx__DOT__u_evt__DOT__armed_r)) 
                   | (0x0000ffffU & ((1U == (vlSelfRef.__PVT__add_devices_ctrlmailboxdma10 
                                             >> 0x0000001eU)) 
                                     << (0x0000000fU 
                                         & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10))));
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r 
                = ((~ ((IData)(1U) << (0x0000000fU 
                                       & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10))) 
                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r));
        }
        if (((0U != (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)) 
             & (IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma0))) {
            vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_wdata_r 
                = vlSelfRef.__PVT__builder_rhs_self1;
            vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_be_r 
                = vlSelfRef.__PVT__builder_rhs_self2;
            vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_we_r 
                = vlSelfRef.__PVT__builder_rhs_self5;
            vlSelfRef.__PVT__KL_mbx_dma__DOT__pend_addr_r 
                = (0x00001fffU & vlSelfRef.__PVT__builder_rhs_self0);
        }
        if (vlSelfRef.__PVT__KL_mbx__DOT__ctr_busy_r) {
            if ((0x00000040U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__ctr_wait_r[0U]))) {
                vlSelfRef.__Vdly__KL_mbx__DOT__ctr_busy_r = 0U;
                vlSelfRef.__PVT__KL_mbx__DOT__ctr_tmo_r = 1U;
            }
            vlSelfRef.__VdlyVal__KL_mbx__DOT__ctr_wait_r__v1 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_wait_r[0U])));
            vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_wait_r__v1 = 1U;
        }
        __Vfunc_mbx_field_f__55__word = vlSelfRef.__PVT__add_devices_ctrlmailboxdma10;
        vlSelfRef.KL_mbx__DOT____VlemCall_55__mbx_field_f 
            = (1U & __Vfunc_mbx_field_f__55__word);
        if (((((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                 & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_refused_w))) 
                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_at_w)) 
               & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_area_w))) 
              & (0x0048U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_reg_w))) 
             & (0U != vlSelfRef.KL_mbx__DOT____VlemCall_55__mbx_field_f))) {
            if ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) {
                vlSelfRef.__VdlyVal__KL_mbx__DOT__ctr_tag_r__v1 
                    = (0x0000000fU & ((IData)(1U) + 
                                      ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))
                                        ? vlSelfRef.__PVT__KL_mbx__DOT__ctr_tag_r
                                       [vlSelfRef.__PVT__KL_mbx__DOT__face_if_w]
                                        : 0U)));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__ctr_tag_r__v1 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_tag_r__v1 = 1U;
                vlSelfRef.__Vdly__KL_mbx__DOT__ctr_busy_r 
                    = ((IData)(vlSelfRef.__Vdly__KL_mbx__DOT__ctr_busy_r) 
                       | (1U & ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))));
                vlSelfRef.__PVT__KL_mbx__DOT__ctr_done_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_done_r));
                vlSelfRef.__PVT__KL_mbx__DOT__ctr_tmo_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__face_if_w))) 
                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_tmo_r));
                vlSelfRef.__VdlyDim0__KL_mbx__DOT__ctr_wait_r__v2 
                    = vlSelfRef.__PVT__KL_mbx__DOT__face_if_w;
                vlSelfRef.__VdlySet__KL_mbx__DOT__ctr_wait_r__v2 = 1U;
            }
        }
    }
}

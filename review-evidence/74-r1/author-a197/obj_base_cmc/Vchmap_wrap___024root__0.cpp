// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vchmap_wrap.h for the primary calling header

#include "Vchmap_wrap__pch.h"

void Vchmap_wrap___024root___eval_triggers_vec__ico(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_triggers_vec__ico\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = (((QData)((IData)(
                                                      (((((IData)(vlSelfRef.b_tready_i) 
                                                          != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_tready_i__0)) 
                                                         << 0x00000012U) 
                                                        | ((((IData)(vlSelfRef.b_tctx_rd_addr_i) 
                                                             != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_rd_addr_i__0)) 
                                                            << 0x00000011U) 
                                                           | (((IData)(vlSelfRef.b_tctx_rd_en_i) 
                                                               != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_rd_en_i__0)) 
                                                              << 0x00000010U))) 
                                                       | (((((((vlSelfRef.b_tctx_wr_data_i 
                                                                != vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_wr_data_i__0) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.b_tctx_wr_addr_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_wr_addr_i__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.b_tctx_wr_en_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_wr_en_i__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.b_en_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_en_i__0)))) 
                                                            << 0x0000000cU) 
                                                           | ((((((IData)(vlSelfRef.b_tick_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_tick_i__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.b_map_rd_addr_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_map_rd_addr_i__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.b_map_rd_en_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_map_rd_en_i__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.b_map_wr_data_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_map_wr_data_i__0)))) 
                                                              << 8U)) 
                                                          | (((((((IData)(vlSelfRef.b_map_wr_addr_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_map_wr_addr_i__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.b_map_wr_en_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_map_wr_en_i__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.a_tready_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_tready_i__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.a_tctx_rd_addr_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_rd_addr_i__0)))) 
                                                              << 4U) 
                                                             | (((((IData)(vlSelfRef.a_tctx_rd_en_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_rd_en_i__0)) 
                                                                  << 3U) 
                                                                 | ((vlSelfRef.a_tctx_wr_data_i 
                                                                     != vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_wr_data_i__0) 
                                                                    << 2U)) 
                                                                | ((((IData)(vlSelfRef.a_tctx_wr_addr_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_wr_addr_i__0)) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.a_tctx_wr_en_i) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_wr_en_i__0))))))))) 
                                      << 0x00000020U) 
                                     | (QData)((IData)(
                                                       ((((((((((IData)(vlSelfRef.a_en_i) 
                                                                != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_en_i__0)) 
                                                               << 3U) 
                                                              | (((IData)(vlSelfRef.a_tick_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_tick_i__0)) 
                                                                 << 2U)) 
                                                             | ((((IData)(vlSelfRef.a_map_rd_addr_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_map_rd_addr_i__0)) 
                                                                 << 1U) 
                                                                | ((IData)(vlSelfRef.a_map_rd_en_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_map_rd_en_i__0)))) 
                                                            << 0x0000000cU) 
                                                           | ((((((IData)(vlSelfRef.a_map_wr_data_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_map_wr_data_i__0)) 
                                                                 << 3U) 
                                                                | (((IData)(vlSelfRef.a_map_wr_addr_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_map_wr_addr_i__0)) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.a_map_wr_en_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_map_wr_en_i__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.b_lb_flush_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__b_lb_flush_i__0)))) 
                                                              << 8U)) 
                                                          | (((((((IData)(vlSelfRef.a_lb_flush_i) 
                                                                  != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__a_lb_flush_i__0)) 
                                                                 << 3U) 
                                                                | ((vlSelfRef.lb_wire_chans_i 
                                                                    != vlSelfRef.__Vtrigprevexpr___TOP__lb_wire_chans_i__0) 
                                                                   << 2U)) 
                                                               | ((((IData)(vlSelfRef.lb_tuser_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__lb_tuser_i__0)) 
                                                                   << 1U) 
                                                                  | ((IData)(vlSelfRef.lb_tlast_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__lb_tlast_i__0)))) 
                                                              << 4U) 
                                                             | (((((IData)(vlSelfRef.lb_tvalid_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__lb_tvalid_i__0)) 
                                                                  << 3U) 
                                                                 | ((vlSelfRef.lb_tdata_i 
                                                                     != vlSelfRef.__Vtrigprevexpr___TOP__lb_tdata_i__0) 
                                                                    << 2U)) 
                                                                | (((vlSelfRef.tone_smp_i 
                                                                     != vlSelfRef.__Vtrigprevexpr___TOP__tone_smp_i__0) 
                                                                    << 1U) 
                                                                   | (vlSelfRef.tdm_r_i 
                                                                      != vlSelfRef.__Vtrigprevexpr___TOP__tdm_r_i__0))))) 
                                                         << 0x00000010U) 
                                                        | (((((((vlSelfRef.tdm_l_i 
                                                                 != vlSelfRef.__Vtrigprevexpr___TOP__tdm_l_i__0) 
                                                                << 3U) 
                                                               | (((IData)(vlSelfRef.tdm_pair_slot_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_pair_slot_i__0)) 
                                                                  << 2U)) 
                                                              | ((((IData)(vlSelfRef.tdm_pair_valid_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tdm_pair_valid_i__0)) 
                                                                  << 1U) 
                                                                 | (vlSelfRef.i2s_r_i 
                                                                    != vlSelfRef.__Vtrigprevexpr___TOP__i2s_r_i__0))) 
                                                             << 0x0000000cU) 
                                                            | (((((vlSelfRef.i2s_l_i 
                                                                   != vlSelfRef.__Vtrigprevexpr___TOP__i2s_l_i__0) 
                                                                  << 3U) 
                                                                 | (((IData)(vlSelfRef.i2s_pair_valid_i) 
                                                                     != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__i2s_pair_valid_i__0)) 
                                                                    << 2U)) 
                                                                | (((vlSelfRef.ptp_ns_i 
                                                                     != vlSelfRef.__Vtrigprevexpr___TOP__ptp_ns_i__0) 
                                                                    << 1U) 
                                                                   | (vlSelfRef.transit_ns_i 
                                                                      != vlSelfRef.__Vtrigprevexpr___TOP__transit_ns_i__0))) 
                                                               << 8U)) 
                                                           | (((((((IData)(vlSelfRef.vlan_vid_i) 
                                                                   != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__vlan_vid_i__0)) 
                                                                  << 3U) 
                                                                 | ((vlSelfRef.station_mac_i 
                                                                     != vlSelfRef.__Vtrigprevexpr___TOP__station_mac_i__0) 
                                                                    << 2U)) 
                                                                | (((vlSelfRef.dest_mac_i 
                                                                     != vlSelfRef.__Vtrigprevexpr___TOP__dest_mac_i__0) 
                                                                    << 1U) 
                                                                   | ((IData)(vlSelfRef.tg_tick_i) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tg_tick_i__0)))) 
                                                               << 4U) 
                                                              | (((((IData)(vlSelfRef.tg_en_i) 
                                                                    != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__tg_en_i__0)) 
                                                                   << 3U) 
                                                                  | (((IData)(vlSelfRef.clk_audio) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_audio__0)) 
                                                                     << 2U)) 
                                                                 | ((((IData)(vlSelfRef.rst_n) 
                                                                      != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0)) 
                                                                     << 1U) 
                                                                    | ((IData)(vlSelfRef.clk) 
                                                                       != (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0))))))))));
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__clk_audio__0 = vlSelfRef.clk_audio;
    vlSelfRef.__Vtrigprevexpr___TOP__tg_en_i__0 = vlSelfRef.tg_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tg_tick_i__0 = vlSelfRef.tg_tick_i;
    vlSelfRef.__Vtrigprevexpr___TOP__dest_mac_i__0 
        = vlSelfRef.dest_mac_i;
    vlSelfRef.__Vtrigprevexpr___TOP__station_mac_i__0 
        = vlSelfRef.station_mac_i;
    vlSelfRef.__Vtrigprevexpr___TOP__vlan_vid_i__0 
        = vlSelfRef.vlan_vid_i;
    vlSelfRef.__Vtrigprevexpr___TOP__transit_ns_i__0 
        = vlSelfRef.transit_ns_i;
    vlSelfRef.__Vtrigprevexpr___TOP__ptp_ns_i__0 = vlSelfRef.ptp_ns_i;
    vlSelfRef.__Vtrigprevexpr___TOP__i2s_pair_valid_i__0 
        = vlSelfRef.i2s_pair_valid_i;
    vlSelfRef.__Vtrigprevexpr___TOP__i2s_l_i__0 = vlSelfRef.i2s_l_i;
    vlSelfRef.__Vtrigprevexpr___TOP__i2s_r_i__0 = vlSelfRef.i2s_r_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tdm_pair_valid_i__0 
        = vlSelfRef.tdm_pair_valid_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tdm_pair_slot_i__0 
        = vlSelfRef.tdm_pair_slot_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tdm_l_i__0 = vlSelfRef.tdm_l_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tdm_r_i__0 = vlSelfRef.tdm_r_i;
    vlSelfRef.__Vtrigprevexpr___TOP__tone_smp_i__0 
        = vlSelfRef.tone_smp_i;
    vlSelfRef.__Vtrigprevexpr___TOP__lb_tdata_i__0 
        = vlSelfRef.lb_tdata_i;
    vlSelfRef.__Vtrigprevexpr___TOP__lb_tvalid_i__0 
        = vlSelfRef.lb_tvalid_i;
    vlSelfRef.__Vtrigprevexpr___TOP__lb_tlast_i__0 
        = vlSelfRef.lb_tlast_i;
    vlSelfRef.__Vtrigprevexpr___TOP__lb_tuser_i__0 
        = vlSelfRef.lb_tuser_i;
    vlSelfRef.__Vtrigprevexpr___TOP__lb_wire_chans_i__0 
        = vlSelfRef.lb_wire_chans_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_lb_flush_i__0 
        = vlSelfRef.a_lb_flush_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_lb_flush_i__0 
        = vlSelfRef.b_lb_flush_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_map_wr_en_i__0 
        = vlSelfRef.a_map_wr_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_map_wr_addr_i__0 
        = vlSelfRef.a_map_wr_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_map_wr_data_i__0 
        = vlSelfRef.a_map_wr_data_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_map_rd_en_i__0 
        = vlSelfRef.a_map_rd_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_map_rd_addr_i__0 
        = vlSelfRef.a_map_rd_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_tick_i__0 = vlSelfRef.a_tick_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_en_i__0 = vlSelfRef.a_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_wr_en_i__0 
        = vlSelfRef.a_tctx_wr_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_wr_addr_i__0 
        = vlSelfRef.a_tctx_wr_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_wr_data_i__0 
        = vlSelfRef.a_tctx_wr_data_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_rd_en_i__0 
        = vlSelfRef.a_tctx_rd_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_tctx_rd_addr_i__0 
        = vlSelfRef.a_tctx_rd_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__a_tready_i__0 
        = vlSelfRef.a_tready_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_map_wr_en_i__0 
        = vlSelfRef.b_map_wr_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_map_wr_addr_i__0 
        = vlSelfRef.b_map_wr_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_map_wr_data_i__0 
        = vlSelfRef.b_map_wr_data_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_map_rd_en_i__0 
        = vlSelfRef.b_map_rd_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_map_rd_addr_i__0 
        = vlSelfRef.b_map_rd_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_tick_i__0 = vlSelfRef.b_tick_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_en_i__0 = vlSelfRef.b_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_wr_en_i__0 
        = vlSelfRef.b_tctx_wr_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_wr_addr_i__0 
        = vlSelfRef.b_tctx_wr_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_wr_data_i__0 
        = vlSelfRef.b_tctx_wr_data_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_rd_en_i__0 
        = vlSelfRef.b_tctx_rd_en_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_tctx_rd_addr_i__0 
        = vlSelfRef.b_tctx_rd_addr_i;
    vlSelfRef.__Vtrigprevexpr___TOP__b_tready_i__0 
        = vlSelfRef.b_tready_i;
    if (VL_UNLIKELY(((1U & (~ (IData)(vlSelfRef.__VicoDidInit)))))) {
        vlSelfRef.__VicoDidInit = 1U;
        vlSelfRef.__VicoTriggered[0U] = (1ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (2ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (4ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (8ULL | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000010ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000020ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000040ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000080ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000100ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000200ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000400ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000000800ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000001000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000002000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000004000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000008000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000010000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000020000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000040000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000080000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000100000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000200000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000400000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000000800000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000001000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000002000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000004000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000008000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000010000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000020000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000040000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000080000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000100000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000200000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000400000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000000800000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000001000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000002000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000004000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000008000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000010000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000020000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000040000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000080000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000100000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000200000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000400000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0000800000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0001000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0002000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
        vlSelfRef.__VicoTriggered[0U] = (0x0004000000000000ULL 
                                         | vlSelfRef.__VicoTriggered[0U]);
    }
}

bool Vchmap_wrap___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___trigger_anySet__ico\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((2U > n));
    return (0U);
}

void Vchmap_wrap___024root___ico_comb__TOP__4(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___ico_comb__TOP__4\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k;
    chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0;
    IData/*31:0*/ chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k;
    chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0;
    // Body
    chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0U;
    while ((0x000000f0U > chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)) {
        if (VL_LIKELY(((0xefU >= (0x000000ffU & chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k))))) {
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[(0x000000ffU 
                                                         & chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)] = 0U;
        }
        chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k 
            = ((IData)(1U) + chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k);
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[0U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[1U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[2U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[3U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[4U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[5U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.station_mac_i));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[12U] = 0x81U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[13U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[14U] 
        = (0x00000060U | (0x0000000fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w) 
                                         >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[15U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[16U] = 0x22U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[17U] = 0xf0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[18U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[19U] 
        = (0x00000081U | ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__emr_r) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[20U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eseq_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[21U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__etu_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[22U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000038U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[23U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000030U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[24U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[25U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[26U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[27U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[28U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[29U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[30U] 
        = (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r 
           >> 0x00000018U);
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[31U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r 
                          >> 0x00000010U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[32U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r 
                          >> 8U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[33U] 
        = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r);
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[34U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[35U] = 0x50U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[36U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r
        [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r];
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[37U] = 0x20U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[38U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[39U] 
        = (0x000000f8U & (((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[40U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[41U] = 0U;
    if ((0U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[42U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[43U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[44U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[45U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[46U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[47U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[48U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[49U] = 0U;
    }
    if ((1U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[50U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[51U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[52U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[53U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[54U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[55U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[56U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[57U] = 0U;
    }
    if ((2U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[58U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[59U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[60U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[61U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[62U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[63U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[64U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[65U] = 0U;
    }
    if ((3U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[66U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[67U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[68U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[69U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[70U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[71U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[72U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[73U] = 0U;
    }
    if ((4U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[74U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[75U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[76U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[77U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[78U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[79U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[80U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[81U] = 0U;
    }
    if ((5U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[82U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[83U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[84U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[85U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[86U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[87U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[88U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[89U] = 0U;
    }
    if ((6U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[90U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[91U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[92U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[93U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[94U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[95U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[96U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[97U] = 0U;
    }
    if ((7U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[98U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[99U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[100U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[101U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[102U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[103U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[104U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[105U] = 0U;
    }
    if ((8U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[106U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[107U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[108U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[109U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[110U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[111U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[112U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[113U] = 0U;
    }
    if ((9U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[114U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[115U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[116U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[117U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[118U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[119U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[120U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[121U] = 0U;
    }
    if ((0x0aU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[122U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[123U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[124U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[125U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[126U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[127U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[128U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[129U] = 0U;
    }
    if ((0x0bU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[130U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[131U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[132U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[133U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[134U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[135U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[136U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[137U] = 0U;
    }
    if ((0x0cU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[138U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[139U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[140U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[141U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[142U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[143U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[144U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[145U] = 0U;
    }
    if ((0x0dU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[146U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[147U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[148U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[149U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[150U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[151U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[152U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[153U] = 0U;
    }
    if ((0x0eU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[154U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[155U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[156U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[157U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[158U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[159U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[160U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[161U] = 0U;
    }
    if ((0x0fU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[162U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[163U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[164U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[165U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[166U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[167U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[168U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[169U] = 0U;
    }
    if ((0x10U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[170U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[171U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[172U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[173U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[174U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[175U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[176U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[177U] = 0U;
    }
    if ((0x11U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[178U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[179U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[180U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[181U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[182U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[183U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[184U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[185U] = 0U;
    }
    if ((0x12U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[186U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[187U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[188U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[189U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[190U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[191U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[192U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[193U] = 0U;
    }
    if ((0x13U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[194U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[195U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[196U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[197U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[198U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[199U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[200U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[201U] = 0U;
    }
    if ((0x14U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[202U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[203U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[204U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[205U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[206U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[207U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[208U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[209U] = 0U;
    }
    if ((0x15U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[210U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[211U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[212U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[213U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[214U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[215U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[216U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[217U] = 0U;
    }
    if ((0x16U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[218U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[219U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[220U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[221U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[222U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[223U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[224U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[225U] = 0U;
    }
    if ((0x17U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[226U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[227U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[228U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[229U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[230U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[231U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[232U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[233U] = 0U;
    }
    chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0U;
    while ((0x000000f0U > chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)) {
        if (VL_LIKELY(((0xefU >= (0x000000ffU & chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k))))) {
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[(0x000000ffU 
                                                         & chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)] = 0U;
        }
        chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k 
            = ((IData)(1U) + chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k);
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[0U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[1U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[2U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[3U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[4U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[5U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.station_mac_i));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[12U] = 0x81U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[13U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[14U] 
        = (0x00000060U | (0x0000000fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w) 
                                         >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[15U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[16U] = 0x22U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[17U] = 0xf0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[18U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[19U] 
        = (0x00000081U | ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__emr_r) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[20U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eseq_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[21U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__etu_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[22U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000038U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[23U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000030U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[24U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[25U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[26U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[27U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[28U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[29U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[30U] 
        = (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r 
           >> 0x00000018U);
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[31U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r 
                          >> 0x00000010U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[32U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r 
                          >> 8U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[33U] 
        = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r);
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[34U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[35U] = 0x50U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[36U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r
        [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r];
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[37U] = 0x20U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[38U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[39U] 
        = (0x000000f8U & (((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[40U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[41U] = 0U;
    if ((0U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[42U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[43U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[44U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[45U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[46U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[47U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[48U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[49U] = 0U;
    }
    if ((1U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[50U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[51U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[52U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[53U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[54U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[55U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[56U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[57U] = 0U;
    }
    if ((2U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[58U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[59U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[60U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[61U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[62U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[63U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[64U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[65U] = 0U;
    }
    if ((3U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[66U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[67U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[68U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[69U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[70U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[71U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[72U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[73U] = 0U;
    }
    if ((4U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[74U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[75U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[76U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[77U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[78U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[79U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[80U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[81U] = 0U;
    }
    if ((5U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[82U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[83U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[84U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[85U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[86U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[87U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[88U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[89U] = 0U;
    }
    if ((6U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[90U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[91U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[92U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[93U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[94U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[95U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[96U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[97U] = 0U;
    }
    if ((7U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[98U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[99U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[100U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[101U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[102U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[103U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[104U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[105U] = 0U;
    }
    if ((8U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[106U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[107U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[108U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[109U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[110U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[111U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[112U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[113U] = 0U;
    }
    if ((9U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[114U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[115U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[116U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[117U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[118U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[119U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[120U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[121U] = 0U;
    }
    if ((0x0aU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[122U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[123U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[124U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[125U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[126U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[127U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[128U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[129U] = 0U;
    }
    if ((0x0bU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[130U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[131U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[132U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[133U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[134U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[135U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[136U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[137U] = 0U;
    }
    if ((0x0cU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[138U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[139U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[140U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[141U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[142U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[143U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[144U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[145U] = 0U;
    }
    if ((0x0dU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[146U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[147U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[148U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[149U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[150U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[151U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[152U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[153U] = 0U;
    }
    if ((0x0eU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[154U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[155U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[156U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[157U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[158U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[159U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[160U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[161U] = 0U;
    }
    if ((0x0fU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[162U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[163U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[164U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[165U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[166U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[167U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[168U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[169U] = 0U;
    }
    if ((0x10U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[170U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[171U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[172U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[173U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[174U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[175U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[176U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[177U] = 0U;
    }
    if ((0x11U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[178U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[179U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[180U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[181U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[182U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[183U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[184U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[185U] = 0U;
    }
    if ((0x12U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[186U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[187U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[188U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[189U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[190U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[191U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[192U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[193U] = 0U;
    }
    if ((0x13U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[194U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[195U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[196U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[197U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[198U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[199U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[200U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[201U] = 0U;
    }
    if ((0x14U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[202U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[203U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[204U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[205U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[206U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[207U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[208U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[209U] = 0U;
    }
    if ((0x15U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[210U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[211U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[212U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[213U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[214U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[215U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[216U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[217U] = 0U;
    }
    if ((0x16U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[218U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[219U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[220U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[221U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[222U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[223U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[224U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[225U] = 0U;
    }
    if ((0x17U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[226U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[227U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[228U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[229U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[230U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[231U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[232U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[233U] = 0U;
    }
    vlSelfRef.b_tdata_o = (((QData)((IData)(((((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                [(0x000000ffU 
                                                  & ((IData)(7U) 
                                                     + 
                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                      << 3U)))] 
                                                & (- (IData)(
                                                             (0xefU 
                                                              >= 
                                                              (0x000000ffU 
                                                               & ((IData)(7U) 
                                                                  + 
                                                                  ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                   << 3U))))))) 
                                               << 0x00000018U) 
                                              | ((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(6U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(6U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 0x00000010U)) 
                                             | (((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(5U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 8U) 
                                                | (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                   [
                                                   (0x000000ffU 
                                                    & ((IData)(4U) 
                                                       + 
                                                       ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                        << 3U)))] 
                                                   & (- (IData)(
                                                                (0xefU 
                                                                 >= 
                                                                 (0x000000ffU 
                                                                  & ((IData)(4U) 
                                                                     + 
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                      << 3U))))))))))) 
                            << 0x00000020U) | (QData)((IData)(
                                                              ((((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                  [
                                                                  (0x000000ffU 
                                                                   & ((IData)(3U) 
                                                                      + 
                                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                       << 3U)))] 
                                                                  & (- (IData)(
                                                                               (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(3U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                 << 0x00000018U) 
                                                                | ((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(2U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(2U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 0x00000010U)) 
                                                               | (((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(1U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(1U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 8U) 
                                                                  | (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                     [
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                      << 3U)] 
                                                                     & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))))));
    vlSelfRef.a_tdata_o = (((QData)((IData)(((((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                [(0x000000ffU 
                                                  & ((IData)(7U) 
                                                     + 
                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                      << 3U)))] 
                                                & (- (IData)(
                                                             (0xefU 
                                                              >= 
                                                              (0x000000ffU 
                                                               & ((IData)(7U) 
                                                                  + 
                                                                  ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                   << 3U))))))) 
                                               << 0x00000018U) 
                                              | ((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(6U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(6U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 0x00000010U)) 
                                             | (((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(5U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 8U) 
                                                | (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                   [
                                                   (0x000000ffU 
                                                    & ((IData)(4U) 
                                                       + 
                                                       ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                        << 3U)))] 
                                                   & (- (IData)(
                                                                (0xefU 
                                                                 >= 
                                                                 (0x000000ffU 
                                                                  & ((IData)(4U) 
                                                                     + 
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                      << 3U))))))))))) 
                            << 0x00000020U) | (QData)((IData)(
                                                              ((((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                  [
                                                                  (0x000000ffU 
                                                                   & ((IData)(3U) 
                                                                      + 
                                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                       << 3U)))] 
                                                                  & (- (IData)(
                                                                               (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(3U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                 << 0x00000018U) 
                                                                | ((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(2U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(2U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 0x00000010U)) 
                                                               | (((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(1U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(1U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 8U) 
                                                                  | (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                     [
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                      << 3U)] 
                                                                     & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))))));
}

void Vchmap_wrap___024root___ico_comb__TOP__6(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___ico_comb__TOP__6\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t = 0;
    // Body
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout 
        = (3U | ((IData)(__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t) 
                 << 4U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
        = __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout;
    if ((4U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (0x0000001fU & (IData)(vlSelfRef.a_tctx_rd_addr_i));
            } else {
                if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w) {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w = 0U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t = 1U;
                } else {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w = 3U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t = 0U;
                }
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w));
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__t) 
                         << 4U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__t) 
                         << 4U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (0x0000001fU & (IData)(vlSelfRef.a_tctx_rd_addr_i));
            } else {
                if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w) {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w = 0U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t = 1U;
                } else {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w = 3U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t = 0U;
                }
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w));
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__w 
                = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__w));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__w 
            = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__w));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__Vfuncout;
    } else {
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w) {
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                = (0x0000001fU & (IData)(vlSelfRef.a_tctx_rd_addr_i));
        } else {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w = 0U;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t = 1U;
            } else {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w = 3U;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t = 0U;
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w));
        }
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr;
    }
}

void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__1(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__1(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__2(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__3(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__4(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__4(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__5(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__6(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__7(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__1(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__2(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__3(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__1(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__4(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__5(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__4(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__6(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__5(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__7(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__8(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__7(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__9(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__8(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__10(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__9(Vchmap_wrap_KL_chan_map_capture* vlSelf);

void Vchmap_wrap___024root___eval_ico(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_ico\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((0x0000000000002000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000006000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__0((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
    }
    if ((0x0000200000000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__0
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
            } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
            } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
            } else if (vlSelfRef.b_tctx_wr_en_i) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
            }
            vlSelfRef.b_tctx_wr_rdy_o = 0U;
            if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r)))) {
                if ((4U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                    if ((5U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                        if (vlSelfRef.b_tctx_wr_en_i) {
                            vlSelfRef.b_tctx_wr_rdy_o = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((0x0000000100000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__1
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
            } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
            } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
            } else if (vlSelfRef.a_tctx_wr_en_i) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
            }
            vlSelfRef.a_tctx_wr_rdy_o = 0U;
            if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r)))) {
                if ((4U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                    if ((5U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                        if (vlSelfRef.a_tctx_wr_en_i) {
                            vlSelfRef.a_tctx_wr_rdy_o = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((0x0000a00000000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__0
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_val_r;
            } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
                    = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eseq_r)));
            } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
                    = ((IData)(1U) + vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r);
            } else if (vlSelfRef.b_tctx_wr_en_i) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
                    = vlSelfRef.b_tctx_wr_data_i;
            }
        }
    }
    if ((0x0000000500000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__1
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_val_r;
            } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
                    = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eseq_r)));
            } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
                    = ((IData)(1U) + vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r);
            } else if (vlSelfRef.a_tctx_wr_en_i) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
                    = vlSelfRef.a_tctx_wr_data_i;
            }
        }
    }
    if ((0x0000100000000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__2
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_we_w 
                = ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_valid_o) 
                   & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w) 
                      & ((~ ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__own_last_w) 
                             & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
                                [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w] 
                                & (5U == vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r
                                   [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w])))) 
                         & ((IData)(vlSelfRef.b_en_i) 
                            >> (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w)))));
        }
    }
    if ((0x0000000080000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__3
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_we_w 
                = ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_valid_o) 
                   & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w) 
                      & ((~ ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__own_last_w) 
                             & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r
                                [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w] 
                                & (5U == vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r
                                   [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w])))) 
                         & ((IData)(vlSelfRef.a_en_i) 
                            >> (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w)))));
        }
    }
    if ((0x0000000000020000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__1((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__1((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000040000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__2((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__2((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000600000000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__2
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_t_r;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout 
                    = (4U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t) 
                             << 4U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
                    = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout;
            } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout 
                    = (3U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t) 
                             << 4U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
                    = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout;
            } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout 
                    = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t) 
                             << 4U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
                    = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout;
            } else if (vlSelfRef.b_tctx_wr_en_i) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
                    = vlSelfRef.b_tctx_wr_addr_i;
            }
        }
    }
    if ((0x0000000300000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__3
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_t_r;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout 
                    = (4U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t) 
                             << 4U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
                    = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout;
            } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout 
                    = (3U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t) 
                             << 4U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
                    = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout;
            } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout 
                    = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t) 
                             << 4U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
                    = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout;
            } else if (vlSelfRef.a_tctx_wr_en_i) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
                    = (0x0000001fU & (IData)(vlSelfRef.a_tctx_wr_addr_i));
            }
        }
    }
    if ((0x0000000000000020ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__4
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                = (0x0000ffffffffffffULL & ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r))
                                             ? vlSelfRef.dest_mac_i
                                             : ((0U 
                                                 != vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r)
                                                 ? vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r
                                                 : 
                                                (vlSelfRef.dest_mac_i 
                                                 + (QData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r))))));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                = (0x0000ffffffffffffULL & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r)
                                             ? ((0U 
                                                 != vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r)
                                                 ? vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r
                                                 : 
                                                (vlSelfRef.dest_mac_i 
                                                 + (QData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r))))
                                             : vlSelfRef.dest_mac_i));
        }
    }
    if ((0x0000000000000080ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__5
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w 
                = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r))
                    ? (IData)(vlSelfRef.vlan_vid_i)
                    : ((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__evid_r))
                        ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__evid_r)
                        : (IData)(vlSelfRef.vlan_vid_i)));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w 
                = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r)
                    ? ((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__evid_r))
                        ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__evid_r)
                        : (IData)(vlSelfRef.vlan_vid_i))
                    : (IData)(vlSelfRef.vlan_vid_i));
        }
    }
    if ((0x0000000000000040ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__6
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                = ((vlSelfRef.station_mac_i << 0x00000010U) 
                   | (QData)((IData)((((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__euid_r))
                                        ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__euid_r)
                                        : (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r)) 
                                      & (- (IData)(
                                                   (0U 
                                                    != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r))))))));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                = ((vlSelfRef.station_mac_i << 0x00000010U) 
                   | (QData)((IData)((((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__euid_r))
                                        ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__euid_r)
                                        : (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r)) 
                                      & (- (IData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r)))))));
        }
    }
    if ((0x0001000000000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__7
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w 
                = ((IData)(vlSelfRef.b_tctx_rd_en_i) 
                   & ((IData)(vlSelfRef.b_tvalid_o) 
                      | ((~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w)) 
                         & (0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r)))));
        }
    }
    if ((0x0000000800000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_sequent__TOP__8
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w 
                = ((IData)(vlSelfRef.a_tctx_rd_en_i) 
                   & ((IData)(vlSelfRef.a_tvalid_o) 
                      | ((~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w)) 
                         & (0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r)))));
        }
    }
    if ((0x0000000000100000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__3((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__3((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000800000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__4((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
    }
    if ((0x0000000001000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_b__4((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000080000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__5((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__5((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000400000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__6((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__6((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000200000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__7((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_sequent__TOP__chmap_wrap__DOT__u_chmap_a__7((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x00000000000000e0ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap___024root___ico_comb__TOP__4(vlSelf);
    }
    if ((0x0003000000000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        {
            // Inlined CFunc: _ico_comb__TOP__5
            CData/*6:0*/ __Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout;
            __Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout = 0;
            CData/*2:0*/ __Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t;
            __Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t = 0;
            __Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
            __Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout 
                = (3U | ((IData)(__Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t) 
                         << 4U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                = __Vinline_0__ico_comb__TOP__5___Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout;
            if ((4U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w) {
                        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                            = vlSelfRef.b_tctx_rd_addr_i;
                    } else {
                        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__w 
                            = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w))
                                ? 3U : 0U);
                        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__t 
                            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
                        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                            = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__t) 
                                << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__w));
                    }
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr;
                } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__t 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__Vfuncout 
                        = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__t) 
                                 << 4U));
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                        = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__Vfuncout;
                } else {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__t 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__Vfuncout 
                        = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__t) 
                                 << 4U));
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                        = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__Vfuncout;
                }
            } else if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w) {
                        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                            = vlSelfRef.b_tctx_rd_addr_i;
                    } else {
                        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__w 
                            = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w))
                                ? 3U : 0U);
                        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__t 
                            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
                        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                            = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__t) 
                                << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__w));
                    }
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr;
                } else {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__w 
                        = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))
                            ? 4U : 3U);
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__t 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__Vfuncout 
                        = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__t) 
                            << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__w));
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                        = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__Vfuncout;
                }
            } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__w 
                    = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))
                        ? 1U : ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))
                                 ? 2U : 3U));
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__Vfuncout 
                    = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__w));
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                    = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__Vfuncout;
            } else {
                if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w) {
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                        = vlSelfRef.b_tctx_rd_addr_i;
                } else {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__w 
                        = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w))
                            ? 3U : 0U);
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__t 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                        = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__t) 
                            << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__w));
                }
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr;
            }
        }
    }
    if ((0x0000001800000000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap___024root___ico_comb__TOP__6(vlSelf);
    }
    if ((0x0000000000a00000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__1((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
    }
    if ((0x0000000000280000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__2((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__2((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000600000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__3((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__1((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000001200000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__1((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000380000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__4((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__4((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000680000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__5((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__4((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000700000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__6((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__5((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000e80000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__7((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
    }
    if ((0x00000000006c0000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__8((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__8((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000001680000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__7((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000780000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__9((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__8((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
    if ((0x0000000000f80000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_a__10((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
    }
    if ((0x0000000001780000ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vchmap_wrap_KL_chan_map_capture___ico_comb__TOP__chmap_wrap__DOT__u_chmap_b__9((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vchmap_wrap___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vchmap_wrap___024root___eval_phase__ico(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_phase__ico\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    Vchmap_wrap___024root___eval_triggers_vec__ico(vlSelf);
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vchmap_wrap___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
    __VicoExecute = Vchmap_wrap___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        Vchmap_wrap___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

bool Vchmap_wrap___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___trigger_anySet__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vchmap_wrap___024root___nba_sequent__TOP__0(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___nba_sequent__TOP__0\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t;
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0;
    IData/*31:0*/ chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k;
    chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0;
    IData/*31:0*/ chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t;
    chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0;
    IData/*31:0*/ chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k;
    chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0;
    CData/*6:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout;
    __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t;
    __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t = 0;
    CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c;
    __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c = 0;
    CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t = 0;
    CData/*3:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_19;
    __VdfgRegularize_h6e95ff9d_0_19 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_28;
    __VdfgRegularize_h6e95ff9d_0_28 = 0;
    QData/*47:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r = 0;
    CData/*0:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r = 0;
    CData/*2:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 0;
    CData/*4:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eiss_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eiss_r = 0;
    CData/*1:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r = 0;
    CData/*4:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ecap_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ecap_r = 0;
    CData/*3:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r = 0;
    CData/*0:0*/ __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r = 0;
    QData/*47:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r = 0;
    CData/*0:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r = 0;
    CData/*2:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 0;
    CData/*4:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eiss_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eiss_r = 0;
    CData/*1:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r = 0;
    CData/*4:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ecap_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ecap_r = 0;
    CData/*3:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r = 0;
    CData/*0:0*/ __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r = 0;
    CData/*5:0*/ __Vdly__chmap_wrap__DOT__u_tone_media__DOT__idx_r;
    __Vdly__chmap_wrap__DOT__u_tone_media__DOT__idx_r = 0;
    IData/*31:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0 = 0;
    CData/*6:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0 = 0;
    QData/*47:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0 = 0;
    SData/*8:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0 = 0;
    CData/*3:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0 = 0;
    CData/*2:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v1 = 0;
    CData/*2:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0 = 0;
    IData/*23:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0 = 0;
    IData/*23:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0 = 0;
    CData/*0:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0 = 0;
    CData/*2:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0 = 0;
    CData/*2:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v0 = 0;
    CData/*2:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v1;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v1 = 0;
    CData/*2:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1;
    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1 = 0;
    CData/*2:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v2;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v2 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v3;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v3 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v4;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v4 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v5;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v5 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v6;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v6 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v7;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v7 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v8;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v8 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v9;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v9 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v1 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v1 = 0;
    IData/*31:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0 = 0;
    QData/*47:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0 = 0;
    CData/*6:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0 = 0;
    CData/*3:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0 = 0;
    CData/*0:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v1 = 0;
    CData/*0:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0 = 0;
    IData/*23:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0 = 0;
    IData/*23:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0 = 0;
    CData/*4:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0 = 0;
    CData/*0:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0;
    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0 = 0;
    CData/*0:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0 = 0;
    CData/*0:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v0;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v0 = 0;
    CData/*0:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v1;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v1 = 0;
    CData/*2:0*/ __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1;
    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1 = 0;
    CData/*0:0*/ __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1;
    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v2;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v2 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v3;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v3 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v1 = 0;
    CData/*0:0*/ __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v1;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v1 = 0;
    VlWide<8>/*255:0*/ __Vtemp_11;
    // Body
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0 = 0U;
    __Vdly__chmap_wrap__DOT__u_tone_media__DOT__idx_r 
        = vlSelfRef.chmap_wrap__DOT__u_tone_media__DOT__idx_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v1 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v1 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0 = 0U;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eiss_r = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eiss_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eo_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ecap_r = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v1 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0 = 0U;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v2 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v3 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0 = 0U;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r;
    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v1 = 0U;
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eiss_r = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eiss_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eo_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ecap_r = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v1 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0 = 0U;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v2 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v3 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v4 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v5 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v6 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v7 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v8 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v9 = 0U;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0 = 0U;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r;
    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v1 = 0U;
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r;
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w) {
        __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w;
        __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w;
        __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0 = 1U;
    }
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w) {
        __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w;
        __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w;
        __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0 = 1U;
    }
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_we_w) {
        __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0 
            = (((QData)((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_l_o)) 
                << 0x00000018U) | (QData)((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_r_o)));
        __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0 
            = (((((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w) 
                  << 1U) | vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r
                 [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w]) 
                << 5U) | (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r
                                   [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w]) 
                           << 2U) | (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w)));
        __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0 = 1U;
    }
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_we_w) {
        __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0 
            = (((QData)((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_l_o)) 
                << 0x00000018U) | (QData)((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_r_o)));
        __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0 
            = (((((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w) 
                  << 1U) | vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__wbank_r
                 [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w]) 
                << 5U) | (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r
                                   [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w]) 
                           << 2U) | (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w)));
        __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0 = 1U;
    }
    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_r
        [(((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r) 
           << 6U) | (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ebank_r) 
                      << 5U) | ((((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__esmp_r) 
                                  << 2U) | (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eo_r)) 
                                & (- (IData)((2U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r)))))))];
    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_r
        [(((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r) 
           << 6U) | (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ebank_r) 
                      << 5U) | ((((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__esmp_r) 
                                  << 2U) | (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eo_r)) 
                                & (- (IData)((2U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r)))))))];
    if (vlSelfRef.rst_n) {
        if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w) 
             & (0U == (0x0000000fU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w))))) {
            __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c 
                = (0x0000000fU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
                                  >> 1U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_1__chn_clamp 
                = ((2U > (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c))
                    ? 2U : ((8U <= (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c))
                             ? 8U : (0x0000000fU & 
                                     ((1U & (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c))
                                       ? ((IData)(1U) 
                                          + (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c))
                                       : (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__chn_clamp__11__c)))));
            __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_1__chn_clamp;
            __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0 
                = (7U & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w) 
                         >> 4U));
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w) 
             & (0U == (0x0000000fU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w))))) {
            __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c 
                = (0x0000000fU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
                                  >> 1U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_1__chn_clamp 
                = ((2U > (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c))
                    ? 2U : ((8U <= (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c))
                             ? 8U : (0x0000000fU & 
                                     ((1U & (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c))
                                       ? ((IData)(1U) 
                                          + (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c))
                                       : (IData)(__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__chn_clamp__23__c)))));
            __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_1__chn_clamp;
            __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0 
                = (1U & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w) 
                         >> 4U));
            __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0 = 1U;
        }
        if (vlSelfRef.tg_en_i) {
            if (vlSelfRef.tg_tick_i) {
                __Vdly__chmap_wrap__DOT__u_tone_media__DOT__idx_r 
                    = ((0x2fU == (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_media__DOT__idx_r))
                        ? 0U : (0x0000003fU & ((IData)(1U) 
                                               + (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_media__DOT__idx_r))));
                vlSelfRef.tone_media_o = ((0x2fU >= (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_media__DOT__idx_r))
                                           ? vlSelfRef.chmap_wrap__DOT__u_tone_media__DOT__TONE_TAB_C
                                          [vlSelfRef.chmap_wrap__DOT__u_tone_media__DOT__idx_r]
                                           : 0U);
            }
        } else {
            __Vdly__chmap_wrap__DOT__u_tone_media__DOT__idx_r = 0U;
            vlSelfRef.tone_media_o = 0U;
        }
        vlSelfRef.b_tctx_rd_valid_o = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r 
            = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w) 
               & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r)));
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r) {
            vlSelfRef.b_tctx_rd_data_o = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r;
            vlSelfRef.b_tctx_rd_valid_o = 1U;
        }
        vlSelfRef.a_tctx_rd_valid_o = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r 
            = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w) 
               & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r)));
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r) {
            vlSelfRef.a_tctx_rd_data_o = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r;
            vlSelfRef.a_tctx_rd_valid_o = 1U;
        }
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r) {
            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r = 0U;
        }
        if ((4U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r)))) {
                    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 0U;
                }
            } else if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r)))) {
                __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                if (vlSelfRef.a_tready_i) {
                    if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                         == (0x0000001fU & ((IData)(5U) 
                                            + ((IData)(6U) 
                                               * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)))))) {
                        __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0 
                            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
                        __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0 = 1U;
                        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 4U;
                    } else {
                        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r)));
                    }
                }
            } else {
                if ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))) {
                    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eseq_r 
                        = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r);
                } else if ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))) {
                    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r;
                }
                if ((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))) {
                    if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eiss_r) 
                         != (0x0000001fU & ((IData)(6U) 
                                            * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
                        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eiss_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eiss_r)));
                        if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eo_r) 
                             == ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20) 
                                 - (IData)(1U)))) {
                            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__esmp_r 
                                = (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__esmp_r)));
                            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r = 0U;
                        } else {
                            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r 
                                = (3U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eo_r)));
                        }
                    }
                    if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r) 
                         != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eiss_r))) {
                        if ((0x17U >= (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r))) {
                            __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0 
                                = (0x00ffffffU & (IData)(
                                                         (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r 
                                                          >> 0x18U)));
                            __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0 
                                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r;
                            __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0 = 1U;
                            __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0 
                                = (0x00ffffffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r));
                            __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0 
                                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r;
                            __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0 = 1U;
                        }
                        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ecap_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r)));
                        if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r) 
                             == (0x0000001fU & (((IData)(6U) 
                                                 * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)) 
                                                - (IData)(1U))))) {
                            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r = 0U;
                            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 3U;
                        }
                    }
                }
                if ((2U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))) {
                    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r)));
                }
            }
        } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__evid_r 
                    = (0x00000fffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r 
                                      >> 5U));
            } else if ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r 
                    = ((0x0000ffff00000000ULL & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r) 
                       | (IData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r)));
            } else {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r 
                    = ((0x00000000ffffffffULL & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r) 
                       | ((QData)((IData)((0x0000ffffU 
                                           & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r))) 
                          << 0x00000020U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__euid_r 
                    = (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r 
                       >> 0x10U);
            }
            if ((2U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))) {
                __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r = 0U;
                __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 2U;
            } else {
                __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r)));
            }
        } else {
            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r = 0U;
            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eiss_r = 0U;
            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ecap_r = 0U;
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__esmp_r = 0U;
            __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w;
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__etu_r = 0U;
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__emr_r = 0U;
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ebank_r 
                    = (1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__wbank_r
                                       [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w])));
                if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w) {
                    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__rr_r = 1U;
                    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 1U;
                } else {
                    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__rr_r = 0U;
                    __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 2U;
                }
            }
        }
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_we_w) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__own_last_w) {
                if ((5U == vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r
                     [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w])) {
                    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0 
                        = (1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__wbank_r
                                           [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w])));
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w;
                    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0 = 1U;
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v0 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w;
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v1 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w;
                } else {
                    __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r
                                                       [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w])));
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w;
                    __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1 = 1U;
                }
            }
            if (((0U == vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r
                  [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w]) 
                 & (0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w)))) {
                __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r = 1U;
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_t_r 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w;
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_val_r 
                    = ((IData)(vlSelfRef.ptp_ns_i) 
                       + (IData)(((((QData)((IData)(vlSelfRef.transit_ns_i)) 
                                    << 0x00000020U) 
                                   | (QData)((IData)(vlSelfRef.transit_ns_i))) 
                                  >> (0x0000003fU & 
                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w) 
                                       << 5U)))));
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.a_en_i)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v2 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.a_en_i) >> 1U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v3 = 1U;
        }
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r) {
            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r = 0U;
        }
        if ((4U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
            if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r)))) {
                    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 0U;
                }
            } else if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r)))) {
                __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
            if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                if (vlSelfRef.b_tready_i) {
                    if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                         == (0x0000001fU & ((IData)(5U) 
                                            + ((IData)(6U) 
                                               * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)))))) {
                        __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0 
                            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
                        __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0 = 1U;
                        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 4U;
                    } else {
                        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r)));
                    }
                }
            } else {
                if ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))) {
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eseq_r 
                        = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r);
                } else if ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))) {
                    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r;
                }
                if ((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))) {
                    if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eiss_r) 
                         != (0x0000001fU & ((IData)(6U) 
                                            * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
                        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eiss_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eiss_r)));
                        if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eo_r) 
                             == ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11) 
                                 - (IData)(1U)))) {
                            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__esmp_r 
                                = (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__esmp_r)));
                            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r = 0U;
                        } else {
                            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r 
                                = (3U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eo_r)));
                        }
                    }
                    if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r) 
                         != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eiss_r))) {
                        if ((0x17U >= (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r))) {
                            __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0 
                                = (0x00ffffffU & (IData)(
                                                         (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r 
                                                          >> 0x18U)));
                            __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0 
                                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r;
                            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0 = 1U;
                            __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0 
                                = (0x00ffffffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r));
                            __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0 
                                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r;
                            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0 = 1U;
                        }
                        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ecap_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r)));
                        if (((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r) 
                             == (0x0000001fU & (((IData)(6U) 
                                                 * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)) 
                                                - (IData)(1U))))) {
                            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r = 0U;
                            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 3U;
                        }
                    }
                }
                if ((2U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))) {
                    __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r 
                        = (0x0000000fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r)));
                }
            }
        } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
            if ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__evid_r 
                    = (0x00000fffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r 
                                      >> 5U));
            } else if ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r 
                    = ((0x0000ffff00000000ULL & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r) 
                       | (IData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r)));
            } else {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r 
                    = ((0x00000000ffffffffULL & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r) 
                       | ((QData)((IData)((0x0000ffffU 
                                           & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r))) 
                          << 0x00000020U));
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__euid_r 
                    = (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r 
                       >> 0x10U);
            }
            if ((2U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))) {
                __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r = 0U;
                __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 2U;
            } else {
                __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r)));
            }
        } else {
            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r = 0U;
            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eiss_r = 0U;
            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ecap_r = 0U;
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__esmp_r = 0U;
            __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r = 0U;
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__etu_r = 0U;
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__emr_r = 0U;
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ebank_r 
                    = (1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r
                                       [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w])));
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
                __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r 
                    = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w))
                        ? 2U : 1U);
            }
        }
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_we_w) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__own_last_w) {
                if ((5U == vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r
                     [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w])) {
                    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0 
                        = (1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r
                                           [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w])));
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w;
                    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0 = 1U;
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v0 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w;
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v1 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w;
                } else {
                    __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r
                                                       [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w])));
                    __VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1 
                        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w;
                    __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1 = 1U;
                }
            }
            if (((0U == vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r
                  [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w]) 
                 & (0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w)))) {
                __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r = 1U;
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_t_r 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w;
                __Vtemp_11[0U] = vlSelfRef.transit_ns_i;
                __Vtemp_11[1U] = vlSelfRef.transit_ns_i;
                __Vtemp_11[2U] = vlSelfRef.transit_ns_i;
                __Vtemp_11[3U] = vlSelfRef.transit_ns_i;
                __Vtemp_11[4U] = vlSelfRef.transit_ns_i;
                __Vtemp_11[5U] = vlSelfRef.transit_ns_i;
                __Vtemp_11[6U] = vlSelfRef.transit_ns_i;
                __Vtemp_11[7U] = vlSelfRef.transit_ns_i;
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_val_r 
                    = ((IData)(vlSelfRef.ptp_ns_i) 
                       + __Vtemp_11[(7U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w))]);
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.b_en_i)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v2 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.b_en_i) >> 1U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v3 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.b_en_i) >> 2U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v4 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.b_en_i) >> 3U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v5 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.b_en_i) >> 4U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v6 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.b_en_i) >> 5U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v7 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.b_en_i) >> 6U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v8 = 1U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.b_en_i) >> 7U)))) {
            __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v9 = 1U;
        }
    } else {
        __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v1 = 1U;
        __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v1 = 1U;
        __Vdly__chmap_wrap__DOT__u_tone_media__DOT__idx_r = 0U;
        vlSelfRef.tone_media_o = 0U;
        vlSelfRef.b_tctx_rd_data_o = 0U;
        vlSelfRef.b_tctx_rd_valid_o = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r = 0U;
        vlSelfRef.a_tctx_rd_data_o = 0U;
        vlSelfRef.a_tctx_rd_valid_o = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eiss_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ecap_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__esmp_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r = 0U;
        __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v1 = 1U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ebank_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__rr_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eseq_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__etu_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__emr_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r = 0ULL;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__euid_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__evid_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_t_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_val_r = 0U;
        __VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v1 = 1U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eiss_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ecap_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__esmp_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r = 0U;
        __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v1 = 1U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ebank_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eseq_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__etu_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__emr_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r = 0ULL;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__euid_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__evid_r = 0U;
        __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_t_r = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_val_r = 0U;
        __VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v1 = 1U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__chans_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[0U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[1U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[2U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[3U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[4U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[5U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[6U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[7U] = 2U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__chans_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r[0U] = 2U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r[1U] = 2U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__stg_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__stg_r__v0;
    }
    vlSelfRef.chmap_wrap__DOT__u_tone_media__DOT__idx_r 
        = __Vdly__chmap_wrap__DOT__u_tone_media__DOT__idx_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[0U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[0U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[0U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[1U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[2U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[3U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[4U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[5U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[7U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[6U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[8U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[7U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r[7U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[0U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[1U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[0U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r[0U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[2U] 
        = (0x0000003fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[1U]) 
                          + (7U & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r[1U] 
                                   >> 1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eiss_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eiss_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eo_r = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__eo_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ecap_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__ecap_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__fph_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_a__DOT__est_r;
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__wbank_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__wbank_r[0U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v0] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v1;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v2) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r[0U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v3) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r[1U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v0] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__wbank_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__pend_r__v1] = 1U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v2) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r[0U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r__v3) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r[1U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__wbank_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[2U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[3U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[4U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[5U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[6U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[7U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[8U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[9U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[10U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[11U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[12U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[13U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[14U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[15U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[16U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[17U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[18U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[19U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[20U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[21U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[22U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[23U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[2U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[3U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[4U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[5U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[6U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[7U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[8U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[9U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[10U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[11U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[12U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[13U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[14U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[15U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[16U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[17U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[18U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[19U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[20U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[21U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[22U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[23U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r[1U] = 0U;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eiss_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eiss_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eo_r = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__eo_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ecap_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__ecap_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__fph_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r 
        = __Vdly__chmap_wrap__DOT__u_pkt_b__DOT__est_r;
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[0U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v0] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v1;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v2) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[0U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v3) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[1U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v4) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[2U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v5) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[3U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v6) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[4U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v7) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[5U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v8) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[6U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r__v0;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v9) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[7U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v0] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__wbank_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__pend_r__v1] = 1U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v2) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[0U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v3) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[1U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v4) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[2U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v5) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[3U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v6) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[4U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v7) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[5U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v8) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[6U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r__v9) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[7U] = 0U;
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r__v1) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[2U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[3U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[4U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[5U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[6U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[7U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[2U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[3U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[4U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[5U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[6U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[7U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[2U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[3U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[4U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[5U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[6U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[7U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[8U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[9U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[10U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[11U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[12U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[13U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[14U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[15U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[16U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[17U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[18U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[19U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[20U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[21U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[22U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[23U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[2U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[3U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[4U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[5U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[6U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[7U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[8U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[9U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[10U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[11U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[12U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[13U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[14U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[15U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[16U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[17U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[18U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[19U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[20U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[21U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[22U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[23U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[0U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[1U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[2U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[3U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[4U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[5U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[6U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r[7U] = 0U;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tctx_r
        [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w];
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 0U;
    vlSelfRef.a_tctx_wr_rdy_o = 0U;
    if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r)))) {
        if ((4U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if ((5U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
                if (vlSelfRef.a_tctx_wr_en_i) {
                    vlSelfRef.a_tctx_wr_rdy_o = 1U;
                }
            }
        }
    }
    vlSelfRef.a_tvalid_o = (3U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w = 0U;
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
            = (0x0000ffffffffffffULL & ((0U != vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r)
                                         ? vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__edmac_r
                                         : (vlSelfRef.dest_mac_i 
                                            + (QData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r)))));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w 
            = ((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__evid_r))
                ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__evid_r)
                : (IData)(vlSelfRef.vlan_vid_i));
    } else {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
            = (0x0000ffffffffffffULL & vlSelfRef.dest_mac_i);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w 
            = vlSelfRef.vlan_vid_i;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
        = ((vlSelfRef.station_mac_i << 0x00000010U) 
           | (QData)((IData)((((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__euid_r))
                                ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__euid_r)
                                : (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r)) 
                              & (- (IData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20 = (7U 
                                                 & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r
                                                    [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r] 
                                                    >> 1U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w = 0U;
    chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (1U & ((IData)(2U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r
        [(1U & chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w 
            = (1U & chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (1U & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r
        [(1U & chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w 
            = (1U & chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tctx_r
        [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w];
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 0U;
    vlSelfRef.b_tctx_wr_rdy_o = 0U;
    if ((1U & (~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r)))) {
        if ((4U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
            if ((5U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
                if (vlSelfRef.b_tctx_wr_en_i) {
                    vlSelfRef.b_tctx_wr_rdy_o = 1U;
                }
            }
        }
    }
    vlSelfRef.b_tvalid_o = (3U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w = 0U;
    if ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
            = (0x0000ffffffffffffULL & vlSelfRef.dest_mac_i);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w 
            = vlSelfRef.vlan_vid_i;
    } else {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
            = (0x0000ffffffffffffULL & ((0U != vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r)
                                         ? vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__edmac_r
                                         : (vlSelfRef.dest_mac_i 
                                            + (QData)((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r)))));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w 
            = ((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__evid_r))
                ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__evid_r)
                : (IData)(vlSelfRef.vlan_vid_i));
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
        = ((vlSelfRef.station_mac_i << 0x00000010U) 
           | (QData)((IData)((((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__euid_r))
                                ? (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__euid_r)
                                : (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r)) 
                              & (- (IData)((0U != (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11 = (7U 
                                                 & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r
                                                    [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r] 
                                                    >> 1U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w = 0U;
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(8U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(7U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(6U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(5U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(4U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(3U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(2U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__rr_r)));
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
        [(7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w 
            = (7U & chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    if (__VdlySet__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tctx_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_a__DOT__tctx_r__v0;
    }
    __VdfgRegularize_h6e95ff9d_0_28 = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                       == (0x0000001fU 
                                           & ((IData)(5U) 
                                              + ((IData)(6U) 
                                                 * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)))));
    chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0U;
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_t_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout 
            = (4U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout;
    } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout 
            = (3U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout;
    } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout 
            = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout;
    } else if (vlSelfRef.a_tctx_wr_en_i) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = (0x0000001fU & (IData)(vlSelfRef.a_tctx_wr_addr_i));
    }
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_t_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout 
            = (4U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout;
    } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout 
            = (3U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout;
    } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout 
            = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout;
    } else if (vlSelfRef.b_tctx_wr_en_i) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.b_tctx_wr_addr_i;
    }
    while ((0x000000f0U > chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)) {
        if (VL_LIKELY(((0xefU >= (0x000000ffU & chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k))))) {
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[(0x000000ffU 
                                                         & chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)] = 0U;
        }
        chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k 
            = ((IData)(1U) + chmap_wrap__DOT__u_pkt_a__DOT__frame_bytes__DOT__unnamedblk5__DOT__k);
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[0U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[1U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[2U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[3U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[4U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[5U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.station_mac_i));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[12U] = 0x81U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[13U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[14U] 
        = (0x00000060U | (0x0000000fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w) 
                                         >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[15U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[16U] = 0x22U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[17U] = 0xf0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[18U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[19U] 
        = (0x00000081U | ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__emr_r) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[20U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eseq_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[21U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__etu_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[22U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000038U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[23U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000030U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[24U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[25U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[26U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[27U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[28U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[29U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[30U] 
        = (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r 
           >> 0x00000018U);
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[31U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r 
                          >> 0x00000010U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[32U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r 
                          >> 8U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[33U] 
        = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ets_r);
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[34U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[35U] = 0x50U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[36U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r
        [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r];
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[37U] = 0x20U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[38U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[39U] 
        = (0x000000f8U & (((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[40U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[41U] = 0U;
    if ((0U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[42U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[43U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[44U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[45U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[46U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[47U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[48U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[49U] = 0U;
    }
    if ((1U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[50U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[51U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[52U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[53U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[54U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[55U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[56U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[57U] = 0U;
    }
    if ((2U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[58U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[59U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[60U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[61U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[62U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[63U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[64U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[65U] = 0U;
    }
    if ((3U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[66U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[67U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[68U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[69U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[70U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[71U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[72U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[73U] = 0U;
    }
    if ((4U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[74U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[75U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[76U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[77U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[78U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[79U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[80U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[81U] = 0U;
    }
    if ((5U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[82U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[83U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[84U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[85U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[86U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[87U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[88U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[89U] = 0U;
    }
    if ((6U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[90U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[91U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[92U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[93U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[94U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[95U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[96U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[97U] = 0U;
    }
    if ((7U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[98U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[99U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[100U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[101U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[102U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[103U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[104U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[105U] = 0U;
    }
    if ((8U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[106U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[107U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[108U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[109U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[110U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[111U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[112U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[113U] = 0U;
    }
    if ((9U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[114U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[115U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[116U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[117U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[118U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[119U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[120U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[121U] = 0U;
    }
    if ((0x0aU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[122U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[123U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[124U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[125U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[126U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[127U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[128U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[129U] = 0U;
    }
    if ((0x0bU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[130U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[131U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[132U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[133U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[134U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[135U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[136U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[137U] = 0U;
    }
    if ((0x0cU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[138U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[139U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[140U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[141U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[142U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[143U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[144U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[145U] = 0U;
    }
    if ((0x0dU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[146U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[147U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[148U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[149U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[150U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[151U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[152U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[153U] = 0U;
    }
    if ((0x0eU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[154U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[155U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[156U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[157U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[158U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[159U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[160U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[161U] = 0U;
    }
    if ((0x0fU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[162U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[163U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[164U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[165U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[166U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[167U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[168U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[169U] = 0U;
    }
    if ((0x10U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[170U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[171U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[172U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[173U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[174U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[175U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[176U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[177U] = 0U;
    }
    if ((0x11U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[178U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[179U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[180U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[181U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[182U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[183U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[184U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[185U] = 0U;
    }
    if ((0x12U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[186U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[187U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[188U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[189U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[190U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[191U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[192U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[193U] = 0U;
    }
    if ((0x13U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[194U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[195U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[196U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[197U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[198U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[199U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[200U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[201U] = 0U;
    }
    if ((0x14U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[202U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[203U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[204U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[205U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[206U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[207U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[208U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[209U] = 0U;
    }
    if ((0x15U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[210U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[211U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[212U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[213U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[214U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[215U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[216U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[217U] = 0U;
    }
    if ((0x16U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[218U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[219U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[220U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[221U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[222U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[223U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[224U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[225U] = 0U;
    }
    if ((0x17U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[226U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[227U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[228U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[229U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[230U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[231U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[232U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb[233U] = 0U;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w 
        = ((IData)(vlSelfRef.a_tctx_rd_en_i) & ((IData)(vlSelfRef.a_tvalid_o) 
                                                | ((~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w)) 
                                                   & (0U 
                                                      == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r)))));
    if (__VdlySet__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tctx_r[__VdlyDim0__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0] 
            = __VdlyVal__chmap_wrap__DOT__u_pkt_b__DOT__tctx_r__v0;
    }
    __VdfgRegularize_h6e95ff9d_0_19 = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                       == (0x0000001fU 
                                           & ((IData)(5U) 
                                              + ((IData)(6U) 
                                                 * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)))));
    chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0U;
    while ((0x000000f0U > chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)) {
        if (VL_LIKELY(((0xefU >= (0x000000ffU & chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k))))) {
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[(0x000000ffU 
                                                         & chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)] = 0U;
        }
        chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k 
            = ((IData)(1U) + chmap_wrap__DOT__u_pkt_b__DOT__frame_bytes__DOT__unnamedblk5__DOT__k);
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[0U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[1U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[2U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[3U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[4U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[5U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.station_mac_i 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.station_mac_i));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[12U] = 0x81U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[13U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[14U] 
        = (0x00000060U | (0x0000000fU & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w) 
                                         >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[15U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[16U] = 0x22U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[17U] = 0xf0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[18U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[19U] 
        = (0x00000081U | ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__emr_r) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[20U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eseq_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[21U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__etu_r;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[22U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000038U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[23U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000030U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[24U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000028U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[25U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000020U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[26U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000018U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[27U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 0x00000010U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[28U] 
        = (0x000000ffU & (IData)((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w 
                                  >> 8U)));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[29U] 
        = (0x000000ffU & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[30U] 
        = (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r 
           >> 0x00000018U);
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[31U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r 
                          >> 0x00000010U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[32U] 
        = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r 
                          >> 8U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[33U] 
        = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ets_r);
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[34U] = 2U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[35U] = 0x50U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[36U] 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r
        [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r];
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[37U] = 0x20U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[38U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[39U] 
        = (0x000000f8U & (((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11)) 
                          << 3U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[40U] = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[41U] = 0U;
    if ((0U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[42U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[43U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[44U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[45U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[46U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[0U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[47U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[0U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[48U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[0U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[49U] = 0U;
    }
    if ((1U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[50U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[51U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[52U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[53U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[54U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[1U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[55U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[1U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[56U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[1U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[57U] = 0U;
    }
    if ((2U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[58U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[59U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[60U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[61U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[62U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[2U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[63U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[2U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[64U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[2U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[65U] = 0U;
    }
    if ((3U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[66U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[67U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[68U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[69U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[70U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[3U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[71U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[3U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[72U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[3U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[73U] = 0U;
    }
    if ((4U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[74U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[75U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[76U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[77U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[78U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[4U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[79U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[4U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[80U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[4U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[81U] = 0U;
    }
    if ((5U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[82U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[83U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[84U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[85U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[86U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[5U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[87U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[5U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[88U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[5U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[89U] = 0U;
    }
    if ((6U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[90U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[91U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[92U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[93U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[94U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[6U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[95U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[6U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[96U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[6U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[97U] = 0U;
    }
    if ((7U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[98U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[99U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[100U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[101U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[102U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[7U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[103U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[7U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[104U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[7U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[105U] = 0U;
    }
    if ((8U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[106U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[107U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[108U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[109U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[110U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[8U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[111U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[8U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[112U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[8U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[113U] = 0U;
    }
    if ((9U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[114U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[115U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[116U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[117U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[118U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[9U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[119U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[9U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[120U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[9U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[121U] = 0U;
    }
    if ((0x0aU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[122U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[123U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[124U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[125U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[126U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[10U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[127U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[10U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[128U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[10U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[129U] = 0U;
    }
    if ((0x0bU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[130U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[131U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[132U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[133U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[134U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[11U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[135U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[11U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[136U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[11U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[137U] = 0U;
    }
    if ((0x0cU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[138U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[139U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[140U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[141U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[142U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[12U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[143U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[12U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[144U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[12U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[145U] = 0U;
    }
    if ((0x0dU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[146U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[147U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[148U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[149U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[150U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[13U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[151U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[13U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[152U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[13U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[153U] = 0U;
    }
    if ((0x0eU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[154U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[155U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[156U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[157U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[158U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[14U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[159U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[14U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[160U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[14U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[161U] = 0U;
    }
    if ((0x0fU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[162U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[163U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[164U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[165U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[166U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[15U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[167U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[15U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[168U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[15U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[169U] = 0U;
    }
    if ((0x10U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[170U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[171U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[172U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[173U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[174U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[16U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[175U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[16U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[176U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[16U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[177U] = 0U;
    }
    if ((0x11U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[178U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[179U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[180U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[181U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[182U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[17U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[183U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[17U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[184U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[17U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[185U] = 0U;
    }
    if ((0x12U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[186U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[187U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[188U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[189U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[190U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[18U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[191U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[18U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[192U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[18U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[193U] = 0U;
    }
    if ((0x13U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[194U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[195U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[196U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[197U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[198U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[19U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[199U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[19U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[200U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[19U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[201U] = 0U;
    }
    if ((0x14U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[202U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[203U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[204U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[205U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[206U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[20U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[207U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[20U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[208U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[20U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[209U] = 0U;
    }
    if ((0x15U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[210U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[211U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[212U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[213U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[214U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[21U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[215U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[21U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[216U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[21U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[217U] = 0U;
    }
    if ((0x16U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[218U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[219U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[220U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[221U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[222U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[22U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[223U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[22U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[224U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[22U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[225U] = 0U;
    }
    if ((0x17U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[226U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[227U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[228U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[229U] = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[230U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[23U] 
                              >> 0x10U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[231U] 
            = (0x000000ffU & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[23U] 
                              >> 8U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[232U] 
            = (0x000000ffU & vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[23U]);
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb[233U] = 0U;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w 
        = ((IData)(vlSelfRef.b_tctx_rd_en_i) & ((IData)(vlSelfRef.b_tvalid_o) 
                                                | ((~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w)) 
                                                   & (0U 
                                                      == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r)))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w = 0U;
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_val_r;
    } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eseq_r)));
    } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = ((IData)(1U) + vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r);
    } else if (vlSelfRef.a_tctx_wr_en_i) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = vlSelfRef.a_tctx_wr_data_i;
    }
    vlSelfRef.a_tkeep_o = (0x000000ffU & (3U | (- (IData)(
                                                          (1U 
                                                           & (~ (IData)(__VdfgRegularize_h6e95ff9d_0_28)))))));
    vlSelfRef.a_tlast_o = ((IData)(vlSelfRef.a_tvalid_o) 
                           & (IData)(__VdfgRegularize_h6e95ff9d_0_28));
    vlSelfRef.a_tdata_o = (((QData)((IData)(((((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                [(0x000000ffU 
                                                  & ((IData)(7U) 
                                                     + 
                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                      << 3U)))] 
                                                & (- (IData)(
                                                             (0xefU 
                                                              >= 
                                                              (0x000000ffU 
                                                               & ((IData)(7U) 
                                                                  + 
                                                                  ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                   << 3U))))))) 
                                               << 0x00000018U) 
                                              | ((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(6U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(6U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 0x00000010U)) 
                                             | (((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(5U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 8U) 
                                                | (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                   [
                                                   (0x000000ffU 
                                                    & ((IData)(4U) 
                                                       + 
                                                       ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                        << 3U)))] 
                                                   & (- (IData)(
                                                                (0xefU 
                                                                 >= 
                                                                 (0x000000ffU 
                                                                  & ((IData)(4U) 
                                                                     + 
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                      << 3U))))))))))) 
                            << 0x00000020U) | (QData)((IData)(
                                                              ((((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                  [
                                                                  (0x000000ffU 
                                                                   & ((IData)(3U) 
                                                                      + 
                                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                       << 3U)))] 
                                                                  & (- (IData)(
                                                                               (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(3U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                 << 0x00000018U) 
                                                                | ((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(2U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(2U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 0x00000010U)) 
                                                               | (((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(1U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(1U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 8U) 
                                                                  | (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fb
                                                                     [
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                      << 3U)] 
                                                                     & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                                                                << 3U))))))))));
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout 
        = (3U | ((IData)(__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t) 
                 << 4U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
        = __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout;
    if ((4U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (0x0000001fU & (IData)(vlSelfRef.a_tctx_rd_addr_i));
            } else {
                if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w) {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w = 0U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t = 1U;
                } else {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w = 3U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t = 0U;
                }
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w));
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__t) 
                         << 4U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__t) 
                         << 4U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (0x0000001fU & (IData)(vlSelfRef.a_tctx_rd_addr_i));
            } else {
                if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w) {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w = 0U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t = 1U;
                } else {
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w = 3U;
                    vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t = 0U;
                }
                vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w));
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__w 
                = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__w));
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__w 
            = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__w));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__Vfuncout;
    } else {
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w) {
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                = (0x0000001fU & (IData)(vlSelfRef.a_tctx_rd_addr_i));
        } else {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w) {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w = 0U;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t = 1U;
            } else {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w = 3U;
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t = 0U;
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr 
                = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w));
        }
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT____VlemCall_0__taddr;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w = 0U;
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_val_r;
    } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eseq_r)));
    } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = ((IData)(1U) + vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r);
    } else if (vlSelfRef.b_tctx_wr_en_i) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = vlSelfRef.b_tctx_wr_data_i;
    }
    vlSelfRef.b_tkeep_o = (0x000000ffU & (3U | (- (IData)(
                                                          (1U 
                                                           & (~ (IData)(__VdfgRegularize_h6e95ff9d_0_19)))))));
    vlSelfRef.b_tlast_o = ((IData)(vlSelfRef.b_tvalid_o) 
                           & (IData)(__VdfgRegularize_h6e95ff9d_0_19));
    vlSelfRef.b_tdata_o = (((QData)((IData)(((((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                [(0x000000ffU 
                                                  & ((IData)(7U) 
                                                     + 
                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                      << 3U)))] 
                                                & (- (IData)(
                                                             (0xefU 
                                                              >= 
                                                              (0x000000ffU 
                                                               & ((IData)(7U) 
                                                                  + 
                                                                  ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                   << 3U))))))) 
                                               << 0x00000018U) 
                                              | ((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(6U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(6U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 0x00000010U)) 
                                             | (((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                  [
                                                  (0x000000ffU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                       << 3U)))] 
                                                  & (- (IData)(
                                                               (0xefU 
                                                                >= 
                                                                (0x000000ffU 
                                                                 & ((IData)(5U) 
                                                                    + 
                                                                    ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                     << 3U))))))) 
                                                 << 8U) 
                                                | (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                   [
                                                   (0x000000ffU 
                                                    & ((IData)(4U) 
                                                       + 
                                                       ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                        << 3U)))] 
                                                   & (- (IData)(
                                                                (0xefU 
                                                                 >= 
                                                                 (0x000000ffU 
                                                                  & ((IData)(4U) 
                                                                     + 
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                      << 3U))))))))))) 
                            << 0x00000020U) | (QData)((IData)(
                                                              ((((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                  [
                                                                  (0x000000ffU 
                                                                   & ((IData)(3U) 
                                                                      + 
                                                                      ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                       << 3U)))] 
                                                                  & (- (IData)(
                                                                               (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(3U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                 << 0x00000018U) 
                                                                | ((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(2U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(2U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 0x00000010U)) 
                                                               | (((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                    [
                                                                    (0x000000ffU 
                                                                     & ((IData)(1U) 
                                                                        + 
                                                                        ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                         << 3U)))] 
                                                                    & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                (0x000000ffU 
                                                                                & ((IData)(1U) 
                                                                                + 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))) 
                                                                   << 8U) 
                                                                  | (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fb
                                                                     [
                                                                     ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                      << 3U)] 
                                                                     & (- (IData)(
                                                                                (0xefU 
                                                                                >= 
                                                                                ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__beat_r) 
                                                                                << 3U))))))))));
    __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t 
        = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
    __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout 
        = (3U | ((IData)(__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__t) 
                 << 4U));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
        = __Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__3__Vfuncout;
    if ((4U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                    = vlSelfRef.b_tctx_rd_addr_i;
            } else {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__w 
                    = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__w));
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__t) 
                         << 4U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__t) 
                         << 4U));
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
            if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w) {
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                    = vlSelfRef.b_tctx_rd_addr_i;
            } else {
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__w 
                    = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__t 
                    = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
                vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__w));
            }
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__w 
                = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__w));
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__w 
            = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__w));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__Vfuncout;
    } else {
        if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w) {
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                = vlSelfRef.b_tctx_rd_addr_i;
        } else {
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__w 
                = ((0U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w))
                    ? 3U : 0U);
            vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__t 
                = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w;
            vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr 
                = (((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__w));
        }
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT____VlemCall_0__taddr;
    }
}

void Vchmap_wrap___024root___nba_sequent__TOP__1(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___nba_sequent__TOP__1\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.a_tdm_skip_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.tdm_skip_cnt_o;
    vlSelfRef.a_tdm_dup_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.tdm_dup_cnt_o;
    vlSelfRef.a_map_rd_valid_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.map_rd_valid_o;
    vlSelfRef.a_dup_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.lb_dup_cnt_o;
    vlSelfRef.a_skip_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.lb_skip_cnt_o;
    vlSelfRef.a_map_rd_data_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.map_rd_data_o;
    vlSelfRef.a_pv_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_valid_o;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w = 0U;
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[0U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[1U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[0U]));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w = 0U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w = 0U;
    } else {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w = 0U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[1U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[2U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[1U]));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w = 1U;
    }
    vlSelfRef.b_map_rd_valid_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.map_rd_valid_o;
    vlSelfRef.b_dup_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.lb_dup_cnt_o;
    vlSelfRef.b_skip_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.lb_skip_cnt_o;
    vlSelfRef.b_map_rd_data_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.map_rd_data_o;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 0U;
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[0U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w = 0U;
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[0U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[0U]));
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]));
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]));
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]));
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]));
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]));
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[7U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U]));
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 0U;
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[0U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 0U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[1U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 1U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[2U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 2U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[3U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 3U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[4U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 4U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[5U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 5U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[6U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[7U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 6U;
    }
    if ((((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
          >= vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[7U]) 
         & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
            < vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[8U]))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w 
            = (3U & ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_slot_o) 
                     - vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[7U]));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = 7U;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__own_last_w 
        = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w) 
           == (3U & ((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r
                      [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w] 
                      >> 1U) - (IData)(1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__own_last_w 
        = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w) 
           == (3U & ((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r
                      [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w] 
                      >> 1U) - (IData)(1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_we_w 
        = ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_valid_o) 
           & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w) 
              & ((~ ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__own_last_w) 
                     & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r
                        [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w] 
                        & (5U == vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r
                           [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w])))) 
                 & ((IData)(vlSelfRef.a_en_i) >> (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w)))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_we_w 
        = ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_valid_o) 
           & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w) 
              & ((~ ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__own_last_w) 
                     & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
                        [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w] 
                        & (5U == vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r
                           [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w])))) 
                 & ((IData)(vlSelfRef.b_en_i) >> (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w)))));
}

void Vchmap_wrap___024root___trigger_orInto__act_vec_vec(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___trigger_orInto__act_vec_vec\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((0U >= n));
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vchmap_wrap___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

bool Vchmap_wrap___024root___eval_phase__act(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_phase__act\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__act
        vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                        ((((IData)(vlSelfRef.clk_audio) 
                                                           & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk_audio__1))) 
                                                          << 1U) 
                                                         | ((IData)(vlSelfRef.clk) 
                                                            & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__1))))));
        vlSelfRef.__Vtrigprevexpr___TOP__clk__1 = vlSelfRef.clk;
        vlSelfRef.__Vtrigprevexpr___TOP__clk_audio__1 
            = vlSelfRef.clk_audio;
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vchmap_wrap___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
    Vchmap_wrap___024root___trigger_orInto__act_vec_vec(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vchmap_wrap___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

void Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf);
void Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0(Vchmap_wrap_KL_chan_map_capture* vlSelf);

bool Vchmap_wrap___024root___eval_phase__nba(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_phase__nba\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vchmap_wrap___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        {
            // Inlined CFunc: _eval_nba
            if ((1ULL & vlSelfRef.__VnbaTriggered[0U])) {
                Vchmap_wrap___024root___nba_sequent__TOP__0(vlSelf);
                Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
                Vchmap_wrap_KL_chan_map_capture___nba_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
                Vchmap_wrap___024root___nba_sequent__TOP__1(vlSelf);
            }
            if ((2ULL & vlSelfRef.__VnbaTriggered[0U])) {
                {
                    // Inlined CFunc: _nba_sequent__TOP__2
                    SData/*8:0*/ __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r;
                    __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r = 0;
                    CData/*5:0*/ __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__idx_r;
                    __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__idx_r = 0;
                    __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r 
                        = vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r;
                    __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__idx_r 
                        = vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__idx_r;
                    if (vlSelfRef.rst_n) {
                        __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r 
                            = (0x000001ffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r)));
                        if (vlSelfRef.tg_en_i) {
                            if ((0x01ffU == (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r))) {
                                __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__idx_r 
                                    = ((0x2fU == (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__idx_r))
                                        ? 0U : (0x0000003fU 
                                                & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__idx_r))));
                                vlSelfRef.tone_legacy_o 
                                    = ((0x2fU >= (IData)(vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__idx_r))
                                        ? vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__TONE_TAB_C
                                       [vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__idx_r]
                                        : 0U);
                            }
                        } else {
                            __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__idx_r = 0U;
                            vlSelfRef.tone_legacy_o = 0U;
                        }
                    } else {
                        __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r = 0U;
                        __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__idx_r = 0U;
                        vlSelfRef.tone_legacy_o = 0U;
                    }
                    vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r 
                        = __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r;
                    vlSelfRef.chmap_wrap__DOT__u_tone_legacy__DOT__idx_r 
                        = __Vinline_0__eval_nba___Vinline_0__nba_sequent__TOP__2___Vdly__chmap_wrap__DOT__u_tone_legacy__DOT__idx_r;
                }
            }
        }
        Vchmap_wrap___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vchmap_wrap___024root___eval(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VicoIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vchmap_wrap___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("chmap_wrap.sv", 28, "", "DIDNOTCONVERGE: Input combinational region did not converge after '--converge-limit' of 10000 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        vlSelfRef.__VicoPhaseResult = Vchmap_wrap___024root___eval_phase__ico(vlSelf);
    } while (vlSelfRef.__VicoPhaseResult);
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vchmap_wrap___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("chmap_wrap.sv", 28, "", "DIDNOTCONVERGE: NBA region did not converge after '--converge-limit' of 10000 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00002710U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vchmap_wrap___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("chmap_wrap.sv", 28, "", "DIDNOTCONVERGE: Active region did not converge after '--converge-limit' of 10000 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactPhaseResult = Vchmap_wrap___024root___eval_phase__act(vlSelf);
        } while (vlSelfRef.__VactPhaseResult);
        vlSelfRef.__VnbaPhaseResult = Vchmap_wrap___024root___eval_phase__nba(vlSelf);
    } while (vlSelfRef.__VnbaPhaseResult);
}

#ifdef VL_DEBUG
void Vchmap_wrap___024root___eval_debug_assertions(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_debug_assertions\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.rst_n & 0xfeU)))) {
        Verilated::overWidthError("rst_n");
    }
    if (VL_UNLIKELY(((vlSelfRef.clk_audio & 0xfeU)))) {
        Verilated::overWidthError("clk_audio");
    }
    if (VL_UNLIKELY(((vlSelfRef.tg_en_i & 0xfeU)))) {
        Verilated::overWidthError("tg_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tg_tick_i & 0xfeU)))) {
        Verilated::overWidthError("tg_tick_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.dest_mac_i & 0ULL)))) {
        Verilated::overWidthError("dest_mac_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.station_mac_i & 0ULL)))) {
        Verilated::overWidthError("station_mac_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.vlan_vid_i & 0xf000U)))) {
        Verilated::overWidthError("vlan_vid_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.i2s_pair_valid_i & 0xfeU)))) {
        Verilated::overWidthError("i2s_pair_valid_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.i2s_l_i & 0xff000000U)))) {
        Verilated::overWidthError("i2s_l_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.i2s_r_i & 0xff000000U)))) {
        Verilated::overWidthError("i2s_r_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tdm_pair_valid_i & 0xfeU)))) {
        Verilated::overWidthError("tdm_pair_valid_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tdm_pair_slot_i & 0xf0U)))) {
        Verilated::overWidthError("tdm_pair_slot_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tdm_l_i & 0xff000000U)))) {
        Verilated::overWidthError("tdm_l_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tdm_r_i & 0xff000000U)))) {
        Verilated::overWidthError("tdm_r_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.tone_smp_i & 0xff000000U)))) {
        Verilated::overWidthError("tone_smp_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.lb_tvalid_i & 0xfeU)))) {
        Verilated::overWidthError("lb_tvalid_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.lb_tlast_i & 0xfeU)))) {
        Verilated::overWidthError("lb_tlast_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.lb_tuser_i & 0xf0U)))) {
        Verilated::overWidthError("lb_tuser_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_map_wr_en_i & 0xfeU)))) {
        Verilated::overWidthError("a_map_wr_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_map_wr_addr_i & 0xc0U)))) {
        Verilated::overWidthError("a_map_wr_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_map_wr_data_i & 0xe000U)))) {
        Verilated::overWidthError("a_map_wr_data_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_map_rd_en_i & 0xfeU)))) {
        Verilated::overWidthError("a_map_rd_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_map_rd_addr_i & 0xc0U)))) {
        Verilated::overWidthError("a_map_rd_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_tick_i & 0xfeU)))) {
        Verilated::overWidthError("a_tick_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_en_i & 0xfcU)))) {
        Verilated::overWidthError("a_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_tctx_wr_en_i & 0xfeU)))) {
        Verilated::overWidthError("a_tctx_wr_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_tctx_wr_addr_i & 0x80U)))) {
        Verilated::overWidthError("a_tctx_wr_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_tctx_rd_en_i & 0xfeU)))) {
        Verilated::overWidthError("a_tctx_rd_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_tctx_rd_addr_i & 0x80U)))) {
        Verilated::overWidthError("a_tctx_rd_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.a_tready_i & 0xfeU)))) {
        Verilated::overWidthError("a_tready_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_map_wr_en_i & 0xfeU)))) {
        Verilated::overWidthError("b_map_wr_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_map_wr_addr_i & 0xc0U)))) {
        Verilated::overWidthError("b_map_wr_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_map_wr_data_i & 0xe000U)))) {
        Verilated::overWidthError("b_map_wr_data_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_map_rd_en_i & 0xfeU)))) {
        Verilated::overWidthError("b_map_rd_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_map_rd_addr_i & 0xc0U)))) {
        Verilated::overWidthError("b_map_rd_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_tick_i & 0xfeU)))) {
        Verilated::overWidthError("b_tick_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_tctx_wr_en_i & 0xfeU)))) {
        Verilated::overWidthError("b_tctx_wr_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_tctx_wr_addr_i & 0x80U)))) {
        Verilated::overWidthError("b_tctx_wr_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_tctx_rd_en_i & 0xfeU)))) {
        Verilated::overWidthError("b_tctx_rd_en_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_tctx_rd_addr_i & 0x80U)))) {
        Verilated::overWidthError("b_tctx_rd_addr_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_tready_i & 0xfeU)))) {
        Verilated::overWidthError("b_tready_i");
    }
}
#endif  // VL_DEBUG

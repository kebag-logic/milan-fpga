// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vchmap_wrap.h for the primary calling header

#include "Vchmap_wrap__pch.h"

VL_ATTR_COLD void Vchmap_wrap_KL_chan_map_capture___eval_static__TOP__chmap_wrap__DOT__u_chmap_a(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___eval_static__TOP__chmap_wrap__DOT__u_chmap_a\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ lb_tdata_i;
    lb_tdata_i = 0;
    // Body
    lb_tdata_i = 0ULL;
    vlSelfRef.lb_tvalid_i = 0U;
    vlSelfRef.lb_tlast_i = 0U;
    vlSelfRef.lb_tuser_i = 0U;
    vlSelfRef.lb_wire_chans_i = 0U;
    vlSelfRef.lb_flush_i = 0U;
}

VL_ATTR_COLD void Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ lb_tdata_i;
    lb_tdata_i = 0;
    CData/*3:0*/ __PVT__lb_chans_raw_w;
    __PVT__lb_chans_raw_w = 0;
    CData/*0:0*/ __PVT__lb_w1_w;
    __PVT__lb_w1_w = 0;
    CData/*0:0*/ __PVT__skid_acc1_w;
    __PVT__skid_acc1_w = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_56;
    __VdfgRegularize_h6e95ff9d_0_56 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_57;
    __VdfgRegularize_h6e95ff9d_0_57 = 0;
    // Body
    vlSelfRef.__PVT__loop_mapped_w = 0U;
    if (((vlSelfRef.__PVT__map_r[0U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[0U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[1U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[1U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[2U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[2U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[3U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[3U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[4U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[4U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[5U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[5U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[6U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[6U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[7U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[7U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[8U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[8U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[9U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[9U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[10U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[10U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[11U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[11U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[12U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[12U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[13U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[13U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[14U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[14U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[15U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[15U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[16U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[16U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[17U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[17U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[18U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[18U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[19U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[19U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[20U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[20U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[21U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[21U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[22U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[22U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[23U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[23U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[24U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[24U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[25U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[25U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[26U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[26U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[27U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[27U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[28U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[28U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[29U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[29U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[30U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[30U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[31U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[31U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[32U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[32U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[33U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[33U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[34U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[34U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[35U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[35U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[36U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[36U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[37U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[37U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[38U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[38U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[39U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[39U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[40U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[40U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[41U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[41U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[42U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[42U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[43U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[43U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[44U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[44U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[45U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[45U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[46U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[46U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[47U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[47U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[48U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[48U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[49U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[49U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[50U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[50U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[51U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[51U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[52U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[52U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[53U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[53U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[54U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[54U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[55U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[55U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[56U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[56U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[57U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[57U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[58U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[58U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[59U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[59U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[60U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[60U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[61U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[61U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[62U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[62U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[63U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[63U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    vlSelfRef.tdm_pair_valid_i = vlSymsp->TOP.tdm_pair_valid_i;
    vlSelfRef.__PVT__tdm_frame_ev_w = ((IData)(vlSymsp->TOP.tdm_pair_valid_i) 
                                       & (0U == (IData)(vlSymsp->TOP.tdm_pair_slot_i)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9 = (7U 
                                                & ((vlSelfRef.__PVT__map_r
                                                    [
                                                    (1U 
                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U))] 
                                                    >> 8U) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (vlSelfRef.__PVT__map_r
                                                                    [
                                                                    (1U 
                                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                        << 1U))] 
                                                                    >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10 = (7U 
                                                 & ((vlSelfRef.__PVT__map_r
                                                     [
                                                     ((IData)(vlSelfRef.__PVT__slot_r) 
                                                      << 1U)] 
                                                     >> 8U) 
                                                    & (- (IData)(
                                                                 (1U 
                                                                  & (vlSelfRef.__PVT__map_r
                                                                     [
                                                                     ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                      << 1U)] 
                                                                     >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [((IData)(vlSelfRef.__PVT__slot_r) 
                                                   << 1U)]);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [(1U 
                                                   | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                      << 1U))]);
    lb_tdata_i = vlSymsp->TOP.lb_tdata_i;
    vlSelfRef.__PVT__push_ram_w = ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                   & ((IData)(vlSelfRef.__PVT__skid_v_r) 
                                      >> (IData)(vlSelfRef.__PVT__skid_rp_r)));
    __VdfgRegularize_h6e95ff9d_0_56 = ((vlSelfRef.__PVT__q_primed_r 
                                        >> (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & ((1U == (IData)(vlSelfRef.__PVT__st_r)) 
                                          & (0x20U 
                                             > (IData)(vlSelfRef.__PVT__pop_idx_r))));
    vlSelfRef.__PVT__skid_free_w = (7U & (((IData)(4U) 
                                           - (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                          + (1U & (- (IData)(
                                                             (0U 
                                                              != (IData)(vlSelfRef.__PVT__skid_cnt_r)))))));
    vlSelfRef.lb_tlast_i = vlSymsp->TOP.lb_tlast_i;
    vlSelfRef.lb_flush_i = vlSymsp->TOP.a_lb_flush_i;
    vlSelfRef.lb_tvalid_i = vlSymsp->TOP.lb_tvalid_i;
    vlSelfRef.lb_wire_chans_i = vlSymsp->TOP.lb_wire_chans_i;
    vlSelfRef.lb_tuser_i = vlSymsp->TOP.lb_tuser_i;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                 << 1U)] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U)])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_32 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                (1U 
                                                                 | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                    << 1U))] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       (1U 
                                                        | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                           << 1U))])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)))))))));
    vlSelfRef.__PVT__lb_smp0_w = ((0x00ff0000U & ((IData)(lb_tdata_i) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((lb_tdata_i 
                                                >> 8U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (lb_tdata_i 
                                                             >> 0x00000010U)))));
    vlSelfRef.__PVT__lb_smp1_w = ((0x00ff0000U & ((IData)(
                                                          (lb_tdata_i 
                                                           >> 0x00000020U)) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((lb_tdata_i 
                                                >> 0x00000028U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (lb_tdata_i 
                                                             >> 0x00000030U)))));
    vlSelfRef.__PVT__dup_sum_w = (0x0001ffffU & (((IData)(__VdfgRegularize_h6e95ff9d_0_56) 
                                                  & ((vlSelfRef.__PVT__q_fed_r 
                                                      >> 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                                     & (0U 
                                                        == vlSelfRef.__PVT__q_cnt_r
                                                        [
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__PVT__pop_idx_r))]))) 
                                                 + (IData)(vlSelfRef.lb_dup_cnt_o)));
    vlSelfRef.__PVT__pop_act_w = ((0U != vlSelfRef.__PVT__q_cnt_r
                                   [(0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r))]) 
                                  & (IData)(__VdfgRegularize_h6e95ff9d_0_56));
    vlSelfRef.__PVT__flush_clr_w = 0U;
    if ((1U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (1U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (2U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (4U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (8U | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((2U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000010U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000020U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000040U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000080U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((4U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000100U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000200U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000400U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000800U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((8U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00001000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00002000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00004000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00008000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000010U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00010000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00020000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00040000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00080000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000020U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00100000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00200000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00400000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00800000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000040U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x01000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x02000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x04000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x08000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000080U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x10000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x20000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x40000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x80000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    vlSelfRef.__PVT__stash_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    vlSelfRef.__PVT__skid_kill_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
         & (0U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 1U) & (1U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 2U) & (2U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 3U) & (3U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    vlSelfRef.__PVT__lb_a0_w = (0x0000001fU & (((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                >> 1U) 
                                               + (0x0000001cU 
                                                  & ((IData)(vlSelfRef.lb_tuser_i) 
                                                     << 2U))));
    vlSelfRef.__PVT__beat_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    vlSelfRef.__PVT__lb_ok_w = ((IData)(vlSelfRef.lb_tvalid_i) 
                                & (8U > (IData)(vlSelfRef.lb_tuser_i)));
    __PVT__lb_chans_raw_w = 0U;
    if ((0U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & vlSelfRef.lb_wire_chans_i);
    }
    if ((1U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 4U));
    }
    if ((2U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 8U));
    }
    if ((3U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x0cU));
    }
    if ((4U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x10U));
    }
    if ((5U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x14U));
    }
    if ((6U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x18U));
    }
    if ((7U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (vlSelfRef.lb_wire_chans_i 
                                 >> 0x1cU);
    }
    vlSelfRef.__PVT__push_same_w = ((IData)(vlSelfRef.__PVT__push_ram_w) 
                                    & ((vlSelfRef.__PVT__skid_addr_r
                                        [vlSelfRef.__PVT__skid_rp_r] 
                                        == (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & (IData)(vlSelfRef.__PVT__pop_act_w)));
    vlSelfRef.__PVT__prime_set_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (0U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (1U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (2U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (4U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (8U | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (1U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00000010U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000020U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000040U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000080U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (2U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00000100U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000200U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000400U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000800U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (3U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00001000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00002000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00004000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00008000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (4U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00010000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00020000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00040000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00080000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (5U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00100000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00200000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00400000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00800000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (6U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x01000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x02000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x04000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x08000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (7U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x10000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x20000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x40000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x80000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    vlSelfRef.__PVT__lb_w0_w = ((8U > (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__lb_chans_w = ((0U == (IData)(__PVT__lb_chans_raw_w))
                                    ? 2U : (IData)(__PVT__lb_chans_raw_w));
    vlSelfRef.__PVT__push_cnt1_w = (0x0000000fU & ((IData)(vlSelfRef.__PVT__q_cnt_r
                                                           [vlSelfRef.__PVT__skid_addr_r
                                                           [vlSelfRef.__PVT__skid_rp_r]]) 
                                                   - (IData)(vlSelfRef.__PVT__push_same_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61 = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                    | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                        - (IData)(1U)) 
                                                       == (IData)(vlSelfRef.__PVT__lb_chpos_r))));
    vlSelfRef.__PVT__lb_ch1_w = (0x0000000fU & (((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                                & (- (IData)(
                                                             ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                              != 
                                                              (0x0000000fU 
                                                               & ((IData)(1U) 
                                                                  + (IData)(vlSelfRef.__PVT__lb_chpos_r))))))));
    vlSelfRef.__PVT__push_drop_w = ((8U == (IData)(vlSelfRef.__PVT__push_cnt1_w)) 
                                    & (IData)(vlSelfRef.__PVT__push_ram_w));
    vlSelfRef.__PVT__cm0_v_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61) 
                                & (IData)(vlSelfRef.__PVT__lb_w0_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59 = ((IData)(vlSelfRef.lb_tlast_i) 
                                                 | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                     - (IData)(1U)) 
                                                    == (IData)(vlSelfRef.__PVT__lb_ch1_w)));
    __PVT__lb_w1_w = ((8U > (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                      & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                                 & (IData)(vlSelfRef.__PVT__cm0_v_w));
    vlSelfRef.__PVT__lb_pair01_w = ((IData)(vlSelfRef.__PVT__lb_w0_w) 
                                    & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61)) 
                                       & (IData)(__PVT__lb_w1_w)));
    vlSelfRef.__PVT__skid_acc0_w = ((1U <= (IData)(vlSelfRef.__PVT__skid_free_w)) 
                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58));
    if (vlSelfRef.__PVT__lb_pair01_w) {
        vlSelfRef.__PVT__cm1_data_w = (((QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)) 
                                        << 0x00000018U) 
                                       | (QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)));
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (IData)(vlSelfRef.__PVT__lb_a0_w));
    } else {
        vlSelfRef.__PVT__cm1_data_w = ((QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)) 
                                       << 0x00000018U);
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                           >> 1U) + 
                                          (0x0000001cU 
                                           & ((IData)(vlSelfRef.lb_tuser_i) 
                                              << 2U))));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60 = ((~ 
                                                  ((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                   | (IData)(vlSelfRef.__PVT__lb_pair01_w))) 
                                                 & (IData)(__PVT__lb_w1_w));
    vlSelfRef.__PVT__stash_open_w = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59)) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60));
    __VdfgRegularize_h6e95ff9d_0_57 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                       & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60)) 
                                          | (IData)(vlSelfRef.__PVT__lb_pair01_w)));
    __PVT__skid_acc1_w = (((IData)(vlSelfRef.__PVT__skid_free_w) 
                           >= ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                ? 2U : 1U)) & (IData)(__VdfgRegularize_h6e95ff9d_0_57));
    vlSelfRef.__PVT__enq1_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w) 
                                 & (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skip_sum_w = (0x0001ffffU & ((3U 
                                                   & ((IData)(vlSelfRef.__PVT__push_drop_w) 
                                                      + 
                                                      (((~ (IData)(__PVT__skid_acc1_w)) 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_57)) 
                                                       + 
                                                       ((~ (IData)(vlSelfRef.__PVT__skid_acc0_w)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58))))) 
                                                  + (IData)(vlSelfRef.lb_skip_cnt_o)));
    vlSelfRef.__PVT__enq0_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                  ? (IData)(vlSelfRef.__PVT__skid_acc0_w)
                                  : (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skid_enq_n_w = (3U & ((IData)(vlSelfRef.__PVT__enq1_v_w) 
                                           + (IData)(vlSelfRef.__PVT__enq0_v_w)));
}

VL_ATTR_COLD void Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ lb_tdata_i;
    lb_tdata_i = 0;
    CData/*3:0*/ __PVT__lb_chans_raw_w;
    __PVT__lb_chans_raw_w = 0;
    CData/*0:0*/ __PVT__lb_w1_w;
    __PVT__lb_w1_w = 0;
    CData/*0:0*/ __PVT__skid_acc1_w;
    __PVT__skid_acc1_w = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_49;
    __VdfgRegularize_h6e95ff9d_0_49 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_50;
    __VdfgRegularize_h6e95ff9d_0_50 = 0;
    // Body
    vlSelfRef.__PVT__loop_mapped_w = 0U;
    if (((vlSelfRef.__PVT__map_r[0U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[0U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[1U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[1U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[2U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[2U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[3U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[3U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[4U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[4U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[5U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[5U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[6U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[6U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[7U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[7U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[8U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[8U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[9U] >> 0x0cU) & (5U 
                                                  == 
                                                  (7U 
                                                   & (vlSelfRef.__PVT__map_r[9U] 
                                                      >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[10U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[10U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[11U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[11U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[12U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[12U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[13U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[13U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[14U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[14U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[15U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[15U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[16U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[16U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[17U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[17U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[18U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[18U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[19U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[19U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[20U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[20U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[21U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[21U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[22U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[22U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[23U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[23U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[24U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[24U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[25U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[25U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[26U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[26U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[27U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[27U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[28U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[28U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[29U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[29U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[30U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[30U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[31U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[31U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[32U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[32U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[33U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[33U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[34U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[34U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[35U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[35U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[36U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[36U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[37U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[37U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[38U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[38U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[39U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[39U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[40U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[40U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[41U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[41U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[42U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[42U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[43U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[43U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[44U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[44U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[45U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[45U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[46U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[46U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[47U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[47U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[48U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[48U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[49U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[49U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[50U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[50U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[51U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[51U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[52U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[52U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[53U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[53U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[54U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[54U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[55U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[55U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[56U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[56U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[57U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[57U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[58U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[58U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[59U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[59U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[60U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[60U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[61U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[61U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[62U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[62U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.__PVT__map_r[63U] >> 0x0cU) & (5U 
                                                   == 
                                                   (7U 
                                                    & (vlSelfRef.__PVT__map_r[63U] 
                                                       >> 8U))))) {
        vlSelfRef.__PVT__loop_mapped_w = 1U;
    }
    vlSelfRef.tdm_pair_valid_i = vlSymsp->TOP.tdm_pair_valid_i;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7 = (7U 
                                                & ((vlSelfRef.__PVT__map_r
                                                    [
                                                    (1U 
                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U))] 
                                                    >> 8U) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (vlSelfRef.__PVT__map_r
                                                                    [
                                                                    (1U 
                                                                     | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                        << 1U))] 
                                                                    >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8 = (7U 
                                                & ((vlSelfRef.__PVT__map_r
                                                    [
                                                    ((IData)(vlSelfRef.__PVT__slot_r) 
                                                     << 1U)] 
                                                    >> 8U) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (vlSelfRef.__PVT__map_r
                                                                    [
                                                                    ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                     << 1U)] 
                                                                    >> 0x0000000cU))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [((IData)(vlSelfRef.__PVT__slot_r) 
                                                   << 1U)]);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40 = (0x0000000fU 
                                                 & vlSelfRef.__PVT__map_r
                                                 [(1U 
                                                   | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                      << 1U))]);
    lb_tdata_i = vlSymsp->TOP.lb_tdata_i;
    vlSelfRef.__PVT__push_ram_w = ((0U != (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                   & ((IData)(vlSelfRef.__PVT__skid_v_r) 
                                      >> (IData)(vlSelfRef.__PVT__skid_rp_r)));
    __VdfgRegularize_h6e95ff9d_0_49 = ((vlSelfRef.__PVT__q_primed_r 
                                        >> (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & ((1U == (IData)(vlSelfRef.__PVT__st_r)) 
                                          & (0x20U 
                                             > (IData)(vlSelfRef.__PVT__pop_idx_r))));
    vlSelfRef.__PVT__skid_free_w = (7U & (((IData)(4U) 
                                           - (IData)(vlSelfRef.__PVT__skid_cnt_r)) 
                                          + (1U & (- (IData)(
                                                             (0U 
                                                              != (IData)(vlSelfRef.__PVT__skid_cnt_r)))))));
    vlSelfRef.lb_tlast_i = vlSymsp->TOP.lb_tlast_i;
    vlSelfRef.lb_flush_i = vlSymsp->TOP.b_lb_flush_i;
    vlSelfRef.lb_tvalid_i = vlSymsp->TOP.lb_tvalid_i;
    vlSelfRef.lb_wire_chans_i = vlSymsp->TOP.lb_wire_chans_i;
    vlSelfRef.lb_tuser_i = vlSymsp->TOP.lb_tuser_i;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                 << 1U)] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       ((IData)(vlSelfRef.__PVT__slot_r) 
                                                        << 1U)])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36 = (0x0000ffffffffffffULL 
                                                 & ((4U 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                     ? 
                                                    (((1U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                       ? 
                                                      (vlSelfRef.__PVT__lb_hold_r
                                                       [
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40) 
                                                           + 
                                                           (0x0000001cU 
                                                            & ((vlSelfRef.__PVT__map_r
                                                                [
                                                                (1U 
                                                                 | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                    << 1U))] 
                                                                >> 4U) 
                                                               << 2U))))] 
                                                       & (- (QData)((IData)(
                                                                            ((8U 
                                                                              > 
                                                                              (0x0000000fU 
                                                                               & (vlSelfRef.__PVT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)))))))
                                                       : 
                                                      (((QData)((IData)(vlSymsp->TOP.tone_smp_i)) 
                                                        << 0x00000018U) 
                                                       | (QData)((IData)(vlSymsp->TOP.tone_smp_i)))) 
                                                     & (- (QData)((IData)(
                                                                          (1U 
                                                                           & (~ 
                                                                              ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7) 
                                                                               >> 1U)))))))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7))
                                                      ? 
                                                     (vlSelfRef.tdm_hold_r
                                                      [
                                                      (3U 
                                                       & vlSelfRef.__PVT__map_r
                                                       [
                                                       (1U 
                                                        | ((IData)(vlSelfRef.__PVT__slot_r) 
                                                           << 1U))])] 
                                                      & (- (QData)((IData)(
                                                                           ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7)) 
                                                                            & (4U 
                                                                               > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40)))))))
                                                      : 
                                                     (vlSelfRef.__PVT__i2s_hold_r 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7)))))))));
    vlSelfRef.__PVT__lb_smp0_w = ((0x00ff0000U & ((IData)(lb_tdata_i) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((lb_tdata_i 
                                                >> 8U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (lb_tdata_i 
                                                             >> 0x00000010U)))));
    vlSelfRef.__PVT__lb_smp1_w = ((0x00ff0000U & ((IData)(
                                                          (lb_tdata_i 
                                                           >> 0x00000020U)) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((lb_tdata_i 
                                                >> 0x00000028U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (lb_tdata_i 
                                                             >> 0x00000030U)))));
    vlSelfRef.__PVT__dup_sum_w = (0x0001ffffU & (((IData)(__VdfgRegularize_h6e95ff9d_0_49) 
                                                  & ((vlSelfRef.__PVT__q_fed_r 
                                                      >> 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                                     & (0U 
                                                        == vlSelfRef.__PVT__q_cnt_r
                                                        [
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__PVT__pop_idx_r))]))) 
                                                 + (IData)(vlSelfRef.lb_dup_cnt_o)));
    vlSelfRef.__PVT__pop_act_w = ((0U != vlSelfRef.__PVT__q_cnt_r
                                   [(0x0000001fU & (IData)(vlSelfRef.__PVT__pop_idx_r))]) 
                                  & (IData)(__VdfgRegularize_h6e95ff9d_0_49));
    vlSelfRef.__PVT__flush_clr_w = 0U;
    if ((1U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (1U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (2U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (4U | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (8U | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((2U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000010U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000020U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000040U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000080U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((4U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00000100U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000200U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000400U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00000800U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((8U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00001000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00002000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00004000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00008000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000010U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00010000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00020000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00040000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00080000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000020U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x00100000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00200000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00400000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x00800000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000040U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x01000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x02000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x04000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x08000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    if ((0x00000080U & (IData)(vlSelfRef.lb_flush_i))) {
        vlSelfRef.__PVT__flush_clr_w = (0x10000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x20000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x40000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
        vlSelfRef.__PVT__flush_clr_w = (0x80000000U 
                                        | vlSelfRef.__PVT__flush_clr_w);
    }
    vlSelfRef.__PVT__stash_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.__PVT__stash_strm_r)))) {
        vlSelfRef.__PVT__stash_flush_w = 1U;
    }
    vlSelfRef.__PVT__skid_kill_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
         & (0U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if ((((IData)(vlSelfRef.__PVT__skid_v_r) & ((IData)(vlSelfRef.lb_flush_i) 
                                                >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[0U]))) {
        vlSelfRef.__PVT__skid_kill_w = (1U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 1U) & (1U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 1U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[1U]))) {
        vlSelfRef.__PVT__skid_kill_w = (2U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 2U) & (2U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 3U)) 
         & (3U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 2U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[2U]))) {
        vlSelfRef.__PVT__skid_kill_w = (4U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & (IData)(vlSelfRef.lb_flush_i)) & (0U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 1U)) 
         & (1U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 2U)) 
         & (2U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) & (IData)(vlSelfRef.lb_flush_i)) 
          >> 3U) & (3U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 4U)) 
         & (4U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 5U)) 
         & (5U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 6U)) 
         & (6U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    if (((((IData)(vlSelfRef.__PVT__skid_v_r) >> 3U) 
          & ((IData)(vlSelfRef.lb_flush_i) >> 7U)) 
         & (7U == vlSelfRef.__PVT__skid_strm_r[3U]))) {
        vlSelfRef.__PVT__skid_kill_w = (8U | (IData)(vlSelfRef.__PVT__skid_kill_w));
    }
    vlSelfRef.__PVT__lb_a0_w = (0x0000001fU & (((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                >> 1U) 
                                               + (0x0000001cU 
                                                  & ((IData)(vlSelfRef.lb_tuser_i) 
                                                     << 2U))));
    vlSelfRef.__PVT__beat_flush_w = 0U;
    if (((IData)(vlSelfRef.lb_flush_i) & (0U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 1U) & (1U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 2U) & (2U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 3U) & (3U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 4U) & (4U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 5U) & (5U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 6U) & (6U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.lb_flush_i) >> 7U) & (7U 
                                                  == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__beat_flush_w = 1U;
    }
    vlSelfRef.__PVT__lb_ok_w = ((IData)(vlSelfRef.lb_tvalid_i) 
                                & (8U > (IData)(vlSelfRef.lb_tuser_i)));
    __PVT__lb_chans_raw_w = 0U;
    if ((0U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & vlSelfRef.lb_wire_chans_i);
    }
    if ((1U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 4U));
    }
    if ((2U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 8U));
    }
    if ((3U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x0cU));
    }
    if ((4U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x10U));
    }
    if ((5U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x14U));
    }
    if ((6U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (0x0000000fU & (vlSelfRef.lb_wire_chans_i 
                                                >> 0x18U));
    }
    if ((7U == (IData)(vlSelfRef.lb_tuser_i))) {
        __PVT__lb_chans_raw_w = (vlSelfRef.lb_wire_chans_i 
                                 >> 0x1cU);
    }
    vlSelfRef.__PVT__push_same_w = ((IData)(vlSelfRef.__PVT__push_ram_w) 
                                    & ((vlSelfRef.__PVT__skid_addr_r
                                        [vlSelfRef.__PVT__skid_rp_r] 
                                        == (0x0000001fU 
                                            & (IData)(vlSelfRef.__PVT__pop_idx_r))) 
                                       & (IData)(vlSelfRef.__PVT__pop_act_w)));
    vlSelfRef.__PVT__prime_set_w = 0U;
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (0U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (1U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (2U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (4U | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (8U | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (1U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00000010U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000020U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000040U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000080U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (2U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00000100U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000200U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000400U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00000800U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (3U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00001000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00002000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00004000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00008000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (4U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00010000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00020000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00040000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00080000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (5U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x00100000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00200000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00400000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x00800000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (6U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x01000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x02000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x04000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x08000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    if ((((IData)(vlSelfRef.__PVT__lb_ok_w) & (IData)(vlSelfRef.lb_tlast_i)) 
         & (7U == (IData)(vlSelfRef.lb_tuser_i)))) {
        vlSelfRef.__PVT__prime_set_w = (0x10000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x20000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x40000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
        vlSelfRef.__PVT__prime_set_w = (0x80000000U 
                                        | vlSelfRef.__PVT__prime_set_w);
    }
    vlSelfRef.__PVT__lb_w0_w = ((8U > (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__PVT__lb_chans_w = ((0U == (IData)(__PVT__lb_chans_raw_w))
                                    ? 2U : (IData)(__PVT__lb_chans_raw_w));
    vlSelfRef.__PVT__push_cnt1_w = (0x0000000fU & ((IData)(vlSelfRef.__PVT__q_cnt_r
                                                           [vlSelfRef.__PVT__skid_addr_r
                                                           [vlSelfRef.__PVT__skid_rp_r]]) 
                                                   - (IData)(vlSelfRef.__PVT__push_same_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54 = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__lb_chpos_r) 
                                                    | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                        - (IData)(1U)) 
                                                       == (IData)(vlSelfRef.__PVT__lb_chpos_r))));
    vlSelfRef.__PVT__lb_ch1_w = (0x0000000fU & (((IData)(1U) 
                                                 + (IData)(vlSelfRef.__PVT__lb_chpos_r)) 
                                                & (- (IData)(
                                                             ((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                              != 
                                                              (0x0000000fU 
                                                               & ((IData)(1U) 
                                                                  + (IData)(vlSelfRef.__PVT__lb_chpos_r))))))));
    vlSelfRef.__PVT__push_drop_w = ((8U == (IData)(vlSelfRef.__PVT__push_cnt1_w)) 
                                    & (IData)(vlSelfRef.__PVT__push_ram_w));
    vlSelfRef.__PVT__cm0_v_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54) 
                                & (IData)(vlSelfRef.__PVT__lb_w0_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52 = ((IData)(vlSelfRef.lb_tlast_i) 
                                                 | (((IData)(vlSelfRef.__PVT__lb_chans_w) 
                                                     - (IData)(1U)) 
                                                    == (IData)(vlSelfRef.__PVT__lb_ch1_w)));
    __PVT__lb_w1_w = ((8U > (IData)(vlSelfRef.__PVT__lb_ch1_w)) 
                      & (IData)(vlSelfRef.__PVT__lb_ok_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                                 & (IData)(vlSelfRef.__PVT__cm0_v_w));
    vlSelfRef.__PVT__lb_pair01_w = ((IData)(vlSelfRef.__PVT__lb_w0_w) 
                                    & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)) 
                                       & (IData)(__PVT__lb_w1_w)));
    vlSelfRef.__PVT__skid_acc0_w = ((1U <= (IData)(vlSelfRef.__PVT__skid_free_w)) 
                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51));
    if (vlSelfRef.__PVT__lb_pair01_w) {
        vlSelfRef.__PVT__cm1_data_w = (((QData)((IData)(vlSelfRef.__PVT__lb_smp0_w)) 
                                        << 0x00000018U) 
                                       | (QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)));
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (IData)(vlSelfRef.__PVT__lb_a0_w));
    } else {
        vlSelfRef.__PVT__cm1_data_w = ((QData)((IData)(vlSelfRef.__PVT__lb_smp1_w)) 
                                       << 0x00000018U);
        vlSelfRef.__PVT__cm1_addr_w = (0x0000001fU 
                                       & (((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                           >> 1U) + 
                                          (0x0000001cU 
                                           & ((IData)(vlSelfRef.lb_tuser_i) 
                                              << 2U))));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53 = ((~ 
                                                  ((IData)(vlSelfRef.__PVT__lb_ch1_w) 
                                                   | (IData)(vlSelfRef.__PVT__lb_pair01_w))) 
                                                 & (IData)(__PVT__lb_w1_w));
    vlSelfRef.__PVT__stash_open_w = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52)) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53));
    __VdfgRegularize_h6e95ff9d_0_50 = ((~ (IData)(vlSelfRef.__PVT__beat_flush_w)) 
                                       & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_53)) 
                                          | (IData)(vlSelfRef.__PVT__lb_pair01_w)));
    __PVT__skid_acc1_w = (((IData)(vlSelfRef.__PVT__skid_free_w) 
                           >= ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                ? 2U : 1U)) & (IData)(__VdfgRegularize_h6e95ff9d_0_50));
    vlSelfRef.__PVT__enq1_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w) 
                                 & (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skip_sum_w = (0x0001ffffU & ((3U 
                                                   & ((IData)(vlSelfRef.__PVT__push_drop_w) 
                                                      + 
                                                      (((~ (IData)(__PVT__skid_acc1_w)) 
                                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_50)) 
                                                       + 
                                                       ((~ (IData)(vlSelfRef.__PVT__skid_acc0_w)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51))))) 
                                                  + (IData)(vlSelfRef.lb_skip_cnt_o)));
    vlSelfRef.__PVT__enq0_v_w = ((IData)(vlSelfRef.__PVT__cm0_v_w)
                                  ? (IData)(vlSelfRef.__PVT__skid_acc0_w)
                                  : (IData)(__PVT__skid_acc1_w));
    vlSelfRef.__PVT__skid_enq_n_w = (3U & ((IData)(vlSelfRef.__PVT__enq1_v_w) 
                                           + (IData)(vlSelfRef.__PVT__enq0_v_w)));
}

VL_ATTR_COLD void Vchmap_wrap_KL_chan_map_capture___ctor_var_reset(Vchmap_wrap_KL_chan_map_capture* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vchmap_wrap_KL_chan_map_capture___ctor_var_reset\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11908517815223722933ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->map_wr_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17776177298405461819ull);
    vlSelf->map_wr_addr_i = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 16016879073073098652ull);
    vlSelf->map_wr_data_i = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 18067740590139364584ull);
    vlSelf->map_rd_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5193524684232999997ull);
    vlSelf->map_rd_addr_i = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3533486531187404249ull);
    vlSelf->map_rd_data_o = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 1060430032878996088ull);
    vlSelf->map_rd_valid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14950701315188709270ull);
    VL_SCOPED_RAND_RESET_W(832, vlSelf->__PVT__map_flat_o, __VscopeHash, 5025342927269499347ull);
    vlSelf->i2s_pair_valid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14077339465330281617ull);
    vlSelf->i2s_l_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 334348167422679340ull);
    vlSelf->i2s_r_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 14153129515527046049ull);
    vlSelf->tdm_pair_valid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17146692315944545839ull);
    vlSelf->tdm_pair_slot_i = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8312376393048704250ull);
    vlSelf->tdm_l_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1407747820938995061ull);
    vlSelf->tdm_r_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 13479095078091550210ull);
    vlSelf->tone_smp_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8040712467294233429ull);
    vlSelf->tick_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7020166277816128902ull);
    vlSelf->pair_valid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9152060621593263586ull);
    vlSelf->pair_slot_o = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11351620933278736616ull);
    vlSelf->pair_l_o = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 7354972667635841268ull);
    vlSelf->pair_r_o = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9523156853590907171ull);
    vlSelf->lb_dup_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6859853933559908191ull);
    vlSelf->lb_skip_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5635680129703874863ull);
    vlSelf->tdm_dup_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 137734022982063467ull);
    vlSelf->tdm_skip_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17055591806186248809ull);
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->__PVT__map_r[__Vi0] = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 8602357650815504462ull);
    }
    vlSelf->__PVT__loop_mapped_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1231592630458884704ull);
    vlSelf->__PVT__loop_fed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11654303830766668680ull);
    vlSelf->__PVT__i2s_hold_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1685730006634618498ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->tdm_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1073392236780839889ull);
    }
    vlSelf->__PVT__tdm_frame_ev_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4938651154300801200ull);
    vlSelf->tdm_fed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9133306384660750419ull);
    vlSelf->tdm_frame_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14901332649393781774ull);
    vlSelf->__PVT__lb_chpos_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11461634428334765202ull);
    vlSelf->__PVT__lb_chans_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14058492431882272789ull);
    vlSelf->__PVT__lb_smp0_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 2601039169623884793ull);
    vlSelf->__PVT__lb_smp1_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15420848075920503006ull);
    vlSelf->__PVT__lb_ch1_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17092224297341655144ull);
    vlSelf->__PVT__lb_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7430396835180313627ull);
    vlSelf->__PVT__lb_w0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2016670262391467892ull);
    vlSelf->__PVT__lb_a0_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11656581766065874178ull);
    vlSelf->__PVT__stash_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17579305291429663219ull);
    vlSelf->__PVT__stash_val_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1830096054979203735ull);
    vlSelf->__PVT__stash_strm_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11325287821766074836ull);
    vlSelf->__PVT__cm0_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1388337692429265435ull);
    vlSelf->__PVT__lb_pair01_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3893646974746688124ull);
    vlSelf->__PVT__cm1_data_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13606773936666879525ull);
    vlSelf->__PVT__cm1_addr_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10406670195350656786ull);
    vlSelf->__PVT__stash_open_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2202758283481584442ull);
    vlSelf->__PVT__stash_flush_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16177868649655207717ull);
    vlSelf->__PVT__beat_flush_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12745679169236337348ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->__PVT__lb_q_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 8115584720530136702ull);
    }
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->__PVT__q_wr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 125606865017472981ull);
    }
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->__PVT__q_rd_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9033883518808301194ull);
    }
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->__PVT__q_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1174109117893807946ull);
    }
    vlSelf->__PVT__q_fed_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3613242719414132592ull);
    vlSelf->__PVT__q_primed_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11370560964129653776ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->__PVT__lb_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7435845949688417684ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__skid_data_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15617780329142607034ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__skid_addr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12880575028148962386ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->__PVT__skid_strm_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14884218194008865525ull);
    }
    vlSelf->__PVT__skid_v_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2363161630259847116ull);
    vlSelf->__PVT__skid_wp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10987681962274185275ull);
    vlSelf->__PVT__skid_rp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12877511935262547470ull);
    vlSelf->__PVT__skid_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5013438388851221427ull);
    vlSelf->__PVT__push_ram_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2593205994896514857ull);
    vlSelf->__PVT__skid_free_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13504112451624693829ull);
    vlSelf->__PVT__skid_acc0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6788922283570714197ull);
    vlSelf->__PVT__enq0_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4393817181369858329ull);
    vlSelf->__PVT__enq1_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12472264213695026020ull);
    vlSelf->__PVT__skid_enq_n_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14287368539817429462ull);
    vlSelf->__PVT__skid_kill_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4600814363408759624ull);
    vlSelf->__PVT__st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4033452030813221370ull);
    vlSelf->__PVT__pop_idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1086397927614987971ull);
    vlSelf->__PVT__pop_act_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13136150344827608744ull);
    vlSelf->__PVT__push_same_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9840445863645419092ull);
    vlSelf->__PVT__push_cnt1_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10923618531712054282ull);
    vlSelf->__PVT__push_drop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15209586496102215198ull);
    vlSelf->__PVT__prime_set_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3333665553396474437ull);
    vlSelf->__PVT__flush_clr_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6375850755770998413ull);
    vlSelf->__PVT__skip_sum_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 10044146347725268677ull);
    vlSelf->__PVT__dup_sum_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 15661348055780067953ull);
    vlSelf->__PVT__q_rdata_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 12920074401101857568ull);
    vlSelf->__PVT__pop_ret_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18191029048775932450ull);
    vlSelf->__PVT__pop_ret_pair_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8356772365206936004ull);
    vlSelf->__PVT__slot_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15317549746751012493ull);
    vlSelf->__PVT__tick_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8206315094111285576ull);
    vlSelf->__PVT__gap_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17328762490737614340ull);
    vlSelf->__VdfgRegularize_h6e95ff9d_0_7 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_8 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_9 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_10 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_30 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_32 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_34 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_36 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_37 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_38 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_39 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_40 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_51 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_52 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_53 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_54 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_58 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_59 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_60 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_61 = 0;
}

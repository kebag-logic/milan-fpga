// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vchmap_wrap.h for the primary calling header

#include "Vchmap_wrap__pch.h"

VL_ATTR_COLD void Vchmap_wrap_KL_chan_map_capture___eval_static__TOP__chmap_wrap__DOT__u_chmap_a(Vchmap_wrap_KL_chan_map_capture* vlSelf);

VL_ATTR_COLD void Vchmap_wrap___024root___eval_static(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_static\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    {
        // Inlined CFunc: _eval_static__TOP
        IData/*31:0*/ __Vinline_0__eval_static__TOP_chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t;
        __Vinline_0__eval_static__TOP_chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0;
        IData/*31:0*/ __Vinline_0__eval_static__TOP_chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t;
        __Vinline_0__eval_static__TOP_chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0;
        __Vinline_0__eval_static__TOP_chmap_wrap__DOT__u_pkt_b__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0U;
        __Vinline_0__eval_static__TOP_chmap_wrap__DOT__u_pkt_a__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0U;
    }
    Vchmap_wrap_KL_chan_map_capture___eval_static__TOP__chmap_wrap__DOT__u_chmap_a((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
    Vchmap_wrap_KL_chan_map_capture___eval_static__TOP__chmap_wrap__DOT__u_chmap_a((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
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
    vlSelfRef.__Vtrigprevexpr___TOP__clk__1 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__clk_audio__1 = vlSelfRef.clk_audio;
}

VL_ATTR_COLD void Vchmap_wrap___024root___eval_initial(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_initial\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vchmap_wrap___024root___eval_final(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_final\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vchmap_wrap___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vchmap_wrap___024root___eval_phase__stl(Vchmap_wrap___024root* vlSelf);

VL_ATTR_COLD void Vchmap_wrap___024root___eval_settle(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_settle\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00002710U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vchmap_wrap___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("chmap_wrap.sv", 28, "", "DIDNOTCONVERGE: Settle region did not converge after '--converge-limit' of 10000 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        vlSelfRef.__VstlPhaseResult = Vchmap_wrap___024root___eval_phase__stl(vlSelf);
        vlSelfRef.__VstlFirstIteration = 0U;
    } while (vlSelfRef.__VstlPhaseResult);
}

VL_ATTR_COLD bool Vchmap_wrap___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vchmap_wrap___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vchmap_wrap___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vchmap_wrap___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD void Vchmap_wrap___024root___stl_sequent__TOP__0(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___stl_sequent__TOP__0\n"); );
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
    CData/*4:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t;
    __Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__15__t = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_19;
    __VdfgRegularize_h6e95ff9d_0_19 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_28;
    __VdfgRegularize_h6e95ff9d_0_28 = 0;
    // Body
    vlSelfRef.a_pv_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_valid_o;
    vlSelfRef.a_dup_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.lb_dup_cnt_o;
    vlSelfRef.a_skip_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.lb_skip_cnt_o;
    vlSelfRef.b_dup_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.lb_dup_cnt_o;
    vlSelfRef.b_skip_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.lb_skip_cnt_o;
    vlSelfRef.a_tdm_dup_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.tdm_dup_cnt_o;
    vlSelfRef.a_tdm_skip_cnt_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.tdm_skip_cnt_o;
    vlSelfRef.a_map_rd_data_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.map_rd_data_o;
    vlSelfRef.a_map_rd_valid_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.map_rd_valid_o;
    vlSelfRef.b_map_rd_data_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.map_rd_data_o;
    vlSelfRef.b_map_rd_valid_o = vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.map_rd_valid_o;
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
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w = 0U;
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w = 0U;
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_val_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tsw_t_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout 
            = (4U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout;
    } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__eseq_r)));
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout 
            = (3U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout;
    } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = ((IData)(1U) + vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r);
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout 
            = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout;
    } else if (vlSelfRef.b_tctx_wr_en_i) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w 
            = vlSelfRef.b_tctx_wr_data_i;
        vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w 
            = vlSelfRef.b_tctx_wr_addr_i;
    }
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w = 0U;
    if (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_val_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tsw_t_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout 
            = (4U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout;
    } else if ((4U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__eseq_r)));
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout 
            = (3U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout;
    } else if ((5U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r))) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = ((IData)(1U) + vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r);
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t 
            = vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r;
        vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout 
            = (5U | ((IData)(vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t) 
                     << 4U));
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout;
    } else if (vlSelfRef.a_tctx_wr_en_i) {
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = 1U;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w 
            = vlSelfRef.a_tctx_wr_data_i;
        vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w 
            = (0x0000001fU & (IData)(vlSelfRef.a_tctx_wr_addr_i));
    }
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11 = (7U 
                                                 & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r
                                                    [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__et_r] 
                                                    >> 1U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20 = (7U 
                                                 & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r
                                                    [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__et_r] 
                                                    >> 1U));
    vlSelfRef.a_tvalid_o = (3U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r));
    vlSelfRef.b_tvalid_o = (3U == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r));
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
    __VdfgRegularize_h6e95ff9d_0_28 = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__beat_r) 
                                       == (0x0000001fU 
                                           & ((IData)(5U) 
                                              + ((IData)(6U) 
                                                 * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_20)))));
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
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w 
        = ((IData)(vlSelfRef.b_tctx_rd_en_i) & ((IData)(vlSelfRef.b_tvalid_o) 
                                                | ((~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w)) 
                                                   & (0U 
                                                      == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__est_r)))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w 
        = ((IData)(vlSelfRef.a_tctx_rd_en_i) & ((IData)(vlSelfRef.a_tvalid_o) 
                                                | ((~ (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w)) 
                                                   & (0U 
                                                      == (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__est_r)))));
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
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__own_last_w 
        = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w) 
           == (3U & ((vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__chans_r
                      [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w] 
                      >> 1U) - (IData)(1U))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__own_last_w 
        = ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w) 
           == (3U & ((vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__chans_r
                      [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w] 
                      >> 1U) - (IData)(1U))));
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
    vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__stg_we_w 
        = ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b.pair_valid_o) 
           & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w) 
              & ((~ ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__own_last_w) 
                     & (vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pend_r
                        [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w] 
                        & (5U == vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r
                           [vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w])))) 
                 & ((IData)(vlSelfRef.b_en_i) >> (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w)))));
    vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__stg_we_w 
        = ((IData)(vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a.pair_valid_o) 
           & ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w) 
              & ((~ ((IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__own_last_w) 
                     & (vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pend_r
                        [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w] 
                        & (5U == vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r
                           [vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w])))) 
                 & ((IData)(vlSelfRef.a_en_i) >> (IData)(vlSelfRef.chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w)))));
}

VL_ATTR_COLD void Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0(Vchmap_wrap_KL_chan_map_capture* vlSelf);
VL_ATTR_COLD void Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0(Vchmap_wrap_KL_chan_map_capture* vlSelf);

VL_ATTR_COLD bool Vchmap_wrap___024root___eval_phase__stl(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___eval_phase__stl\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__stl
        vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                          & vlSelfRef.__VstlTriggered[0U]) 
                                         | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vchmap_wrap___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vchmap_wrap___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vchmap_wrap___024root___stl_sequent__TOP__0(vlSelf);
                Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_a__0((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_a));
                Vchmap_wrap_KL_chan_map_capture___stl_sequent__TOP__chmap_wrap__DOT__u_chmap_b__0((&vlSymsp->TOP__chmap_wrap__DOT__u_chmap_b));
            }
        }
    }
    return (__VstlExecute);
}

bool Vchmap_wrap___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 2> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vchmap_wrap___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 2> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vchmap_wrap___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( clk_audio)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( tg_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( tg_tick_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( dest_mac_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( station_mac_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( vlan_vid_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( transit_ns_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( ptp_ns_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( i2s_pair_valid_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @( i2s_l_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @( i2s_r_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @( tdm_pair_valid_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 14 is active: @( tdm_pair_slot_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 15 is active: @( tdm_l_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000010U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 16 is active: @( tdm_r_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000011U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 17 is active: @( tone_smp_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000012U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 18 is active: @( lb_tdata_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000013U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 19 is active: @( lb_tvalid_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000014U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 20 is active: @( lb_tlast_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000015U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 21 is active: @( lb_tuser_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000016U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 22 is active: @( lb_wire_chans_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000017U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 23 is active: @( a_lb_flush_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000018U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 24 is active: @( b_lb_flush_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000019U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 25 is active: @( a_map_wr_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 26 is active: @( a_map_wr_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 27 is active: @( a_map_wr_data_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 28 is active: @( a_map_rd_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 29 is active: @( a_map_rd_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 30 is active: @( a_tick_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 31 is active: @( a_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000020U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 32 is active: @( a_tctx_wr_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000021U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 33 is active: @( a_tctx_wr_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000022U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 34 is active: @( a_tctx_wr_data_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000023U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 35 is active: @( a_tctx_rd_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000024U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 36 is active: @( a_tctx_rd_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000025U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 37 is active: @( a_tready_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000026U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 38 is active: @( b_map_wr_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000027U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 39 is active: @( b_map_wr_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000028U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 40 is active: @( b_map_wr_data_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000029U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 41 is active: @( b_map_rd_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 42 is active: @( b_map_rd_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 43 is active: @( b_tick_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 44 is active: @( b_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 45 is active: @( b_tctx_wr_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 46 is active: @( b_tctx_wr_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 47 is active: @( b_tctx_wr_data_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000030U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 48 is active: @( b_tctx_rd_en_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000031U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 49 is active: @( b_tctx_rd_addr_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000032U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 50 is active: @( b_tready_i)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vchmap_wrap___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vchmap_wrap___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vchmap_wrap___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge clk_audio)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vchmap_wrap___024root___ctor_var_reset(Vchmap_wrap___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vchmap_wrap___024root___ctor_var_reset\n"); );
    Vchmap_wrap__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->clk_audio = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3590482352682242802ull);
    vlSelf->tg_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1463545521387278845ull);
    vlSelf->tg_tick_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14970158769442277583ull);
    vlSelf->tone_legacy_o = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15350660033775167855ull);
    vlSelf->tone_media_o = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 4730755083693379043ull);
    vlSelf->dest_mac_i = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 469293600448656375ull);
    vlSelf->station_mac_i = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10528157047001530127ull);
    vlSelf->vlan_vid_i = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 3688649701903990608ull);
    vlSelf->transit_ns_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10182791821642968674ull);
    vlSelf->ptp_ns_i = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7822373044525220339ull);
    vlSelf->i2s_pair_valid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14077339465330281617ull);
    vlSelf->i2s_l_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 334348167422679340ull);
    vlSelf->i2s_r_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 14153129515527046049ull);
    vlSelf->tdm_pair_valid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17146692315944545839ull);
    vlSelf->tdm_pair_slot_i = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8312376393048704250ull);
    vlSelf->tdm_l_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1407747820938995061ull);
    vlSelf->tdm_r_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 13479095078091550210ull);
    vlSelf->tone_smp_i = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8040712467294233429ull);
    vlSelf->lb_tdata_i = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1148341407525956502ull);
    vlSelf->lb_tvalid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4214301162520367129ull);
    vlSelf->lb_tlast_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 376850022024927819ull);
    vlSelf->lb_tuser_i = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2332282880939794331ull);
    vlSelf->lb_wire_chans_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11635510782298212953ull);
    vlSelf->a_lb_flush_i = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5285226476654128649ull);
    vlSelf->b_lb_flush_i = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17877448774388914483ull);
    vlSelf->a_dup_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1532105962521289889ull);
    vlSelf->a_skip_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14010232585655704770ull);
    vlSelf->a_tdm_dup_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4008047662391876426ull);
    vlSelf->a_tdm_skip_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12083990191384574513ull);
    vlSelf->b_dup_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12427101375361669639ull);
    vlSelf->b_skip_cnt_o = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9932380082425642067ull);
    vlSelf->a_map_wr_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6553082188741862611ull);
    vlSelf->a_map_wr_addr_i = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 7895640203102077112ull);
    vlSelf->a_map_wr_data_i = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 13316676436706129995ull);
    vlSelf->a_map_rd_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3541412580077004339ull);
    vlSelf->a_map_rd_addr_i = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 5423178998015068149ull);
    vlSelf->a_map_rd_data_o = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 17079300379608986732ull);
    vlSelf->a_map_rd_valid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15409125511444166080ull);
    vlSelf->a_tick_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16723120614362745757ull);
    vlSelf->a_pv_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12019906240305176131ull);
    vlSelf->a_en_i = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2725333800498231471ull);
    vlSelf->a_tctx_wr_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3355727363311086682ull);
    vlSelf->a_tctx_wr_addr_i = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 7853139774682293989ull);
    vlSelf->a_tctx_wr_data_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1199285038153563348ull);
    vlSelf->a_tctx_wr_rdy_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9041196822234010807ull);
    vlSelf->a_tctx_rd_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3201106058556008704ull);
    vlSelf->a_tctx_rd_addr_i = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 4004367451545433530ull);
    vlSelf->a_tctx_rd_data_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14265098425041505104ull);
    vlSelf->a_tctx_rd_valid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12053606868072509003ull);
    vlSelf->a_tdata_o = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 916730200609535529ull);
    vlSelf->a_tkeep_o = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17388197808775782993ull);
    vlSelf->a_tvalid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1223096230440876991ull);
    vlSelf->a_tlast_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6779837024322357530ull);
    vlSelf->a_tready_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4480184342750289985ull);
    vlSelf->b_map_wr_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11784291760784093004ull);
    vlSelf->b_map_wr_addr_i = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 13411193178433623479ull);
    vlSelf->b_map_wr_data_i = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 14928755159703819610ull);
    vlSelf->b_map_rd_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17113401012322486850ull);
    vlSelf->b_map_rd_addr_i = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1491096742948620476ull);
    vlSelf->b_map_rd_data_o = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 15581600815403877259ull);
    vlSelf->b_map_rd_valid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3989785334592607565ull);
    vlSelf->b_tick_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10305345535518569364ull);
    vlSelf->b_en_i = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7994818966178244450ull);
    vlSelf->b_tctx_wr_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14452824841937742318ull);
    vlSelf->b_tctx_wr_addr_i = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9290577256304368836ull);
    vlSelf->b_tctx_wr_data_i = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8549891306046889393ull);
    vlSelf->b_tctx_wr_rdy_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15208149083577066629ull);
    vlSelf->b_tctx_rd_en_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7391409147769536858ull);
    vlSelf->b_tctx_rd_addr_i = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 7347894637300764854ull);
    vlSelf->b_tctx_rd_data_o = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17482749229910539034ull);
    vlSelf->b_tctx_rd_valid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4179879114237670163ull);
    vlSelf->b_tdata_o = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6997400822401017808ull);
    vlSelf->b_tkeep_o = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5138492919344675802ull);
    vlSelf->b_tvalid_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11054023654015712553ull);
    vlSelf->b_tlast_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2323522421837777441ull);
    vlSelf->b_tready_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 734837527730146238ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tctx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7941563898641063367ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tram_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2328004528609931060ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tram_waddr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 1838347172118691592ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tram_raddr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 13014805446561462423ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tram_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6230008616904910244ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tram_q_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14223423149615171181ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__stg_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1044023663372384119ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__stg_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18257266878703381760ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__stg_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9337588224019319688ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__nsamp_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6011712090950909802ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__wbank_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8841897827613805981ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2011007127189508357ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__chans_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 829183233666899112ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__pbase_w[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 18316329362242892768ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__pown_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14495739499888060874ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__pown_t_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12300124800135680386ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__pown_o_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13248910181921395066ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__own_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4339652370918676239ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tsw_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7255872450018054723ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tsw_t_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 352953216552793353ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__tsw_val_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9657061438246491811ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__est_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5892865265186916037ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__et_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6288757470844361052ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__ebank_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9254066350021368593ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__fph_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11458093743227955804ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__beat_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4260311704331726513ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__rr_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12047554526036086561ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__eiss_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 5611422619705724056ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__ecap_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12075598574101776210ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__esmp_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10359446796202262593ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__eo_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11924956759330864219ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__eseq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10992264748334012204ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__ets_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1192421806340983172ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__etu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7011924180288700111ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__emr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12905118918009425539ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__edmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1028036519897117935ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__euid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13050357319166710586ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__evid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 1883719947843381978ull);
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__buf_l_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9390239924718040021ull);
    }
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__buf_r_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 2080529892590157429ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__grant_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2325520416975791902ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__grant_t_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2258035992783915946ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__eff_dmac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6913720270180031122ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__eff_vid_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 7768398058862949977ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__stream_id_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15421639743041178514ull);
    for (int __Vi0 = 0; __Vi0 < 240; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3149906551100580652ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17929931330747135341ull);
    vlSelf->chmap_wrap__DOT__u_pkt_b__DOT__ext_trd_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6577593842101616198ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tctx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1369489962848385501ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tram_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4474091567472518525ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tram_waddr_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3385676560448724558ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tram_raddr_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1960934464612154554ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tram_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1719129799311303496ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tram_q_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11574647460969997720ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__stg_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6945154685319373594ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__stg_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12631925879487935278ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__stg_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5324602715746260742ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__nsamp_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 126524727870200831ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__wbank_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11014597089704475059ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6374620656211409398ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__chans_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13493894297283003154ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__pbase_w[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 2366640591117035621ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__pown_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1136545855581999221ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__pown_t_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2665683103755793038ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__pown_o_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17594925914196471896ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__own_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9664087179444232114ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tsw_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13328024686755295902ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tsw_t_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1363163483302420361ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__tsw_val_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15725935197358345014ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__est_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5313571389864638788ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__et_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6787515007178766363ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__ebank_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7478624820335793081ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__fph_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1778819104365497126ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__beat_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 2844462001375062419ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__rr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13608759938423059745ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__eiss_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 14867416791918003297ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__ecap_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15105493672849715073ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__esmp_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5822433674839788578ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__eo_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11071164185202349529ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__eseq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9068877587271067266ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__ets_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7360806734221029022ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__etu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14274587446649391554ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__emr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15713541952834392092ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__edmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 12510665012856672507ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__euid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1023040451788567819ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__evid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 2023215063420975471ull);
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__buf_l_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10025842196908600720ull);
    }
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__buf_r_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 7649598692620207287ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__grant_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13798990613433024272ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__grant_t_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17952255942146419135ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__eff_dmac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17765875521101723841ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__eff_vid_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 9791683068053162128ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__stream_id_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 18000268795541232453ull);
    for (int __Vi0 = 0; __Vi0 < 240; ++__Vi0) {
        vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6768572543228998374ull);
    }
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11573367373915439912ull);
    vlSelf->chmap_wrap__DOT__u_pkt_a__DOT__ext_trd_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13964228844798926891ull);
    vlSelf->chmap_wrap__DOT__u_tone_media__DOT__idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 15315896142769248083ull);
    vlSelf->chmap_wrap__DOT__u_tone_legacy__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 13480069427326452640ull);
    vlSelf->chmap_wrap__DOT__u_tone_legacy__DOT__idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 4107542191406232128ull);
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__0__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__1__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__2__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__4__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__5__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__6__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__7__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__8__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__9__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_b__DOT__taddr__10__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__12__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__13__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__14__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__16__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__17__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__18__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__19__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__20__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__Vfuncout = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__21__w = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__t = 0;
    vlSelf->__Vfunc_chmap_wrap__DOT__u_pkt_a__DOT__taddr__22__w = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_11 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_20 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_audio__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tg_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tg_tick_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__dest_mac_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__station_mac_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__vlan_vid_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__transit_ns_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ptp_ns_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i2s_pair_valid_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i2s_l_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i2s_r_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_pair_valid_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_pair_slot_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_l_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_r_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tone_smp_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__lb_tdata_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__lb_tvalid_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__lb_tlast_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__lb_tuser_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__lb_wire_chans_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_lb_flush_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_lb_flush_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_map_wr_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_map_wr_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_map_wr_data_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_map_rd_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_map_rd_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_tick_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_tctx_wr_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_tctx_wr_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_tctx_wr_data_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_tctx_rd_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_tctx_rd_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__a_tready_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_map_wr_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_map_wr_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_map_wr_data_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_map_rd_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_map_rd_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_tick_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_tctx_wr_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_tctx_wr_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_tctx_wr_data_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_tctx_rd_en_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_tctx_rd_addr_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__b_tready_i__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_audio__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}

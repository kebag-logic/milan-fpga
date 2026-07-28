// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

// Parameter definitions for Vmilan_datapath___024root
constexpr VlUnpacked<CData/*0:0*/, 9> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_STRIN_CRF_C;
constexpr VlUnpacked<QData/*63:0*/, 9> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_STRIN_FMT_C;
constexpr VlUnpacked<QData/*63:0*/, 9> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_STROUT_FMT_C;
constexpr VlUnpacked<SData/*15:0*/, 9> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__WB_STRIN_FMT_ADDR_C;
constexpr VlUnpacked<SData/*15:0*/, 9> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__WB_STROUT_FMT_ADDR_C;
constexpr VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_IN_ADDR_C;
constexpr VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_IN_ROWS_C;
constexpr VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_IN_MOFF_C;
constexpr VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_OUT_ADDR_C;
constexpr VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_OUT_ROWS_C;
constexpr VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_OUT_MOFF_C;
constexpr VlUnpacked<QData/*63:0*/, 268> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__u_acc__DOT__AEM_DIR_C;
constexpr VlUnpacked<CData/*7:0*/, 23713> Vmilan_datapath___024root::milan_datapath__DOT__aecp_listener__DOT__u_store__DOT__AEM_ROM_INIT_C;
constexpr VlUnpacked<IData/*31:0*/, 5> Vmilan_datapath___024root::milan_datapath__DOT__csr__DOT__CBS_IDLE_RST;
constexpr VlUnpacked<IData/*31:0*/, 5> Vmilan_datapath___024root::milan_datapath__DOT__csr__DOT__CBS_HI_RST;
constexpr VlUnpacked<IData/*31:0*/, 5> Vmilan_datapath___024root::milan_datapath__DOT__csr__DOT__CBS_LO_RST;
constexpr VlUnpacked<IData/*23:0*/, 48> Vmilan_datapath___024root::milan_datapath__DOT__tone_gen__DOT__TONE_TAB_C;


void Vmilan_datapath___024root___ctor_var_reset(Vmilan_datapath___024root* vlSelf);

Vmilan_datapath___024root::Vmilan_datapath___024root(Vmilan_datapath__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vmilan_datapath___024root___ctor_var_reset(this);
}

void Vmilan_datapath___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vmilan_datapath___024root::~Vmilan_datapath___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}

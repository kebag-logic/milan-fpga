// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vchmap_wrap.h for the primary calling header

#include "Vchmap_wrap__pch.h"

// Parameter definitions for Vchmap_wrap___024root
constexpr VlUnpacked<IData/*23:0*/, 48> Vchmap_wrap___024root::chmap_wrap__DOT__u_tone_media__DOT__TONE_TAB_C;
constexpr VlUnpacked<IData/*23:0*/, 48> Vchmap_wrap___024root::chmap_wrap__DOT__u_tone_legacy__DOT__TONE_TAB_C;


void Vchmap_wrap___024root___ctor_var_reset(Vchmap_wrap___024root* vlSelf);

Vchmap_wrap___024root::Vchmap_wrap___024root(Vchmap_wrap__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    Vchmap_wrap___024root___ctor_var_reset(this);
}

void Vchmap_wrap___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

Vchmap_wrap___024root::~Vchmap_wrap___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}

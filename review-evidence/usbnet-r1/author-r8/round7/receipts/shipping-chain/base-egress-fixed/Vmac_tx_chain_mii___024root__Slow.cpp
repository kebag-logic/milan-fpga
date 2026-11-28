// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmac_tx_chain_mii.h for the primary calling header

#include "Vmac_tx_chain_mii__pch.h"

void Vmac_tx_chain_mii___024root___ctor_var_reset(Vmac_tx_chain_mii___024root* vlSelf);

void Vmac_tx_chain_mii___024root__ctor(Vmac_tx_chain_mii___024root* vlSelf, Vmac_tx_chain_mii__Syms* symsp, const char* namep) {
    vlSelf->vlSymsp = symsp;
    vlSelf->vlNamep = strdup(namep);
    // Construct members
    // Reset structure values
    Vmac_tx_chain_mii___024root___ctor_var_reset(vlSelf);
}

Vmac_tx_chain_mii___024root::Vmac_tx_chain_mii___024root(Vmac_tx_chain_mii__Syms* symsp, const char* namep) {
    Vmac_tx_chain_mii___024root__ctor(this, symsp, namep);
}

void Vmac_tx_chain_mii___024root__dtor(Vmac_tx_chain_mii___024root* vlSelf) {
    // Destroy members
    VL_DO_DANGLING(std::free(const_cast<char*>(vlSelf->vlNamep)), vlSelf->vlNamep);
}

Vmac_tx_chain_mii___024root::~Vmac_tx_chain_mii___024root() {
    Vmac_tx_chain_mii___024root__dtor(this);
}

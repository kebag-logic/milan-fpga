// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vmac_tx_chain_mii__pch.h"


void Vmac_tx_chain_mii__Syms__ctor(Vmac_tx_chain_mii__Syms* vlSymsp, const char* namep) {
    // Setup top module instance
    VL_INPLACE_CONSTRUCT(vlSymsp->vlInst.TOP, vlSymsp, namep);
    // Check resources
    Verilated::stackCheck(55);
    // Setup names of the model and of its top module instances
    vlSymsp->__Vm_topNames[0] = vlSymsp->name();
    vlSymsp->__Vm_topNames[1] = vlSymsp->__Vm_isRoot ? Verilated::catName(vlSymsp->name(), "mac_tx_chain_mii") : vlSymsp->name();
    // Setup sub module instances
    // Configure time unit / time precision
    vlSymsp->_vm_contextp__->timeunit(-12);
    vlSymsp->_vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
}

Vmac_tx_chain_mii__Syms::Vmac_tx_chain_mii__Syms(VerilatedContext* contextp, Vmac_tx_chain_mii* modelp, const char* namep, bool isRoot)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    , __Vm_isRoot{isRoot}
    , __Vm_didInit{modelp->m_didInit}
{
    Vmac_tx_chain_mii__Syms__ctor(this, namep);
}

void Vmac_tx_chain_mii__Syms__dtor(Vmac_tx_chain_mii__Syms* vlSymsp) {
    // Tear down scopes
    // Tear down sub module instances
    // Tear down top module instance
    VL_INPLACE_DESTRUCT(vlSymsp->vlInst.TOP);
}

Vmac_tx_chain_mii__Syms::~Vmac_tx_chain_mii__Syms() {
    Vmac_tx_chain_mii__Syms__dtor(this);
}

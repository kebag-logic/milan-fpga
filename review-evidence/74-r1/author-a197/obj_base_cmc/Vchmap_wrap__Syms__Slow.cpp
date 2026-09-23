// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vchmap_wrap__pch.h"

Vchmap_wrap__Syms::Vchmap_wrap__Syms(VerilatedContext* contextp, const char* namep, Vchmap_wrap* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(1768);
    // Setup sub module instances
    TOP__chmap_wrap__DOT__u_chmap_a.ctor(this, "chmap_wrap.u_chmap_a");
    TOP__chmap_wrap__DOT__u_chmap_b.ctor(this, "chmap_wrap.u_chmap_b");
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    TOP.__PVT__chmap_wrap__DOT__u_chmap_a = &TOP__chmap_wrap__DOT__u_chmap_a;
    TOP.__PVT__chmap_wrap__DOT__u_chmap_b = &TOP__chmap_wrap__DOT__u_chmap_b;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    TOP__chmap_wrap__DOT__u_chmap_a.__Vconfigure(true);
    TOP__chmap_wrap__DOT__u_chmap_b.__Vconfigure(false);
    // Setup scopes
    __Vscopep_chmap_wrap__u_chmap_a = new VerilatedScope{this, "chmap_wrap.u_chmap_a", "u_chmap_a", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_chmap_wrap__u_chmap_b = new VerilatedScope{this, "chmap_wrap.u_chmap_b", "u_chmap_b", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_chmap_wrap__u_chmap_a->varInsert("tdm_fed_r", &(TOP__chmap_wrap__DOT__u_chmap_a.tdm_fed_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_chmap_wrap__u_chmap_a->varInsert("tdm_frame_pend_r", &(TOP__chmap_wrap__DOT__u_chmap_a.tdm_frame_pend_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_chmap_wrap__u_chmap_a->varInsert("tdm_hold_r", &(TOP__chmap_wrap__DOT__u_chmap_a.tdm_hold_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RD, 1, 1 ,0,3 ,47,0);
    __Vscopep_chmap_wrap__u_chmap_a->varInsert("tdm_pair_valid_i", &(TOP__chmap_wrap__DOT__u_chmap_a.tdm_pair_valid_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RD|VLVF_NET, 0, 0);
    __Vscopep_chmap_wrap__u_chmap_b->varInsert("tdm_fed_r", &(TOP__chmap_wrap__DOT__u_chmap_b.tdm_fed_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_chmap_wrap__u_chmap_b->varInsert("tdm_frame_pend_r", &(TOP__chmap_wrap__DOT__u_chmap_b.tdm_frame_pend_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_chmap_wrap__u_chmap_b->varInsert("tdm_hold_r", &(TOP__chmap_wrap__DOT__u_chmap_b.tdm_hold_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RD, 1, 1 ,0,3 ,47,0);
    __Vscopep_chmap_wrap__u_chmap_b->varInsert("tdm_pair_valid_i", &(TOP__chmap_wrap__DOT__u_chmap_b.tdm_pair_valid_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RD|VLVF_NET, 0, 0);
}

Vchmap_wrap__Syms::~Vchmap_wrap__Syms() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_chmap_wrap__u_chmap_a, __Vscopep_chmap_wrap__u_chmap_a = nullptr);
    VL_DO_CLEAR(delete __Vscopep_chmap_wrap__u_chmap_b, __Vscopep_chmap_wrap__u_chmap_b = nullptr);
    // Tear down sub module instances
    TOP__chmap_wrap__DOT__u_chmap_b.dtor();
    TOP__chmap_wrap__DOT__u_chmap_a.dtor();
}

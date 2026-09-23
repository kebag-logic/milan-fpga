// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vmedia_grid_align_wrap__pch.h"

Vmedia_grid_align_wrap__Syms::Vmedia_grid_align_wrap__Syms(VerilatedContext* contextp, const char* namep, Vmedia_grid_align_wrap* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(368);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_media_grid_align_wrap__u_junction = new VerilatedScope{this, "media_grid_align_wrap.u_junction", "u_junction", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_media_grid_align_wrap__u_junction->varInsert("tdm_fed_r", &(TOP.media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_media_grid_align_wrap__u_junction->varInsert("tdm_frame_pend_r", &(TOP.media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 0);
    __Vscopep_media_grid_align_wrap__u_junction->varInsert("tdm_hold_r", &(TOP.media_grid_align_wrap__DOT__u_junction__DOT__tdm_hold_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RD, 1, 1 ,0,0 ,47,0);
    __Vscopep_media_grid_align_wrap__u_junction->varInsert("tdm_pair_valid_i", &(TOP.media_grid_align_wrap__DOT__u_junction__DOT__tdm_pair_valid_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 0);
}

Vmedia_grid_align_wrap__Syms::~Vmedia_grid_align_wrap__Syms() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_media_grid_align_wrap__u_junction, __Vscopep_media_grid_align_wrap__u_junction = nullptr);
    // Tear down sub module instances
}

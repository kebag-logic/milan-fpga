// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vsemantics_probe__pch.h"

Vsemantics_probe__Syms::Vsemantics_probe__Syms(VerilatedContext* contextp, const char* namep, Vsemantics_probe* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(618);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_semantics_probe = new VerilatedScope{this, "semantics_probe", "semantics_probe", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__ap_bad_flag = new VerilatedScope{this, "semantics_probe.ap_bad_flag", "ap_bad_flag", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__ap_past_one = new VerilatedScope{this, "semantics_probe.ap_past_one", "ap_past_one", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__ap_stable_one = new VerilatedScope{this, "semantics_probe.ap_stable_one", "ap_stable_one", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__real_checker = new VerilatedScope{this, "semantics_probe.real_checker", "real_checker", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__real_checker__ap_tdata_stable_until_handshake = new VerilatedScope{this, "semantics_probe.real_checker.ap_tdata_stable_until_handshake", "ap_tdata_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__real_checker__ap_tkeep_stable_until_handshake = new VerilatedScope{this, "semantics_probe.real_checker.ap_tkeep_stable_until_handshake", "ap_tkeep_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__real_checker__ap_tlast_stable_until_handshake = new VerilatedScope{this, "semantics_probe.real_checker.ap_tlast_stable_until_handshake", "ap_tlast_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_semantics_probe__real_checker__ap_tvalid_held_until_handshake = new VerilatedScope{this, "semantics_probe.real_checker.ap_tvalid_held_until_handshake", "ap_tvalid_held_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
}

Vsemantics_probe__Syms::~Vsemantics_probe__Syms() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_semantics_probe, __Vscopep_semantics_probe = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__ap_bad_flag, __Vscopep_semantics_probe__ap_bad_flag = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__ap_past_one, __Vscopep_semantics_probe__ap_past_one = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__ap_stable_one, __Vscopep_semantics_probe__ap_stable_one = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__real_checker, __Vscopep_semantics_probe__real_checker = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__real_checker__ap_tdata_stable_until_handshake, __Vscopep_semantics_probe__real_checker__ap_tdata_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__real_checker__ap_tkeep_stable_until_handshake, __Vscopep_semantics_probe__real_checker__ap_tkeep_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__real_checker__ap_tlast_stable_until_handshake, __Vscopep_semantics_probe__real_checker__ap_tlast_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_semantics_probe__real_checker__ap_tvalid_held_until_handshake, __Vscopep_semantics_probe__real_checker__ap_tvalid_held_until_handshake = nullptr);
    // Tear down sub module instances
}

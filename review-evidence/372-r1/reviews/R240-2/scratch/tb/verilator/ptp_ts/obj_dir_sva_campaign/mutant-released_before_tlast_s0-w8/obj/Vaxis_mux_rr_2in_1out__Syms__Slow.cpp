// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vaxis_mux_rr_2in_1out__pch.h"

Vaxis_mux_rr_2in_1out__Syms::Vaxis_mux_rr_2in_1out__Syms(VerilatedContext* contextp, const char* namep, Vaxis_mux_rr_2in_1out* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(1676);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_axis_mux_rr_2in_1out__u_sva = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva", "u_sva", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_grant_only_to_requester = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.ap_grant_only_to_requester", "ap_grant_only_to_requester", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_held_until_tlast_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.ap_owner_held_until_tlast_handshake", "ap_owner_held_until_tlast_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_released_after_tlast = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.ap_owner_released_after_tlast", "ap_owner_released_after_tlast", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_reset_releases_owner = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.ap_reset_releases_owner", "ap_reset_releases_owner", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_state_legal = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.ap_state_legal", "ap_state_legal", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_grants_mutually_exclusive = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_grants_mutually_exclusive", "ai_grants_mutually_exclusive", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_payload_forwarded_on_transfer = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_payload_forwarded_on_transfer", "ai_payload_forwarded_on_transfer", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_ready_only_for_owner_and_ready_sink = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_ready_only_for_owner_and_ready_sink", "ai_ready_only_for_owner_and_ready_sink", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_tvalid_forwarded = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.forwarding_laws.ai_tvalid_forwarded", "ai_tvalid_forwarded", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_m_dut", "u_m_dut", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tdata_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tdata_stable_until_handshake", "ap_tdata_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tkeep_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tkeep_stable_until_handshake", "ap_tkeep_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tlast_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tlast_stable_until_handshake", "ap_tlast_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tvalid_held_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tvalid_held_until_handshake", "ap_tvalid_held_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s0_stimulus", "u_s0_stimulus", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tdata_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tdata_stable_until_handshake", "ap_tdata_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tkeep_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tkeep_stable_until_handshake", "ap_tkeep_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tlast_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tlast_stable_until_handshake", "ap_tlast_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tvalid_held_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tvalid_held_until_handshake", "ap_tvalid_held_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s1_stimulus", "u_s1_stimulus", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tdata_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tdata_stable_until_handshake", "ap_tdata_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tkeep_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tkeep_stable_until_handshake", "ap_tkeep_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tlast_stable_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tlast_stable_until_handshake", "ap_tlast_stable_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tvalid_held_until_handshake = new VerilatedScope{this, "axis_mux_rr_2in_1out.u_sva.u_s1_stimulus.ap_tvalid_held_until_handshake", "ap_tvalid_held_until_handshake", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
}

Vaxis_mux_rr_2in_1out__Syms::~Vaxis_mux_rr_2in_1out__Syms() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva, __Vscopep_axis_mux_rr_2in_1out__u_sva = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_grant_only_to_requester, __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_grant_only_to_requester = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_held_until_tlast_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_held_until_tlast_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_released_after_tlast, __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_released_after_tlast = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_reset_releases_owner, __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_reset_releases_owner = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_state_legal, __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_state_legal = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_grants_mutually_exclusive, __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_grants_mutually_exclusive = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_payload_forwarded_on_transfer, __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_payload_forwarded_on_transfer = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_ready_only_for_owner_and_ready_sink, __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_ready_only_for_owner_and_ready_sink = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_tvalid_forwarded, __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_tvalid_forwarded = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tdata_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tdata_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tkeep_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tkeep_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tlast_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tlast_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tvalid_held_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tvalid_held_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tdata_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tdata_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tkeep_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tkeep_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tlast_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tlast_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tvalid_held_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tvalid_held_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tdata_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tdata_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tkeep_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tkeep_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tlast_stable_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tlast_stable_until_handshake = nullptr);
    VL_DO_CLEAR(delete __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tvalid_held_until_handshake, __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tvalid_held_until_handshake = nullptr);
    // Tear down sub module instances
}

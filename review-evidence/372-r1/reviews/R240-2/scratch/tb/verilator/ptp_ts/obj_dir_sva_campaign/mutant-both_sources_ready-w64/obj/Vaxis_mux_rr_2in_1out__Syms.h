// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VAXIS_MUX_RR_2IN_1OUT__SYMS_H_
#define VERILATED_VAXIS_MUX_RR_2IN_1OUT__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vaxis_mux_rr_2in_1out.h"

// INCLUDE MODULE CLASSES
#include "Vaxis_mux_rr_2in_1out___024root.h"
#include "Vaxis_mux_rr_2in_1out___024unit.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vaxis_mux_rr_2in_1out__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vaxis_mux_rr_2in_1out* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vaxis_mux_rr_2in_1out___024root TOP;

    // SCOPE NAMES
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_grant_only_to_requester;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_held_until_tlast_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_owner_released_after_tlast;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_reset_releases_owner;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__ap_state_legal;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_grants_mutually_exclusive;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_payload_forwarded_on_transfer;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_ready_only_for_owner_and_ready_sink;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__forwarding_laws__ai_tvalid_forwarded;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tdata_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tkeep_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tlast_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_m_dut__ap_tvalid_held_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tdata_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tkeep_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tlast_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s0_stimulus__ap_tvalid_held_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tdata_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tkeep_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tlast_stable_until_handshake;
    VerilatedScope* __Vscopep_axis_mux_rr_2in_1out__u_sva__u_s1_stimulus__ap_tvalid_held_until_handshake;

    // CONSTRUCTORS
    Vaxis_mux_rr_2in_1out__Syms(VerilatedContext* contextp, const char* namep, Vaxis_mux_rr_2in_1out* modelp);
    ~Vaxis_mux_rr_2in_1out__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard

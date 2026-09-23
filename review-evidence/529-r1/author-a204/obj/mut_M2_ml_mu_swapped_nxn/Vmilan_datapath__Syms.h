// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VMILAN_DATAPATH__SYMS_H_
#define VERILATED_VMILAN_DATAPATH__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vmilan_datapath.h"

// INCLUDE MODULE CLASSES
#include "Vmilan_datapath___024root.h"
#include "Vmilan_datapath_axi_stream_if.h"
#include "Vmilan_datapath___024unit.h"

// DPI TYPES for DPI Export callbacks (Internal use)

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vmilan_datapath__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vmilan_datapath* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vmilan_datapath___024root      TOP;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__rx_axis_fabric;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__rx_axis_from_mac;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__tx_axis_to_mac;

    // SCOPE NAMES
    VerilatedScope* __Vscopep_milan_datapath;
    VerilatedScope* __Vscopep_milan_datapath__chan_map_capture;
    VerilatedScope* __Vscopep_milan_datapath__media_clock_restart;
    VerilatedScope* __Vscopep_milan_datapath__pp_shadow__u_pp__u_aecp__u_dyn;
    VerilatedScope* __Vscopep_milan_datapath__talker_diag;

    // CONSTRUCTORS
    Vmilan_datapath__Syms(VerilatedContext* contextp, const char* namep, Vmilan_datapath* modelp);
    ~Vmilan_datapath__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard

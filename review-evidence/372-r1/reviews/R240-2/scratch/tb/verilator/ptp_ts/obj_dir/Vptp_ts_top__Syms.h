// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VPTP_TS_TOP__SYMS_H_
#define VERILATED_VPTP_TS_TOP__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vptp_ts_top.h"

// INCLUDE MODULE CLASSES
#include "Vptp_ts_top___024root.h"
#include "Vptp_ts_top_axi_stream_if.h"
#include "Vptp_ts_top___024unit.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vptp_ts_top__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vptp_ts_top* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vptp_ts_top___024root          TOP;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__m_axis_rx;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__m_axis_tx;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__s_axis_rx;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__s_axis_tx;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__ts_m_axis_rx;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__ts_m_axis_tx;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__ts_rx_buffered;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__ts_switch_to_fifo;
    Vptp_ts_top_axi_stream_if      TOP__ptp_ts_top__DOT__ts_tx_buffered;

    // CONSTRUCTORS
    Vptp_ts_top__Syms(VerilatedContext* contextp, const char* namep, Vptp_ts_top* modelp);
    ~Vptp_ts_top__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard

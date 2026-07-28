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
#include "Vmilan_datapath___024unit.h"
#include "Vmilan_datapath_axi_stream_if.h"
#include "Vmilan_datapath_axi_stream_if__TC3.h"

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
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__rx_axis_ptp_to_filt;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__rx_axis_to_dma;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__rx_axis_to_ts;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo;
    Vmilan_datapath_axi_stream_if__TC3 TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue;
    Vmilan_datapath_axi_stream_if__TC3 TOP__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__ts_metadata_axis;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__tx_axis_dp_to_arb;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__tx_axis_shaper_to_ts;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__tx_axis_to_mac;
    Vmilan_datapath_axi_stream_if  TOP__milan_datapath__DOT__tx_axis_to_shaper;

    // SCOPE NAMES
    VerilatedScope* __Vscopep_milan_datapath;
    VerilatedScope* __Vscopep_milan_datapath__acmp_listener_sm__u_ctx;
    VerilatedScope* __Vscopep_milan_datapath__acmp_listener_sm__u_ctx__probe_byte;
    VerilatedScope* __Vscopep_milan_datapath__aecp_listener__u_parser;
    VerilatedScope* __Vscopep_milan_datapath__traffic_controller__classifier__class_map;
    VerilatedScope* __Vscopep_milan_datapath__traffic_controller__classifier__class_map__classify;

    // CONSTRUCTORS
    Vmilan_datapath__Syms(VerilatedContext* contextp, const char* namep, Vmilan_datapath* modelp);
    ~Vmilan_datapath__Syms();

    // METHODS
    const char* name() const { return TOP.vlNamep; }
};

#endif  // guard

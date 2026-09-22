// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vptp_ts_top__pch.h"

Vptp_ts_top__Syms::Vptp_ts_top__Syms(VerilatedContext* contextp, const char* namep, Vptp_ts_top* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(770);
    // Setup sub module instances
    TOP__ptp_ts_top__DOT__m_axis_rx.ctor(this, "ptp_ts_top.m_axis_rx");
    TOP__ptp_ts_top__DOT__m_axis_tx.ctor(this, "ptp_ts_top.m_axis_tx");
    TOP__ptp_ts_top__DOT__s_axis_rx.ctor(this, "ptp_ts_top.s_axis_rx");
    TOP__ptp_ts_top__DOT__s_axis_tx.ctor(this, "ptp_ts_top.s_axis_tx");
    TOP__ptp_ts_top__DOT__ts_m_axis_rx.ctor(this, "ptp_ts_top.ts_m_axis_rx");
    TOP__ptp_ts_top__DOT__ts_m_axis_tx.ctor(this, "ptp_ts_top.ts_m_axis_tx");
    TOP__ptp_ts_top__DOT__ts_rx_buffered.ctor(this, "ptp_ts_top.ts_rx_buffered");
    TOP__ptp_ts_top__DOT__ts_switch_to_fifo.ctor(this, "ptp_ts_top.ts_switch_to_fifo");
    TOP__ptp_ts_top__DOT__ts_tx_buffered.ctor(this, "ptp_ts_top.ts_tx_buffered");
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    TOP.__PVT__ptp_ts_top__DOT__m_axis_rx = &TOP__ptp_ts_top__DOT__m_axis_rx;
    TOP.__PVT__ptp_ts_top__DOT__m_axis_tx = &TOP__ptp_ts_top__DOT__m_axis_tx;
    TOP.__PVT__ptp_ts_top__DOT__s_axis_rx = &TOP__ptp_ts_top__DOT__s_axis_rx;
    TOP.__PVT__ptp_ts_top__DOT__s_axis_tx = &TOP__ptp_ts_top__DOT__s_axis_tx;
    TOP.__PVT__ptp_ts_top__DOT__ts_m_axis_rx = &TOP__ptp_ts_top__DOT__ts_m_axis_rx;
    TOP.__PVT__ptp_ts_top__DOT__ts_m_axis_tx = &TOP__ptp_ts_top__DOT__ts_m_axis_tx;
    TOP.__PVT__ptp_ts_top__DOT__ts_rx_buffered = &TOP__ptp_ts_top__DOT__ts_rx_buffered;
    TOP.__PVT__ptp_ts_top__DOT__ts_switch_to_fifo = &TOP__ptp_ts_top__DOT__ts_switch_to_fifo;
    TOP.__PVT__ptp_ts_top__DOT__ts_tx_buffered = &TOP__ptp_ts_top__DOT__ts_tx_buffered;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    TOP__ptp_ts_top__DOT__m_axis_rx.__Vconfigure(true);
    TOP__ptp_ts_top__DOT__m_axis_tx.__Vconfigure(false);
    TOP__ptp_ts_top__DOT__s_axis_rx.__Vconfigure(false);
    TOP__ptp_ts_top__DOT__s_axis_tx.__Vconfigure(false);
    TOP__ptp_ts_top__DOT__ts_m_axis_rx.__Vconfigure(false);
    TOP__ptp_ts_top__DOT__ts_m_axis_tx.__Vconfigure(false);
    TOP__ptp_ts_top__DOT__ts_rx_buffered.__Vconfigure(false);
    TOP__ptp_ts_top__DOT__ts_switch_to_fifo.__Vconfigure(false);
    TOP__ptp_ts_top__DOT__ts_tx_buffered.__Vconfigure(false);
    // Setup scopes
}

Vptp_ts_top__Syms::~Vptp_ts_top__Syms() {
    // Tear down scopes
    // Tear down sub module instances
    TOP__ptp_ts_top__DOT__ts_tx_buffered.dtor();
    TOP__ptp_ts_top__DOT__ts_switch_to_fifo.dtor();
    TOP__ptp_ts_top__DOT__ts_rx_buffered.dtor();
    TOP__ptp_ts_top__DOT__ts_m_axis_tx.dtor();
    TOP__ptp_ts_top__DOT__ts_m_axis_rx.dtor();
    TOP__ptp_ts_top__DOT__s_axis_tx.dtor();
    TOP__ptp_ts_top__DOT__s_axis_rx.dtor();
    TOP__ptp_ts_top__DOT__m_axis_tx.dtor();
    TOP__ptp_ts_top__DOT__m_axis_rx.dtor();
}

// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vptp_ts_top.h for the primary calling header

#include "Vptp_ts_top__pch.h"

void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_tx__0(Vptp_ts_top_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_tx__0\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg) 
                        != (2U ^ (IData)(vlSymsp->TOP.ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg)));
}

void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_rx__0(Vptp_ts_top_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_m_axis_rx__0\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg) 
                        != (2U ^ (IData)(vlSymsp->TOP.ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg)));
}

void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_tx_buffered__0(Vptp_ts_top_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_tx_buffered__0\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((2U == (IData)(vlSymsp->TOP.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state)) 
                        & (IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_switch_to_fifo.tready));
}

void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_rx_buffered__0(Vptp_ts_top_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_rx_buffered__0\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((1U == (IData)(vlSymsp->TOP.ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state)) 
                        & (IData)(vlSymsp->TOP__ptp_ts_top__DOT__ts_switch_to_fifo.tready));
}

void Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_switch_to_fifo__0(Vptp_ts_top_axi_stream_if* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vptp_ts_top_axi_stream_if___nba_sequent__TOP__ptp_ts_top__DOT__ts_switch_to_fifo__0\n"); );
    Vptp_ts_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tready = ((IData)(vlSymsp->TOP.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg) 
                        != (2U ^ (IData)(vlSymsp->TOP.ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg)));
}
